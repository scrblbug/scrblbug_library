def get_prime_list(limit):
    primep = [True] * (limit + 1)
    primep[0], primep[1] = False, False

    for n in range(2, int(limit ** 0.5) + 1):
        if primep[n] == True:
            for p in range(n * 2, limit + 1, n):
                primep[p] = False

    return [p for p in range(limit + 1) if primep[p]==True]

