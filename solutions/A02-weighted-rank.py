def weighted_rank(readings, rank):
    if rank < 1:
        return None
    for value, count in sorted(readings):
        if rank <= count:
            return value
        rank -= count
    return None
