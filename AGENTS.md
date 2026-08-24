# claude-skills

직접 만들어 쓰는 Claude Code 스킬 모음. 스킬 하나당 디렉토리 하나, 그 안에 `SKILL.md`.

## 저장소 구조

```
skills/<이름>/SKILL.md   스킬 하나당 디렉토리 하나
skills/<이름>/references/  필요할 때 읽는 보조 문서
templates/SKILL.md       새 스킬 시작용 템플릿
install.sh               ~/.claude/skills 로 symlink 설치
```

`install.sh` 는 `SKILL.md` 를 가진 디렉토리만 스킬로 인식한다. 보조 파일은 스킬 디렉토리 아래 `references/`(필요할 때 읽는 문서)·`scripts/`(실행 코드)·`assets/`(산출물에 쓰는 파일)에 두고 `SKILL.md` 에서 상대경로로 가리킨다 — symlink 설치라 경로가 유지된다.

`/<이름>` 슬래시 커맨드는 디렉토리 이름에서 온다. frontmatter 의 `name` 은 목록에 보이는 레이블일 뿐이지만, 둘이 갈리면 헷갈리므로 디렉토리 이름과 같게 둔다.

## 커밋

이 저장소는 scoped-commits 컨벤션을 쓴다. 커밋은 scoped-commits 스킬이 만들고, 규칙은 `skills/scoped-commits/` 에 있다. 강제하는 층은 없다 — 규약은 스킬과 문서로만 전달된다.
