# 정리

다 쓴 브랜치·워크트리를 치울 때 읽는다.

## 판정 — 두 조건을 함께 건다

이니셜부터 확보한다. 값이 없으면 아래 판정이 `--list "/*"` 로 축약되어, 지울 브랜치가 있어도 **빈 목록에 exit 0** 을 돌려준다(실측). 값이 없으면 [`../SKILL.md`](../SKILL.md) 1단계로 가서 정하고 돌아온다.

```bash
git config --local topic-branch.initials
```

값이 있으면 두 조건을 함께 건다.

```bash
git branch --merged main --list "$(git config --local topic-branch.initials)/*"
```

`--merged` 단독은 커밋이 없는 브랜치를 전부 머지됨으로 세서, 사람이 방금 딴 브랜치를 지운다 — 실측에서 `hotfix-session-leak`·`spike-wasm` 이 그대로 목록에 들어왔다. 이니셜 필터가 **소유** 밖을 구조적으로 막는다.

이름이 유일하게 살아남는 표식이다. 워크트리 경로는 표식이 못 된다 — 워크트리를 지우는 순간 그 표식도 함께 사라지고, 원격에는 애초에 워크트리가 안 따라간다.

## 절차

1. 위 판정으로 목록을 뽑아 사용자에게 보인다.
2. 워크트리가 달린 것은 워크트리를 먼저 지운다. `git worktree list` 에서 `.claude/worktrees/` 아래 경로를 확인하고 `git worktree remove <경로>`. 미커밋 변경으로 거부되면 그 항목은 건너뛰고 보고한다.
3. `git branch -d <이름>` — 소문자 `-d` 라야 git 이 머지 확인을 한 번 더 한다.
4. 원격에 밀어 둔 것은 같은 판정을 통과한 것만 `git push origin --delete <이름>`.

지금 세션이 `EnterWorktree` 로 연 그 워크트리 안에 있다면 `ExitWorktree` 의 `remove` 가 2·3단계를 한 번에 한다 — 워크트리 디렉토리와 **브랜치를 함께** 지우므로 그 브랜치는 3단계에서 뺀다(미커밋 변경이 있으면 거부한다). 이전 세션이 연 워크트리에는 안 먹고 조용히 no-op 이라, 정리는 대개 위 `git worktree remove` 경로로 간다.

**완료 기준**: 이니셜이 설정된 상태에서 판정 명령이 빈 목록을 돌려주거나, 남은 항목마다 건너뛴 이유가 보고됐다. 원격까지 지웠으면 `git branch -r --list "origin/$(git config --local topic-branch.initials)/*"` 에도 그 이름이 없다.
