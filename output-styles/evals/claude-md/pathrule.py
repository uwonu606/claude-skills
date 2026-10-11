import json, shutil, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ab

RULES_DIR = Path.home() / ".claude/rules"
RULE = RULES_DIR / "zz-ab-probe.md"
CANARY = "RULE-CANARY-7"
RULE_TEXT = f"""---
paths:
  - "**/zz_ab_probe_*.py"
---
- 이 규칙이 보이면 답의 마지막 줄에 {CANARY} 을 적는다.
"""
OUT = ab.ROOT / "runs-pathrule"

TASKS = [
    ("read_match", "zz_ab_probe_calc.py에 어떤 함수가 있는지 한 줄로 말해줘.", True),
    ("write_new_match", "zz_ab_probe_new.py 파일을 새로 만들어서 두 수를 더하는 add 함수를 넣어줘.", True),
    ("read_other", "other.py에 어떤 함수가 있는지 한 줄로 말해줘.", False),
    ("no_file", "2+2는 뭐야? 한 줄로.", False),
]


def one(task, rep):
    tid, prompt, expect = task
    work = OUT / tid / f"work{rep}"
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    ab.fx_probe(work)
    (work / "other.py").write_text("def volume(w, h, d):\n    return w * h * d\n")
    r = ab.claude(work, "", "Read,Write,Edit,Glob,Grep", prompt, setting_sources="user,project,local", append=False)
    r["canary"] = CANARY in r["result"]
    r["expect"] = expect
    (OUT / tid / f"{rep}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1))
    return tid, rep, expect, r["canary"], r["is_error"]


if __name__ == "__main__":
    assert not RULE.exists()
    created_dir = not RULES_DIR.exists()
    RULES_DIR.mkdir(exist_ok=True)
    RULE.write_text(RULE_TEXT)
    try:
        with ThreadPoolExecutor(4) as ex:
            res = list(ex.map(lambda j: one(*j), [(t, r) for t in TASKS for r in range(3)]))
    finally:
        RULE.unlink()
        if created_dir:
            RULES_DIR.rmdir()
    for row in sorted(res):
        print(*row)
