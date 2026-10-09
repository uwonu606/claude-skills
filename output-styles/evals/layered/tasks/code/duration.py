import re

UNITS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    text = text.strip().lower()
    if not text:
        raise ValueError("empty duration")
    match = re.fullmatch(r"(\d+)([hms])", text)
    if match is None:
        raise ValueError(f"bad duration: {text!r}")
    amount, unit = match.groups()
    return int(amount) * UNITS[unit]


def format_duration(seconds):
    parts = []
    for unit, size in UNITS.items():
        amount, seconds = divmod(seconds, size)
        if amount:
            parts.append(f"{amount}{unit}")
    return "".join(parts) or "0s"
