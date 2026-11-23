import csv
from io import StringIO


def invoice_totals(csv_text):
    totals = {}
    for row in csv.DictReader(StringIO(csv_text.removeprefix("\ufeff"), newline="")):
        if row["state"] != "posted":
            continue
        currency = row["currency"].strip().upper()
        minor_units = int(row["amount"].replace(".", ""))
        totals[currency] = totals.get(currency, 0) + minor_units
    return totals
