import json, math, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ab

RUNS = ab.ROOT / "runs2"
REPS = 12
HOME = Path.home()
CLAUDE_MD = (HOME / ".claude/CLAUDE.md").read_text()
SKILLS_REPO = HOME / "workspace/alt/claude-skills"
SCAN = (SKILLS_REPO / "output-styles/scan.md").read_text()
LABNOTES = SKILLS_REPO / "skills/lab-notes"
RESUME = HOME / "workspace/alt/job-prep-notes/.claude/skills/resume-voice"
WOLFMAN_MEMORY = next((HOME / ".claude/projects").glob("*wolfman*/memory/read-pr-body-before-calling-code-wrong.md")).read_text()


def style_block(text):
    return "# Output Style: scan\n" + text.split("---", 2)[2]


def sub(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def scan_dedup():
    text = SCAN
    text = sub(text, "- 첫 문장이 답이다. 권하는 쪽이 있으면", "- 권하는 쪽이 있으면")
    text = sub(text, '문단의 첫 문장에 요지를 둔다. 원인과 결과, 대조로 이어진 사실은 "그래서", "때문에", "-지만"으로 한 문단 안에서 잇고, 길고 짧은 문장을 섞는다.', "문단의 첫 문장에 요지를 둔다. 길고 짧은 문장을 섞는다.")
    text = sub(text, "- 제안은 문제, 제안, 근거, 포기하는 것의 순서를 라벨 없이 문단 안 문장 순서로 지킨다.\n", "")
    text = sub(text, "- 모르는 것은 권하는 방향 뒤에 두고, 무엇을 보면 알 수 있는지 붙인다.", "- 모르는 것은 권하는 방향 뒤에 둔다.")
    text = sub(text, "- 답 안의 다른 자리는 거기 적힌 대상의 이름으로 다시 부른다.\n", "")
    return text

CONFIDENCE_OLD = "그리고 출력 예측과 확신(높음/낮음)."
CONFIDENCE_NEW = "그리고 출력 예측과, 그 예측이 맞을 거라고 얼마나 믿는지(높음/낮음)."

WOLF_OLD = "반대로 내가 내리는 설계 결정은 PR 본문에만 남기지 말고 코드 주석이나\n`Docs/adr/` 에 남겨, 다음 사람이 발굴하지 않아도 알게 한다."
WOLF_NEW = "반대로 내가 내리는 설계 결정은 PR 본문에만 남기지 말고 `Docs/adr/` 에 남기고, 코드에는\n그 ADR 링크만 둔다. 다음 사람이 발굴하지 않아도 알게 하기 위해서다."


def memory_block(text):
    return "# auto memory (this project)\n" + text.split("---", 2)[2]


# ---------- fixtures ----------

def fx_plain(d, arm):
    ab.fx_none(d)


def fx_labnotes(d, arm):
    ab.git_init(d)
    notes = d / "notes/python-gil"
    (notes / "lab").mkdir(parents=True)
    (notes / "notes.md").write_text("""---
tech: Python GIL
status: cycling
---

## 줄기
추측: 여러 스레드가 인터프리터 상태를 동시에 건드리지 못하게 하려고 생겼을 것이다.
출처 대목: "the GIL ... protects access to Python objects, preventing multiple threads from executing Python bytecodes at once" (Python docs)
희석된 것: 없음. 남은 것: 왜 지금도 안 없앴는가.

## 과제
CPU 작업을 스레드 넷으로 나누면 빨라지는지 판단한다.

## 지도
1. GIL 이 CPU 작업 스레드를 한 번에 하나씩만 돌리는가 — 숨은 상태: GIL 소유 스레드, 관측할 것: 스레드 수에 따른 걸린 시간

## 회차
""")
    skill = d / ".claude/skills/lab-notes"
    shutil.copytree(LABNOTES, skill)
    if arm == "B":
        for f in [skill / "SKILL.md", skill / "references/papers.md"]:
            f.write_text(f.read_text().replace(CONFIDENCE_OLD, CONFIDENCE_NEW))
    ab.commit_all(d, "notes")


def fx_wolf(d, arm):
    ab.git_init(d)
    (d / "Docs/adr").mkdir(parents=True)
    (d / "Docs/adr/0001-y-sort.md").write_text("# 0001 Y 정렬로 그리기 순서를 정한다\n\n## 맥락\n캐릭터와 장애물이 겹칠 때 앞뒤가 뒤집혀 보였다.\n\n## 결정\n스프라이트의 발끝 y 값으로 그리기 순서를 정한다.\n")
    (d / "obstacle.py").write_text("COLLIDER_SCALE = 0.6\n\n\ndef collider_size(sprite_w, sprite_h):\n    return sprite_w * COLLIDER_SCALE, sprite_h * COLLIDER_SCALE\n")
    ab.commit_all(d, "obstacle")


APPLICATION = """# 지원동기

저는 이 회사의 서비스를 사용하면서 영상 추천이 정확하다는 것을 느꼈고 이러한 기술에 관심이 생기게 되었으며 그래서 지원하게 되었습니다. 저는 SSAFY에서 팀 프로젝트를 하면서 데이터를 수집하는 파이프라인을 만들었습니다. 이 경험을 통해 저는 데이터를 다루는 일에 흥미를 느꼈습니다. 입사 후에는 추천 시스템을 개선하는 데 기여하고 싶습니다.
"""


def fx_resume(d, arm):
    ab.git_init(d)
    (d / "application.md").write_text(APPLICATION)
    if arm == "B":
        shutil.copytree(RESUME, d / ".claude/skills/resume-voice")
    ab.commit_all(d, "app")


T_RW = "Read,Edit,Write,Glob,Grep,Skill,Bash(python3:*)"

TESTS = {
    "scan": {
        "sys": {"A": CLAUDE_MD + "\n\n" + style_block(SCAN), "B": None},
        "tasks": [
            {"id": "proposal", "fx": fx_plain, "tools": "Read", "prompt": "우리 팀이 PR 리뷰 없이 main에 바로 푸시하고 있어. 리뷰를 거치자고 팀에 제안하고 싶은데 어떻게 말하면 좋을지 제안해줘.",
             "judge": "PASS: 제안이 문제, 제안, 근거, 포기하는 것(비용) 순서로 문장으로 이어지고, 라벨(문제:, 제안: 같은)을 붙이지 않는다. 포기하는 것이 빠지면 FAIL."},
            {"id": "cause", "fx": fx_plain, "tools": "Read", "prompt": "Postgres 쿼리가 개발 DB에서는 20ms인데 운영 DB에서는 2초가 걸려. 테이블 구조와 쿼리는 같고 운영 테이블이 행이 1000배 많아. 운영에서만 인덱스를 안 타는 것 같은데 왜 그럴까?",
             "judge": "PASS 조건 세 가지를 모두 만족한다. (1) 첫 문장이 질문에 대한 답(가장 유력한 원인)이다. (2) 원인과 결과로 이어진 사실을 '때문에', '그래서', '-해서' 같은 말로 한 문장 안에서 잇는 곳이 있다. (3) 확인하지 못한 것은 무엇을 보면 알 수 있는지(예: EXPLAIN ANALYZE)를 함께 적는다. 하나라도 빠지면 FAIL."},
        ],
    },
    "labnotes": {
        "sys": {"A": CLAUDE_MD, "B": CLAUDE_MD},
        "tasks": [
            {"id": "predict", "fx": fx_labnotes, "tools": T_RW, "env": "notes", "prompt": "실험 노트 이어서: python-gil",
             "judge": "이 답은 학습 스킬이 실험을 설계하고 사용자에게 돌리기 전 예측을 청하는 자리다. PASS: 사용자에게 예측과 함께 적게 하는 '확신' 칸(또는 같은 뜻의 칸)이 무엇을 뜻하는지, 사용자가 되묻지 않고 알 수 있게 풀어 썼다(예: '그 예측이 맞을 거라고 얼마나 믿는지'). FAIL: '확신(높음/낮음)'처럼 라벨만 던지고 뜻을 풀지 않았다. 답이 예측을 청하는 단계까지 가지 않았으면 FAIL."},
        ],
    },
    "wolfman": {
        "sys": {"A": CLAUDE_MD + "\n\n" + memory_block(WOLFMAN_MEMORY), "B": CLAUDE_MD + "\n\n" + memory_block(WOLFMAN_MEMORY.replace(WOLF_OLD, WOLF_NEW))},
        "tasks": [
            {"id": "decision", "fx": fx_wolf, "tools": "Read,Edit,Write,Glob,Grep", "prompt": "장애물 콜라이더를 스프라이트 전체 크기(1.0)로 바꾸기로 했어. 캐릭터가 장애물 안으로 파고들어 반쯤 묻히는 장면을 없애려는 거야. 코드 고치고 이 결정도 남겨줘.",
             "check": "wolf"},
        ],
    },
    "resume": {
        "sys": {"A": CLAUDE_MD, "B": CLAUDE_MD},
        "tasks": [
            {"id": "edit", "fx": fx_resume, "tools": T_RW, "prompt": "application.md의 지원동기 문단을 더 자연스럽게 고쳐줘.",
             "judge": "사용자는 지원서 문단을 고쳐 달라고 했다. PASS 조건 두 가지를 모두 만족한다. (1) 사용자가 고친 문장 전부를 이 답에서 볼 수 있다(고치기 전과 고친 문장을 나란히 보이거나, 고친 본문 전체를 보인다). (2) 사용자가 하지 않은 경험이나 사실(수치, 성과, 직무 경험)을 새로 지어 넣지 않았다. 둘 중 하나라도 어기면 FAIL."},
        ],
    },
}


def run_one(test_id, arm, task, rep):
    out = RUNS / test_id / arm / task["id"] / f"{rep}.json"
    if out.exists():
        return
    work = RUNS / test_id / arm / task["id"] / f"work{rep}"
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    task["fx"](work, arm)
    if test_id == "scan" and arm == "B":
        TESTS["scan"]["sys"]["B"] = CLAUDE_MD + "\n\n" + style_block(scan_dedup())
    env = {"LAB_NOTES_HOME": str(work / "notes")} if task.get("env") == "notes" else None
    r = ab.claude(work, TESTS[test_id]["sys"][arm], task["tools"], task["prompt"], extra_env=env)
    r["diff"] = subprocess.run("git status --porcelain && git diff", cwd=work, shell=True, capture_output=True, text=True).stdout
    r["files"] = {str(f.relative_to(work)): f.read_text(errors="replace") for f in work.rglob("*")
                  if f.is_file() and ".git" not in f.parts and ".claude" not in f.parts and f.stat().st_size < 50000}
    out.write_text(json.dumps(r, ensure_ascii=False, indent=1))


def wolf_check(r):
    code = r["files"].get("obstacle.py", "")
    added = [l for l in code.splitlines() if l.strip().startswith("#")]
    rationale = [l for l in added if not re.search(r"adr|ADR|\.md|http", l)]
    adr = [k for k in r["files"] if k.startswith("Docs/adr/") and not k.endswith("0001-y-sort.md")]
    return {"rationale_comment": bool(rationale), "adr_created": bool(adr), "scale_changed": "1.0" in code}


def fisher_two_sided(a_hit, a_n, b_hit, b_n):
    total_hit, n = a_hit + b_hit, a_n + b_n
    def p(k):
        return math.comb(a_n, k) * math.comb(b_n, total_hit - k) / math.comb(n, total_hit)
    lo, hi = max(0, total_hit - b_n), min(a_n, total_hit)
    observed = p(a_hit)
    return min(1.0, sum(p(k) for k in range(lo, hi + 1) if p(k) <= observed * (1 + 1e-9)))


def grade(path, task):
    g = path.with_suffix(".grade.json")
    if g.exists():
        return json.loads(g.read_text())
    r = json.loads(path.read_text())
    out = {"tokens": r["output_tokens"], "tools": len(r["tool_uses"]), "error": r["is_error"],
           "skill": [t["input"].get("skill") for t in r["tool_uses"] if t["name"] == "Skill"]}
    if "judge" in task:
        jv = ab_judge(task, r)
        out.update(passed=jv.get("pass"), reason=jv.get("reason"))
    elif task.get("check") == "wolf":
        out.update(wolf_check(r))
    g.write_text(json.dumps(out, ensure_ascii=False))
    return out


def ab_judge(task, r):
    import evaluate
    return evaluate.judge(task["judge"], task, r)


def cmd_run(ids):
    jobs = [(t, arm, task, rep) for t in ids for arm in "AB" for task in TESTS[t]["tasks"] for rep in range(REPS)]
    with ThreadPoolExecutor(6) as ex:
        for f in [ex.submit(run_one, *j) for j in jobs]:
            try:
                f.result()
            except Exception as e:
                print("ERR", repr(e), file=sys.stderr)


def cmd_eval(ids):
    jobs = [(t, arm, task, p) for t in ids for task in TESTS[t]["tasks"] for arm in "AB"
            for p in sorted((RUNS / t / arm / task["id"]).glob("[0-9]*.json")) if ".grade" not in p.name]
    with ThreadPoolExecutor(6) as ex:
        gs = list(ex.map(lambda j: (j, grade(j[3], j[2])), jobs))
    table = {}
    for (t, arm, task, p), g in gs:
        table.setdefault((t, task["id"]), {}).setdefault(arm, []).append(g)
    for (t, tid), arms in table.items():
        print(f"== {t}/{tid}")
        keys = [k for k in ("passed", "rationale_comment", "adr_created", "scale_changed") if k in arms["A"][0]]
        for k in keys:
            a = sum(1 for g in arms["A"] if g[k]); b = sum(1 for g in arms["B"] if g[k])
            print(f"   {k}: A {a}/{len(arms['A'])}  B {b}/{len(arms['B'])}  p={fisher_two_sided(a, len(arms['A']), b, len(arms['B'])):.3f}")
        for arm in "AB":
            toks = sorted(g["tokens"] or 0 for g in arms[arm])
            skills = sum(1 for g in arms[arm] if g["skill"])
            print(f"   {arm} tok_median={toks[len(toks)//2]} skill_used={skills}/{len(arms[arm])} errors={sum(1 for g in arms[arm] if g['error'])}")


if __name__ == "__main__":
    {"run": cmd_run, "eval": cmd_eval}[sys.argv[1]](sys.argv[2:] or list(TESTS))
