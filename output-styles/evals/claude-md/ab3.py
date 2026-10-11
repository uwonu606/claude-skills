import json, math, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ab

OUT = ab.ROOT / "runs3"
REPS = 10
HOME = Path.home()
SKILLS = HOME / "workspace/alt/claude-skills"
CLAUDE_MD = (HOME / ".claude/CLAUDE.md").read_text()
ARROW_LINE = "- 제안은 문제 → 제안 → 근거 → 포기하는 것 순서로, 라벨 없이 문장으로 잇는다."
COMMA_LINE = "- 제안은 문제, 제안, 근거, 포기하는 것 순서로, 라벨 없이 문장으로 잇는다."
assert CLAUDE_MD.count(ARROW_LINE) == 1
LAYERED = (SKILLS / "output-styles/layered.md").read_text()
SCAN_BEFORE = subprocess.run(["git", "show", "HEAD:output-styles/scan.md"], cwd=SKILLS, capture_output=True, text=True, check=True).stdout
SCAN_AFTER = (SKILLS / "output-styles/scan.md").read_text()
assert SCAN_BEFORE != SCAN_AFTER


def style(name, text):
    return f"# Output Style: {name}\n" + text.split("---", 2)[2]


TESTS = {
    "arrow": {"A": CLAUDE_MD + "\n\n" + style("layered", LAYERED),
              "B": CLAUDE_MD.replace(ARROW_LINE, COMMA_LINE) + "\n\n" + style("layered", LAYERED)},
    "scan": {"A": CLAUDE_MD + "\n\n" + style("scan", SCAN_BEFORE),
             "B": CLAUDE_MD + "\n\n" + style("scan", SCAN_AFTER)},
}

SCENARIOS = {
    "fx": "우리 Spring 서버가 요청마다 외부 환율 API를 불러서 응답이 느려(평균 800ms). 환율은 하루에 몇 번만 바뀌어. 어떻게 하면 좋을지 제안해줘.",
    "ci": "팀 저장소 테스트가 CI에서 25분 걸려서 PR 머지가 밀려. 테스트 1,200개 중 통합 테스트 80개가 시간의 대부분을 차지해. 어떻게 바꾸면 좋을지 제안해줘.",
    "sqlite": "사이드 프로젝트 DB를 SQLite로 쓰는데 동시 쓰기에서 'database is locked' 에러가 하루에 몇 번 나. 사용자는 하루 200명 정도야. 어떻게 할지 제안해줘.",
    "store": "프론트에서 상태를 전부 전역 store 하나에 넣었더니 화면 하나만 바뀌어도 다른 화면까지 다시 그려져. 어떻게 바꿀지 제안해줘.",
}

EXTRACT = """아래 답에서 어시스턴트가 사용자에게 권하는 주된 제안 하나를 찾고, 네 요소가 처음 나오는 곳을 답에서 그대로 인용한다.
인용은 답 원문에서 한 글자도 바꾸지 않고 연속된 12~40자를 복사한다. 제목 줄도 답의 일부로 본다.

- problem: 지금 무엇이 문제인지(원인 포함)를 처음 말하는 곳
- proposal: 주된 제안을 처음 말하는 곳
- basis: 그 제안이 왜 맞는지 근거를 처음 대는 곳
- cost: 그 제안을 따르면 포기하거나 감수하는 것(비용, 단점, 잃는 것)을 처음 말하는 곳. 다른 대안의 단점은 넣지 않는다.

요소가 없으면 null 이다. labels 는 이 네 요소 중 하나라도 "문제:", "제안:", "근거:", "비용:", "포기하는 것:", "**문제**" 처럼 요소 이름을 라벨로 달고 시작하면 true 다. "모르는 것:", "덜어낸 것:", "### 흐름" 같은 머리말이나 다른 라벨은 세지 않는다.

JSON 한 줄만 출력한다: {"problem": "인용"|null, "proposal": "인용"|null, "basis": "인용"|null, "cost": "인용"|null, "labels": true|false}

답:
"""


def run_one(test, arm, scen, rep):
    out = OUT / test / arm / scen / f"{rep}.json"
    if out.exists():
        return
    work = OUT / test / arm / scen / f"work{rep}"
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    ab.fx_none(work)
    r = ab.claude(work, TESTS[test][arm], "Read", SCENARIOS[scen])
    out.write_text(json.dumps({k: r[k] for k in ("result", "output_tokens", "is_error", "tool_uses")}, ensure_ascii=False))


def extract(path):
    g = path.with_suffix(".x.json")
    if g.exists():
        return json.loads(g.read_text())
    r = json.loads(path.read_text())
    x = None
    for _ in range(3):
        j = ab.claude(ab.ROOT, "", "Read", EXTRACT + r["result"], append=False)
        m = re.search(r"\{.*\}", j["result"], re.S)
        if m:
            try:
                x = json.loads(m.group(0)); break
            except Exception:
                pass
    x = x or {"problem": None, "proposal": None, "basis": None, "cost": None, "labels": None, "failed": True}
    norm = lambda t: re.sub(r"[\s`*_]", "", t or "")
    body = norm(r["result"])
    pos = {}
    for k in ("problem", "proposal", "basis", "cost"):
        q = x.get(k)
        pos[k] = None if q is None else body.find(norm(q))
        if pos[k] == -1:
            x["unlocated"] = x.get("unlocated", 0) + 1
            pos[k] = None
    x["pos"] = pos
    x["all_present"] = all(pos[k] is not None for k in pos)
    x["after_proposal"] = x["all_present"] and pos["proposal"] <= pos["basis"] <= pos["cost"]
    x["problem_first"] = x["all_present"] and pos["problem"] <= pos["proposal"]
    x["ordered"] = x["after_proposal"] and x["problem_first"]
    x["comply"] = x["after_proposal"] and x.get("labels") is False
    x["cost_present"] = x.get("cost") is not None
    x["tokens"] = r["output_tokens"]
    g.write_text(json.dumps(x, ensure_ascii=False))
    return x


def fisher(a, an, b, bn):
    t, n = a + b, an + bn
    p = lambda k: math.comb(an, k) * math.comb(bn, t - k) / math.comb(n, t)
    o = p(a)
    return min(1.0, sum(p(k) for k in range(max(0, t - bn), min(an, t) + 1) if p(k) <= o * (1 + 1e-9)))


def cmd_run(tests):
    jobs = [(t, arm, s, i) for t in tests for arm in "AB" for s in SCENARIOS for i in range(REPS)]
    with ThreadPoolExecutor(6) as ex:
        for f in [ex.submit(run_one, *j) for j in jobs]:
            try:
                f.result()
            except Exception as e:
                print("ERR", repr(e), file=sys.stderr)


def cmd_eval(tests):
    paths = [(t, arm, s, p) for t in tests for arm in "AB" for s in SCENARIOS
             for p in sorted((OUT / t / arm / s).glob("[0-9]*.json")) if ".x" not in p.name]
    with ThreadPoolExecutor(6) as ex:
        xs = list(ex.map(lambda j: (j, extract(j[3])), paths))
    for t in tests:
        print(f"== {t}")
        rows = {arm: [x for (tt, a, s, p), x in xs if tt == t and a == arm] for arm in "AB"}
        for key in ("comply", "all_present", "after_proposal", "problem_first", "ordered", "cost_present", "labels"):
            a = sum(1 for x in rows["A"] if x.get(key)); b = sum(1 for x in rows["B"] if x.get(key))
            print(f"   {key:13s} A {a}/{len(rows['A'])}  B {b}/{len(rows['B'])}  p={fisher(a, len(rows['A']), b, len(rows['B'])):.3f}")
        for arm in "AB":
            toks = sorted(x["tokens"] or 0 for x in rows[arm])
            per = {s: sum(1 for (tt, a, ss, p), x in xs if tt == t and a == arm and ss == s and x.get("comply")) for s in SCENARIOS}
            print(f"   {arm} tok_median={toks[len(toks)//2]} extract_failed={sum(1 for x in rows[arm] if x.get('failed'))} unlocated={sum(x.get('unlocated',0) for x in rows[arm])} comply_by_scenario={per}")


if __name__ == "__main__":
    {"run": cmd_run, "eval": cmd_eval}[sys.argv[1]](sys.argv[2:] or list(TESTS))
