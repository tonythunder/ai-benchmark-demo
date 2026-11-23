from datetime import datetime, timedelta


def office_days(entries, offset_minutes):
    offset = timedelta(minutes=offset_minutes)
    totals = {}
    for timestamp, amount in entries:
        local = datetime.fromisoformat(timestamp) + offset
        day = local.date().isoformat()
        totals[day] = totals.get(day, 0) + amount
    return totals
