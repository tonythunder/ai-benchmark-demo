# Fix cent rounding in discount allocation

Repair `discount_shares(line_totals, discount)`. Each line total is a nonnegative integer in cents. The discount is an integer between zero and the sum of line totals. Allocate the discount proportionally using exact integer arithmetic. Take the floor of each line's ideal share and distribute leftover cents in descending order of fractional remainder. Ties go to the earlier input line. Return allocations in input order. If the total is zero, return all zero shares.

Example. `discount_shares([30, 30, 40], 2)` returns `[1, 0, 1]`.

## Starter code

```python
def discount_shares(line_totals, discount):
    total = sum(line_totals)
    if total == 0:
        return [0] * len(line_totals)
    return [round(amount * discount / total) for amount in line_totals]
```
