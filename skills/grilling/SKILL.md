---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.

## 추천의 근거 (fork 추가)

각 질문의 추천에는 근거 등급을 붙인다 — ① 실행 결과 ② 출처 ③ 감.

등급 ①로 확인 가능한 판단이 걸린 질문이면, 추천을 제시하기 전에 측정을 서브에이전트에 위임한다:

- 위임 대상은 측정 코드가 필요한 것만이다. 한 줄 조회(grep, 파일 존재, 설정값)는 직접 한다 — 위임 왕복이 조회보다 비싸다.
- 위임 프롬프트에는 질문·후보·의심되는 경계를 담는다. 전역 CLAUDE.md 의 측정 배선이 없는 환경에 이식했다면, 해당 측정 방법론 스킬(benchmark 등)을 열라는 한 줄을 프롬프트에 추가한다.
- 보고는 조건부 결론 + 측정 표 + 환경으로 받고, 원본 코드·출력은 서브에이전트가 scratchpad 에 남기게 한다.

측정 잔해를 인터뷰 컨텍스트에 쌓지 않기 위한 구조다 — 근거는 [`README.md`](README.md).

## 마무리 출구 (fork 추가 — 구 grill-me 흡수)

합의에 도달했고 산출물이 구현으로 이어질 설계일 때만:

1. 합의된 설계를 design-agreement 파일로 쓰겠다고 제안한다. 파일 위치는 그 시점에 사용자와 확정한다.
2. 파일이 쓰였으면 `/fableplan <그 파일 경로>` 실행을 제안한다. fableplan 이 없는 환경이면 그 사실을 밝히고 이 제안은 생략한다.

구현으로 이어지지 않는 그릴링(취향 판단, 계획 스트레스 테스트)에서는 이 출구를 꺼내지 않는다.

## 유형 커버리지 (fork 추가)

인터뷰를 닫기 전에 아래 네 유형을 최소 한 번씩 던졌는지 점검하고, 빠진 것이 있으면 닫기 전에 던진다:

- 목적·성공 기준 — 무엇이 관찰되면 성공인가
- 근거 요구 — 그 전제·숫자의 근거는 무엇인가 (추정인가, 실측인가)
- 트레이드오프 — 이 선택으로 무엇을 포기하는가
- 경계·반례 — 어떤 조건이면 이 계획이 깨지는가
