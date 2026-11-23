# Fix slot release at the window boundary

Repair `allocate_slots(arrivals, window, limit)`. Arrivals are integer timestamps in nondecreasing order. Accept an arrival if fewer than `limit` accepted arrivals remain in its active window. A previously accepted timestamp expires when it is at or before `arrival - window`. A rejected arrival consumes no slot. Return one boolean per arrival. Both window and limit are positive integers.

Example. `allocate_slots([0, 2, 5, 5], 5, 2)` returns `[True, True, True, False]`.

## Starter code

```python
from collections import deque


def allocate_slots(arrivals, window, limit):
    active = deque()
    decisions = []
    for arrival in arrivals:
        while active and active[0] < arrival - window:
            active.popleft()
        accepted = len(active) < limit
        decisions.append(accepted)
        if accepted:
            active.append(arrival)
    return decisions
```
