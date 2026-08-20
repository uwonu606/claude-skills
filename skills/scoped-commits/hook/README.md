# scoped-commits 가드 훅

`/scoped-commits`는 사용자 호출 전용이라 Claude가 스스로 부를 수 없다. 그래서 Claude가 직접 `git commit`을 실행하면 스킬을 건너뛰게 되는데, 그때 제목이 어떻게 나가는지 재보면 **6회 중 6회가 Conventional Commits(type 접두어)** 였다. 이 훅이 그 자리를 막는다.

## 무엇을 하는가

- `git commit` 명령의 제목을 검사해서 `type:` 또는 `type(scope):` 형태이거나 `<scope>: ` 형태가 아니면 **거부**하고, `/scoped-commits`를 사용자에게 요청하라는 지시를 되돌려준다.
- 거부 문면에 "이 스킬은 사용자만 호출할 수 있다"를 넣는 것이 핵심이다. 금지만 알린 문면으로는 3회 모두 제목만 고쳐 우회했고, 이 한 줄을 더하자 3회 모두 사용자에게 넘겼다.
- 부수적으로 현재 권한 모드를 `~/.claude/.scoped-commits-mode`에 남긴다. 스킬이 분할안 승인을 받을지 판단하는 데 쓴다.

## 두 층

| 층 | 파일 | 누구에게 |
|---|---|---|
| 강제 | 저장소의 `.githooks/commit-msg` | **커밋을 만드는 모든 것** — Claude Code, Cursor, Codex, Aider, 사람, CI |
| 조기 차단 | 이 PreToolUse 훅 | Claude Code (더 자세한 메시지, 스킬로 라우팅) |

PreToolUse 훅은 Claude Code 에만 걸린다. 다른 에이전트가 커밋하면 아예 돌지 않으므로, 강제는 git 수준 훅이 맡는다.

## 어디에 걸리는가

**저장소의 `.githooks/commit-msg` 존재가 옵인이다.** 그 파일이 곧 강제 장치이므로, 별도 마커를 두면 "마커는 있는데 훅은 없다" 같은 어긋남이 생긴다.

```bash
mkdir -p .githooks
cp ~/.claude/skills/scoped-commits/githooks/commit-msg .githooks/commit-msg
chmod +x .githooks/commit-msg
git config core.hooksPath .githooks
```

`core.hooksPath` 는 git 보안 정책상 커밋으로 전파되지 않으므로 **클론마다 한 번** 설정해야 한다.

`git -C <경로> commit` 이나 `cd <경로> && git commit` 처럼 다른 저장소를 가리키는 경우 **cwd 가 아니라 그 대상 저장소**를 본다.

heredoc 본문은 데이터로 취급해 건너뛴다 — 본문에 `git commit` 이라는 글자가 있다고 커밋으로 읽으면, 그 문자열을 담은 파일을 쓰는 명령이 전부 막힌다.

권한 모드 기록은 옵인과 무관하게 항상 돈다 — 스킬이 어디서 호출되든 그 값을 읽어야 하기 때문이다.

## 무엇을 하지 않는가

**분할은 강제하지 않는다.** 커밋이 제대로 나뉘었는지는 diff의 의미를 판정해야 알 수 있고, 훅이 할 수 있는 일이 아니다. 형식만 맞으면 한 덩어리 커밋도 통과한다.

## 설치

`~/.claude/settings.json`의 `PreToolUse`에 붙인다. 스킬을 symlink로 설치했다면 아래 경로가 그대로 맞는다.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/skills/scoped-commits/hook/scoped-commits-guard.sh\""
          }
        ]
      }
    ]
  }
}
```

`matcher`를 `"*"`로 두는 이유는 권한 모드 기록 때문이다. `"Bash"`로 좁혀도 커밋 차단은 그대로 동작하지만, 모드 파일이 Bash 호출에서만 갱신된다.

이미 다른 `PreToolUse` 훅을 쓰고 있으면 같은 matcher의 `hooks` 배열에 항목을 하나 더 넣는다.

## 확인

```bash
check() {
  python3 -c 'import json,sys;sys.stdout.write(json.dumps(
    {"tool_name":"Bash","permission_mode":"default",
     "tool_input":{"command":sys.argv[1]}})+"\0")' "$1" \
  | bash ~/.claude/skills/scoped-commits/hook/scoped-commits-guard.sh
}

check 'git commit -m "fix: x"'          # deny 가 나와야 한다
check 'git -C /tmp commit -m "fix: x"'  # deny 가 나와야 한다
check 'git commit -m "some-scope: x"'   # 아무것도 출력하지 않아야 한다
```

`bash printf` 로 JSON 을 만들지 마라. 작은따옴표 안의 `\"` 에서 백슬래시가 떨어져 나가
깨진 JSON 이 되고, 훅은 그것을 조용히 삼켜 아무것도 출력하지 않는다 — 훅이 멀쩡한데도
"안 걸린다"로 읽힌다.
