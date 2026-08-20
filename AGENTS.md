# claude-skills

직접 만들어 쓰는 Claude Code 스킬 모음. 스킬 하나당 디렉토리 하나, 그 안에 `SKILL.md`.

## 저장소 구조

```
skills/<이름>/SKILL.md   스킬 하나당 디렉토리 하나
templates/SKILL.md       새 스킬 시작용 템플릿
install.sh               ~/.claude/skills 로 symlink 설치
```

`install.sh` 는 `SKILL.md` 를 가진 디렉토리만 스킬로 인식한다. 스킬이 보조 파일(스크립트, 참고 문서)을 쓰면 같은 디렉토리에 두고 `SKILL.md` 에서 상대경로로 가리킨다 — symlink 설치라 경로가 유지된다.

`SKILL.md` frontmatter 의 `name` 은 디렉토리 이름과 같아야 하고, 그대로 `/<이름>` 슬래시 커맨드가 된다.

## 커밋

이 저장소는 **scoped-commits** 컨벤션을 쓴다.

- 제목은 `<scope>: <설명>` 이다. `feat`·`fix`·`docs` 같은 **type 접두어를 쓰지 않는다.** 로그를 읽는 사람이 알고 싶은 것은 변경의 종류가 아니라 어느 영역을 건드렸는가다.
- scope 는 그 코드가 하는 일의 이름이다. 소문자 kebab-case, **파일명·디렉토리명을 그대로 쓰지 않는다.**
- 제목은 scope 포함 36자 이내, `~한다` 로 끝내고 마침표를 붙이지 않는다.
- **모든 커밋에 본문을 쓴다.** 왜 했는지, 고려했다가 하지 않은 것과 그 이유, 확인하지 못한 것을 담는다.
- 커밋은 의미 단위로 나눈다 — 커밋 하나가 혼자 읽었을 때 하나의 이야기다.

전체 규칙은 `skills/scoped-commits/` 에 있다. Claude Code 에서는 `/scoped-commits` 로 커밋하면 이 규칙이 적용된다.

강제는 `.githooks/commit-msg` 가 한다. git 수준 훅이라 Claude Code·Cursor·Codex·Aider·사람·CI 어디서 커밋하든 걸린다. 그 파일의 존재가 곧 이 컨벤션을 쓴다는 뜻이다.

클론한 뒤 한 번 켜야 한다 — `core.hooksPath` 는 git 보안 정책상 커밋으로 전파되지 않는다.

    git config core.hooksPath .githooks

