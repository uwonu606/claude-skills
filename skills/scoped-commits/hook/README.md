# scoped-commits 가드 훅

`/scoped-commits`는 사용자 호출 전용이라 Claude가 스스로 부를 수 없다. 그래서 Claude가 직접 `git commit`을 실행하면 스킬을 건너뛰게 되는데, 그때 제목이 어떻게 나가는지 재보면 **6회 중 6회가 Conventional Commits(type 접두어)** 였다. 이 훅이 그 자리를 막는다.

## 무엇을 하는가

- `git commit` 명령의 제목을 검사해서 `type:` 또는 `type(scope):` 형태이거나 `<scope>: ` 형태가 아니면 **거부**하고, `/scoped-commits`를 사용자에게 요청하라는 지시를 되돌려준다.
- 거부 문면에 "이 스킬은 사용자만 호출할 수 있다"를 넣는 것이 핵심이다. 금지만 알린 문면으로는 3회 모두 제목만 고쳐 우회했고, 이 한 줄을 더하자 3회 모두 사용자에게 넘겼다.
- 부수적으로 현재 권한 모드를 `~/.claude/.scoped-commits-mode`에 남긴다. 스킬이 분할안 승인을 받을지 판단하는 데 쓴다.

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
printf '{"tool_name":"Bash","permission_mode":"default","tool_input":{"command":"git commit -m \"fix: x\""}}\0' \
  | bash ~/.claude/skills/scoped-commits/hook/scoped-commits-guard.sh
```

`permissionDecision: deny`가 나오면 걸린 것이다. 같은 명령을 `-m "some-scope: x"`로 바꾸면 아무것도 출력하지 않는다.
