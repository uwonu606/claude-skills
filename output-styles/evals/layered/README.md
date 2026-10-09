# layered 시험

layered 의 줄을 넣거나 뺄 때, 바꾸기 전 판(`base`)과 바꾼 판(`cand`)에 같은 과제를 주고 답을 견준다.

```bash
python3 run.py --out /tmp/ev/title-is-answer --task explain --n 5 base=before.md cand=after.md
python3 check.py /tmp/ev/title-is-answer --test title-is-answer
```

`run.py` 는 판마다 작업 폴더를 따로 만들고 `claude -p --settings '{"outputStyle": ...}'` 로 돌린다. 사용자 CLAUDE.md 는 평소처럼 함께 읽힌다.

## 과제

| 과제 | 묻는 것 | 보는 것 |
|---|---|---|
| `explain` | 원자료는 `lab/` 파일에만 두고 "덩어리 셋으로 갈렸다는 게 무슨 말이야?" | 흐름의 한 일 → 바란 것 순서, 첫 문단, 내부 이름 |
| `diagnose` | FastAPI 커넥션 풀 타임아웃 원인 | 정리 층 라벨, 흐름 줄 수 |
| `propose` | `pool_size` 를 올리자는 의견에 대한 판단 | 제안 4요소의 자리 |
| `procedure` | 운영 PostgreSQL 14 → 16 업그레이드 | 위험한 명령 앞 경고, 성공 확인 |
| `code` | `parse_duration` 수정 (편집 허용) | 테스트 통과, 답 길이 |
| `explain-holdout` | 캐시 hit rate 실험 기록. "7% 밖에 안 나왔다는 게 무슨 말이야?" | 떼어 둔 과제 |
| `diagnose-holdout` | CI 실패 로그와 코드 | 떼어 둔 과제, 실제 오류 출력 인용 |

## 줄을 남기는 기준

시험은 줄을 고르는 목표가 아니라 회귀를 막는 장치다. 과제가 적고 지표가 꼴만 세서, 점수에 맞춰 다듬으면 과제에 과적합한다.

- 사용자가 실제로 겪은 실패에서 나온 줄은 시험에서 해가 보이지 않으면 남긴다.
- 추정에서 나온 줄은 시험에서 효과가 보일 때만 남긴다.
- `*-holdout` 과제는 통과 규칙(`check.py` 의 `HOLDOUT`)을 돌리기 전에 정하고, 결과를 보고 layered 를 다듬지 않는다. 떼어 둔 과제에 맞춰 고치면 그 과제는 더 이상 떼어 둔 것이 아니다. 새 판을 확인할 때마다 한 번씩만 돌린다.

## 시험

`check.py` 의 `TESTS` 가 바뀐 것 하나마다 과제와 통과 규칙을 정하고, `--integration` 이 과제 다섯 개를, `--holdout` 이 떼어 둔 과제 둘을 한 번에 판정한다. 지표는 문자열로 센 근삿값이라, 판정이 갈리면 답을 직접 읽는다.

- 잡음이 크다. 같은 판의 `explain` 에서 `expect_in_flow` 는 회차마다 0.4~1.0, `lead_cause` 는 0.3~1.0 사이를 오갔다(2026-10-09, 3~10회씩 7번). `explain` 은 판마다 10회 이상 돌리고, 갈리면 여러 회차를 모아 본다.
- `procedure` 의 `unguarded` 는 리허설용 VM 에서 돌리는 명령도 센다. 0 이 아니면 그 명령이 운영 서버 단계인지 읽어서 가린다.
