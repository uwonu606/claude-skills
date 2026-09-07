# claude-skills

직접 만들어 쓰는 Claude Code 스킬 모음. 스킬 하나당 디렉토리 하나, 그 안에 `SKILL.md`.

## 설치

```bash
git clone git@gh-alt:uwonu606/claude-skills.git && cd claude-skills
bash install.sh                # skills/ 전부 ~/.claude/skills 로 symlink
```

symlink 라 저장소에서 `SKILL.md` 를 고치면 다음 세션부터 반영된다. 일부만 설치·프로젝트 설치·복사본·제거는 `bash install.sh -h` 에 있다.

지워진 스킬의 symlink 는 `install.sh` 가 걷는다 — 스킬끼리 설명문으로 발동을 다투므로, 지운 스킬이 옛 이름으로 남아 있으면 안 된다.

## 새 스킬 만들기

```bash
mkdir -p skills/<이름>
$EDITOR skills/<이름>/SKILL.md
bash install.sh <이름>
```

`install.sh` 는 `SKILL.md` 를 가진 디렉토리만 스킬로 본다. 보조 파일은 스킬 디렉토리 아래에 두고 `SKILL.md` 에서 상대경로로 가리킨다 — symlink 설치라 경로가 유지된다.

| 디렉토리 | 담는 것 |
|---|---|
| `references/` | 필요할 때 읽는 보조 문서 |
| `scripts/` | 실행 코드 |
| `assets/` | 산출물에 쓰는 파일 |
| `agents/` | 서브에이전트 정의, 파일 하나가 에이전트 하나 (`~/.claude/agents` 로 설치) |

`/<이름>` 슬래시 커맨드는 디렉토리 이름에서 온다. frontmatter 의 `name` 은 목록에 보이는 레이블일 뿐이지만, 둘이 갈리면 헷갈리므로 디렉토리 이름과 같게 둔다.

`description` 은 Claude 가 이 스킬을 띄울지 판단하는 유일한 근거다. 무엇을 하는지 + 어떤 상황·표현에서 트리거되는지를 같이 적는다.

본문은 Claude 가 읽고 실행하는 절차서다. 템플릿이 아니라 기존 스킬의 짜임을 본떠 시작한다 — 단계마다 완료 기준, 보조 문서는 읽는 시점에 맞춰 `references/` 로.

## 규약

**커밋** — 제목은 `<scope>: <설명>`, 본문은 모든 커밋에 쓴다. 규칙은 `skills/scoped-commits/` 에 있다.

**브랜치** — 작업 하나를 `<이니셜>/<산출물>` 브랜치와 워크트리로 열고 `--no-ff` 로 합친다. 규칙은 `skills/topic-branch/` 에 있다.

강제하는 층은 없다 — 규약은 스킬로만 전달된다.
