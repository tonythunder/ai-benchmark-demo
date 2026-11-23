# Summarize posted invoice totals from CSV

Implement `invoice_totals(csv_text)`. A valid CSV contains columns `invoice_id,currency,amount,state` in any order. Use CSV quoting rules, including commas inside quoted fields. Count only rows with state `posted` and ignore completely blank lines. Normalize currency by trimming whitespace and uppercasing. Amounts are signed decimal strings with exactly two fractional digits. Return a dictionary of currency codes to exact total integer minor units. Keep currencies whose totals net to zero. A header-only or empty file returns `{}`. A file may start with a UTF-8 BOM character (`\ufeff`).

Example. The row `"store,001", usd ,120.05,posted` under the listed header contributes `12005` to `USD`.
