# 정리

다 쓴 브랜치·워크트리를 치울 때 읽는다.

## 판정 — 머지 커밋이 이름을 부르는 것만

`--no-ff` 로 합치므로, 합쳐진 브랜치마다 main 에 제 이름을 담은 머지 커밋이 남는다. 그 **표식**이 지울 것을 정한다.

```bash
git branch --format='%(refname:short)' | grep -vx main | while read -r b; do
  if git log main --merges --format='%s' | grep -qE "'$b'|/$b\$"; then echo "$b"; fi
done
```

머지 커밋 제목 두 모양을 다 잡는다 — 로컬의 `Merge branch '<이름>'`, PR 의 `Merge pull request #N from <소유자>/<이름>`.

`git branch --merged main` 만으로 판정하면 커밋이 없는 브랜치가 전부 머지됨으로 들어와 사람이 방금 딴 작업을 지운다 — 실측에서 방금 딴 `hotfix-session-leak`·`spike-wasm` 과 합쳐진 이름의 접두인 `login-rate` 까지 합쳐진 둘과 한 목록에 올랐고, 위 판정은 합쳐진 둘만 돌려줬다. 표식은 합쳐졌다는 **증거**고, `--merged` 는 도달 가능성일 뿐이다.

목록이 비면 지울 것이 없다고 보고한다 — squash 로 합친 브랜치는 표식을 안 남겨 여기 안 뜨고, 그건 손으로 지운다.

## 절차

1. 위 판정으로 목록을 뽑아 사용자에게 보인다.
2. 워크트리가 달린 것은 워크트리를 먼저 지운다. `git worktree list` 에서 `.claude/worktrees/` 아래 경로를 확인하고 `git worktree remove <경로>`. 미커밋 변경으로 거부되면 그 항목은 건너뛰고 보고한다.
3. `git branch -d <이름>` — 소문자 `-d` 라야 git 이 머지 확인을 한 번 더 한다.
4. 원격에 밀어 둔 것은 같은 판정을 통과한 것만 `git push origin --delete <이름>`.

지금 세션이 `EnterWorktree` 로 연 그 워크트리 안에 있다면 `ExitWorktree` 의 `remove` 가 2·3단계를 한 번에 한다 — 워크트리 디렉토리와 **브랜치를 함께** 지우므로 그 브랜치는 3단계에서 뺀다(미커밋 변경이 있으면 거부한다). 이전 세션이 연 워크트리에는 안 먹고 조용히 no-op 이라, 정리는 대개 위 `git worktree remove` 경로로 간다.

**완료 기준**: 판정 명령이 빈 목록을 돌려주거나, 남은 항목마다 건너뛴 이유가 보고됐다. 원격까지 지웠으면 `git ls-remote --heads origin <이름>` 이 비어 있다.
