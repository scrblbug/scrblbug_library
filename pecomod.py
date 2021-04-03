# MOD付き順列組み合わせ用ライブラリ in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# 順列や組み合わせの通り数をMODで求める時に楽をしたいクラス
# そんなに速くはない……むしろ遅いので注意
# PErmutation and COmbination with MOD
# Pecomod(MOD) にてMOD付きで初期化、MOD初期値は10**9+7
class Pecomod:
    def __init__(self, MOD=10**9+7):
        self._fact = [1, 1]
        self._inv = [1, 1]
        self._inv_fact = [1, 1]
        self._MOD = MOD

    # 必要に応じて階乗リストを拡張する
    def _extend_fact(self, N):
        if len(self._fact) > N+1:
            return
        for i in range(len(self._fact), N+1):
            self._fact.append((i * self._fact[-1]) % self._MOD)

    # 必要に応じて逆元リストを拡張する
    def _extend_inv(self, N):
        if len(self._inv) > N+1:
            return
        for i in range(len(self._inv), N+1):
            self._inv.append((-self._inv[self._MOD % i] * (self._MOD // i)) % self._MOD)

    # 必要に応じて逆元の階乗リストを拡張する
    def _extend_inv_fact(self, N):
        if len(self._inv_fact) > N+1:
            return
        self._extend_inv(N)
        for i in range(len(self._inv_fact), N+1):
            self._inv_fact.append((self._inv[i] * self._inv_fact[-1]) % self._MOD)

    # N!を取得
    def fact(self, N):
        self._extend_fact(N)
        return self._fact[N]

    # Nの逆元を取得
    def inv(self, N):
        self._extend_inv(N)
        return self._inv[N]

    # Nの逆元の階乗を取得
    def inv_fact(self, N):
        self._extend_inv_fact(N)
        return self._inv_fact[N]

    # n 個から r 個選ぶ組み合わせ数を計算
    def calc_comb(self, n, r):
        return (self.fact(n) * self.inv_fact(n-r) * self.inv_fact(r)) % self._MOD

    # n 種類のものから重複ありで r 個選ぶ組み合わせ数を計算
    def calc_comb_with_repeat(self, n, r):
        return (self.fact(n+r-1) * self.inv_fact(n-1) * self.inv_fact(r)) % self._MOD
