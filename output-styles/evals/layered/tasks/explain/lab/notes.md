# AutoSchemaKG 재현 실험 노트

## 실험 설정
- 스크립트 `01_three_stages.py`. 모델 Llama 3.1 8B (ollama), temperature 0.7, seed 1.
- 원문 하나에 공식 프롬프트 셋을 각각 따로 보냈다. 단계마다 새 대화를 열고, 메시지는 system 한 줄 + user(지시문 + 원문)이다.
  - 질문 1 `entity_relation`: "Given a passage, summarize all the important entities and the relations between them in a concise manner..."
  - 질문 2 `event_entity`: "Please analyze and summarize the participation relations between the events and entities in the given paragraph. Each event is a single independent sentence..."
  - 질문 3 `event_relation`: "Please analyze and summarize the relationships between the events in the paragraph. Each event is a single independent sentence. Identify temporal and causal relationships ... before, after, at the same time, because, and as a result. Each extracted triple should be specific, meaningful, and able to stand alone."
- 노드 합치기: 공식 코드 `json_to_csv.py` 의 `clean_text` + `visited_nodes` 를 옮겼다. 앞뒤 공백만 정리하고 문자열이 같으면 같은 노드다.

- 원문과 세 질문의 원답은 `runs/02-seed1.json` 에 있다.

## 결과
노드 12개, 선 10개. 연결 덩어리 3개:
- 덩어리 1: 민수 / 우산 / 비 / 민수는 우산을 집에 두고 출근했다. / 민수는 퇴근길에 옷이 다 젖었다. / 민수는 우산을 샀다. / 점심 무렵 비가 쏟어졌다. / 민수는 편의점에서 우산을 샀다.
- 덩어리 2: 아침에 민수는 우산을 집에 두고 출근했다. / 점심 무렵 비가 쏟아졌다.
- 덩어리 3: 비 오는 날에는 우산을 챙겨야 한다. / 민수는 우산은 집에 두고 출근했다.

