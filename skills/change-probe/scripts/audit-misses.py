#!/usr/bin/env python3
"""세션 기록 감사 — 되돌리기 비싼 설계 판단을 실측 없이 미루기 문구로 닫은 턴을 골라낸다.

판정기가 아니라 트리아지 목록이다 (2026-09-02 실측: 알려진 양성 재현율 2/3, 알려진 음성 오검출 0,
실세션 31일치 20건 중 진짜 후보 3~4건 — 정밀도 ~20%). 목록에서 사람이 입장 여부를 가르고,
입장이면 change-probe 를 소급 적용해 단정의 참·거짓을 측정으로 판정한다. 근거는 README.

판정 = (설계 비교 단서) AND (미루기·단정 문구) AND (그 턴 앞뒤 ±window 메시지에 도구 호출 없음)

    python3 audit-misses.py            # 최근 31일
    python3 audit-misses.py --days 90
"""
import argparse, datetime, glob, json, os, re

ROOT = os.path.expanduser('~/.claude/projects')

DESIGN = re.compile(r'(테이블|컬럼|스키마|API|이벤트 ?로그|서비스|모듈|구조|설계|아키텍처|저장|DB|큐|캐시|파티션|샤드|계약|인터페이스)')
COMPARE = re.compile(r'(vs\.?|대\s|중에|어느 쪽|갈지|할지|골라|둘 중|A안|B안|후보)')
DEFER = re.compile(r'(나중에 .{0,12}(얹|추가|붙|도입|바꾸|전환|옮기)|필요해지면|필요할 때 .{0,6}(추가|도입)|그때 .{0,8}(추가|도입|얹)|오버스펙|과설계|YAGNI|지금 .{0,10}충분|미리 .{0,8}(짊어|지불|만들)|벤치마크.{0,10}(대상이 아니|필요 없)|실행.{0,6}(없이|않고) 답)')


def texts_of(msg):
    c = msg.get('message', {}).get('content')
    out, tools = [], 0
    if isinstance(c, str):
        out.append(c)
    elif isinstance(c, list):
        for b in c:
            if not isinstance(b, dict):
                continue
            if b.get('type') == 'text':
                out.append(b['text'])
            elif b.get('type') == 'tool_use':
                tools += 1
    return '\n'.join(out), tools


def scan(path, window):
    msgs = []
    for line in open(path, errors='replace'):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get('type') not in ('assistant', 'user'):
            continue
        t, tools = texts_of(d)
        msgs.append((d.get('type'), t, tools, d.get('timestamp', '')))
    hits = []
    for i, (typ, t, tools, ts) in enumerate(msgs):
        if typ != 'assistant' or len(t) < 200:
            continue
        if not (DESIGN.search(t) and COMPARE.search(t) and DEFER.search(t)):
            continue
        lo, hi = max(0, i - window), min(len(msgs), i + window + 1)
        if any(m[2] > 0 for m in msgs[lo:hi]):
            continue
        m = DEFER.search(t)
        snippet = t[max(0, m.start() - 60): m.end() + 60].replace('\n', ' ')
        hits.append((ts[:16], snippet))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=31)
    ap.add_argument('--window', type=int, default=6)
    ap.add_argument('--include-scratchpad', action='store_true', help='실험용 세션(scratchpad 경로)도 포함')
    a = ap.parse_args()

    since = datetime.datetime.now() - datetime.timedelta(days=a.days)
    rows = []
    for path in glob.glob(f'{ROOT}/**/*.jsonl', recursive=True):
        if not a.include_scratchpad and 'scratchpad' in path:
            continue
        try:
            if datetime.datetime.fromtimestamp(os.path.getmtime(path)) < since:
                continue
        except OSError:
            continue
        proj = path.split('/projects/')[1].split('/')[0]
        for ts, snip in scan(path, a.window):
            rows.append((ts, proj, os.path.basename(path), snip))

    print(f'후보 {len(rows)}건 (최근 {a.days}일) — 입장 여부를 가르고, 입장이면 change-probe 를 소급 적용한다')
    for ts, proj, fn, snip in sorted(rows):
        print(f'- {ts} [{proj}] {fn[:8]} …{snip}…')


if __name__ == '__main__':
    main()
