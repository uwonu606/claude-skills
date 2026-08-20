# commit-msg 훅

커밋 제목이 scope 형식인지 검사한다. **git 수준 훅이라 커밋을 만드는 모든 것에 걸린다** — Claude Code, Cursor, Codex, Aider, 사람, CI.

## 왜 git 훅인가

Claude Code 의 PreToolUse 훅으로도 같은 검사를 할 수 있지만, 그건 Claude Code 에만 걸린다. 다른 에이전트가 커밋하면 아예 돌지 않는다.

실측으로 두 가지가 확인됐다.

- **훅은 다른 에이전트를 실제로 막는다.** Codex 를 규약을 모르는 저장소에서 돌렸더니 3/3 이 `Add parser normalization and config defaults` 같은 제목으로 시도했다가 거부됐다.
- **거부 메시지만으로 1회 만에 복구한다.** 3/3 이 두 번째 시도에서 통과했고, `--no-verify` 나 훅 삭제 같은 우회는 한 번도 없었다. 셋 중 둘은 훅 스크립트를 열어보지도 않고 거부 메시지만 보고 고쳤다.

같은 프롬프트로 Claude 를 돌렸을 때는 6/6 이 Conventional Commits 로 나갔다. 기본값은 모델마다 다르지만 어느 쪽도 이 규약을 알아서 지키지 않는다.

## 설치

```bash
mkdir -p .githooks
cp ~/.claude/skills/scoped-commits/githooks/commit-msg .githooks/commit-msg
chmod +x .githooks/commit-msg
git config core.hooksPath .githooks
```

`.githooks/commit-msg` 를 저장소에 커밋하면 클론에 따라온다. 하지만 **`core.hooksPath` 는 전파되지 않는다** — git 보안 정책이라 우회할 방법이 없고, 클론마다 한 번 설정해야 한다. 설정하지 않으면 훅은 조용히 꺼진 채로 돈다.

이 저장소를 쓰지 않기로 하면 `git config --unset core.hooksPath` 한 줄이면 된다.

## 무엇을 검사하는가

제목 한 줄만 본다.

- `feat`·`fix`·`docs`·`chore`·`refactor`·`style`·`test`·`build`·`ci`·`perf`·`revert` 접두어를 거부한다. `type(scope):` 형태도 거부한다.
- `<scope>: <설명>` 형태가 아니면 거부한다. scope 는 소문자로 시작하는 kebab-case.
- 머지·리버트·`fixup!`·`squash!` 커밋은 형식을 git 이 만든 것이므로 건드리지 않는다.

## 무엇을 검사하지 않는가

**분할을 강제하지 않는다.** 커밋이 제대로 나뉘었는지는 diff 의 의미를 판정해야 알 수 있고, 훅이 할 수 있는 일이 아니다. 형식만 맞으면 한 덩어리 커밋도 통과한다. 분할은 `/scoped-commits` 스킬이 맡는다.

**제목 길이와 본문도 검사하지 않는다.** 36자 상한과 본문 세 요소는 `messages.md` 의 규칙이지만, 훅이 그것까지 막으면 급한 커밋이 통째로 멈춘다. 형식 위반은 되돌리기 어렵고 길이는 `--amend` 로 고쳐지므로, 되돌리기 어려운 쪽만 막는다.
