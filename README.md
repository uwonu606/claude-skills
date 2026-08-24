# claude-skills

직접 만들어 쓰는 Claude Code 스킬 모음. 스킬 하나당 디렉토리 하나, 그 안에 `SKILL.md`.

## 설치

```bash
git clone git@gh-alt:uwonu606/claude-skills.git && cd claude-skills
bash install.sh                # skills/ 전부 전역 설치 (~/.claude/skills) — symlink
bash install.sh foo bar        # 일부만 설치
bash install.sh --project      # 현재 프로젝트의 .claude/skills 에만 설치
bash install.sh --copy         # symlink 대신 복사본
bash install.sh --list         # 저장소에 있는 스킬 목록
bash install.sh --uninstall    # 제거 (이름 주면 그것만)
```

기본이 symlink라 저장소에서 `SKILL.md`를 고치면 다음 세션부터 바로 반영됩니다. `--copy`로 깔았다면 수정 후 `install.sh --copy --force`를 다시 실행해야 합니다 — 복사본은 이 저장소가 건 symlink 가 아니어서 `--force` 없이는 덮어쓰지 않습니다.

## 새 스킬 만들기

```bash
mkdir -p skills/<이름>
cp templates/SKILL.md skills/<이름>/SKILL.md
$EDITOR skills/<이름>/SKILL.md      # frontmatter의 name 을 디렉토리 이름과 맞출 것
bash install.sh <이름>
```

- `name`은 디렉토리 이름과 같아야 하고, 그대로 `/<이름>` 슬래시 커맨드가 됩니다.
- `description`은 Claude가 "이 스킬을 띄울지" 판단하는 유일한 근거입니다. 무엇을 하는지 + 어떤 상황/표현에서 트리거되는지를 같이 적으세요.
- 본문은 Claude가 읽는 절차서입니다. 설명문보다 실행 가능한 단계로 씁니다.
- 보조 파일은 스킬 디렉토리 아래 `references/`(필요할 때 읽는 문서)·`scripts/`(실행 코드)·`assets/`(산출물에 쓰는 파일)에 두고 `SKILL.md`에서 상대경로로 가리킵니다. symlink 설치라 경로가 그대로 유지됩니다.

만든 것을 커밋할 때는 이 저장소의 컨벤션을 따릅니다 — 제목은 `<scope>: <설명>` 이고 본문은 필수입니다. 규칙과 설계는 [`skills/scoped-commits/README.md`](skills/scoped-commits/README.md) 에 있습니다.

## 저장소 구성

```
claude-skills/
├── README.md
├── install.sh              # 설치/제거 스크립트
├── templates/SKILL.md      # 새 스킬 시작용 템플릿
└── skills/<이름>/
    ├── SKILL.md        # 스킬 하나당 디렉토리 하나
    └── references/     # 필요할 때 읽는 보조 문서
```
