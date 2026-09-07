---
name: topic-branch
description: 작업 하나를 브랜치+워크트리로 열고 닫는 생명주기. 새 작업을 시작해 브랜치를 딸 때, 작업 브랜치를 main 에 합치거나 PR 을 열 때, 다 쓴 브랜치와 워크트리를 정리할 때 쓴다.
disable-model-invocation: false
---

작업 하나를 워크트리+브랜치로 연다. 아래는 새로 여는 경로다.

- **작업을 main 에 합치는 요청이면** — 머지·PR·충돌 — [`references/merge.md`](references/merge.md) 를 읽는다.
- **다 쓴 브랜치·워크트리를 치우는 요청이면** [`references/cleanup.md`](references/cleanup.md) 를 읽는다.

## 1. 이름을 짓는다

지금 받은 작업 설명에서 바로 뽑는다. **산출물을 부르는 kebab-case 명사구** 하나다 — 예: `login-rate-limit`.

영숫자·점·밑줄·하이픈만 쓰고 64자 이내다(`EnterWorktree` 의 `name` 제약).

**완료 기준**: 이름이 kebab 명사구이고, 문자 제약과 64자를 지킨다.

## 2. 워크트리를 열고 들어간다

두 경로 다 `.claude/worktrees/<이름>` 에 열고 origin/main(없으면 로컬 main)을 기준점으로 잡는다. 갈림은 **무엇이 워크트리를 요청했는가**다.

- 사용자가 "워크트리"라고 말했거나 `CLAUDE.md`·메모리가 워크트리로 일하라고 지시했으면 `EnterWorktree` 에 그 이름을 `name` 으로 준다. 그 도구가 스스로 요구하는 조건이다.
- 그 밖에는 git 으로 직접 만들고 그 디렉토리에서 이어 간다.

  ```bash
  base=origin/main; git rev-parse -q --verify "$base" >/dev/null || base=main
  git worktree add -b <이름> .claude/worktrees/<이름> "$base"
  ```

  경로가 이미 차 있는 것처럼 브랜치를 만든 **뒤** 실패하면 그 브랜치가 고아로 남는다(실측) — 실패했으면 `git branch -d <이름>` 으로 확인해 치운다. 기준점이 안 풀려서 실패한 경우에는 브랜치가 안 생긴다.

이름을 다시 짓기로 했으면, 아직 커밋이 없을 때 워크트리째 버리고 다시 단다. 브랜치만 rename 하면 워크트리 디렉토리 이름은 따라오지 않아 둘이 갈린 채 남는다(실측).

**완료 기준**: 세션이 워크트리 안에 있고 `git branch --show-current` 가 1단계에서 지은 이름을 돌려준다.
