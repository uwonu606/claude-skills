# 저장 형식

## 레이아웃

```
$YT_GRILL_HOME/            없으면 ~/video-notes/
├── .gitignore             처음 만들 때 스크립트가 놓는다: */transcript.md
└── <slug>/
    ├── transcript.md      원문. 스크립트가 만들고 사람은 손대지 않는다
    └── notes.md           정리. 토의 중 채워진다
```

**slug** 는 제목의 뜻을 옮긴 영문 kebab 이다. 유튜브 ID 는 frontmatter 에 있고, 같은 영상인지는 ID 로 판정한다. 별도 index 는 없다 — `yt_grill.py list` 가 frontmatter 를 훑어 만든다.

**원문은 git 에 올리지 않는다.** 남의 저작물이고, URL 이 살아 있으면 다시 받는다. 정리는 올려도 된다.

## transcript.md

```markdown
---
id: IoI3LQUctkM
url: https://www.youtube.com/watch?v=IoI3LQUctkM
title: "AI 시대, 기업은 어떤 인재를 뽑을까?"
channel: "조코딩 JoCoding"
duration: 181                 # 초
upload_date: 2026-08-21
language: ko
source: auto                  # manual | auto | whisper
saved: 2026-09-06
---
[00:00] 네, 오늘은 AX 인재 전쟁 본선
[00:03] 시간입니다. 제 AI 시대 인재
```

자막 큐 하나가 한 줄이다. 자동자막은 문장 중간에서 끊기고 오인식이 있다 — 그대로 둔다. 원문은 증거이고 다듬은 글은 `notes.md` 몫이다. 1시간을 넘으면 `[h:mm:ss]`.

`source` 가 `whisper` 면 로컬 전사다. 유튜브 자동자막과 오인식 수는 비슷하고 구두점이 있다(실측).

## notes.md

```markdown
---
id: IoI3LQUctkM
url: https://www.youtube.com/watch?v=IoI3LQUctkM
title: "AI 시대, 기업은 어떤 인재를 뽑을까?"
status: discussing            # transcribed | discussing | done
discussed: [2026-09-06]
---

## 요약
- 시험 점수로는 AI 시대 인재를 정의할 수 없다 [00:06]
- ...

## 핵심 주장

### 1. 모호한 문제를 정의하는 것부터가 문제 풀이의 시작이다
- 영상의 말: "문제를 정의한 것부터가 문제 풀이의 시작점이라고 생각하고" [00:29]
- 네 말: (사용자의 답을 그대로)
- 걸린 점: (막힌 곳, 반론, 영상과 다르게 이해한 곳)
- 판정: 도달 (1회)

### 2. ...

## 내 질문
- Q: ... → A: ... [mm:ss]

## open_questions
- 주장 3 — 3회 미도달, 쓴 각도: 자기 예 / 반례 / 원문 대조. 다음엔 다른 영상과 견주는 각도로
- 주장 4, 5 — 사용자가 끊음 (2026-09-06)
```

`네 말` 은 사용자가 쓴 낱말과 문장 길이를 그대로 옮긴다. 군말과 반복만 덜어낸다. **비워 두는 것이 지어내는 것보다 항상 낫다.**

`판정` 의 회수는 그 주장에 질문을 던진 횟수다. 3회 미도달이면 `open_questions` 로 가고, 거기엔 **어느 각도를 이미 썼는지**를 적는다 — 없으면 다음 세션이 같은 질문을 네 번째로 던진다.

재진입으로 `네 말` 이 다시 쌓이면 이전 것을 지우지 않고 아래에 날짜를 붙여 덧붙인다.
