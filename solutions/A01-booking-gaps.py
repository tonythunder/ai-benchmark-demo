def free_windows(bookings, start, end):
    available = []
    cursor = start
    for a, b in sorted(bookings):
        left, right = max(start, a), min(end, b)
        if left >= right:
            continue
        if left > cursor:
            available.append((cursor, left))
        cursor = max(cursor, right)
    if cursor < end:
        available.append((cursor, end))
    return available
