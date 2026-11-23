from solution import cheapest_route


def test_saves_coupon_for_the_right_edge():
    edges = [("a", "b", 2), ("b", "z", 12), ("a", "c", 5), ("c", "z", 5)]
    assert cheapest_route(edges, "a", "z") == 2


def test_coupon_can_be_used_before_the_last_edge():
    edges = [("a", "b", 9), ("b", "z", 2), ("a", "c", 4), ("c", "z", 8)]
    assert cheapest_route(edges, "a", "z") == 2


def test_requires_distinct_coupon_states_at_a_node():
    edges = [("a", "b", 6), ("b", "a", 0), ("b", "z", 20), ("a", "b", 3)]
    assert cheapest_route(edges, "a", "z") == 3


def test_zero_cost_unreachable_and_identity():
    assert cheapest_route([("a", "b", 0)], "a", "b") == 0
    assert cheapest_route([("a", "b", 0)], "b", "a") is None
    assert cheapest_route([], "x", "x") == 0
