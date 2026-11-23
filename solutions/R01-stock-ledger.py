def reconcile_stock(opening, movements):
    balances = opening.copy()
    seen = set()
    for movement_id, sku, change in movements:
        if movement_id in seen:
            continue
        seen.add(movement_id)
        balance = balances.get(sku, 0) + change
        if balance < 0:
            raise ValueError(sku)
        balances[sku] = balance
    return balances
