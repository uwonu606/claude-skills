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

전역 `core.hooksPath` 를 걸면 git 은 저장소별 `.git/hooks/` 를 통째로 무시한다. 그래서 디스패처가 세 곳을 대신 부른다 — `~/.git-hooks/user/<이름>`, 저장소의 `.githooks/<이름>`, 그리고 `.git/hooks/<이름>`. 넓은 것에서 좁은 것 순서이고, 앞의 것이 0 이 아닌 코드로 끝나면 거기서 멈춘다. husky 처럼 로컬에 훅을 까는 도구가 죽지 않는다. `pre-push` 처럼 stdin 을 쓰는 훅에는 읽어 둔 입력을 **원본 바이트 그대로** 다시 먹인다 — 끝의 개행이 하나라도 어긋나면 자식 훅의 `while read` 가 마지막 줄을 버린다.

서버측 훅(`pre-receive`·`update`·`post-receive`·`post-update`·`proc-receive`)에서는 `.githooks/` 쪽이 사실상 닿지 않는다. receive-pack 중에는 `git rev-parse --show-toplevel` 이 워킹트리 루트가 아니라 `.git` 디렉토리를 돌려주고(non-bare), bare 저장소에서는 아예 실패한다. 서버측 훅은 `<gitdir>/hooks/` 에 두어야 한다 — 거기는 디스패처가 확실히 부른다.

`proc-receive` 는 stdin/stdout 양방향 프로토콜 훅이라 읽어 뒀다 재생하지 않고 그대로 물려준다. 프로토콜을 말하는 훅으로 `refs/for/*` push 를 돌려 버전 협상부터 `ok` 응답까지 완주하는 것을 확인했다.

`git-p4` 의 훅 4종(`p4-pre-submit`·`p4-changelist`·`p4-prepare-changelist`·`p4-post-changelist`)도 `core.hooksPath` 를 탄다. `git-p4` 가 `git hook run --ignore-missing` 으로 부르기 때문이다 — 이름이 없으면 조용히 건너뛰므로 깔아 두어야 한다.

디스패처는 **복사본**으로 깔린다. 스킬을 갱신한 뒤에는 이 명령을 다시 돌려야 새 디스패처가 반영된다 — 다시 돌리면 최신인지 갱신했는지 알려주므로, 확실치 않으면 그냥 돌리면 된다.

되돌리려면 `bash install-dispatch.sh --uninstall`.

### 기계 전체에 걸 훅은 `user/` 에

```bash
cp 내훅 ~/.git-hooks/user/pre-commit
chmod +x ~/.git-hooks/user/pre-commit
```

**훅 이름 자리(`~/.git-hooks/<이름>`)를 직접 건드리지 마라.** 거기는 디스패처를 부르는 래퍼다. 덮어쓰면 그 이름의 위임이 끊겨 저장소 훅이 안 돈다. `user/` 에 두면 저장소 훅과 **함께** 실행된다.

## 왜 훅 이름 자리가 잠겨 있나

예전에는 훅 이름 27개가 전부 디스패처 본체로의 심볼릭 링크였다. 그래서 `echo ... > ~/.git-hooks/pre-commit` 한 번이면 링크를 따라가 본체가 덮어써졌다. 실측하니 2316바이트가 65바이트가 됐고, 그 뒤로 **훅 이름 27개 전부**가 그 스크립트를 실행했다 — 커밋 규약 강제가 죽고 레거시 `.git/hooks` 위임도 끊겼는데 **오류 한 줄 나지 않았다.**

쓰기 방식이 운명을 갈랐다. 경로를 열어서 쓰는 것(`>`, `cat >`, `cp`, `tee`)은 링크를 따라가고, 엔트리를 갈아치우는 것(`mv`, `install`, `sed -i`, `ln -sf`, `rm` 후 생성)은 안전하다. 하필 사람이 제일 자연스럽게 쓰는 `>` 와 `cp` 가 파괴 쪽이었다.

지금은 세 층으로 막는다.

- **`user/` 가 정당한 요구를 받는다.** 훅 이름 자리를 건드릴 이유 자체를 없앤다.
- **훅 이름 자리가 심볼릭 링크가 아니라 래퍼 파일이다.** 덮어써도 그 이름 하나만 바뀐다 — 폭발 반경이 27에서 1로 준다.
- **본체와 래퍼에 쓰기 권한이 없다(`555`).** 덮어쓰려는 시도가 조용한 성공 대신 `Permission denied` 로 끝난다. 갱신은 설치 스크립트가 `rm -f` 를 먼저 하므로 막히지 않는다 — 파일을 지우는 것은 디렉토리 권한이다.

작정하고 `chmod` 를 걸어 덮어쓰는 것은 막지 못한다. 막을 생각도 없다 — 여기서 막으려는 것은 고의가 아니라 실수다.

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
- `dispatch` — 워킹트리에서 `user/` → `.githooks/` → `.git/hooks/` 순서로 부르고 첫 훅의 종료코드(7)를 그대로 내보내며 뒤를 부르지 않는다. 세 곳에 stdin 을 쓰는 훅을 동시에 두어도 각각 같은 페이로드를 온전히 받는다. bare 저장소(toplevel 없음)에서도 `<gitdir>/hooks/` 를 부르고, stdin 페이로드가 ref 1·2·3개 모두 **바이트 그대로** 자식에게 간다.
- `install-dispatch.sh` — 설치·최신·갱신 3상태가 각각 맞고, 훅 27종이 깔리고, 본체·래퍼가 `555` 로 놓이고, 래퍼가 훅 이름을 제대로 넘기고, `--uninstall` 이 디렉토리와 `core.hooksPath` 를 되돌린다.
- `pre-commit` 불변 4건 — 정상 트리 통과, commit-msg 두 벌 어긋남 거부, type 목록 어긋남 거부, 배포본이 없으면 검사 생략.

bash 4 이상에서만 되는 구문(대소문자 변환 `${v,,}`, 연관배열, `mapfile`, nameref, `&>>`)은 쓰지 않았다.

`sed` 는 두 구현에서 쟀다. bash 3.2 컨테이너의 것은 busybox 이고, 그와 별개로 FreeBSD 의 sed 소스를 받아 컴파일해 돌렸다 — macOS 가 싣는 것이 FreeBSD sed 다. 판정 21건과 `pre-commit` 의 목록 추출식이 양쪽에서 GNU sed 와 같은 결과를 냈다.

다만 그 빌드는 **FreeBSD 의 sed 이지 FreeBSD 의 정규식 엔진은 아니다.** 리눅스에서 링크하느라 정규식은 musl 것이 들어갔고, BRE 에서 `\+` 가 먹는 것으로 그 사실이 드러난다. 즉 명령 파싱과 `s///` 의미론까지가 실측이고 엔진 동작은 아니다. 쓰는 식이 전부 POSIX BRE 기본(`^` `.*` `\(...\)` `\1`)이라 엔진 차이가 물릴 자리는 좁다고 보지만, 그건 판단이다.

Windows 의 심볼릭 링크 문제는 **원인째 사라졌다.** 훅 이름 자리를 래퍼 파일로 바꾸면서 설치 스크립트가 `ln` 을 아예 부르지 않는다. `ln` 을 실패하도록 만든 스텁을 `PATH` 앞에 놓고 돌려도 설치가 끝까지 도는 것을 확인했다.

남은 Windows 미검증은 권한 쪽이다. NTFS 는 유닉스 권한 비트를 그대로 쓰지 않으므로 `555` 가 실제로 쓰기를 막을지 모른다. 막지 못해도 앞의 두 층(`user/` 와 래퍼)은 그대로 살아 있다.

## 무엇을 검사하는가

제목 한 줄만 본다.

- `feat`·`fix`·`docs`·`chore`·`refactor`·`style`·`test`·`build`·`ci`·`perf`·`revert` 접두어를 거부한다. `type(scope):` 형태도 거부한다.
- `<scope>: <설명>` 형태가 아니면 거부한다. scope 는 소문자로 시작하는 kebab-case.
- 머지·리버트·`fixup!`·`squash!` 커밋은 형식을 git 이 만든 것이므로 건드리지 않는다.

## 무엇을 검사하지 않는가

**분할을 강제하지 않는다.** 커밋이 제대로 나뉘었는지는 diff 의 의미를 판정해야 알 수 있고, 훅이 할 수 있는 일이 아니다. 형식만 맞으면 한 덩어리 커밋도 통과한다. 분할은 `/scoped-commits` 스킬이 맡는다.

**제목 길이와 본문도 검사하지 않는다.** 36자 상한과 본문 세 요소는 `messages.md` 의 규칙이지만, 훅이 그것까지 막으면 급한 커밋이 통째로 멈춘다. 형식 위반은 되돌리기 어렵고 길이는 `--amend` 로 고쳐지므로, 되돌리기 어려운 쪽만 막는다.
