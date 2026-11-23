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
