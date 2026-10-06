# notes.md 형식

```markdown
---
id: UNzCG3lw6O0
url: https://www.youtube.com/watch?v=UNzCG3lw6O0
title: "Building Great Agent Skills: The Missing Manual"
status: discussing            # transcribed | discussing | confirming | done
discussed: [2026-09-06]
---

## 정리                        # 5단계에 쓴다. 그전에는 이 절이 없다
- 주장 2 는 수긍에서 비판으로 갔다. leading word 는 길이가 아니라 에이전트가 이미 뜻을 가진 말이라야 먹힌다 — scope 가 먹힌 건 개발자들이 이미 쓰는 말이라서
- "다음 단계를 감추면 지금 단계의 legwork 가 는다"의 이유는 영상에 없고, 저자 문서의 premature completion 이 답이다 (writing-for-agents)

## 판정                        # 4단계에 쓴다. 이야기 중 판정이 바뀌면 화살표로
| # | 주장 | 판정 | 이유 |
|---|---|---|---|
| 1 | 두 load 는 어느 쪽도 공짜가 아니다 [05:25] | 수긍 | "내 스킬 목록이 이미 스무 개라 체감한다" |
| 2 | leading word 가 스킬을 예측 가능하게 한다 [09:10] | 수긍 → 비판 | "말이 짧다고 먹히는 게 아니라 이미 쓰는 말이라야" |
| 3 | 다음 단계를 감추면 지금 단계의 legwork 가 는다 [16:17] | 추가 정보 | "왜 그런지 영상이 안 말한다" |

## 핵심
- 좋은 스킬을 가릴 공유 채점 기준이 없다. triggering·structure·steering·pruning 넷으로 본다 [02:04]
- 모델 호출은 에이전트의 context load, 사용자 호출은 사용자의 cognitive load — 어느 쪽도 공짜가 아니다 [05:25]
- ...

## 흐름
### 1. skill hell [00:00-02:04]
- tutorial hell, framework hell 에 이어 skill hell — 좋은 스킬을 가릴 눈이 없다 [00:47]
- 빠진 건 다 같이 쓰는 채점 기준이다 [01:54]

### 2. triggering [02:04-07:32]
- ...

## 이야기
### 1. 다음 단계를 감추면 왜 지금 단계의 legwork 가 느나
- 영상: "increasing legwork on the step that you're on by hiding the future steps" [16:17]
- 왜 여기: 추가 정보 — "왜 그런지 영상이 안 말한다"
- 네 말: (사용자의 답 그대로)
- 되물음: "무엇을 알면 정해지나" → "감추는 게 왜 먹히는지의 기제" (되물음과 답 — 있을 때만)
- 걸린 점: (막힌 곳, 원문과 갈린 곳 — 있을 때만)
- 더 찾은 것: 저자 문서의 premature completion — 보이는 후속 단계가 "끝내자"는 당김을 만들고, 완료 기준의 명확함이 그 저항이다 (writing-for-agents SKILL.md)
- 정정: (영상이 틀린 데와 출처 — 있을 때만)

### 2. leading word 가 스킬을 예측 가능하게 한다
- 영상: "the word scope ... the agent already knows what that means" [09:10]
- 왜 여기: 수긍인데 이유가 영상의 말 그대로 — "짧은 말이 먹힌다"
- 네 말:
- 되물음: "네 스킬에서 먹힌 말과 안 먹힌 말은" → "scope 는 먹혔고 내가 지은 '회차'는 처음엔 안 먹혔다"
- 제안: "이미 쓰는 말이라 먹힌다 — 저자 문서가 pretraining 에 사는 말을 고르라고 한다" → "맞다. 내가 지은 말은 정의를 붙이고서야 먹혔다" (5단계에서 붙인 후보 → 사용자가 고르거나 고쳐 쓴 말)

## open_questions
- 주제 3 — 사용자가 끊음 (2026-09-06)
- 주제 5 — 영상이 X 라고 하는데 출처를 못 찾았다. 의심으로 둔다
```

**주제 번호는 영상 전체로 이어 붙인다** — `open_questions` 가 번호로만 가리키기 때문이다.

`영상`·`왜 여기`·`네 말` 은 주제마다 늘 있고, `되물음`·`걸린 점`·`더 찾은 것`·`정정`·`제안` 은 내용이 생겼을 때 더한다. `제안` 의 화살표 뒤 말만 `## 판정` 이나 `네 말` 로 옮긴다. `## 판정` 의 주장 번호는 `## 핵심` 의 줄 순서다.
