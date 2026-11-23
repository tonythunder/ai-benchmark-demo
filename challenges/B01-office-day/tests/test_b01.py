from solution import office_days


def test_crosses_utc_midnight_with_fractional_hour_offset():
    assert office_days([("2026-01-01T23:45:00Z", 120)], 30) == {"2026-01-02": 120}


def test_crosses_year_backward():
    assert office_days([("2026-01-01T00:10:00Z", 10)], -30) == {"2025-12-31": 10}


def test_groups_at_local_midnight_and_keeps_zero_total():
    rows = [("2026-01-01T23:30:00Z", 120), ("2026-01-02T03:00:00Z", -120)]
    assert office_days(rows, 30) == {"2026-01-02": 0}


def test_empty_entries():
    assert office_days([], 0) == {}
