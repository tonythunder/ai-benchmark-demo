from solution import event_page


def test_equal_timestamp_uses_id_tie_breaker():
    assert event_page([(1, "a"), (1, "b"), (2, "c")], (1, "a"), 1) == ([(1, "b")], (1, "b"))


def test_pages_walk_every_event_once():
    events = [(9, "d"), (7, "b"), (7, "a"), (7, "c")]
    page, cursor = event_page(events, None, 2)
    assert (page, cursor) == ([(7, "a"), (7, "b")], (7, "b"))
    assert event_page(events, cursor, 2) == ([(7, "c"), (9, "d")], None)


def test_absent_cursor_inside_timestamp_bucket():
    assert event_page([(1, "a"), (1, "z")], (1, "h"), 2) == ([(1, "z")], None)


def test_empty_page_has_no_cursor():
    assert event_page([(1, "a")], (1, "a"), 1) == ([], None)
