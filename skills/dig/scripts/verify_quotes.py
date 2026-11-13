#!/usr/bin/env python3
"""카드의 인용이 받아 둔 원문에 글자 그대로 있는지 대조한다.

  verify_quotes.py <card.md> <raw-dir>
  verify_quotes.py - <raw-dir> < card.md     카드를 표준 입력으로 받는다

인용은 큰따옴표로 감싸고 바로 뒤에 `(옮김`, `[출처]`, ` / "` 가 오는 구절이다.
원문은 <raw-dir> 아래 모든 파일(HTML·텍스트·JSON·VTT 자막)이다. 태그, 자막의 시간 표시,
줄바꿈, 따옴표 모양, 대소문자는 무시한다. 인용 안의 `...`·`…` 는 생략으로 보고 앞뒤 조각을 따로 찾는다.
JSON 원문의 `\\"`·`\\n`·`\\uXXXX` 는 풀어서 읽는다.
인용 안의 큰따옴표는 인용의 글자로 본다. `"A" ... "B"` 처럼 이어 붙인 인용은 한 인용으로 본다.
인용 앞 설명에 큰따옴표 쌍이 있으면 그 쌍을 건너뛴 자리에서 다시 찾는다.
`[출처]` 가 있는데 잡힌 인용이 없는 줄은 `unchecked:` 로 알린다.
stdout 에 못 찾은 인용(`miss:`)과 대조 못 한 줄(`unchecked:`)을 한 줄씩, 마지막 줄에 `ok <n> miss <n> unchecked <n>`.
종료 0 전부 찾음 / 1 miss 나 unchecked 있음 / 5 인자 오류
"""
import html
import re
import sys
from pathlib import Path

CLOSING_QUOTE = re.compile(r'"(?=\s*(?:\(옮김|\[출처\]|/\s*"))')
OMISSION = re.compile(r"\s*(?:\.\.\.|…)\s*")
JOINED_QUOTES = re.compile(r'"\s*(?:\.\.\.|…)\s*"')
JSON_ESCAPE = re.compile(r'\\(u[0-9a-fA-F]{4}|["/ntr])')
JSON_WHITESPACE = {"n": "\n", "t": "\t", "r": "\r"}
MIN_PART = 8


def unescape_json(text: str) -> str:
    def decoded(escape: re.Match) -> str:
        token = escape.group(1)
        if token.startswith("u"):
            return chr(int(token[1:], 16))
        return JSON_WHITESPACE.get(token, token)

    return JSON_ESCAPE.sub(decoded, text)


def normalize(text: str) -> str:
    text = html.unescape(text)
    for curly, plain in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), (" ", " ")):
        text = text.replace(curly, plain)
    return re.sub(r"\s+", " ", text).strip().lower()


def strip_markup(text: str) -> str:
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", text)


def strip_subtitle_timing(text: str) -> str:
    text = re.sub(r"^(WEBVTT|Kind:|Language:|NOTE).*$", "", text, flags=re.M)
    text = re.sub(r"^[\d:.]+\s*-->\s*[\d:.]+.*$", "", text, flags=re.M)
    text = re.sub(r"\[\d{1,2}:\d{2}(?::\d{2})?\]", " ", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    deduped = [line for i, line in enumerate(lines) if i == 0 or line != lines[i - 1]]
    return " ".join(deduped)


def load_corpus(raw_dir: Path) -> str:
    texts = []
    for path in sorted(raw_dir.rglob("*")):
        if path.is_file():
            text = strip_subtitle_timing(strip_markup(unescape_json(path.read_text(errors="ignore"))))
            texts.append(normalize(text))
    return "\n".join(texts)


def quote_parts(quote: str) -> list[str]:
    return [normalize(unescape_json(p)) for p in OMISSION.split(quote) if len(p.strip()) >= MIN_PART]


def spans_per_closing_quote(line: str) -> list[list[str]]:
    line = JOINED_QUOTES.sub(" ... ", line)
    groups = []
    search_from = 0
    for closing in CLOSING_QUOTE.finditer(line):
        quote_marks = [i for i in range(search_from, closing.start()) if line[i] == '"']
        openings = [
            position
            for pairs_skipped, position in enumerate(quote_marks[::2])
            if pairs_skipped == 0 or line[position - 1].isspace()
        ]
        spans = [line[opening + 1 : closing.start()] for opening in openings]
        longest_first = [span for span in spans if len(span) >= MIN_PART]
        if longest_first:
            groups.append(longest_first)
            search_from = closing.end()
    return groups


def is_in_corpus(span: str, corpus: str) -> bool:
    parts = quote_parts(span)
    return bool(parts) and all(part in corpus for part in parts)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 5
    card_arg, raw_dir = sys.argv[1], Path(sys.argv[2])
    if not raw_dir.is_dir() or (card_arg != "-" and not Path(card_arg).is_file()):
        print(__doc__, file=sys.stderr)
        return 5
    card_text = sys.stdin.read() if card_arg == "-" else Path(card_arg).read_text()
    corpus = load_corpus(raw_dir)
    found = missed = unchecked = 0
    for line in card_text.splitlines():
        groups = spans_per_closing_quote(line)
        if not groups and "[출처](" in line:
            unchecked += 1
            print(f"unchecked: {line.strip()}")
        for longest_first in groups:
            if any(is_in_corpus(span, corpus) for span in longest_first):
                found += 1
            else:
                missed += 1
                print(f"miss: {longest_first[-1]}")
    print(f"ok {found} miss {missed} unchecked {unchecked}")
    return 1 if missed or unchecked else 0


if __name__ == "__main__":
    sys.exit(main())
