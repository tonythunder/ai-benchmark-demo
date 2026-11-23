# Fix office-day revenue rollover

Repair `office_days(entries, offset_minutes)`. Each entry is a tuple `(utc_timestamp, cents)`, where the timestamp is formatted as `YYYY-MM-DDTHH:MM:SSZ` and cents is a signed integer. Convert each timestamp to the fixed local offset in minutes, then accumulate cents by local date. Return a dictionary with date keys formatted as `YYYY-MM-DD`. Keep a date whose net sum is zero. Inputs are valid and the offset can be positive, zero or negative.

Example. `office_days([("2026-01-01T23:45:00Z", 120)], 30)` returns `{"2026-01-02": 120}`.

## Starter code

```python
def office_days(entries, offset_minutes):
    totals = {}
    for timestamp, amount in entries:
        day = timestamp[:10]
        totals[day] = totals.get(day, 0) + amount
    return totals
```
