def discount_shares(line_totals, discount):
    total = sum(line_totals)
    if total == 0:
        return [0] * len(line_totals)

    quotient_remainder = [divmod(amount * discount, total) for amount in line_totals]
    shares = [quotient for quotient, _ in quotient_remainder]
    unassigned = discount - sum(shares)
    order = sorted(range(len(shares)), key=lambda index: (-quotient_remainder[index][1], index))
    for index in order[:unassigned]:
        shares[index] += 1
    return shares
