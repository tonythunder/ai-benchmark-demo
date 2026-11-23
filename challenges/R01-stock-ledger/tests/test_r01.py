import pytest

from solution import reconcile_stock


def test_deduplicates_by_global_id_and_leaves_opening_unchanged():
    opening = {"A": 3}
    moves = [("m1", "A", -2), ("m2", "B", 5), ("m1", "B", 20)]
    assert reconcile_stock(opening, moves) == {"A": 1, "B": 5}
    assert opening == {"A": 3}


def test_keeps_zero_balances_and_new_skus():
    assert reconcile_stock({"A": 4}, [("a", "A", -4), ("b", "B", 0)]) == {"A": 0, "B": 0}


def test_rejects_first_negative_balance_in_feed_order():
    with pytest.raises(ValueError, match="^X$"):
        reconcile_stock({}, [("m", "X", -1), ("n", "X", 10)])


def test_empty_feed_returns_a_separate_mapping():
    opening = {"A": 1}
    result = reconcile_stock(opening, [])
    assert result == opening and result is not opening
