def latest_parcel_state(events):
    seen = set()
    latest = {}
    for event_id, parcel, timestamp, state in events:
        if event_id in seen:
            continue
        seen.add(event_id)
        rank = timestamp, event_id
        if parcel not in latest or rank > latest[parcel][0]:
            latest[parcel] = (rank, state)
    return {parcel: event[1] for parcel, event in latest.items()}
