# 합치기

작업 브랜치를 main 에 합칠 때 읽는다.

두 경로 다 `--no-ff` 다. 머지 커밋이 제 제목에 브랜치명을 박아 로그에 **표식**을 남긴다 — `scoped-commits` 가 나눈 의미 단위 커밋이 어느 작업이었는지 남고, 정리의 판정이 이 표식을 읽는다.

## 로컬 경로

주 워크트리(main)에서 친다.

```bash
git merge --no-ff <브랜치>
```

머지 커밋 메시지는 git 이 만든 그대로 둔다 — git 이 메시지를 만든 커밋은 `scoped-commits` 도 그대로 둔다.

## PR 경로

PR 을 연다. 저장소의 PR 머지 방식이 merge commit 인지 확인하고, squash 만 켜져 있으면 사용자에게 알린다 — squash 는 표식을 안 남겨 정리가 그 브랜치를 못 찾는다.

```bash
gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
```

`gh` 가 없으면 이 확인을 건너뛰고, 머지 버튼을 누르기 전에 방식을 직접 보라고 알린다.

## 동기화

PR 이 열려 있는 동안 main 이 움직여도 그대로 둔다. 충돌이 났을 때만 브랜치에서 `git merge main` 을 친다 — rebase 는 이미 push 한 커밋을 다시 써서 PR 의 리뷰 이력과 어긋난다.

## 다 쓴 뒤

머지가 끝난 브랜치와 워크트리를 지우는 절차는 [`cleanup.md`](cleanup.md) 에 있다.

**완료 기준**: 로컬로 합쳤으면 `git log -1 --format=%s main` 이 그 브랜치명을 담은 머지 커밋 제목이다. PR 로 열었으면 PR 이 열려 있고 충돌 없음 상태다.
