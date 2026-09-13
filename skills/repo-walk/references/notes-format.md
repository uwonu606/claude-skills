# 노트 형식

레포 하나가 디렉토리 하나다. `notes.md` 는 레포에 하나이고 걸음이 끝날 때마다 자란다. `walks/` 는 걸음 하나에 파일 하나다.

```
unlazy/
  notes.md
  walks/
    2026-09-13-whole.md
    2026-09-20-thread.md
```

파일 이름의 갈래는 `whole`(전체 짜임)·`thread`(한 가닥)다.

## walks/<날짜>-<갈래>.md

```markdown
---
status: walking               # walking | done(갈래의 끝에 닿음)
branch: whole                 # whole | thread
reason: "스킬 레포가 제품과 문서를 어떻게 나누는지 본다"
head: 1667149
repo: /home/ssafy/workspace/clone/unlazy
---

## 정찰
- 정체: 에이전트가 "다 했다" 대신 돌아가는 검사로 증명하게 하는 스킬. 제품은 `scripts/` 와 `SKILL.md`
- 들어오기 전 `git status --porcelain`: (빈 출력)
- 파일 43개 — mjs 12, md 9, json 3 …
- 최상위: scripts 14, references 9, test 7, …
- 진입점 후보: `SKILL.md`, `package.json`, `scripts/gate-check.mjs`
- 시작점: `scripts/` — 실행되는 것이 전부 여기라서

## 정거장
- [x] `scripts/` — 읽음
  - 본 것: "gate-check 가 진입이고 lib 는 그걸 쪼갠 것. 테스트가 소스보다 많아 보인다"
  - 걸린 점: 진입은 `gate-check.mjs` 가 맞지만 셸을 직접 띄우지 않는다. `gate-check.mjs:684` 가 Node 를 띄워 `check-supervisor.mjs:16` 을 돌리고 거기서 셸이 뜬다
  - 왜: "왜 한 층을 더 두나" → `git log -S'check-supervisor'` → 커밋 `a1b2c3d` "타임아웃 때 자손 프로세스까지 죽이려면 감독이 따로 있어야" — 인용
- [x] `references/` — 돌림: `GATES.md` 를 하나 만들어 `--status` 로 돌려 원장 파싱 출력을 봄
  - 본 것: "사람이 아니라 에이전트가 읽는 문서. gates.md 가 원장 문법"
  - 확인: `- [ ] G1:` 줄 하나에 `CHECK:` 없이 돌리니 "incomplete runnable gate" 로 거부. 문법이 문서와 같다
- [ ] `test/`

다음: `test/` — 테스트 7종의 이름이 기능 목록이라서
```

`본 것` 은 정거장마다 늘 있고 사용자의 낱말 그대로다. `확인` 은 돌렸을 때, `걸린 점` 은 어긋났을 때, `왜` 는 판 것이 있을 때 더한다. 체크박스 뒤의 확인 방법은 `읽음`·`돌림`·`테스트` 셋이다.

`다음:` 은 늘 한 줄이다. 끊긴 걸음은 여기서 잇는다. 끝에 닿았으면 `다음: 끝` 이다.

## notes.md

```markdown
---
repo: /home/ssafy/workspace/clone/unlazy
---

## 정체
- 에이전트가 "다 했다" 대신 돌아가는 검사로 증명하게 하는 스킬. 의존성 0, Node 16+. HEAD `1667149` (2026-09-13)

## 지도                        # 정거장마다 한 줄. 전체 짜임은 디렉토리·역할, 한 가닥은 경로
| 자리 | 무엇 | 확인 |
|---|---|---|
| `scripts/gate-check.mjs` | CLI 진입. 모드를 갈라 `lib/` 로 넘긴다 | 읽음 |
| `scripts/lib/check-supervisor.mjs` | 검사 하나를 감독하는 프로세스. 셸은 여기서 뜬다 | 읽음 |
| `references/gates.md` | 원장 문법. 에이전트가 읽는다 | 돌림 |

## 옮길 것                     # 4단계. 사용자의 낱말로
- "실행을 한 층 더 감싸서 죽이는 책임을 따로 두는 것" — 타임아웃이 있는 실행이면 어디든. 이름: 감독 프로세스(supervisor)
- "문서를 사람용과 에이전트용으로 디렉토리부터 나누는 것" — 이름 없음

## 왜                          # 4단계
- 감독 프로세스 한 층 — 인용 `a1b2c3d`: 타임아웃 때 자손까지 죽이려면 감독이 따로 있어야
- `lib/regex-worker.mjs` 가 워커인 이유 — 추측: 사용자가 쓴 정규식이 멈출 수 있어서. 물어볼 사람: blame 의 @author

## 안 본 것                    # 4단계
- 전문: `gate-check.mjs`, `check-supervisor.mjs`
- 일부: `references/gates.md` 앞 절
- 이름만: `test/` 아래 전부, `lib/process-tree.mjs`
```

`## 정체` 와 `## 지도` 는 걸음 중에 쓴다. `## 옮길 것`·`## 왜`·`## 안 본 것` 은 4단계에 쓰고, 다음 걸음이 끝나면 갈아 쓴다.
