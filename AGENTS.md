# claude-skills

직접 만들어 쓰는 Claude Code 스킬 모음. 스킬 하나당 디렉토리 하나, 그 안에 `SKILL.md`.

## 저장소 구조

```
skills/<이름>/SKILL.md     스킬 하나당 디렉토리 하나
skills/<이름>/references/  필요할 때 읽는 보조 문서
skills/<이름>/agents/      그 스킬이 위임하는 전문 에이전트 정의 (~/.claude/agents 로 설치)
install.sh                 ~/.claude/skills, ~/.claude/agents 로 symlink 설치
```

새 스킬은 템플릿이 아니라 기존 스킬의 짜임을 본떠 시작한다 — 단계마다 완료 기준, 보조 문서는 읽는 시점에 맞춰 `references/` 로.

`install.sh` 는 `SKILL.md` 를 가진 디렉토리만 스킬로 인식한다. 보조 파일은 스킬 디렉토리 아래 `references/`(필요할 때 읽는 문서)·`scripts/`(실행 코드)·`assets/`(산출물에 쓰는 파일)·`agents/`(서브에이전트 정의, 파일 하나가 에이전트 하나)에 두고 `SKILL.md` 에서 상대경로로 가리킨다 — symlink 설치라 경로가 유지된다. 저장소에서 사라진 스킬의 symlink 는 `install.sh` 가 걷는다 — 스킬 설명문끼리 발동 경쟁을 하므로, 흡수된 스킬이 옛 이름으로 남아 있으면 안 된다(verify-first README 의 1라운드 실측).

**측정 기법은 스킬이 아니라 에이전트에 둔다.** 추천 전 검증은 verify-first 하나가 진입점이고, 성능·설계 변경 같은 도메인의 측정 기법은 `skills/verify-first/agents/` 의 에이전트 정의가 갖는다. 새 도메인이 생기면 스킬을 하나 더 만드는 게 아니라 에이전트를 하나 더 두고 verify-first 3단계 표에 한 줄 더한다.

`/<이름>` 슬래시 커맨드는 디렉토리 이름에서 온다. frontmatter 의 `name` 은 목록에 보이는 레이블일 뿐이지만, 둘이 갈리면 헷갈리므로 디렉토리 이름과 같게 둔다.

## 규약

**커밋** — scoped-commits 컨벤션을 쓴다. 커밋은 scoped-commits 스킬이 만들고, 규칙은 `skills/scoped-commits/` 에 있다.

**브랜치** — topic-branch 컨벤션을 쓴다. 작업 하나를 `<이니셜>/<산출물>` 브랜치와 워크트리로 열고 `--no-ff` 로 합치며, 규칙은 `skills/topic-branch/` 에 있다.

강제하는 층은 없다 — 규약은 스킬과 문서로만 전달된다.
