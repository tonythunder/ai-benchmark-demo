from collections import defaultdict
from heapq import heappop, heappush


def cheapest_route(edges, start, end):
    graph = defaultdict(list)
    for origin, destination, cost in edges:
        graph[origin].append((destination, cost))

    queue = [(0, start, False)]
    best = {(start, False): 0}
    while queue:
        total, node, used_coupon = heappop(queue)
        if total != best[(node, used_coupon)]:
            continue
        if node == end:
            return total
        for neighbor, cost in graph[node]:
            options = [(total + cost, used_coupon)]
            if not used_coupon:
                options.append((total, True))
            for price, spent in options:
                state = (neighbor, spent)
                if price < best.get(state, float("inf")):
                    best[state] = price
                    heappush(queue, (price, neighbor, spent))
    return None
