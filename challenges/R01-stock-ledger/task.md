# Reconcile an inventory movement ledger

Implement `reconcile_stock(opening, movements)`. Opening stock maps a SKU string to a nonnegative integer. Each movement is a tuple `(movement_id, sku, signed_delta)` in feed order. Process each ID only on its first occurrence, even if later data for that ID differs. A new SKU starts at zero. Raise `ValueError(sku)` the first time a new movement would leave a negative balance. Return a new mapping containing all opening and encountered SKUs, including zero balances. Leave the inputs unchanged.

Example. `reconcile_stock({"A": 3}, [("m1","A",-2), ("m2","B",5), ("m1","A",-2)])` returns `{"A": 1, "B": 5}`.
