# Find a weighted reading by rank

Implement `weighted_rank(readings, rank)` for a list of `(value, count)` integer pairs. Each count is nonnegative and indicates that the value occurs that many times. Return the value at the 1-based rank of the multiset sorted in ascending order. Return `None` if the rank is outside the multiset. Inputs may be unsorted and include duplicates. Handle counts up to 10**12 without materializing repeated readings.

Example. `weighted_rank([(8, 2), (3, 1), (5, 2)], 3)` returns `5`.
