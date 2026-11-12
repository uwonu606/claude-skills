# 지도 형식

`map.md`는 사용자가 다시 읽는 글이다. 큰 그림과, 부품마다 사용자가 물은 것과 그 답이 한 줄씩 남는다. 한 판 따라가기는 화면에 보인 번호 줄을 그대로 옮긴다. 예시의 `<원문 대목>` 자리에는 실제로 읽은 원문을 그대로 넣는다. 읽지 않은 대목을 지어 넣지 않도록 예시에도 비워 두었다.

```markdown
---
topic: git rebase
kind: tech                    # tech | paper | video | repo
why: "PR 올리기 전에 지저분한 커밋을 정리하고 싶어"   # 사용자가 넘기면 없음
sources:                      # 논문·문서·레포의 경로나 URL. 받은 파일은 sources/ 에 둔다
  - "git-rebase 문서 https://git-scm.com/docs/git-rebase"
  - "Pro Git 3.6 Rebasing https://git-scm.com/book/en/v2/Git-Branching-Rebasing"
---

## 쓰임새
- 무엇: 커밋 여러 개를 다른 밑동 위에 하나씩 다시 쌓는 명령 — git-rebase 문서 DESCRIPTION "<원문 대목>"
- 잘 맞는 곳: 아직 남과 나누지 않은 내 브랜치의 커밋 정리 — Pro Git 3.6 "<원문 대목>"
- 안 맞는 곳: 이미 push 해서 남이 받은 커밋. 다시 쌓으면 해시가 바뀐다 — Pro Git 3.6 "The Perils of Rebasing"
- 대안: 이력을 그대로 두고 합치기만 하면 merge 가 더 안전하다 · 커밋 하나만 고치면 commit --amend 가 더 쉽다 — 출처
- 판단: 그대로 — 이유가 "PR 올리기 전"이라 아직 나누지 않은 커밋이다

## 큰 그림
- 왜: <원문이 말한 문제 한두 줄> — <출처> "<원문 대목>"
- 부품:
  | 부품 | 맡는 일 | 주고받는 것 |
  |---|---|---|
  | todo 목록 | 다시 쌓을 커밋과 할 일(pick·squash·drop)의 차례 | rebase 가 한 줄씩 읽음 |
  | 밑동(upstream) | 커밋을 다시 쌓을 자리 | rebase 가 여기서 시작 |
  | 커밋 다시 쓰기 | 커밋 하나의 변경을 새 자리에 적용해 새 커밋을 만든다 | 새 해시 |
  | reflog | 브랜치가 가리켰던 옛 자리의 기록 | 되돌릴 때 씀 |
- 이 예시에서는 안 지난다: --onto, autosquash, rerere
- 한 판 따라가기: `lab/01-rebase.sh` → out-01.txt
  1. feature 의 커밋 셋이 todo 목록에 pick 으로 오른다
  2. 밑동 main 의 끝으로 옮겨 간다
  3. 커밋을 하나씩 다시 써서 새 해시 셋이 생긴다
  4. feature 가 새 커밋 셋을 가리키고, 옛 자리는 reflog 에 남는다

## 확대한 곳                    # 부품마다 제목 하나, 큰 그림의 부품 순서로. 근거는 출처 이름과 실험이고 대목은 안 넣는다

### todo 목록
- 갈고리: squash 하면 메시지가 둘 다 남는다 → 편집기에 두 메시지가 이어 붙어 열린다 — git-rebase 문서 INTERACTIVE MODE, `lab/03-squash.sh` → out-03.txt

### 커밋 다시 쓰기
- "rebase 하면 커밋이 옮겨지는 거야?" → 옮겨지지 않고 새로 만들어진다. 옛 커밋은 reflog 가 가리킨 채 남는다 — `lab/02-rewrite.sh` → out-02.txt, 해시 a1b2→c3d4

## 이유                        # why 를 바꿨을 때만. 옛 문장과 날짜

## 밖                          # 주제 밖이라 미룬 것
- git 내부의 객체 저장 방식
```

**완료 기준**: `map.md`에 frontmatter 의 넷과 `## 쓰임새`·`## 큰 그림`이 있고, 따옴표 안의 대목은 모두 실제로 읽은 원문이다.
