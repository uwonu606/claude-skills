# 로그 점검

이미 안착한 커밋에서 규약 표류를 찾는다. 커밋을 새로 만드는 절차는 `SKILL.md`, 메시지 규칙 원문은 [`messages.md`](messages.md) 다.

규약을 어긴 커밋을 커밋 시점에 잡아 주는 층은 없다. 대신 언제든 로그를 통째로 훑어 표류를 찾는다.

```bash
T='feat|fix|docs|chore|refactor|style|test|build|ci|perf|revert'
git log --no-merges --format='%s' | grep -vE '^(Revert|Reapply) "' | grep -vE '^[^ :()]+: [^ ].*[^.。．｡…]$'
git log --no-merges --format='%s' | grep -E "^($T)(\([^)]*\))?: "
```

첫 줄은 `<scope>: <설명>` 형태를 벗어난 제목과 마침표로 끝나는 제목을 찾는다. `Revert`·`Reapply` 를 먼저 걷는 것은 git 이 만든 메시지가 규약 대상이 아니어서다 — [`SKILL.md`](../SKILL.md) 가 손대지 않기로 한 커밋이 표류로 잡히면 안 된다. scope 의 문자집합은 제한하지 않는다 — 문서 저장소의 한글 개념 scope([`messages.md`](messages.md))도 규약 안이다. 둘째 줄은 type 접두어를 찾는데, 넓게 잡으므로 그 프로젝트의 실제 영역 이름(`test/`·`build/` 를 가진 저장소의 `test:`·`build:`, Linux 의 `perf:`)은 눈으로 걸러 낸다 — 게이트가 아니라 보고서다.

**잡지 못하는 것**: 제목 폭, `~다` 종결, 본문 유무와 내용, 분할이 옳은지. 그것들은 커밋을 만들 때 [`messages.md`](messages.md) 가 맡는다.

점검에서 걸린 커밋을 실제로 고치는 것은 재작성이다 — [`rewriting.md`](rewriting.md) 로 간다.
