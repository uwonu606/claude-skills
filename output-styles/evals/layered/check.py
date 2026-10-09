"""run.py 가 모은 답을 세고, 시험마다 base 와 cand 를 견준다.

    python3 check.py DIR                  # 과제마다 arm 별 지표 평균
    python3 check.py DIR --test NAME      # 시험 하나의 판정 (arm 이름은 base, cand)
    python3 check.py DIR --integration    # 과제 다섯 개 전부의 판정
    python3 check.py DIR --holdout        # 떼어 둔 과제 둘의 판정
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path
from statistics import mean

STORY_MARKERS = {
    "explain": (("따로", "새 대화", "보냈", "물었"),
                ("글자", "문자열", "합치", "합쳐", "clean_text", "visited_nodes", "달라", "다르게")),
    "explain-holdout": (("1,000번", "1000번", "조회했", "locust", "보냈"),
                        ("ts", "타임스탬프", "매번 다른", "키가 달라", "928")),
}
FORWARD_REF = re.compile(r"#\d|아래|세부|뒤에서|다음 표")
QUOTED_EVIDENCE = {"diagnose-holdout": "0.30000000000000004"}
INTERNAL_NAMES = ("clean_text", "visited_nodes", "temperature", "Head", "Tail", "Entity",
                  "entity_relation", "event_entity", "event_relation", "nodes", "stages")
FILE_LINE_REF = re.compile(r"[\w./-]+\.(?:md|json|py):\d+")
SUMMARY_PREFIXES = ("[확인]", "[추정]", "모르는 것", "덜어낸 것", "작성함", "린트 통과", "테스트 통과",
                    "실행 확인함", "미검증", "참고", "제안", "필수")
DANGEROUS_COMMAND = re.compile(r"pg_dropcluster|--link|-m link|apt(?:-get)? (?:remove|purge)|rm -rf")
WARNING_MARKERS = ("⚠", "주의", "경고", "되돌릴 수 없", "돌아갈 수 없", "다시 확인")
CODE_TEST = ("import test_duration as t; t.test_single(); t.test_roundtrip(); "
             "from duration import parse_duration as p; "
             "assert p('1h30m') == 5400 and p('2h5s') == 7205")


def split_layers(text):
    layers = {"lead": [], "흐름": [], "세부": [], "정리": []}
    current = None
    seen_title = False
    for line in text.splitlines():
        if line.startswith("## ") and not seen_title:
            seen_title, current = True, "lead"
            continue
        if line.startswith("### "):
            current = line[4:].strip() if line[4:].strip() in layers else None
            continue
        layers.setdefault(current or "lead", []).append(line)
    return {name: "\n".join(lines) for name, lines in layers.items()}


def first_index(text, markers):
    hits = [text.find(m) for m in markers if m in text]
    return min(hits) if hits else None


def did_before_cause(flow, did_markers, cause_markers):
    did, cause = first_index(flow, did_markers), first_index(flow, cause_markers)
    return did is not None and (cause is None or did < cause)


def unlabeled_summary_lines(summary):
    items = [re.sub(r"^\s*(?:[-*]|\d+\.)\s*", "", line) for line in summary.splitlines()
             if re.match(r"^\s*(?:[-*]|\d+\.)\s", line)]
    return sum(not item.startswith(SUMMARY_PREFIXES) for item in items)


def guarded_dangerous_commands(text):
    lines = text.splitlines()
    in_code, total, guarded = False, 0, 0
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code and DANGEROUS_COMMAND.search(line):
            total += 1
            before = "\n".join(lines[max(0, i - 6):i])
            guarded += any(marker in before for marker in WARNING_MARKERS)
    return guarded, total


def code_tests_pass(workdir):
    result = subprocess.run([sys.executable, "-c", CODE_TEST], cwd=workdir, capture_output=True)
    return result.returncode == 0


def measure(answer, workdir, task):
    text = answer.read_text()
    did_markers, cause_markers = STORY_MARKERS.get(task, STORY_MARKERS["explain"])
    layers = split_layers(text)
    flow = layers["흐름"] or text
    guarded, dangerous = guarded_dangerous_commands(text)
    metrics = {
        "chars": len(text),
        "flow_items": len(re.findall(r"^\d+\. ", layers["흐름"], re.M)),
        "expect_in_flow": bool(re.search(r"바란|바랐|기대|여야|어야 했", flow)),
        "did_first_in_flow": did_before_cause(flow, did_markers, cause_markers),
        "flow_code_spans": len(re.findall(r"`[^`\n]+`", layers["흐름"])),
        "flow_forward_refs": len(FORWARD_REF.findall(layers["흐름"])),
        "lead_cause": any(m in layers["lead"] for m in cause_markers),
        "internal_refs": len(FILE_LINE_REF.findall(text)) + sum(name in text for name in INTERNAL_NAMES),
        "unlabeled": unlabeled_summary_lines(layers["정리"]),
        "gam": text.count("[감]"),
        "four_parts": all(re.search(rf"{part}[^\n]{{0,6}}:", layers["세부"]) for part in ("문제", "제안", "근거", "포기")),
        "success_checks": text.count("성공"),
        "dangerous": dangerous,
        "unguarded": dangerous - guarded,
    }
    if task in QUOTED_EVIDENCE:
        metrics["quotes_evidence"] = QUOTED_EVIDENCE[task] in text
    if workdir.is_dir() and (workdir / "duration.py").exists():
        metrics["code_ok"] = code_tests_pass(workdir)
    return metrics


def collect(out):
    stats = {}
    for task_dir in sorted(p for p in out.iterdir() if p.is_dir() and p.name != "work"):
        for answer in sorted(task_dir.glob("*.md")):
            arm = answer.stem.rsplit("-", 1)[0]
            workdir = out / "work" / task_dir.name / answer.stem
            stats.setdefault(task_dir.name, {}).setdefault(arm, []).append(measure(answer, workdir, task_dir.name))
    return stats


def averaged(runs, key):
    return mean(float(run[key]) for run in runs if key in run)


TESTS = {
    "unknown-label": ("diagnose", "정리 항목이 모두 라벨·모르는 것·완료 어휘로 시작하고 [감] 이 없다",
                      lambda b, c: averaged(c, "unlabeled") == 0 and averaged(c, "gam") == 0),
    "density-merge": ("explain", "바란 것을 덜 쓰지 않고 길이가 15% 넘게 늘지 않는다",
                      lambda b, c: averaged(c, "expect_in_flow") >= averaged(b, "expect_in_flow")
                      and averaged(c, "chars") <= averaged(b, "chars") * 1.15),
    "proposal-home": ("propose", "4요소를 세부에 두는 비율이 줄지 않는다",
                      lambda b, c: averaged(c, "four_parts") >= averaged(b, "four_parts")),
    "flow-verb": ("explain", "바란 것과 한 일 먼저가 줄지 않는다",
                  lambda b, c: averaged(c, "expect_in_flow") >= averaged(b, "expect_in_flow")
                  and averaged(c, "did_first_in_flow") >= averaged(b, "did_first_in_flow") - 0.34),
    "title-is-answer": ("explain", "첫 문단이 원인부터 말하는 비율이 준다",
                        lambda b, c: averaged(c, "lead_cause") < averaged(b, "lead_cause")),
    "io-line": ("explain", "내부 이름이 줄고 한 일 먼저는 줄지 않는다",
                lambda b, c: averaged(c, "internal_refs") < averaged(b, "internal_refs")
                and averaged(c, "did_first_in_flow") >= averaged(b, "did_first_in_flow")),
    "preamble-removable": ("explain", "서문 줄을 빼도(cand) 흐름의 코드 이름·앞질러 가리키기가 늘지 않고 바란 것·한 일 먼저가 줄지 않는다 — 통과면 이 줄은 효과가 없다",
                           lambda b, c: averaged(c, "flow_code_spans") <= averaged(b, "flow_code_spans") * 1.2 + 0.5
                and averaged(c, "flow_forward_refs") <= averaged(b, "flow_forward_refs") + 0.3
                and averaged(c, "expect_in_flow") >= averaged(b, "expect_in_flow") - 0.2
                and averaged(c, "did_first_in_flow") >= averaged(b, "did_first_in_flow") - 0.2),
    "preamble-removable-holdout": ("explain-holdout", "서문 줄을 빼도(cand) 흐름의 코드 이름·앞질러 가리키기가 늘지 않고 바란 것·한 일 먼저가 줄지 않는다 — 통과면 이 줄은 효과가 없다",
                                   lambda b, c: averaged(c, "flow_code_spans") <= averaged(b, "flow_code_spans") * 1.2 + 0.5
                                   and averaged(c, "flow_forward_refs") <= averaged(b, "flow_forward_refs") + 0.3
                                   and averaged(c, "expect_in_flow") >= averaged(b, "expect_in_flow") - 0.2
                                   and averaged(c, "did_first_in_flow") >= averaged(b, "did_first_in_flow") - 0.2),
}


INTEGRATION = {
    "explain": ("바란 것과 한 일 먼저가 줄지 않고, 첫 문단이 원인부터 말하는 비율이 늘지 않는다",
                lambda b, c: averaged(c, "expect_in_flow") >= averaged(b, "expect_in_flow") - 0.2
                and averaged(c, "did_first_in_flow") >= averaged(b, "did_first_in_flow") - 0.2
                and averaged(c, "lead_cause") <= averaged(b, "lead_cause")),
    "diagnose": ("정리 항목이 모두 정해진 꼴로 시작하고 흐름이 1.5줄 넘게 늘지 않는다",
                 lambda b, c: averaged(c, "unlabeled") == 0 and averaged(c, "gam") == 0
                 and averaged(c, "flow_items") <= averaged(b, "flow_items") + 1.5),
    "propose": ("4요소를 세부에 두는 비율이 줄지 않는다",
                lambda b, c: averaged(c, "four_parts") >= averaged(b, "four_parts") - 0.34),
    "procedure": ("위험한 명령이 모두 경고 뒤에 온다",
                  lambda b, c: averaged(c, "unguarded") == 0),
    "code": ("고친 코드가 테스트를 통과한다",
             lambda b, c: averaged(c, "code_ok") == 1),
}


# 떼어 둔 과제: 규칙은 결과를 보기 전에 정했고, 결과를 보고 layered 를 다듬지 않는다.
HOLDOUT = {
    "explain-holdout": ("바란 것과 한 일 먼저가 줄지 않고, 정리가 정해진 꼴이며, 30% 넘게 길어지지 않는다",
                        lambda b, c: averaged(c, "expect_in_flow") >= averaged(b, "expect_in_flow")
                        and averaged(c, "did_first_in_flow") >= averaged(b, "did_first_in_flow") - 0.2
                        and averaged(c, "unlabeled") == 0
                        and averaged(c, "chars") <= averaged(b, "chars") * 1.3),
    "diagnose-holdout": ("실제 오류 출력을 인용하는 비율이 줄지 않고, 정리가 정해진 꼴이며, 30% 넘게 길어지지 않는다",
                         lambda b, c: averaged(c, "quotes_evidence") >= averaged(b, "quotes_evidence")
                         and averaged(c, "unlabeled") == 0
                         and averaged(c, "chars") <= averaged(b, "chars") * 1.3),
}


def print_table(stats):
    for task, arms in stats.items():
        keys = [k for k in next(iter(arms.values()))[0]]
        print(f"\n## {task}\n| arm | n | " + " | ".join(keys) + " |")
        print("|---|---|" + "---|" * len(keys))
        for arm, runs in arms.items():
            print(f"| {arm} | {len(runs)} | " + " | ".join(f"{averaged(runs, k):.2f}" for k in keys) + " |")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("--test", choices=TESTS)
    parser.add_argument("--integration", action="store_true")
    parser.add_argument("--holdout", action="store_true")
    args = parser.parse_args()
    stats = collect(args.out)
    print_table(stats)
    if args.integration:
        print()
        for task, (rule, passes) in INTEGRATION.items():
            verdict = "통과" if passes(stats[task]["base"], stats[task]["cand"]) else "실패"
            print(f"{task}: {rule} → {verdict}")
    if args.holdout:
        print()
        for task, (rule, passes) in HOLDOUT.items():
            verdict = "통과" if passes(stats[task]["base"], stats[task]["cand"]) else "실패"
            print(f"{task}: {rule} → {verdict}")
    if args.test:
        task, rule, passes = TESTS[args.test]
        arms = stats[task]
        verdict = "통과" if passes(arms["base"], arms["cand"]) else "실패"
        print(f"\n{args.test}: {rule} → {verdict}")


if __name__ == "__main__":
    main()
