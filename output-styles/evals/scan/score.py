"""scan 출력 스타일의 두 판(A=바꾸기 전, B=바꾼 뒤) 답에 점수를 매긴다.

    python3 score.py DIR            # DIR 은 ../layered/run.py --out 으로 준 폴더
    python3 score.py DIR --judge    # 블라인드 쌍 비교까지

판정 기준은 README.md 에 돌리기 전에 적어 둔다.
"""
import argparse
import json
import math
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CLAUDE_MD = (Path.home() / ".claude/CLAUDE.md").read_text()
REPORT_TASKS = ("report", "report-holdout")
ELEMENTS = ("what", "method", "interpretation", "limits")
DROPPED_LINE = re.compile(r"^\s*(?:[-*]\s*)?[`*]*덜어낸 것[`*]*\s*(?::[`*]*\s*(.*)|[`*]*\s*$)", re.M)
TABLE_RULE = re.compile(r"^(?=.*\|)\s*\|?\s*:?-{3,}", re.M)
SCRIPT_RUN = re.compile(r"python3?\s+(?:-\S+\s+)*\S*(sim|bench)\.py\s+.*--(workers|batch-size)")

REPORT_EXTRACT = """아래는 시뮬레이션이나 벤치마크를 돌린 뒤 쓴 답이다. 다섯 가지를 찾아 답 원문에서 그대로 인용한다.
인용은 한 글자도 바꾸지 않고 연속된 10~40자를 복사한다. 없으면 null 이다.

- lead: 답의 첫 문장. 그리고 lead_is_answer 는 그 첫 문장이 견준 두 선택지 가운데 어느 쪽이 나은지(또는 둘 다 아니라는 결론)를 말하면 true 다.
- what: 무엇을 어떤 모형으로 시뮬레이션하거나 쟀는지 밝힌 곳
- method: 어떻게 돌렸는지(파라미터, seed, 반복 횟수, 실행 시간 같은 조건)를 밝힌 곳
- interpretation: 수치를 해석해 왜 그런 결과가 나왔는지 말한 곳
- limits: 이 결과가 말해 주지 못하는 것, 가정의 한계, 확인하지 못한 것을 말한 곳

JSON 한 줄만 출력한다: {"lead": "인용", "lead_is_answer": true|false, "what": "인용"|null, "method": "인용"|null, "interpretation": "인용"|null, "limits": "인용"|null}

답:
"""

DROPPED_EXTRACT = """아래 답의 끝에 `덜어낸 것:` 줄이 있다. 그 줄에 적힌 이름마다 두 가지를 판정한다.
- in_body: 그 이름(같은 대안을 가리키는 다른 표현 포함)이 `덜어낸 것:` 줄 앞의 본문에서 이미 다뤄졌으면 true
- is_alternative: 그 이름이 물음에 대한 답으로 고를 수 있었던 실제 대안(방법, 설정, 도구)이면 true. 주의사항, 확인할 값, 개념 이름이면 false

JSON 한 줄만 출력한다: {"names": [{"name": "...", "in_body": true|false, "is_alternative": true|false}]}

물음:
{question}

답:
{answer}
"""

JUDGE = """너는 아래 사용자의 전역 지침(CLAUDE.md)을 따르는 한국어 사용자를 대신해 두 답을 견준다.
이 사용자는 Claude Code 터미널에서 답을 읽고, 첫 문장으로 결론을 잡은 뒤 필요한 만큼만 훑는다.
판단을 바꾸는 근거와 측정 과정이 빠지면 되묻고, 쓸모없이 긴 답도 싫어한다. 길이 자체로 점수를 주지 마라.

물음과 두 답(X, Y)을 읽고 이 사용자에게 더 나은 답을 고른다. 차이가 없으면 tie.
JSON 한 줄만 출력한다: {"winner": "X"|"Y"|"tie", "reason": "한 문장"}

<CLAUDE.md>
{claude_md}
</CLAUDE.md>

<물음>
{question}
</물음>

<X>
{x}
</X>

<Y>
{y}
</Y>
"""

TASKS_DIR = Path(__file__).resolve().parent.parent / "layered" / "tasks"


def ask(prompt):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    with tempfile.TemporaryDirectory() as cwd:
        for _ in range(3):
            result = subprocess.run(
                ["claude", "-p", "--setting-sources", "project",
                 "--disallowedTools", "Bash Edit Write Read Glob Grep NotebookEdit WebFetch WebSearch Agent"],
                input=prompt, capture_output=True, text=True, cwd=cwd, env=env, timeout=600)
            match = re.search(r"\{.*\}", result.stdout, re.S)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
    return None


def normalize(text):
    return re.sub(r"[\s`*_|]", "", text or "")


def located(answer, quote):
    return quote is not None and normalize(quote) in normalize(answer)


def ran_script(transcript):
    if not transcript.exists():
        return None
    for line in transcript.read_text().splitlines():
        if not line.startswith("{"):
            continue
        event = json.loads(line)
        if event.get("type") != "assistant":
            continue
        for block in event["message"]["content"]:
            command = block.get("input", {}).get("command", "") if block.get("type") == "tool_use" else ""
            if SCRIPT_RUN.search(command):
                return True
    return False


def score_report(answer):
    x = ask(REPORT_EXTRACT + answer) or {}
    row = {k: located(answer, x.get(k)) for k in ELEMENTS}
    row["table"] = bool(TABLE_RULE.search(answer))
    row["all_five"] = all(row[k] for k in ELEMENTS) and row["table"]
    row["lead_is_answer"] = bool(x.get("lead_is_answer"))
    body = normalize(answer)
    positions = [body.find(normalize(x.get(k))) for k in ("what", "method", "interpretation", "limits") if row[k]]
    table_at = body.find(normalize(TABLE_RULE.search(answer).group(0))) if row["table"] else -1
    row["ordered"] = row["all_five"] and positions[0] <= positions[1] <= table_at <= positions[2] <= positions[3]
    row["extract_failed"] = not x
    return row


def score_dropped(question, answer):
    line = DROPPED_LINE.search(answer)
    row = {"dropped": bool(line), "dropped_anywhere": "덜어낸 것" in answer}
    if line:
        x = ask(DROPPED_EXTRACT.replace("{question}", question).replace("{answer}", answer)) or {"names": []}
        names = x.get("names", [])
        row["names"] = [n.get("name") for n in names]
        row["dup_in_body"] = any(n.get("in_body") for n in names)
        row["non_alternative"] = any(not n.get("is_alternative") for n in names)
    return row


def score_one(task, path):
    answer = path.read_text()
    question = (TASKS_DIR / f"{task}.txt").read_text()
    row = {"task": task, "arm": path.stem.split("-")[0], "i": path.stem.split("-")[1], "chars": len(answer),
           "empty": not answer.strip()}
    if task in REPORT_TASKS:
        row["ran_script"] = ran_script(path.with_suffix(".jsonl"))
        row.update(score_report(answer))
    row.update(score_dropped(question, answer))
    return row


def fisher(a, an, b, bn):
    total, n = a + b, an + bn
    p = lambda k: math.comb(an, k) * math.comb(bn, total - k) / math.comb(n, total)
    observed = p(a)
    return min(1.0, sum(p(k) for k in range(max(0, total - bn), min(an, total) + 1) if p(k) <= observed * (1 + 1e-9)))


def fisher_b_lower(a, an, b, bn):
    total, n = a + b, an + bn
    p = lambda k: math.comb(an, k) * math.comb(bn, total - k) / math.comb(n, total)
    return sum(p(k) for k in range(a, min(an, total) + 1))


def sign_test_low(wins, n):
    return sum(math.comb(n, k) for k in range(wins + 1)) / 2 ** n


def judge(task, a_path, b_path, i):
    question = (TASKS_DIR / f"{task}.txt").read_text()
    a, b = a_path.read_text(), b_path.read_text()
    x, y = (a, b) if i % 2 else (b, a)
    verdict = ask(JUDGE.replace("{claude_md}", CLAUDE_MD).replace("{question}", question)
                  .replace("{x}", x).replace("{y}", y)) or {}
    winner = verdict.get("winner")
    if winner == "tie" or winner is None:
        return {"task": task, "i": i, "winner": winner, "reason": verdict.get("reason")}
    b_won = (winner == "Y") == bool(i % 2)
    return {"task": task, "i": i, "winner": "B" if b_won else "A", "reason": verdict.get("reason")}


def summarize(rows, judged):
    for task in sorted({r["task"] for r in rows}):
        arms = {arm: [r for r in rows if r["task"] == task and r["arm"] == arm] for arm in ("A", "B")}
        empty = {arm: sum(1 for r in rs if r.get("empty")) for arm, rs in arms.items()}
        if task in REPORT_TASKS:
            skipped = {arm: sum(1 for r in rs if not r.get("ran_script")) for arm, rs in arms.items()}
            arms = {arm: [r for r in rs if r.get("ran_script")] for arm, rs in arms.items()}
            print(f"   (sim/bench 를 돌리지 않아 뺀 회차 A {skipped['A']}  B {skipped['B']})")
        print(f"== {task}  A n={len(arms['A'])}  B n={len(arms['B'])}  빈 답 A {empty['A']}  B {empty['B']}")
        keys = ["dropped", "dropped_anywhere", "dup_in_body", "non_alternative"]
        if task in REPORT_TASKS:
            keys = ["ran_script", "all_five", "table", *ELEMENTS, "ordered", "lead_is_answer", "extract_failed"] + keys
        for key in keys:
            a = sum(1 for r in arms["A"] if r.get(key))
            b = sum(1 for r in arms["B"] if r.get(key))
            if arms["A"] and arms["B"]:
                extra = (f"  p(B 가 낮다, 한쪽)={fisher_b_lower(a, len(arms['A']), b, len(arms['B'])):.3f}"
                         if key == "lead_is_answer" else "")
                print(f"   {key:16s} A {a}/{len(arms['A'])}  B {b}/{len(arms['B'])}  p={fisher(a, len(arms['A']), b, len(arms['B'])):.3f}{extra}")
            else:
                print(f"   {key:16s} A {a}/{len(arms['A'])}  B {b}/{len(arms['B'])}")
        medians = {arm: sorted(r["chars"] for r in rs)[len(rs) // 2] for arm, rs in arms.items() if rs}
        if len(medians) == 2:
            print(f"   chars_median     A {medians['A']}  B {medians['B']}  ratio={medians['B'] / medians['A']:.2f}")
        verdicts = [j for j in judged if j["task"] == task]
        if verdicts:
            b_wins = sum(1 for j in verdicts if j["winner"] == "B")
            a_wins = sum(1 for j in verdicts if j["winner"] == "A")
            ties = len(verdicts) - a_wins - b_wins
            print(f"   judge            B {b_wins}  A {a_wins}  tie {ties}  p(B 가 낮다, 한쪽)={sign_test_low(b_wins, a_wins + b_wins):.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("--judge", action="store_true")
    args = parser.parse_args()
    cache = args.out / "scores.json"
    rows = json.loads(cache.read_text()) if cache.exists() else []
    seen = {(r["task"], r["arm"], r["i"]) for r in rows}
    todo = [(task_dir.name, p) for task_dir in sorted(args.out.iterdir()) if task_dir.is_dir() and task_dir.name != "work"
            for p in sorted(task_dir.glob("[AB]-*.md")) if (task_dir.name, p.stem.split("-")[0], p.stem.split("-")[1]) not in seen]
    with ThreadPoolExecutor(8) as pool:
        rows += list(pool.map(lambda job: score_one(*job), todo))
    cache.write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    judged = []
    if args.judge:
        judge_cache = args.out / "judge.json"
        judged = json.loads(judge_cache.read_text()) if judge_cache.exists() else []
        done = {(j["task"], j["i"]) for j in judged}
        pairs = [(task_dir.name, task_dir / f"A-{i}.md", task_dir / f"B-{i}.md", i)
                 for task_dir in sorted(args.out.iterdir()) if task_dir.is_dir() and task_dir.name != "work"
                 for i in range(1, 100) if (task_dir / f"A-{i}.md").exists() and (task_dir / f"B-{i}.md").exists()
                 and (task_dir.name, i) not in done]
        with ThreadPoolExecutor(8) as pool:
            judged += list(pool.map(lambda job: judge(*job), pairs))
        judge_cache.write_text(json.dumps(judged, ensure_ascii=False, indent=1))
    summarize(rows, judged)


if __name__ == "__main__":
    main()
