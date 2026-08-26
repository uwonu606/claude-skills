# topic-branch

작업 하나를 브랜치+워크트리로 **열고, 합치고, 치우는** 생명주기. `scoped-commits` 와 짝이 된다 — 그 스킬이 커밋 하나의 단위를 정하고, 이 스킬이 그 커밋들이 사는 브랜치의 단위를 정한다.

이 문서는 **구조와 왜**를 적는다. 절차 원문은 아래 세 파일에 살고 여기서는 링크만 한다.

## 구조

| 층 | 어디 | 하는 일 |
|---|---|---|
| 시작 | [`SKILL.md`](SKILL.md) | 이니셜을 확보하고 **이름을 지어** 워크트리를 연다 |
| 합치기 | [`references/merge.md`](references/merge.md) | `--no-ff` 로 main 에 넣고, 충돌 났을 때만 동기화한다 |
| 정리 | [`references/cleanup.md`](references/cleanup.md) | **무엇을 지워도 되는지** 판정하고 지운다 |

읽는 시점으로 갈린 층이다. 세 층은 한 작업의 서로 다른 시점에 불리고, 한 번에 하나만 필요하다.

## 설계 판단

### 접두어는 소유다

형식 자체는 [`SKILL.md`](SKILL.md) 2단계가 정한다. 여기 적는 것은 그 형식을 고른 이유다.

슬래시 앞자리가 뜻하는 것은 **누구의 작업인가**다. 분류(`feat/`)도 성질(`work/`)도 기전(`wt/`)도 아니다. 성질 이름은 손으로 딴 브랜치도 같은 성질을 가져 경계가 사실로 성립하지 않고, 기전 이름은 워크트리를 지우고 이어 작업하는 순간 거짓이 된다.

슬래시 뒤는 산출물 **명사구**다 — 무엇을 하는가가 아니라 무엇이 생기는가. 영역을 앞에 세우지 않는 것도 같은 이유다. 패키지를 가로지르는 작업에서 거짓이 되고, 영역은 커밋 scope 가 이미 말한다.

`scoped-commits` README 가 근거로 든 여섯 저장소(Linux·Git·Go·nixpkgs·Node.js·FreeBSD)의 PR 브랜치 500건 중 봇·중복을 뺀 410건 실측(2026-08-25):

- 75%가 접두어 없는 순수 kebab. 슬래시 접두어 24%는 타입 37 · 사람 30 · 영역 12 · 도구 12 로 흩어져 **하나의 규약을 이루지 못한다.** 이 저장소들은 브랜치가 통합 단위가 아니다(메일링 리스트·Gerrit).
- 83%가 명사/영역으로 시작, 16%만 동사로 시작.
- 자동화가 만든 브랜치는 예외 없이 **그 자동화의 이름**을 네임스페이스로 쓴다 — `auto-update/`(41) · `actions/`(4) · `agent/`(3) · `codex/`(3) · `cursor/`(1).

유일하게 진짜 규약을 가진 곳이 `<scope>: <설명>` 을 만든 프로젝트다. `gitster/git` 토픽 브랜치 100건:

- **99건이 `<2글자>/<kebab>`, 이니셜 길이 100% 정확히 2자.**
- 슬래시 뒤는 `영역-무엇을` 순(`ag/rebase-update-refs-limit-to-branches`), 95%가 명사 시작.
- 그 앞 토큰이 실제 커밋 scope 와 일치하는 비율 29% 이상(최근 300커밋에서 뽑은 scope 73종만 대조한 하한치). 즉 **겹치되 강제되지 않는다.**
- `topic/` 접두어는 500건 중 **0건**. Git 문서의 용어이지 브랜치명 접두어가 아니다.

실측 길이는 중앙값 21자·3~4토큰, 90분위 32자다.

### 이니셜은 `git config --local topic-branch.initials` 에 산다

- **local 인 이유**: 저장소마다 다른 이름을 쓸 수 있다. `--global` 로 두면 그 선택지가 없어진다.
- **git config 에 둬도 되는 근거**: git-config 문서가 명시한다 — "Other git-related tools may and do use their own variables. When inventing new variables for use in your own tool, make sure their names do not conflict with those that are used by Git itself and other popular tools, and describe them in your documentation." 조건은 겹치지 않을 것과 문서에 적을 것 둘이다. 실측으로 git 은 모르는 키를 조용히 무시했다(`git status`·`git fsck` 경고 없음).
- **섹션이 `topic-branch` 인 이유**: `user.*` 는 git 자신의 섹션이라(`user.name`·`user.email`·`user.signingKey`·`user.useConfigOnly`) 나중에 조용히 충돌한다. 같은 일을 하는 도구들이 전부 자기 이름을 쓴다 — git-flow 의 `gitflow.prefix.feature`, git-town 의 `git-town.branch-prefix`.
- **핸들을 그대로 안 쓰는 이유**: `uwonu606/login-rate-limit` 25자 대 `uw/login-rate-limit` 19자. 실측 평균 브랜치명이 20.9자라 접두어가 이름 절반을 먹는다. GitHub PR 목록에는 작성자가 이미 아바타로 붙어 중복이고, 값을 버는 곳은 `git log` 뿐이다.

**혼자 쓰는 저장소를 전제로 이니셜을 그냥 정한다.** 여러 사람이 같은 저장소에서 이 스킬을 쓰면 2자가 겹칠 수 있고, 겹치면 정리 판정(`--merged --list '<이니셜>/*'`)이 남의 브랜치를 끌어온다. 겹칠 확률은 작지 않다 — gitster 는 브랜치 100건에 고유 이니셜 36개를 쓰는데, 그 규모에서 2자를 무작위 배정하면 충돌 없을 확률이 39%뿐이다(기여자 5명 1% · 20명 25% · 40명 69%). git 이 안 부딪히는 건 이니셜이 실명에서 오고 메인테이너가 손으로 조정하기 때문이다.

한때 `SKILL.md` 1단계가 브랜치와 머지 커밋에서 이미 쓰인 이니셜을 뽑아 피했다. 걷어 냈다 — 이 저장소들은 기여자가 1명이라 그 명령이 빈 출력만 돌려주고, 제안되는 값이 명령을 돌리든 안 돌리든 같았다. **기여자가 둘 이상이 되면 되살릴 자리가 여기다.**

### 머지는 `--no-ff` — 알고 고른 소수파

fast-forward 와 squash 를 둘 다 막는다. 머지 커밋이 안 생기면 브랜치명이 로그에서 통째로 사라져(실측: ff 이력에서 `ag/` 0건) **어디부터 어디까지가 한 작업인지**가 남지 않는다 — 동시에 여러 갈래를 열어 두면 그 경계가 로그에서 유일한 단서다. squash 는 `scoped-commits` 가 **의미 단위**로 나눈 커밋을 하나로 뭉개서, 그 스킬의 전제("커밋 하나는 혼자 정당화되는 변경")를 무너뜨린다.

유명 저장소 12곳 실측: squash 8(react·vscode·vue·svelte·deno·pytorch·elasticsearch·grafana) · 머지 커밋 3(kubernetes·rust·rails) · rebase 1(django).

두 진영은 **커밋을 무엇으로 보느냐**에서 갈린다 — squash 진영은 PR 이 의미 단위고, 머지 커밋 진영은 커밋이 의미 단위다. `scoped-commits` 는 후자다.

rebase 는 개별 커밋을 보존하므로 `scoped-commits` 를 안 깬다 — squash 와 달리 여기서 막는 이유는 하나뿐이다. 작업 경계가 사라진다. 갈래가 하나씩만 열린다면 그 손실이 작으니, 그때는 rebase 도 성립한다.

### 동기화는 충돌이 났을 때만

rebase 는 작성일을 보존한다(실측: 작성일 유지, 커밋일만 오늘). 잃는 것은 SHA 다 — 바뀌면 force-push 가 되고, 리뷰 중이던 커밋이 PR 에서 사라진다.

### 구조는 main 하나 + 태그

release 브랜치를 두지 않는다. 배포 지점은 태그로 표시한다.

- 패치를 안 할 거면 태그가 그 일을 다 한다 — `git checkout v1.0` · `git diff v1.0..main` · `git show v1.0:<파일>` · `git worktree add -b <핫픽스> <경로> v1.0` 전부 실측으로 확인했다. **나중에 진짜 패치가 필요해지면 그때 태그에서 브랜치를 따면 된다.**
- 미리 두면 쓰지도 않을 브랜치가 목록에 쌓인다. 태그는 `git branch -d` 가 건드리지 못해(실측) 배포 지점 표시로 더 튼튼하다.
- **이 스킬의 정리가 릴리스 브랜치를 지켜 주지는 않는다.** `release-1.0` 은 main 의 **조상**이라 `--merged` 단독으로 훑는 도구나 사람에게는 그대로 잡힌다(실측). 이 스킬의 판정은 이니셜 필터를 함께 걸어 `release-1.0` 을 아예 안 건드리지만, 그건 이 스킬 밖에서 도는 정리까지 막아 주지는 못한다는 뜻이기도 하다. 브랜치를 안 두면 그 층이 통째로 없어진다.
- 실측한 네 저장소(node·go·nixpkgs·freebsd)는 전부 release 브랜치를 두지만, 그건 **백포트 의무** 때문이다(`backport-556078-to-release-26.05`). 그 표본은 `<scope>: <설명>` 커밋을 쓴다는 이유로 골랐고 전부 버전 배포판이라, 릴리스 구조의 근거로는 편향돼 있다.

**구버전에 패치를 보내야 하는 종류라면 이 결정을 다시 봐야 한다.** 그때는 release 브랜치가 필요하고, 자동 정리에서 제외하는 규칙도 함께 정해야 한다.

### 모노레포 특수 규칙은 없다

패키지 접두어(`web/...`)를 브랜치에 붙이지 않는다 — 모노레포를 쓰는 이유 자체가 여러 패키지를 한 번에 고치는 것이고, 그런 작업에서 접두어는 하나만 고르거나 나머지를 숨겨 **거짓이 된다.** 영역은 커밋 scope 가 이미 말하므로 층이 겹칠 이유도 없다.

## 알고 남긴 구멍

**`description` 이 안 걸리면 규약을 우회한다.** 세 트리거(시작·합치기·정리)를 `description` 하나에 담은 것은 그래서다 — 정리 트리거가 거기 없으면 정리할 때 스킬이 아예 안 불리고, 그냥 `git branch -d` 를 친다. 담아도 이건 확률이지 보장이 아니다.

훅으로 막지 않는다. 이 저장소는 `commit-msg` 훅 층을 이미 걷어 냈고("훅이 실제로 거부한 것은 없다" — [`scoped-commits/README.md`](../scoped-commits/README.md)), 되살리면 그 판단을 뒤집는 셈이다.

**GitHub 저장소 기본 머지 방식이 squash 면 조용히 깨진다.** 스킬은 PR 을 열 때 설정을 확인해 알려 줄 뿐이고, 스킬 밖에서 머지 버튼을 누르면 걸리는 것이 없다. 저장소 설정에서 merge commit 을 켜는 것은 사람 몫이다.

## 어디를 볼 것

- [`SKILL.md`](SKILL.md) — 작업을 새로 여는 절차. `/topic-branch` 로 부르거나 새 작업을 시작하면 이걸 따른다
- [`references/merge.md`](references/merge.md) — `--no-ff` 머지의 로컬·PR 두 경로와 충돌 시 동기화
- [`references/cleanup.md`](references/cleanup.md) — 무엇을 지워도 되는지 판정하는 두 조건과 삭제 순서
