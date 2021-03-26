# 順列や組み合わせの通り数をMODで求めるのに楽をしたいクラス
# MOD付きで初期化して使用する - COmbination With MOD
class Cowmod:
    def __init__(self, MOD=10**9+7):
        self._fact = [1, 1]
        self._inv = [1, 1]
        self._inv_fact = [1, 1]
        self._MOD = MOD

    def extend_fact(self, N):
        if len(self._fact) > N+1:
            return
        for i in range(len(self._fact), N+1):
            self._fact.append((i * self._fact[-1]) % self._MOD)

    def extend_inv(self, N):
        if len(self._inv) > N+1:
            return
        for i in range(len(self._inv), N+1):
            self._inv.append((-self._inv[self._MOD % i] * (self._MOD // i)) % self._MOD)

    def extend_inv_fact(self, N):
        if len(self._inv_fact) > N+1:
            return
        self.extend_inv(N)
        for i in range(len(self._inv_fact), N+1):
            self._inv_fact.append((self._inv[i] * self._inv_fact[-1]) % self._MOD)

    def fact(self, N):
        self.extend_fact(N)
        return self._fact[N]
    
    def inv(self, N):
        self.extend_inv(N)
        return self._inv[N]
    
    def inv_fact(self, N):
        self.extend_inv_fact(N)
        return self._inv_fact[N]

    def calc_comb(self, n, r):
        return (self.fact(n) * self.inv_fact(n-r) * self.inv_fact(r)) % self._MOD
