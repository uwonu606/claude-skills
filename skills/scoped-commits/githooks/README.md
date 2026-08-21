# commit-msg 훅

커밋 제목이 scope 형식인지 검사한다. **git 수준 훅이라 커밋을 만드는 모든 것에 걸린다** — Claude Code, Cursor, Codex, Aider, 사람, CI.

## 왜 git 훅인가

Claude Code 의 PreToolUse 훅으로도 같은 검사를 할 수 있지만, 그건 Claude Code 에만 걸린다. 다른 에이전트가 커밋하면 아예 돌지 않는다.

실측으로 두 가지가 확인됐다.

- **훅은 다른 에이전트를 실제로 막는다.** Codex 를 규약을 모르는 저장소에서 돌렸더니 3/3 이 `Add parser normalization and config defaults` 같은 제목으로 시도했다가 거부됐다.
- **거부 메시지만으로 1회 만에 복구한다.** 3/3 이 두 번째 시도에서 통과했고, `--no-verify` 나 훅 삭제 같은 우회는 한 번도 없었다. 셋 중 둘은 훅 스크립트를 열어보지도 않고 거부 메시지만 보고 고쳤다.

같은 프롬프트로 Claude 를 돌렸을 때는 6/6 이 Conventional Commits 로 나갔다. 기본값은 모델마다 다르지만 어느 쪽도 이 규약을 알아서 지키지 않는다.

## 설치

### 1. 전역 디스패처 — 기계당 한 번

```bash
bash ~/.claude/skills/scoped-commits/githooks/install-dispatch.sh
```

`~/.git-hooks/` 에 디스패처를 깔고 전역 `core.hooksPath` 를 거기로 건다. 이후 **저장소마다 설정할 일이 없다.**

이 단계가 있는 이유는 `core.hooksPath` 가 커밋으로 전파되지 않기 때문이다(git 보안 정책). 저장소마다 켜는 방식이면 클론 직후 한 줄을 잊는 순간 훅이 **조용히 꺼진 채로** 돈다 — 파일은 멀쩡히 있고 문서도 컨벤션을 말하는데 아무것도 안 막는다. 조용한 실패는 시끄러운 실패보다 비싸다.

전역 `core.hooksPath` 를 걸면 git 은 저장소별 `.git/hooks/` 를 통째로 무시한다. 그래서 디스패처가 두 곳을 대신 부른다 — 저장소의 `.githooks/<이름>` 과 `.git/hooks/<이름>`. husky 처럼 로컬에 훅을 까는 도구가 죽지 않는다. `pre-push` 처럼 stdin 을 쓰는 훅에는 읽어 둔 입력을 **원본 바이트 그대로** 다시 먹인다 — 끝의 개행이 하나라도 어긋나면 자식 훅의 `while read` 가 마지막 줄을 버린다.

서버측 훅(`pre-receive`·`update`·`post-receive`·`post-update`·`proc-receive`)에서는 `.githooks/` 쪽이 사실상 닿지 않는다. receive-pack 중에는 `git rev-parse --show-toplevel` 이 워킹트리 루트가 아니라 `.git` 디렉토리를 돌려주고(non-bare), bare 저장소에서는 아예 실패한다. 서버측 훅은 `<gitdir>/hooks/` 에 두어야 한다 — 거기는 디스패처가 확실히 부른다.

`proc-receive` 는 stdin/stdout 양방향 프로토콜 훅이라 읽어 뒀다 재생하지 않고 그대로 물려준다. 프로토콜을 말하는 훅으로 `refs/for/*` push 를 돌려 버전 협상부터 `ok` 응답까지 완주하는 것을 확인했다.

`git-p4` 의 훅 4종(`p4-pre-submit`·`p4-changelist`·`p4-prepare-changelist`·`p4-post-changelist`)도 `core.hooksPath` 를 탄다. `git-p4` 가 `git hook run --ignore-missing` 으로 부르기 때문이다 — 이름이 없으면 조용히 건너뛰므로 깔아 두어야 한다.

디스패처는 **복사본**으로 깔린다. 스킬을 갱신한 뒤에는 이 명령을 다시 돌려야 새 디스패처가 반영된다 — 다시 돌리면 최신인지 갱신했는지 알려주므로, 확실치 않으면 그냥 돌리면 된다.

되돌리려면 `bash install-dispatch.sh --uninstall`.

### 2. 저장소를 옵인 — 저장소당 한 번

```bash
mkdir -p .githooks
cp ~/.claude/skills/scoped-commits/githooks/commit-msg .githooks/commit-msg
chmod +x .githooks/commit-msg
```

커밋하면 클론에 따라오고, 디스패처가 깔린 기계에서는 **클론 직후 아무 설정 없이 걸린다.**

이 저장소를 쓰지 않기로 하면 `.githooks/commit-msg` 를 지우면 된다.

### 디스패처 없이 쓰려면

저장소마다 `git config core.hooksPath .githooks` 를 직접 걸어도 동작한다. 대신 클론마다 그 한 줄이 필요하다.

## 이식성

macOS 는 GPLv2 에 묶여 **bash 3.2.57**(2007년)을 싣는다. `#!/usr/bin/env bash` 는 보통 그것을 집으므로, 이 디렉토리의 스크립트는 bash 3.2 에서 돌아야 한다.

bash 3.2 컨테이너로 실측했다.

- 스크립트 5개(`.githooks/` 두 벌, 이 디렉토리의 `commit-msg`·`dispatch`·`install-dispatch.sh`)가 `bash -n` 을 통과한다.
- `commit-msg` 판정 21건이 bash 5.3 과 **완전히 같다** — type 접두어 4종과 `type(scope):` 형태, 접두어 없음, 대문자 scope, 콜론 뒤 공백 없음, 하이픈으로 끝나는 scope, 언더스코어·점 scope, 설명 없음까지 12건 거부. 한 글자 scope, 하이픈 scope, 숫자 섞인 scope, Merge·Revert·`fixup!`·`squash!`·주석·빈 제목 9건 통과.
- `dispatch` — 워킹트리에서 `.githooks/` 다음 `.git/hooks/` 순서로 부르고 첫 훅의 종료코드(7)를 그대로 내보내며 둘째를 부르지 않는다. bare 저장소(toplevel 없음)에서도 `<gitdir>/hooks/` 를 부르고, stdin 페이로드가 ref 1·2·3개 모두 **바이트 그대로** 자식에게 간다.
- `install-dispatch.sh` — 설치·최신·갱신 3상태가 각각 맞고, 훅 27종이 깔리고, `--uninstall` 이 디렉토리와 `core.hooksPath` 를 되돌린다.
- `pre-commit` 불변 4건 — 정상 트리 통과, commit-msg 두 벌 어긋남 거부, type 목록 어긋남 거부, 배포본이 없으면 검사 생략.

bash 4 이상에서만 되는 구문(대소문자 변환 `${v,,}`, 연관배열, `mapfile`, nameref, `&>>`)은 쓰지 않았다.

`sed` 는 두 구현에서 쟀다. bash 3.2 컨테이너의 것은 busybox 이고, 그와 별개로 FreeBSD 의 sed 소스를 받아 컴파일해 돌렸다 — macOS 가 싣는 것이 FreeBSD sed 다. 판정 21건과 `pre-commit` 의 목록 추출식이 양쪽에서 GNU sed 와 같은 결과를 냈다.

다만 그 빌드는 **FreeBSD 의 sed 이지 FreeBSD 의 정규식 엔진은 아니다.** 리눅스에서 링크하느라 정규식은 musl 것이 들어갔고, BRE 에서 `\+` 가 먹는 것으로 그 사실이 드러난다. 즉 명령 파싱과 `s///` 의미론까지가 실측이고 엔진 동작은 아니다. 쓰는 식이 전부 POSIX BRE 기본(`^` `.*` `\(...\)` `\1`)이라 엔진 차이가 물릴 자리는 좁다고 보지만, 그건 판단이다.

Windows 실기는 확인하지 않았다. Git for Windows(MSYS)의 `ln` 이 심볼릭 링크 대신 **복사**로 동작하는 경우를 스텁으로 재현해, 설치가 끝까지 돌고 훅 22개가 전부 디스패처와 같은 내용으로 깔리는 것까지는 확인했다. Git for Windows 가 실제로 그 동작을 하는지, 한다면 어느 조건에서인지는 미검증이다.

## 무엇을 검사하는가

제목 한 줄만 본다.

- `feat`·`fix`·`docs`·`chore`·`refactor`·`style`·`test`·`build`·`ci`·`perf`·`revert` 접두어를 거부한다. `type(scope):` 형태도 거부한다.
- `<scope>: <설명>` 형태가 아니면 거부한다. scope 는 소문자로 시작하는 kebab-case.
- 머지·리버트·`fixup!`·`squash!` 커밋은 형식을 git 이 만든 것이므로 건드리지 않는다.

## 무엇을 검사하지 않는가

**분할을 강제하지 않는다.** 커밋이 제대로 나뉘었는지는 diff 의 의미를 판정해야 알 수 있고, 훅이 할 수 있는 일이 아니다. 형식만 맞으면 한 덩어리 커밋도 통과한다. 분할은 `/scoped-commits` 스킬이 맡는다.

**제목 길이와 본문도 검사하지 않는다.** 36자 상한과 본문 세 요소는 `messages.md` 의 규칙이지만, 훅이 그것까지 막으면 급한 커밋이 통째로 멈춘다. 형식 위반은 되돌리기 어렵고 길이는 `--amend` 로 고쳐지므로, 되돌리기 어려운 쪽만 막는다.
