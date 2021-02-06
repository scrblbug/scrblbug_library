def get_prime_list_sundaram(limit):
    limit = (limit - 1) // 2
    ing = [True] * (limit+1)
    ing[0] = False
    i = 1
    # while 2 * i**2 + 2 * i < limit + 1:
    for i in range(1, (((4 + 8 * limit) ** 0.5 - 2) // 4) + 1):
        j = i
        while i + j + 2 * i * j < limit + 1:
            ing[i + j + 2 * i * j] = False
            j += 1
        i += 1
    return [2] + [2 * n + 1 for n in range(limit+1) if ing[n]==True]
