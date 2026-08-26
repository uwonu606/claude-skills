---
name: topic-branch
description: 작업 하나를 브랜치+워크트리로 열고 닫는 생명주기. 새 작업을 시작해 브랜치를 딸 때, 작업 브랜치를 main 에 합치거나 PR 을 열 때, 다 쓴 브랜치와 워크트리를 정리할 때 쓴다.
disable-model-invocation: false
---

작업 하나를 워크트리+브랜치로 열고, `--no-ff` 로 합치고, 다 쓰면 치운다. 아래 절차는 작업을 새로 여는 경로다.

**작업을 main 에 합치는 요청이면 — 머지·PR·충돌 처리 — [`references/merge.md`](references/merge.md) 를 읽는다.**

**다 쓴 브랜치·워크트리를 치우는 요청이면 [`references/cleanup.md`](references/cleanup.md) 를 읽는다.**

## 1. 이니셜을 확보한다

`git config --local topic-branch.initials` 를 읽는다. 값이 있으면 그것을 쓴다.

없으면 이 저장소에서 이미 쓰인 이니셜을 뽑아 피한다. 브랜치가 지워진 뒤에도 머지 커밋에 이름이 남는다.

```bash
{ git branch -a --format='%(refname:short)'
  git log --merges --format=%s \
    | sed -nE "s/^Merge (remote-tracking )?branch '([^']+)'.*/\2/p
s|^Merge pull request #[0-9]+ from [^/]+/||p" ; } \
  | sed -E 's#^origin/##' | sed -nE 's#^(..)/.*#\1#p' | sort -u
```

CLI 머지·GitHub PR 머지·remote-tracking 세 형식만 읽는다. 옥토퍼스(`Merge branches 'a/x' and 'b/y'`)와 Bitbucket(`Merged in x/y (pull request #4)`)은 안 잡히고, 못 잡은 이니셜은 후보로 남아 제안될 뿐이라 사용자 확인이 걸러 낸다.

`user.name` 에서 2자 후보를 만들어 제안하고, 사용자 확인을 받아 박는다.

```bash
git config --local topic-branch.initials <값>
```

**완료 기준**: `git config --local topic-branch.initials` 가 2자 값을 돌려준다. 새로 정한 값이면 사용자 확인을 거쳤다.

## 2. 이름을 짓는다

지금 받은 작업 설명에서 바로 뽑는다. 형식은 `<이니셜>/<명사구-산출물>` kebab-case 다 — 예: `ag/login-rate-limit`.

- 슬래시 앞자리는 **소유**다 — 이니셜만 선다.
- `/` 로 나뉜 각 조각은 영숫자·점·밑줄·하이픈만 쓰고, 전체 64자 이내다(`EnterWorktree` 의 `name` 제약).

**완료 기준**: 이름이 `<이니셜>/<kebab 명사구>` 형식이고, 문자 제약과 64자를 지킨다.

## 3. 워크트리를 열고 들어간다

경로가 둘이고, **무엇이 워크트리를 요청했는가**로 갈린다.

- 사용자가 "워크트리"라고 말했거나 `CLAUDE.md`·메모리가 워크트리로 일하라고 지시했으면 `EnterWorktree` 에 그 이름을 `name` 으로 준다. 그 도구가 스스로 요구하는 조건이다.
- 그 밖에는 git 으로 직접 만들고 그 디렉토리에서 이어 간다.

  ```bash
  base=origin/main; git rev-parse -q --verify "$base" >/dev/null || base=main
  git worktree add -b <이름> .claude/worktrees/<이름> "$base"
  ```

  경로가 이미 차 있는 것처럼 브랜치를 만든 **뒤** 실패하면 그 브랜치가 고아로 남는다(실측) — 실패했으면 `git branch -d <이름>` 으로 확인해 치운다. 기준점이 안 풀려서 실패한 경우에는 브랜치가 안 생긴다.

두 경로 다 `.claude/worktrees/` 아래에 origin/기본브랜치를 기준점으로 잡고, 원격이 없으면 로컬 main 으로 떨어진다. `EnterWorktree` 쪽은 `worktree.baseRef` 가 정하고 기본값 `fresh` 가 그 값이다 — main 하나에 PR 흐름이라 로컬 main 은 origin/main 을 따라간다.

이름을 잘못 지었다고 판단되면, 아직 커밋이 없을 때 워크트리를 버리고 다시 단다. 브랜치를 rename 해도 워크트리 디렉토리 이름은 따라오지 않아 둘이 갈린 채 남는다(실측).

**완료 기준**: 세션이 워크트리 안에 있고 `git branch --show-current` 가 2단계에서 지은 이름을 돌려준다.
