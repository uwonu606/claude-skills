"""layered 출력 스타일 변형들을 같은 과제로 돌려 답을 모은다.

    python3 run.py --out DIR --task explain --n 3 base=A.md cand=B.md

답은 DIR/<task>/<arm>-<i>.md, 작업 폴더는 DIR/work/<task>/<arm>-<i>/ 에 남는다.
"""
import argparse
import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TASKS_DIR = Path(__file__).resolve().parent / "tasks"
TASKS = ("explain", "diagnose", "propose", "procedure", "code", "explain-holdout", "diagnose-holdout")
READ_ONLY = ["--disallowedTools", "Bash Edit Write NotebookEdit WebFetch WebSearch Agent"]
CAN_EDIT = [
    "--permission-mode", "acceptEdits",
    "--allowedTools", "Bash(python3:*)",
    "--disallowedTools", "WebFetch WebSearch Agent",
]


def style_named(style_text, name):
    lines = style_text.splitlines(keepends=True)
    renamed = [f"name: {name}\n" if line.startswith("name:") else line for line in lines]
    return "".join(renamed)


def prepare_workdir(workdir, task, arm, style_text):
    if workdir.exists():
        shutil.rmtree(workdir)
    fixture = TASKS_DIR / task
    if fixture.is_dir():
        shutil.copytree(fixture, workdir)
    styles = workdir / ".claude" / "output-styles"
    styles.mkdir(parents=True, exist_ok=True)
    style_name = f"eval-{arm}"
    (styles / f"{style_name}.md").write_text(style_named(style_text, style_name))
    return style_name


def run_one(out, task, arm, style_text, i):
    workdir = out / "work" / task / f"{arm}-{i}"
    style_name = prepare_workdir(workdir, task, arm, style_text)
    tool_flags = CAN_EDIT if task == "code" else READ_ONLY
    # The env var marks a nested session; claude -p refuses to start inside one.
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    command = ["claude", "-p", "--settings", json.dumps({"outputStyle": style_name}), *tool_flags]
    prompt = (TASKS_DIR / f"{task}.txt").read_text()
    result = subprocess.run(command, input=prompt, capture_output=True, text=True,
                            cwd=workdir, env=env, timeout=900)
    answer = out / task / f"{arm}-{i}.md"
    answer.parent.mkdir(parents=True, exist_ok=True)
    answer.write_text(result.stdout)
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--task", choices=TASKS, required=True)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("arms", nargs="+", help="arm=style.md")
    args = parser.parse_args()

    arms = dict(arm.split("=", 1) for arm in args.arms)
    jobs = [(arm, Path(path).read_text(), i) for arm, path in arms.items() for i in range(1, args.n + 1)]
    with ThreadPoolExecutor(args.jobs) as pool:
        for answer in pool.map(lambda job: run_one(args.out, args.task, *job), jobs):
            print(answer)


if __name__ == "__main__":
    main()
