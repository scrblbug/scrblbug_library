# 素因数分解 in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# 素因数分解用ライブラリ
# 特に早くはないので注意。

# エラトステネスの篩
def get_prime_list(limit):
    if limit < 2:
        return []
    primep = [True] * (limit+1)

    # 3以上の奇数のみを順番に見ていく
    for n in range(3, int(limit ** 0.5) + 1 , 2):
        if primep[n] == True:
            # 素数の奇数倍のみ書き換えすればOK
            for i in range(n * 3, limit + 1, n * 2):
                primep[i] = False
    return [2] + [p for p in range(3, limit+1, 2) if primep[p]==True]

# 素因数分解
# 素数列挙を行った後、それをもとに素因数分解を行い、
# (素数, 指数) のリストを返す。
# 何度も呼び出す必要がある場合を考慮して、
# 作成済みの素数リストがあれば引き渡すことができる。
def prime_factorize(n, primes=[]):
    if primes == [] or primes[-1] < int(n**0.5):
        primes = get_prime_list(int(n**0.5))
    result = []
    for p in primes:
        if p >= n:
            break
        power = 0
        if n % p == 0:
            while n % p == 0:
                power += 1
                n //= p
            result.append((p, power))
    if n > 1:
        result.append((n, 1))
    return result
