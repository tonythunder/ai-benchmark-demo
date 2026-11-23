def invoice_totals(csv_text):
    lines = csv_text.splitlines()
    if not lines:
        return {}
    fields = lines[0].removeprefix("\ufeff").split(",")
    totals = {}
    for line in lines[1:]:
        if not line:
            continue
        row = dict(zip(fields, line.split(",", maxsplit=3), strict=True))
        code = row["currency"].strip().upper()
        cents = int(row["amount"].replace(".", ""))
        if row["state"] == "posted":
            totals[code] = totals.get(code, 0) + cents
    return totals
