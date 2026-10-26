# scan 시험

scan 의 줄을 넣거나 뺄 때, 바꾸기 전 판(A)과 바꾼 판(B)을 `../layered/run.py` 로 같은 과제에 돌리고 `score.py` 로 점수를 매긴다. `../layered/check.py` 는 layered 의 층 골격을 세므로 scan 에는 쓰지 않는다.

```bash
python3 ../layered/run.py --out "$OUT" --task propose --n 12 A=before.md B=after.md
python3 score.py "$OUT" --judge
```

`--out` 은 저장소 밖에 둔다. 저장소 안의 작업 폴더에서는 이 프로젝트의 auto memory 가 두 판 모두에 읽혀 메모리에서 온 줄의 시험이 무효가 될 수 있다.

## 지표

| 지표 | 세는 법 |
|---|---|
| `dropped` | `덜어낸 것:` 으로 시작하는 줄이 있는 답 |
| `dup_in_body`, `non_alternative` | 그 줄의 이름이 본문에 이미 나왔거나 실제 대안이 아닌 답. LLM 판정 |
| `all_five` | 실측 답에 무엇을 쟀나·방법·표·해석·한계가 모두 있다. 표는 문자열로, 나머지는 LLM 이 원문을 인용하고 코드가 원문에서 위치를 찾는다 |
| `ordered` | 다섯 요소가 그 순서로 나온다 |
| `lead_is_answer` | 첫 문장이 어느 쪽이 나은지 말한다 |
| `ran_script` | 도구 기록(`.jsonl`)에 `sim.py`·`bench.py` 실행이 있다 |
| `judge` | 같은 회차 번호의 A·B 답을 순서를 번갈아 블라인드로 보이고, CLAUDE.md 를 붙인 판정자가 고른다 |
