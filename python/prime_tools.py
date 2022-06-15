# エラトステネスの篩＋高速素因数分解 in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

class PrimeTools:
    def __init__(self, limit=10**7):
        self.limit = limit
        self._prime_list = None

        # _divisor[value]: value の素因数
        # _divisor[value] == value なら、value は素数となる
        self._divisor = [i for i in range(limit+1)]

        # エラトステネスの篩を行いつつ、_divisor を更新していく
        for i in range(2, int(limit**0.5)+1):
            if self._divisor[i] == i:
                for j in range(i*2, limit+1, i):
                    self._divisor[j] = i
    
    # 素数かどうか
    def is_prime(self, value):
        if value < 2:
            return False
        
        if value > self.limit:
            raise ValueError('Limit Exceeded (value too large)')

        return self._divisor[value] == value

    # limit までの素数リストを返す
    def get_prime_list(self):
        if self._prime_list == None:
            self._prime_list = [i for i in range(2, self.limit+1)
                                if self._divisor[i]==i]
        return self._prime_list

    # 高速素因数分解
    def _fast_prime_factorize(self, value):
        if not 1 <= value <= self.limit:
            raise ValueError('Value out of range for fast factorization', value)

        if value == 1:
            return []
        
        result = []
        while value != 1:
            div = self._divisor[value]
            power = 0
            while value % div == 0:
                power += 1
                value //= div
            result.append((div, power))
        return sorted(result)

    # 素因数分解
    def prime_factorize(self, value):
        if not 1 <= value <= self.limit**2:
            raise ValueError('Value out of range for factorization', value)

        if value <= self.limit:
            return self._fast_prime_factorize(value)

        result = []
        for div in self.get_prime_list():
            if div >= value:
                break
            power = 0
            while value % div == 0:
                power += 1
                value //= div
            if power > 0:
                result.append((div, power))
                if value <= self.limit:
                    return sorted(result + self._fast_prime_factorize(value))

        # 割れずに残った数字は素数
        if value > 1:
            result.append((value, 1))

        return sorted(result)
