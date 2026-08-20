# scoped-commits 가드 훅

`/scoped-commits`는 사용자 호출 전용이라 Claude가 스스로 부를 수 없다. 그래서 Claude가 직접 `git commit`을 실행하면 스킬을 건너뛰게 되는데, 그때 제목이 어떻게 나가는지 재보면 **6회 중 6회가 Conventional Commits(type 접두어)** 였다. 이 훅이 그 자리를 막는다.

## 무엇을 하는가

- `git commit` 명령의 제목을 검사해서 `type:` 또는 `type(scope):` 형태이거나 `<scope>: ` 형태가 아니면 **거부**하고, `/scoped-commits`를 사용자에게 요청하라는 지시를 되돌려준다.
- 거부 문면에 "이 스킬은 사용자만 호출할 수 있다"를 넣는 것이 핵심이다. 금지만 알린 문면으로는 3회 모두 제목만 고쳐 우회했고, 이 한 줄을 더하자 3회 모두 사용자에게 넘겼다.
- 부수적으로 현재 권한 모드를 `~/.claude/.scoped-commits-mode`에 남긴다. 스킬이 분할안 승인을 받을지 판단하는 데 쓴다.

## 어디에 걸리는가

저장소의 **`AGENTS.md`** 안에 있는 마커 줄이 적용 범위를 정한다.

```markdown
<!-- scoped-commits: on -->
```

이 줄이 없는 저장소에서는 커밋을 검사하지 않는다. 훅은 전역(`~/.claude/settings.json`)에 한 번만 걸고, 저장소를 늘리는 것은 `AGENTS.md` 에 줄 하나다.

`AGENTS.md` 를 고른 이유는 **도구 중립 규약**이기 때문이다. Codex·Cursor·Copilot·Gemini CLI·Aider·Zed 등 6만 개 넘는 저장소가 쓰는 형식이라, 컨벤션을 거기 적으면 어느 에이전트가 커밋하든 같은 사실을 읽는다. 저장소별 `.claude/settings.json` 이나 전용 dotfile 은 Claude 전용이거나 아무 에이전트도 안 읽는다.

**Claude Code 는 `AGENTS.md` 를 직접 읽지 않는다.** `CLAUDE.md` 에 한 줄로 임포트한다.

```markdown
@AGENTS.md
```

마커 줄은 전용 HTML 주석이라 렌더링에는 안 보이고, 본문에 `scoped-commits` 가 산문으로 스쳐 나와도 걸리지 않는다.

`git -C <경로> commit` 처럼 다른 저장소를 가리키는 경우 **cwd 가 아니라 그 대상 저장소**의 `AGENTS.md` 를 본다. 그러지 않으면 엉뚱한 저장소의 설정을 읽는다.

권한 모드 기록은 마커와 무관하게 항상 돈다 — 스킬이 어디서 호출되든 그 값을 읽어야 하기 때문이다.

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
