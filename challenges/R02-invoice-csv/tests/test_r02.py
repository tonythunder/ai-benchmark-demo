from solution import invoice_totals

HEADER = "invoice_id,currency,amount,state\n"


def test_reads_quoted_commas_as_part_of_invoice_id():
    assert invoice_totals(HEADER + '"store,001", usd ,120.05,posted\n') == {"USD": 12005}


def test_sums_currency_groups_and_signed_amounts_exactly():
    csv_text = HEADER + "a,usd,0.10,posted\nb,USD,0.20,posted\nc,EUR,-2.25,posted\n"
    assert invoice_totals(csv_text) == {"USD": 30, "EUR": -225}


def test_column_order_bom_and_draft_exclusion():
    csv_text = "\ufeffstate,amount,currency,invoice_id\r\nposted,0.00,GBP,k\r\n\r\ndraft,9.99,JPY,z\r\n"
    assert invoice_totals(csv_text) == {"GBP": 0}


def test_empty_files():
    assert invoice_totals(HEADER) == {}
    assert invoice_totals("") == {}
