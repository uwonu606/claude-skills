---
name: isolated-tdd
description: 기능 하나를 설계·테스트·구현·품질 agent 로 나눠 test-first 로 만든다. 구현 agent 는 acceptance test 를 보지 않고 실패를 규칙 문장으로 건네받는다.
disable-model-invocation: true
---

# 나눠서 하는 TDD

**design.md** 는 모든 판정의 기준이다. 동작마다 `B<n>`, 그 동작의 규칙을 지켜졌는지 따로 가를 수 있는 문장으로 나눈 **규칙 문장** `B<n>.<m>`, 규칙 문장마다 입력과 기대 출력이 있는 예, interface, 확인된 seam, 사용자가 정한 spec 의 빈 곳이 들어 있다. **seam** 은 바깥에서 동작을 관찰하는 공개 경계이고, 테스트는 확인된 seam 에서만 부른다. agent 가 테스트와 구현 가운데 어느 쪽이 틀렸는지 다툴 때는 design.md 가 가른다. 테스트가 성공 신호의 전부가 되면 테스트에 맞춘 코드가 나오기 때문이다.

agent 넷은 서로의 산출물 가운데 아래 표의 것만 받는다. 구현이 acceptance test 를 보면 테스트에 맞춘 코드가, 테스트 쪽이 구현을 보면 구현에 맞춘 테스트가 나올 수 있어서다.

| agent | 받는 것 | 돌려주는 것 | 열지 않는 것 | 역할 파일 |
|---|---|---|---|---|
| 설계 | spec, 사용자의 답, `gap-question-N`, `dispute-N` | `design.md`, `review.md`, `ruling-N.md` | 구현 코드 | [`references/design-agent.md`](references/design-agent.md) |
| 테스트 | spec, `design.md`, `results-N`, `review.md`, `gaps-N`, `ruling-N` | `<work>/acceptance/`, `coverage.md`, `feedback-N.md`, `dispute-N.md`, `gap-question-N.md` | 구현 코드 | [`references/test-agent.md`](references/test-agent.md) |
| 구현 | spec, `design.md`, `feedback-N`, `ruling-N`, `survivors-N`, `quality-N` | 저장소의 구현과 unit test, `dispute-N.md`, `gaps-N.md`, `quality-reply-N.md` | `<work>/acceptance/` | [`references/impl-agent.md`](references/impl-agent.md) |
| 품질 | `design.md`, 구현 코드, 저장소의 코드 기준, 복잡도 측정값, `quality-reply-N` | `quality-N.md` | 테스트 코드 | [`references/quality-agent.md`](references/quality-agent.md) |

메인은 단계마다 subagent 하나를 새로 띄우고, 그 agent 의 역할 파일과 받는 것의 절대 경로, 열지 않는 경로를 넘긴다. 같은 agent 를 다시 부를 때는 SendMessage 로 이어 간다. md 로 된 산출물은 subagent 가 최종 답으로 돌려주고 메인이 `<work>/` 에 저장한다. subagent 의 보고 파일 쓰기는 harness 가 막는다. 코드와 테스트 파일은 subagent 가 직접 쓴다. 메인은 모든 산출물을 보므로 역할 파일이 agent 에게 맡긴 일(테스트, 구현, design.md 를 쓰고 고치기)을 하지 않는다. subagent 가 도구 권한이나 한도 때문에 자기 일을 끝내지 못하면 막힌 것을 사용자에게 가져간다.

`<스킬>` 은 이 `SKILL.md` 가 있는 디렉토리의 절대 경로다. `<work>` 는 `${ISOLATED_TDD_HOME:-$HOME/isolated-tdd}/<slug>/` 를 펼친 절대 경로이고, `<slug>` 는 기능을 가리키는 짧은 이름이다. acceptance test 는 끝날 때까지 `<work>/acceptance/` 에 두고 메인이 저장소 코드에 대고 돌린다. 저장소 안에 두면 구현 agent 가 unit test 를 돌릴 때 같이 돌아 내용이 보인다.

## 1. 설계

**의도**: design.md 가 spec 의 규칙과 단서를 빠짐없이 규칙 문장과 예로 담고, spec 이 정하지 않은 interface 와 seam 과 spec 의 빈 곳이 사용자에게 확인됐다.

설계 agent 가 design.md 초안과 사용자에게 물을 것(spec 이 정하지 않은 interface, seam 후보, 빈 곳마다 해석과 권하는 쪽)을 돌려준다. 메인은 물을 것을 한 메시지로 사용자에게 묻고, 답을 설계 agent 에게 넘겨 design.md 를 확정한다.

**넘기는 것**: `<work>/design.md`.

**완료 기준**: spec 의 규칙과 단서마다 그것이 들어간 규칙 문장이 있고, spec 에서 끌어낼 수 없는 규칙 문장과 interface 마다 사용자의 어느 답에서 왔는지가 표시돼 있다. 규칙 문장마다 예가 있고, "확인된 seam" 절이 사용자의 답과 맞는다. 사용자의 답이 오기 전에는 2단계를 시작하지 않는다.

## 2. acceptance test

**의도**: 규칙 문장마다 그것을 확인하는 acceptance test 가 있고, 기대값은 모두 design.md 에서 끌어낸 것이다.

테스트 agent 가 테스트와 `coverage.md` 를 쓰고, 설계 agent 가 `review.md` 로 판정한다. `GAPS` 면 테스트 agent 가 고치고 설계 agent 가 다시 판정한다.

**넘기는 것**: `<work>/acceptance/`, `<work>/coverage.md`, `<work>/review.md`.

**완료 기준**: `review.md` 첫 줄이 `PASS` 다. 두 번 고친 뒤에도 `GAPS` 면 남은 지적을 사용자에게 가져간다.

## 3. 구현

**의도**: 구현이 확인된 seam 에서 실패하는 unit test 를 하나씩 보며 자랐다.

**넘기는 것**: 저장소의 구현과 unit test, 구현 agent 가 돌려준 cycle 기록을 메인이 저장한 `<work>/cycles.md`.

**완료 기준**: unit test 가 모두 통과하고 확인된 seam 으로만 부른다. `cycles.md` 에서 구현을 고친 cycle 마다, 그 고침 전에 실패한 테스트 하나와 그 실패 결과가 적혀 있다. 이 순서를 어긴 cycle 은 구현을 되돌려 실패를 다시 만들지 않고, 어긴 대로 적어 사용자에게 가져간다.

## 4. acceptance 실행과 feedback

**의도**: 구현이 acceptance test 를 모두 통과하고, 그 사이의 고침은 테스트 쪽이든 구현 쪽이든 design.md 를 근거로 했다.

메인이 acceptance test 를 저장소 코드에 대고 돌려 `results-N.txt` 로 남긴다. 실패가 있으면 테스트 agent 가 `feedback-N.md` 를 쓰고 구현 agent 가 고친다. 테스트 agent 는 design.md 가 틀렸다고 보면, 구현 agent 는 feedback 의 기대값이 틀렸다고 보면, 고치지 않고 `dispute-N.md` 를 쓴다. 이의는 설계 agent 가 `ruling-N.md` 로 판정하고, 틀렸다고 판정된 쪽이 고친다. 구현 agent 가 고친 뒤에는 테스트 agent 가 고쳐진 규칙 문장마다 feedback 과 다른 입력의 테스트를 하나 더하고, 메인이 다시 돌린다.

**넘기는 것**: `results-N.txt`, `feedback-N.md`, 더한 acceptance test, 있으면 `dispute-N.md` 와 `ruling-N.md`.

**완료 기준**: 마지막 `results-N.txt` 에 실패가 없고, `feedback-N.md` 의 테스트 수정과 `ruling-N.md` 마다 근거가 된 규칙 문장 번호나 spec 의 대목이 있다. feedback 으로 구현이 고쳐진 규칙 문장마다 그 뒤에 더한 테스트가 `coverage.md` 에 있고, 이 단계에서 design.md 가 바뀐 곳마다 `ruling-N.md` 가 있다. feedback 이 세 번 오간 뒤에도 실패가 남으면 남은 실패를 사용자에게 가져간다.

## 5. mutation 검사

**의도**: acceptance test 가 구현의 바깥 동작을 붙잡는다.

메인이 구현에 버그를 하나씩 넣어 acceptance test 가 잡는지 본다. Python 이면 `python3 <스킬>/scripts/mutate.py <구현 파일> <work>/acceptance`, 다른 언어면 그 언어의 mutation testing 도구를 쓴다. 살아남은 버그를 `survivors-N.txt` 로 구현 agent 에게 넘기면 구현 agent 가 `gaps-N.md` 를 쓰고, 테스트 agent 가 테스트를 더한다. 테스트 agent 가 기대값을 design.md 로 끌어내지 못해 `gap-question-N.md` 를 쓰면 설계 agent 가 design.md 를 고치고, 설계 agent 가 사용자에게 물을 것을 돌려주면 메인이 1단계처럼 묻는다. 더한 테스트는 설계 agent 가 다시 판정하고, 메인이 4단계처럼 다시 돌린다.

**넘기는 것**: `survivors-N.txt`, `gaps-N.md`, 더한 acceptance test, 다시 쓴 `review.md`, 다시 돌린 결과.

**완료 기준**: 살아남은 버그마다 `gaps-N.md` 에 동등한 이유가 있거나, 그 동작을 확인하는 테스트가 더해졌거나, 설계 agent 가 정하지 않는다고 적었다. 다시 쓴 `review.md` 첫 줄이 `PASS` 이고, 다시 돌린 acceptance test 가 모두 통과한다. 도구를 찾지 못했으면 이 단계를 건너뛰었다고 보고에 적는다.

## 6. 코드 품질 검토

**의도**: 구현이 저장소의 코드 기준을 따르고, 그렇게 고치는 동안 바깥 동작은 바뀌지 않았다.

품질 agent 가 `quality-N.md` 를 쓴다. 그 언어의 복잡도 측정 도구가 있으면 함수마다 잰 값을 같이 넘긴다. 구현 agent 가 고치고 `quality-reply-N.md` 를 쓰면, 메인이 4단계처럼 acceptance test 를 다시 돌리고 품질 agent 가 다시 본다. 다시 본 판정은 다음 번호의 `quality-N.md` 로 저장하고, `GAPS` 면 한 번 더 되풀이한다.

**넘기는 것**: `quality-N.md`, `quality-reply-N.md`, 다시 돌린 결과.

**완료 기준**: 마지막 `quality-N.md` 첫 줄이 `PASS` 이거나 남은 지적마다 구현 agent 의 이의가 있고, 고친 구현에서 unit test 와 acceptance test 가 모두 통과한다. 두 번 고친 뒤에도 이의 없이 남은 지적은 사용자에게 가져간다.

## 7. 마무리

**의도**: 사용자가 무엇이 확인됐고 무엇이 남았는지 알고, acceptance test 가 저장소에 남는다.

`<work>/acceptance/` 를 저장소의 테스트 자리로 옮기고 저장소의 테스트 실행 방법으로 한 번 돌린다. 사용자에게 단계마다 완료 기준의 판정, 사용자가 정한 것, 남은 버그와 그 이유, 품질 지적의 처리, 가져간 것을 보고한다.

**넘기는 것**: 저장소에 옮긴 acceptance test, 보고.

**완료 기준**: 저장소에서 돌린 테스트가 모두 통과하고, 보고에 1–6단계의 판정이 하나씩 있다.
