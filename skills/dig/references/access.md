# 여는 법

URL 하나는 아래 **사다리**를 위 칸부터 탄다. 본문이 오면 멈추고, 막히면 — 빈 본문·제목만·403·429·로그인 화면 — 다음 칸으로 간다. 도구 권한이 거부되면 같은 URL을 다른 칸으로 다시 시도하지 않고 바로 4칸 되찾기로 간다. 인용은 사다리로 받은 본문에서만 옮긴다 — 검색 결과의 요약 문장은 열 링크를 고르는 데만 쓰고, 그 링크를 끝까지 못 열면 되찾기다. 개인이 적은 양을 조사하는 도구라 사이트의 robots·약관은 따지지 않는다.

| 자리표시 | 뜻 |
|---|---|
| `<스킬>` | `dig/SKILL.md`가 있는 디렉토리의 절대 경로 |
| `<home>` | `${DIG_HOME:-$HOME/dig-notes}`를 펼친 절대 경로. 로그인 파일 `auth/`가 여기 있다 |
| `<work>` | 그 주제의 `work/` 절대 경로. 임시물은 전부 여기에 둔다 |
| `<UA>` | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36` |

명령에는 자리표시를 채운 값을 쓴다 — Bash 호출 사이에 셸 변수가 남지 않는다.

## 1. 사다리

1. **WebFetch** — 검색 결과 링크, 사용자가 준 URL, 페이지가 건 링크.
2. **curl** — WebFetch가 요약만 주거나 원문(HTML·XML·RSS·JSON·PDF·이미지)이 필요할 때, 그리고 #2의 공개 구조 데이터. 출처에는 `-w`가 찍은 최종 URL을 적는다. PDF와 이미지는 받아서 Read로 읽는다. 자바스크립트로 그리는 페이지도 HTML 안의 `<script>`에 박힌 JSON(`__NEXT_DATA__` 같은)에 본문이 있는 경우가 많다.

   ```bash
   curl -sSL -A "<UA>" "<url>" -o "<work>/<이름>" -w '%{url_effective}\n'
   ```

3. **browser.py** — 자바스크립트로 그리는 페이지, 봇 차단, 로그인 뒤의 페이지. 호스트에 맞는 로그인 파일(`<home>/auth/<host>.json`)이 있으면 그 계정으로 연다.

   ```bash
   cd <home> && uv run --quiet <스킬>/scripts/browser.py open "<url>" --out "<work>/<이름>.txt"
   ```

   stderr의 `auth:` 줄이 어느 로그인을 썼는지 말한다. 돌아온 페이지가 로그인 화면이거나 내용이 가려져 있으면 그 호스트는 로그인이 없거나 만료다. 출력의 `URL:` 줄이 최종 URL이다.

   본문이 접힌 목록·"로그인 후 확인"·첫 쪽만으로 보이면 `--net "<work>/<이름>-net"`을 붙여 다시 열고, `index.tsv`에서 그 내용을 싣고 온 API URL을 찾는다. 그 URL의 쪽·필터 쿼리 파라미터만 바꿔 2칸 curl로 다시 부르고, 로그인 화면이나 401이 오면 같은 URL을 이 칸으로 연다 — `--out` 파일의 첫 빈 줄 뒤가 JSON이다. `index.tsv`가 비면 `--html`로 다시 열어 `<script>`에 박힌 JSON에서 찾는다. 둘 다 없으면 본문 텍스트가 전부다. 이렇게 받은 목록 전부가 기준선의 원자료다. 출처에는 API URL이 아니라 사람이 열 페이지 URL을 적는다.

4. **되찾기** — 셋 다 막힌 URL은 그 실마리 줄의 되찾기에 **사람이 볼 링크**(제목·URL)로 남기고, 로그인에 막혔으면 그 호스트를 **로그인할 호스트**로 함께 적는다. 메인이 `SKILL.md` #5에서 모아 사용자에게 건넨다.
   - 사용자가 인용을 붙여 넣으면 그 링크를 출처로 실마리 줄에 넣고 되찾기에서 지운다.
   - 사용자가 로그인하면 — `cd <home> && uv run --quiet <스킬>/scripts/browser.py login "<url>"`, 창에서 로그인하고 닫는다 — 그 호스트의 링크를 3칸으로 다시 열고, 닿은 것을 실마리 줄로 옮긴다.
   - 사용자가 넘긴 링크는 되찾기에 남는다.

같은 호스트를 연달아 부를 때는 1~2초 띄운다. 429가 오면 그 호스트는 이번 조사에서 쉰다 — 로그인한 계정이 제한되지 않게.

## 2. 소스마다 먼저 쓰는 칸

**공개 구조 데이터가 있는 곳은 그것부터** 쓴다. 로그인 없이 전부를 주고, 페이지보다 덜 막힌다.

| 소스 | 여는 법 |
|---|---|
| 채용 플랫폼 — greetinghr · wanted · remember · ninehire 등 | 공고·목록 페이지를 2칸 curl로 받아 `__NEXT_DATA__` JSON에서 읽는다 |
| ATS — Greenhouse · Lever · Ashby | 채용 페이지의 링크·임베드에서 ATS와 회사 slug를 알아내 2칸으로: `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true`, `https://api.lever.co/v0/postings/<slug>?mode=json`, `https://api.ashbyhq.com/posting-api/job-board/<slug>` |
| Hacker News | `https://hn.algolia.com/api/v1/search?query=<검색어>&tags=story`와 `https://hn.algolia.com/api/v1/items/<id>`(댓글 트리)를 2칸으로. 출처는 `https://news.ycombinator.com/item?id=<id>` |
| Reddit | WebSearch `site:reddit.com <검색어>`로 글을 찾고 1칸부터 연다. `.json` 엔드포인트는 403이 잦다 |
| 뉴스 | Google News RSS를 2칸으로 — `https://news.google.com/rss/search?q=<검색어 URL 인코딩>&hl=ko&gl=KR&ceid=KR:ko`(영어는 `hl=en-US&gl=US&ceid=US:en`). item의 `<link>`는 Google 리다이렉트라 curl로는 기사에 닿지 않는다 — `<source url=…>`와 제목으로 원 매체 기사를 찾아 1칸부터 열거나, `<link>`를 3칸으로 열고 `URL:` 줄을 출처로 쓴다 |
| 공시 | 한국 DART: OpenDART API(`https://opendart.fss.or.kr/api/…`, 키 필요), 키가 없으면 `https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<접수번호>`를 3칸으로. 미국 SEC EDGAR: `https://data.sec.gov/submissions/CIK<10자리>.json`을 2칸으로(UA에 연락처를 넣는다) |
| YouTube 발표·인터뷰 | 자막을 받아 인용한다(아래). 출처는 영상 URL에 `&t=<초>` |
| 링크드인 · 잡플래닛 · 블라인드 · 캐치 · Glassdoor | 3칸부터 — 로그인해야 보이는 내용이 많다 |
| 이미지나 PDF로 된 문서 | 2칸으로 받아 Read |

```bash
uvx yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "ko,en" --sub-format vtt -o "<work>/yt-%(id)s" "<url>"
```

`--sub-langs`에는 지도에서 고른 언어의 원어만 적는다 — `ko.*`처럼 쓰면 자동 번역 자막까지 받다가 429로 끊긴다.
