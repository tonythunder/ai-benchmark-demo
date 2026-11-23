from collections import defaultdict
from heapq import heappop, heappush


def cheapest_route(edges, start, end):
    graph = defaultdict(list)
    for origin, destination, cost in edges:
        graph[origin].append((destination, cost))
    queue = [(0, start)]
    visited = set()
    while queue:
        total, node = heappop(queue)
        if node in visited:
            continue
        if node == end:
            return total
        visited.add(node)
        for neighbor, cost in graph[node]:
            if neighbor == end:
                cost = 0
            heappush(queue, (total + cost, neighbor))
    return None
