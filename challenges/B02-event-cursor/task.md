# Fix cursor pagination across tied timestamps

Repair `event_page(events, after, limit)`. Each event is a unique tuple `(timestamp, event_id)`, with an integer timestamp and a string ID. Sort these tuples in ascending order and return up to `limit` events strictly after the entire cursor pair. `after=None` means start from the beginning. A cursor need not exist in the input. Return `(page, next_cursor)`, with a list for page. Set next_cursor to the last item in the page only if another item remains. The limit is at least one.

Example. `event_page([(1,"a"), (1,"b"), (2,"c")], (1,"a"), 1)` returns `([(1,"b")], (1,"b"))`.

## Starter code

```python
def event_page(events, after, limit):
    ordered = sorted(events)
    if after is not None:
        ordered = [event for event in ordered if event[0] > after[0]]
    page = ordered[:limit]
    return page, page[-1] if len(ordered) > limit else None
```
