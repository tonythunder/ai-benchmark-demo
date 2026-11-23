from solution import latest_parcel_state


def test_handles_late_arrival_and_timestamp_tie():
    events = [("z", "P", 9, "sent"), ("a", "P", 9, "packed"), ("c", "P", 4, "created")]
    assert latest_parcel_state(events) == {"P": "sent"}


def test_duplicate_id_cannot_create_a_second_parcel():
    events = [("dup", "P", 1, "sent"), ("dup", "Q", 9, "delivered"), ("b", "P", 2, "lost")]
    assert latest_parcel_state(events) == {"P": "lost"}


def test_handles_independent_parcels_and_keeps_input_order():
    events = [("x", "Q", 0, "new"), ("b", "P", 1, "new"), ("y", "P", 2, "sent")]
    assert latest_parcel_state(events) == {"P": "sent", "Q": "new"}
    assert [row[0] for row in events] == ["x", "b", "y"]


def test_empty_feed():
    assert latest_parcel_state([]) == {}
