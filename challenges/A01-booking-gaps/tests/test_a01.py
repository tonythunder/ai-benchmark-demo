from solution import free_windows


def test_clips_sorts_and_merges():
    assert free_windows([(7, 10), (2, 4), (4, 6)], 0, 9) == [(0, 2), (6, 7)]


def test_ignores_empty_and_outside_bookings():
    assert free_windows([(-3, -1), (3, 3), (10, 15)], 0, 10) == [(0, 10)]


def test_handles_empty_day_and_full_coverage():
    assert free_windows([(0, 3)], 2, 2) == []
    assert free_windows([(-1, 4), (3, 12)], 0, 8) == []


def test_does_not_reorder_input():
    bookings = [(6, 8), (1, 3)]
    assert free_windows(bookings, 0, 10) == [(0, 1), (3, 6), (8, 10)]
    assert bookings == [(6, 8), (1, 3)]
