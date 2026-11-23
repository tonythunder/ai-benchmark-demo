# Find the cheapest route with a coupon

Implement `cheapest_route(edges, start, end)`. The input contains directed edges `(origin, destination, cost)` with string node IDs and nonnegative integer costs. There is one optional coupon that makes a single traversed edge free. Return the minimum numeric cost from start to end after applying the coupon optimally, or `None` if there is no route. If start equals end, return `0`. Cycles, parallel edges and zero-cost edges are allowed. Aim for a heap-based algorithm suitable for thousands of edges.

Example. `cheapest_route([("a","b",7), ("b","z",2), ("a","c",4), ("c","z",4)], "a", "z")` returns `2`.
