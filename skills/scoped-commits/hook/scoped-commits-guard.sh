#!/usr/bin/env bash
# PreToolUse 훅: scope 없는 커밋을 막고 /scoped-commits 로 보낸다.
#
# 이것은 Claude Code 에만 걸리는 조기 차단이다. 강제는 저장소의
# .githooks/commit-msg 가 맡는다 — 그쪽은 커밋을 만드는 모든 것에 걸린다.
# 여기서 먼저 막는 이유는 메시지를 더 자세히 줄 수 있고 스킬로 라우팅할 수
# 있기 때문이다. 규칙 없이 커밋하게 두면 제목이 6/6 으로 Conventional
# Commits 로 나가고, 그것은 히스토리에 영구히 남는다.
#
# 적용 범위는 저장소의 .githooks/commit-msg 가 정한다. 그 파일이 곧 옵인
# 아티팩트이자 강제 장치라, "마커는 있는데 훅은 없다" 같은 어긋남이 없다.
# 분할이 맞는지는 diff 의 의미를 판정해야 알 수 있어 훅이 못 하므로
# 강제하지 않는다.
#
# 부수 효과로 현재 권한 모드를 ~/.claude/.scoped-commits-mode 에 남긴다.
# 스킬이 분할안 승인을 받을지 판단하는 데 쓴다. PreToolUse 는 명령 실행
# 전에 돌므로, 스킬이 그 파일을 cat 하는 시점에는 이미 최신이다.

IFS= read -r -d '' input

# 공백을 지운 사본. 컴팩트 JSON과 정렬된 JSON을 같은 패턴으로 맞춘다.
compact=${input// /}

# 권한 모드 기록. 실패해도 훅을 멈추지 않는다.
mode=default
case "$compact" in
  *'"permission_mode":"bypassPermissions"'*) mode=bypassPermissions ;;
  *'"permission_mode":"acceptEdits"'*)       mode=acceptEdits ;;
  *'"permission_mode":"dontAsk"'*)           mode=dontAsk ;;
  *'"permission_mode":"auto"'*)              mode=auto ;;
  *'"permission_mode":"plan"'*)              mode=plan ;;
esac
printf '%s' "$mode" > "$HOME/.claude/.scoped-commits-mode" 2>/dev/null || true

[[ $compact == *'"tool_name":"Bash"'* ]] || exit 0
# `git -C <경로> commit` 은 공백을 지우면 git-C/x/ycommit 이 되어 gitcommit 을
# 찾는 검사로는 걸리지 않는다. commit 이라는 글자만 보고 넘긴다.
[[ $compact == *commit* ]] || exit 0

printf '%s' "$input" | python3 -S -c '
import json, os, re, shlex, sys

HOOK_REL = os.path.join(".githooks", "commit-msg")
HOOK_TOKEN = "scoped-commits"

DENY_TAIL = """이 변경은 /scoped-commits 스킬로 커밋해야 합니다. 이 스킬은 사용자만 호출할 수 있으므로, 명령을 고쳐 다시 시도하지 말고 사용자에게 실행을 요청하십시오."""

DENY_SCOPE = """커밋이 거부되었습니다.
이 저장소는 커밋 제목에 type 접두어(feat, fix, docs, chore, refactor, style, test, build, ci, perf, revert)를 쓰지 않습니다.
제목은 `<scope>: <설명>` 형태이고, scope 는 그 코드가 하는 일의 이름입니다 — 소문자 kebab-case 이며 파일명·디렉토리명을 그대로 쓰지 않습니다.
""" + DENY_TAIL

DENY_UNSEEN = """커밋이 거부되었습니다.
훅이 제목을 확인할 수 없습니다. 메시지를 `-m` 이나 heredoc(`git commit -F -`)으로 주십시오.
`-F <파일>` 이나 에디터로는 명령줄에 제목이 없어 검사할 수 없습니다.
""" + DENY_TAIL

TYPES = ("feat", "fix", "docs", "chore", "refactor", "style",
         "test", "build", "ci", "perf", "revert")

# 값을 따로 받는 git 전역 옵션. 이것들 뒤의 토큰은 하위명령이 아니다.
GLOBAL_VALUE_OPTS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                     "--exec-path", "--config-env", "--super-prefix"}
SHELL_OPS = {"&&", "||", ";", "|", ">", ">>", "<", "2>", "&"}

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))
    sys.exit(0)

def split_heredocs(command):
    """(명령 부분, {구분자: 본문}) 로 가른다.

    heredoc 본문은 데이터지 명령이 아니다. 본문에 `git commit` 이라는 글자가
    있다고 커밋으로 읽으면, 그 문자열을 담은 파일을 쓰는 명령이 전부 막힌다.
    """
    lines = command.split("\n")
    code, bodies, i = [], {}, 0
    while i < len(lines):
        line = lines[i]
        code.append(line)
        m = re.search(r"<<-?\s*[\"\x27]?([A-Za-z_][A-Za-z0-9_]*)[\"\x27]?", line)
        i += 1
        if not m:
            continue
        delim, body = m.group(1), []
        while i < len(lines) and lines[i].strip() != delim:
            body.append(lines[i])
            i += 1
        i += 1                      # 구분자 줄을 건너뛴다
        bodies[delim] = "\n".join(body)
    return "\n".join(code), bodies

def commit_argv(code):
    """git ... commit 의 (인자, -C 대상, 그 시점의 cwd 이동). 없으면 (None, None, None)."""
    try:
        toks = shlex.split(code)
    except ValueError:
        return None, None, None
    toks = [t.lstrip("({") for t in toks]
    cd = None
    for i, t in enumerate(toks):
        # `cd <경로> && git commit` 도 대상 저장소를 바꾼다. -C 만 보면 놓친다.
        if t == "cd" and i + 1 < len(toks) and toks[i + 1] not in SHELL_OPS:
            nxt = toks[i + 1]
            cd = nxt if os.path.isabs(nxt) else os.path.join(cd or ".", nxt)
            continue
        if t != "git" and not t.endswith("/git"):
            continue
        j, target = i + 1, None
        while j < len(toks) and toks[j].startswith("-"):
            if toks[j] in GLOBAL_VALUE_OPTS:
                if toks[j] == "-C" and j + 1 < len(toks):
                    target = toks[j + 1]
                j += 2
            else:
                if toks[j].startswith("--git-dir="):
                    target = os.path.dirname(toks[j].split("=", 1)[1])
                j += 1
        if j < len(toks) and toks[j] == "commit":
            rest = []
            for a in toks[j + 1:]:
                if a in SHELL_OPS:
                    break
                rest.append(a)
            return rest, target, cd
    return None, None, None

def opted_in(target, cd, cwd):
    """대상 저장소가 이 컨벤션을 쓰기로 했는가.

    옵인 아티팩트는 .githooks/commit-msg 자체다 — 그 파일이 모든 도구에
    걸리는 강제 장치이므로, 따로 마커를 두면 둘이 어긋날 수 있다.
    """
    try:
        base = cwd or os.getcwd()
        if cd:
            base = os.path.join(base, cd)
        d = os.path.abspath(os.path.join(base, target or "."))
    except Exception:
        return False
    while True:
        p = os.path.join(d, HOOK_REL)
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                if HOOK_TOKEN in fh.read():
                    return True
        except Exception:
            pass
        if os.path.exists(os.path.join(d, ".git")):
            return False        # 저장소 루트인데 훅이 없다
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)
command = (payload.get("tool_input") or {}).get("command")
if not isinstance(command, str):
    sys.exit(0)

code, bodies = split_heredocs(command)
argv, target, cd = commit_argv(code)
if argv is None:
    sys.exit(0)

if not opted_in(target, cd, payload.get("cwd")):
    sys.exit(0)

# 기존 메시지를 재사용하는 형태는 검사 대상이 아니다.
if any(a.startswith(("-C", "--reuse-message", "--reedit-message",
                     "--fixup", "--squash")) for a in argv):
    sys.exit(0)

title = None
for i, a in enumerate(argv):
    if a in ("-m", "--message") and i + 1 < len(argv):
        title = argv[i + 1]
        break
    if a.startswith("--message="):
        title = a.split("=", 1)[1]
        break
    # 묶인 단축 플래그도 값을 싣는다: -am, -sm.
    if re.match(r"^-[A-Za-z]*m$", a) and i + 1 < len(argv):
        title = argv[i + 1]
        break
    if a.startswith("-m") and len(a) > 2 and not a[2:].startswith("-"):
        title = a[2:]
        break
    if a in ("-F", "--file") and i + 1 < len(argv) and argv[i + 1] == "-":
        # 메시지가 heredoc 본문으로 들어온다. 첫 비어 있지 않은 줄이 제목이다.
        for body in bodies.values():
            cand = next((l for l in body.split("\n") if l.strip()), None)
            if cand:
                title = cand
                break
        break

if title is None:
    # --amend 로 기존 메시지를 그대로 쓰는 경우는 통과.
    if "--amend" in argv:
        sys.exit(0)
    deny(DENY_UNSEEN)

title = title.strip().split("\n", 1)[0].strip()
m = re.match(r"^([a-z0-9][a-z0-9._/-]*)(\([^)]*\))?\s*:\s+\S", title)
if not m:
    deny(DENY_SCOPE)
if m.group(2) is not None or m.group(1) in TYPES:
    deny(DENY_SCOPE)
sys.exit(0)
'
