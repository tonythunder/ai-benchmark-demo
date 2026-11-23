# Programming Benchmark · Mock run

> Bundled synthetic submissions · no model was called.

**7 / 12 passed · 58.3%**

Submission source: offline-fixture

Each challenge is worth one point and passes only if all its tests pass. Every challenge is included in the denominator.

## Score breakdown

| Group | Passed | Total | Pass rate |
| --- | ---: | ---: | ---: |
| Category · Algorithms | 2 | 4 | 50.0% |
| Category · Bug fixes | 2 | 4 | 50.0% |
| Category · Practical tasks | 3 | 4 | 75.0% |
| Difficulty · Easy | 3 | 5 | 60.0% |
| Difficulty · Medium | 3 | 5 | 60.0% |
| Difficulty · Hard | 1 | 2 | 50.0% |

## Challenge results

| ID | Challenge | Difficulty | Verdict | First failure |
| --- | --- | --- | --- | --- |
| A01-booking-gaps | Find free booking windows | easy | pass | — |
| A02-weighted-rank | Find a weighted reading by rank | easy | fail | FAILED tests/test_a02.py::test_sorts_values_and_uses_one_based_rank — assert 8 == 5 |
| A03-build-waves | Schedule dependency waves | medium | pass | — |
| A04-coupon-route | Find the cheapest route with a coupon | hard | fail | FAILED tests/test_a04.py::test_coupon_can_be_used_before_the_last_edge — AssertionError: assert 4 == 2 |
| B01-office-day | Fix office-day revenue rollover | easy | pass | — |
| B02-event-cursor | Fix cursor pagination across tied timestamps | medium | fail | FAILED tests/test_b02.py::test_equal_timestamp_uses_id_tie_breaker — AssertionError: assert ([(2, &#x27;c&#x27;)], None) == ([(1, &#x27;b&#x27;)], (1, &#x27;b&#x27;)) |
| B03-discount-share | Fix cent rounding in discount allocation | medium | pass | — |
| B04-slot-release | Fix slot release at the window boundary | easy | fail | FAILED tests/test_b04.py::test_releases_at_exact_expiry — assert [True, True, False, False] == [True, True, True, False] |
| R01-stock-ledger | Reconcile an inventory movement ledger | medium | pass | — |
| R02-invoice-csv | Summarize posted invoice totals from CSV | medium | fail | FAILED tests/test_r02.py::test_reads_quoted_commas_as_part_of_invoice_id — ValueError: invalid literal for int() with base 10: &#x27; usd &#x27; |
| R03-parcel-events | Reduce parcel events to latest state | hard | pass | — |
| R04-release-manifest | Diff release manifests | easy | pass | — |

See report.json for status counts, category labels and judge timings.
