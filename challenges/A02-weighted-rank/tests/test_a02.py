from solution import weighted_rank


def test_sorts_values_and_uses_one_based_rank():
    assert weighted_rank([(8, 2), (3, 1), (5, 2)], 3) == 5


def test_last_position_of_one_bucket_belongs_to_that_bucket():
    assert weighted_rank([(7, 2), (-3, 4), (0, 0)], 4) == -3


def test_returns_none_for_invalid_ranks():
    assert weighted_rank([(1, 1)], 0) is None
    assert weighted_rank([(1, 1)], 2) is None
    assert weighted_rank([], 1) is None


def test_handles_large_counts_and_duplicate_values():
    assert weighted_rank([(2, 10**12), (3, 2), (2, 2)], 10**12 + 1) == 2
