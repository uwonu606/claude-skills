# 합치기

작업 브랜치를 main 에 합칠 때 읽는다.

머지는 두 경로 다 `--no-ff` 다 — `scoped-commits` 가 나눈 **의미 단위** 커밋과 브랜치명을 로그에 그대로 남기려는 선택이다. 근거는 [`../README.md`](../README.md) 의 "머지는 `--no-ff`" 절에 있다.

## 로컬 경로

주 워크트리(main)에서 친다.

```bash
git merge --no-ff <브랜치>
```

머지 커밋 메시지는 git 이 만든 그대로 둔다 — git 이 메시지를 만든 커밋은 `scoped-commits` 도 그대로 둔다.

## PR 경로

PR 을 연다. 저장소의 PR 머지 방식이 merge commit 인지 확인하고, squash 만 켜져 있으면 사용자에게 알린다.

```bash
gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
```

## 동기화

PR 이 열려 있는 동안 main 이 움직여도 그대로 둔다. 충돌이 났을 때만 브랜치에서 `git merge main` 을 친다. rebase 를 고르지 않는 이유는 [`../README.md`](../README.md) 의 "동기화는 충돌이 났을 때만" 절에 있다.

## 다 쓴 뒤

머지가 끝난 브랜치와 워크트리를 지우는 절차는 [`cleanup.md`](cleanup.md) 에 있다.

**완료 기준**: 로컬로 합쳤으면 main 의 최신 커밋이 그 브랜치명을 담은 머지 커밋이다. PR 로 열었으면 PR 이 열려 있고 충돌 없음 상태다.
