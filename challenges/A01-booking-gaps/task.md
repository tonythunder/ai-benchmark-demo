# Find free booking windows

Implement `free_windows(bookings, start, end)`. Each booking is a pair `(a, b)` of integer minutes with `a <= b`. Consider the half-open day `[start, end)`, where `start <= end`. Return the maximal available half-open intervals as a list of `(a, b)` tuples in ascending order. Clip bookings to the day and ignore intervals of zero length. The input may be unsorted and may contain overlapping or touching intervals. Do not mutate it.

Example. `free_windows([(7, 10), (2, 4), (4, 6)], 0, 9)` returns `[(0, 2), (6, 7)]`.
