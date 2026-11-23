def event_page(events, after, limit):
    ordered = sorted(events)
    if after is not None:
        ordered = [event for event in ordered if event[0] > after[0]]
    page = ordered[:limit]
    return page, page[-1] if len(ordered) > limit else None
