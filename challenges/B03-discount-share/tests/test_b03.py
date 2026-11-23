from solution import discount_shares


def test_allocates_every_cent_with_stable_tie_breaker():
    assert discount_shares([30, 30, 40], 2) == [1, 0, 1]


def test_ranks_remainder_after_flooring():
    assert discount_shares([7, 4, 1], 7) == [4, 2, 1]


def test_no_floating_point_rounding_on_large_inputs():
    assert discount_shares([10**18 + 1, 10**18], 1) == [1, 0]


def test_handles_no_discount_and_zero_totals():
    assert discount_shares([], 0) == []
    assert discount_shares([0, 10], 0) == [0, 0]
    assert discount_shares([0, 0], 0) == [0, 0]
