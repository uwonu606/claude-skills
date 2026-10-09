from pricing import order_total


def test_no_discount():
    assert order_total([1000, 2500]) == 3500


def test_small_items():
    assert order_total([0.1, 0.2]) == 0.3
