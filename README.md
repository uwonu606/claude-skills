# claude-skills

직접 만들어 쓰는 Claude Code 스킬 모음. 스킬 하나당 디렉토리 하나, 그 안에 `SKILL.md`. 출력 스타일은 `output-styles/` 에 파일 하나씩. 모든 프로젝트에 싣는 지침은 `claude-md/CLAUDE.md`.

## 설치

```bash
git clone git@gh-alt:uwonu606/claude-skills.git && cd claude-skills
bash install.sh                # skills/ 전부 ~/.claude/skills 로, output-styles/ 는 ~/.claude/output-styles 로 symlink
```

symlink 라 저장소에서 `SKILL.md` 를 고치면 다음 세션부터 반영된다. 일부만 설치·프로젝트 설치·복사본·제거는 `bash install.sh -h` 에 있다.

지워진 스킬의 symlink 는 `install.sh` 가 걷는다 — 스킬끼리 description 으로 발동을 다투므로, 지운 스킬이 옛 이름으로 남아 있으면 안 된다.

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

`/<이름>` 슬래시 커맨드는 디렉토리 이름에서 온다. frontmatter 의 `name` 은 목록에 보이는 레이블일 뿐이지만, 둘이 갈리면 헷갈리므로 디렉토리 이름과 같게 둔다.

`description` 은 Claude 가 이 스킬을 띄울지 판단하는 유일한 근거다. 무엇을 하는지 + 어떤 상황·표현에서 트리거되는지를 같이 적는다.

본문은 Claude 가 읽고 실행하는 절차서다. template 이 아니라 기존 스킬의 짜임을 본떠 시작한다 — 단계마다 완료 기준, 보조 문서는 읽는 시점에 맞춰 `references/` 로.

## 출력 스타일

출력 스타일은 그 도구가 답을 그리는 방식 때문에 생기는 것만 정한다. 어느 도구에서나 뜻이 통하는 지침은 답의 모양까지 `CLAUDE.md` 에 둔다. 출력 스타일은 시스템 프롬프트에 붙어 매 턴 적용되고, subagent 에는 안 간다.

`output-styles/<파일>.md` 하나가 스타일 하나다. frontmatter 의 `name` 이 스타일 이름이고, `keep-coding-instructions: true` 를 빼면 Claude Code 의 코딩 지침이 통째로 빠진다. 켜는 것은 `~/.claude/settings.json` 에 `"outputStyle": "<name>"` 을 적는 것이고, 새 세션이나 `/clear` 뒤에 적용된다.

| 스타일 | 하는 것 |
|---|---|
| `scan` | Claude Code 터미널이 답을 그리는 방식에 맞춘다: 눌러 여는 `경로:줄`, 굵은 글자 묶음 제목, 백틱, 이미 보인 diff. 설명·절차·보고의 모양은 `claude-md/CLAUDE.md` 가 정하므로 그 파일과 함께 쓴다 |

## CLAUDE.md

`claude-md/CLAUDE.md` 는 모든 프로젝트의 session 에 싣는 지침이다. 사용자는 방향을 정하고 답만 읽는다는 첫 문단에서 세 절(정하는 사람, 읽는 사람, 믿는 정도)이 내려온다. Claude Code 의 기능 이름을 쓰지 않아서 다른 도구의 지침 파일로 옮겨도 뜻이 통한다. `install.sh` 는 이 파일을 설치하지 않는다. 쓰려면 `~/.claude/CLAUDE.md` 로 복사한다.

## 규약

**커밋** — 제목은 `<scope>: <설명>`, 본문은 모든 커밋에 쓴다. 규칙은 `skills/scoped-commits/` 에 있다.

**브랜치** — 작업 하나를 `<산출물>` 브랜치와 워크트리로 열고 `--no-ff` 로 합친다. 규칙은 `skills/topic-branch/` 에 있다.

강제하는 층은 없다 — 규약은 스킬로만 전달된다.
