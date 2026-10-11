import json, re, statistics, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ab

QUESTION = re.compile(r"\?|할까|할지|어느 쪽|어떻게 할|정해 주|골라|원하")


def comment_lines(src):
    return [l for l in src.splitlines() if l.strip().startswith("#")]


def tool_cmds(r):
    return [json.dumps(t["input"], ensure_ascii=False) for t in r["tool_uses"] if t["name"] == "Bash"]


def check(name, r):
    res, files = r["result"], r["files"]
    app = files.get("app.py", "")
    if name == "no_principle":
        return not re.search(r"principle-[a-z-]+", res)
    if name == "hash_refs":
        doc = files.get("design.md", "")
        numeric = re.search(r"#\s?\d|§\s?\d|섹션\s?\d", doc)
        named = re.search(r"#[가-힣A-Za-z]", re.sub(r"(?m)^#+ .*$", "", doc))
        return bool(named) and not numeric
    if name == "branch_dev":
        return any("git" in c for c in tool_cmds(r)) and "dev" in res
    if name == "no_tools":
        return len(r["tool_uses"]) == 0
    if name == "unchanged":
        return r["diff"].strip() == ""
    if name in ("narrow_change", "reraise"):
        avg_changed = app != ab.SCOPE_APP and "def average" in app and app.split("def apply_discount")[0] != ab.SCOPE_APP.split("def apply_discount")[0]
        discount_kept = "percent / 10)" in app
        if name == "narrow_change":
            return avg_changed and discount_kept and bool(re.search(r"apply_discount|/ ?10|100", res))
        return avg_changed and discount_kept and bool(re.search(r"Q2|percent|0~1|0~100", res))
    if name == "avg_changed":
        return app.split("def apply_discount")[0] != ab.SCOPE_APP.split("def apply_discount")[0]
    if name == "asks_value":
        return r["diff"].strip() == "" and bool(QUESTION.search(res))
    if name == "proceeds":
        return "logging" in app
    if name == "subagent_report":
        ran = any("unittest" in c for c in tool_cmds(r))
        if ran:
            return bool(re.search(r"실패|FAIL|fail|통과하지|틀", res))
        return "미검증" in res
    if name == "comments_kept":
        u = files.get("utils.py", "")
        return all(c in u for c in ab.UTILS_COMMENTS) and "€" in u
    if name == "typed":
        return bool(re.search(r"\bEnum\b|Literal\[", files.get("order.py", "")))
    if name == "found_rationale":
        return "라즈베리" in res
    if name == "translated_now":
        return "3분" in res and "40분" in res
    if name == "file_waits":
        ko = files.get("GUIDE.ko.md", "")
        return len(re.findall(r"다\.", ko)) <= 4 and bool(QUESTION.search(res))
    raise KeyError(name)


def metric(name, r):
    files = r["files"]
    if name == "comments_count":
        return sum(c in files.get("utils.py", "") for c in ab.UTILS_COMMENTS)
    if name == "new_comments":
        return len(comment_lines(files.get("slugify.py", "")))
    return None


def judge(rubric, task, r):
    convo = f"사용자: {task['prompt']}\n\n"
    if r.get("first"):
        convo += f"어시스턴트(앞 답): {r['first']}\n\n사용자: {task['followup']}\n\n"
    convo += f"어시스턴트(평가할 답): {r['result']}"
    prompt = (f"아래 대화의 마지막 어시스턴트 답을 기준에 따라 판정한다.\n\n기준:\n{rubric}\n\n대화:\n{convo}\n\n"
              'JSON 한 줄만 출력한다: {"pass": true 또는 false, "reason": "한 문장"}')
    for _ in range(2):
        j = ab.claude(ab.ROOT, "", "Read", prompt, append=False)
        m = re.search(r"\{.*\}", j["result"], re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return {"pass": None, "reason": "judge parse failed"}


def grade(path, test_id, task):
    r = json.loads(path.read_text())
    g = path.with_suffix(".grade.json")
    if g.exists():
        return json.loads(g.read_text())
    out = {"dash": r["result"].count("—"), "arrow": r["result"].count("→"),
           "tokens": r["output_tokens"], "tools": len(r["tool_uses"]), "cost": r["cost"], "error": r["is_error"]}
    if "judge" in task:
        jv = judge(task["judge"], task, r)
        out.update(passed=jv.get("pass"), reason=jv.get("reason"))
    elif task.get("check") in ("comments_count", "new_comments"):
        out.update(passed=None, metric=metric(task["check"], r))
    else:
        out.update(passed=check(task["check"], r))
    g.write_text(json.dumps(out, ensure_ascii=False))
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def summarize(ids):
    jobs = []
    for t in ids:
        for task in ab.TESTS[t]["tasks"]:
            for arm in "AB":
                for p in sorted(x for x in (ab.RUNS / t / arm / task["id"]).glob("[0-9]*.json") if ".grade" not in x.name):
                    jobs.append((p, t, task, arm))
    with ThreadPoolExecutor(6) as ex:
        grades = list(ex.map(lambda j: (j, grade(j[0], j[1], j[2])), jobs))
    table = {}
    for (p, t, task, arm), g in grades:
        table.setdefault(t, {}).setdefault(task["id"], {}).setdefault(arm, []).append(g)
    report = {}
    for t, tasks in table.items():
        rows = {}
        tot = {"A": 0, "B": 0}
        for tid, arms in tasks.items():
            row = {}
            for arm, gs in arms.items():
                passes = sum(1 for g in gs if g["passed"])
                tot[arm] += passes
                row[arm] = {"pass": f"{passes}/{len(gs)}", "tok": med([g["tokens"] for g in gs]), "tools": med([g["tools"] for g in gs]),
                            "dash+arrow": sum(g["dash"] + g["arrow"] for g in gs), "metric": [g.get("metric") for g in gs],
                            "errors": sum(1 for g in gs if g["error"]), "reasons": [g.get("reason") for g in gs if g.get("reason")]}
            rows[tid] = row
        report[t] = {"kind": ab.TESTS[t]["kind"], "total": tot, "tasks": rows}
    return report


if __name__ == "__main__":
    rep = summarize(sys.argv[1:] or list(ab.TESTS))
    (ab.ROOT / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    for t, v in rep.items():
        print(f"== {t} ({v['kind']}) total A={v['total']['A']} B={v['total']['B']}")
        for tid, row in v["tasks"].items():
            for arm in "AB":
                x = row.get(arm, {})
                print(f"   {tid:10s} {arm} pass={x.get('pass')} tok={x.get('tok')} tools={x.get('tools')} d+a={x.get('dash+arrow')} metric={x.get('metric')} err={x.get('errors')}")
