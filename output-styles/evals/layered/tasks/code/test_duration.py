from duration import parse_duration, format_duration

def test_single():
    assert parse_duration("90s") == 90

def test_roundtrip():
    assert format_duration(5400) == "1h30m"
