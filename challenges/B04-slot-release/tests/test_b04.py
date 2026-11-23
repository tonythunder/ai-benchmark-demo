from solution import allocate_slots


def test_releases_at_exact_expiry():
    assert allocate_slots([0, 2, 5, 5], 5, 2) == [True, True, True, False]


def test_rejected_arrival_does_not_extend_the_window():
    assert allocate_slots([0, 1, 3, 4, 6], 3, 1) == [True, False, True, False, True]


def test_expires_all_old_slots_before_admitting_a_batch():
    assert allocate_slots([1, 1, 8, 8, 8], 4, 2) == [True, True, True, True, False]


def test_empty_stream():
    assert allocate_slots([], 5, 1) == []
