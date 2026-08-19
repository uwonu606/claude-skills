#!/usr/bin/env bash
# PreToolUse 훅: scope 없는 커밋을 막고 /scoped-commits 로 보낸다.
#
# 막는 것은 제목 형식 하나다. 규칙 없이 커밋하게 두면 제목이 6/6으로
# Conventional Commits(type 접두어)로 나가고, 그것은 히스토리에 영구히 남는다.
# 분할이 맞는지는 diff의 의미를 판정해야 알 수 있어 훅이 못 하므로 강제하지 않는다.
#
# 부수 효과로 현재 권한 모드를 ~/.claude/.scoped-commits-mode 에 남긴다.
# 스킬이 분할안 승인을 받을지 판단하는 데 쓴다. PreToolUse 는 명령 실행
# 전에 돌므로, 스킬이 그 파일을 cat 하는 시점에는 이미 최신이다.
#
# 흔한 경로(git commit 이 아닌 모든 호출)는 서브프로세스 없이 끝난다.

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
[[ $compact == *'gitcommit'* ]] || exit 0

printf '%s' "$input" | python3 -S -c '
import json, re, shlex, sys

DENY_SCOPE = """커밋이 거부되었습니다.
이 저장소는 커밋 제목에 type 접두어(feat, fix, docs, chore, refactor, style, test, build, ci, perf, revert)를 쓰지 않습니다.
제목은 `<scope>: <설명>` 형태이고, scope 는 그 코드가 하는 일의 이름입니다 — 소문자 kebab-case 이며 파일명·디렉토리명을 그대로 쓰지 않습니다.
이 변경은 /scoped-commits 스킬로 커밋해야 합니다. 이 스킬은 사용자만 호출할 수 있으므로, 제목만 고쳐 다시 시도하지 말고 사용자에게 실행을 요청하십시오."""

DENY_UNSEEN = """커밋이 거부되었습니다.
훅이 제목을 확인할 수 없습니다. 메시지를 `-m` 이나 heredoc(`git commit -F -`)으로 주십시오.
`-F <파일>` 이나 에디터로는 명령줄에 제목이 없어 검사할 수 없습니다."""

TYPES = ("feat", "fix", "docs", "chore", "refactor", "style",
         "test", "build", "ci", "perf", "revert")

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))
    sys.exit(0)

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)
command = (payload.get("tool_input") or {}).get("command")
if not isinstance(command, str):
    sys.exit(0)

# 파이프·연쇄 안에서 git commit 조각만 꺼낸다.
segments = [s.strip() for s in re.split(r"&&|\|\||;|\n", command)]
seg = next((s for s in segments if re.match(r"^git\s+(-\S+\s+|--\S+(=\S+)?\s+)*commit\b", s)), None)
if seg is None:
    sys.exit(0)

try:
    argv = shlex.split(seg)
except ValueError:
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
    if a.startswith("-m") and len(a) > 2:
        title = a[2:]
        break
    if a in ("-F", "--file") and i + 1 < len(argv) and argv[i + 1] == "-":
        # heredoc 본문이 명령줄에 실려 있다. 첫 비어 있지 않은 줄이 제목이다.
        body = command.split("<<", 1)[-1]
        lines = body.split("\n")[1:]
        title = next((l for l in lines if l.strip()), None)
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
