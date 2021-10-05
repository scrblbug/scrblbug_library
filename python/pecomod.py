# MOD付き順列組み合わせ用ライブラリ in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# PErmutation and COmbination with MOD
# Pecomod(MOD, fact範囲, inv範囲, inv_fact範囲, 自動拡張=False) にて初期化
# 順列や組み合わせの通り数をMODで求める時に楽をしたいクラス
# そんなに速くはない……初期値をきちんと設定しないとむしろ遅いので注意
# 逆に、計算の確認程度ならMOD以外の初期値設定無しで気軽に呼び出してOK
# 気軽な初期化: peco = Pecomod(MOD)
# それなりな初期化: peco = Pecomod(MOD, N, N, N, False)
class Pecomod:
    def __init__(self, MOD=10**9+7, range_f=2, range_i=2, range_if=2, auto_extend=True):
        self._fact = [1, 1]
        self._inv = [1, 1]
        self._inv_fact = [1, 1]
        self._MOD = MOD
        self._extend_fact(range_f)
        self._extend_inv(range_i)
        self._extend_inv_fact(range_if)
        self._auto_extend = auto_extend

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
        if self._auto_extend:
            self._extend_fact(N)
        return self._fact[N]

    # Nの逆元を取得
    def inv(self, N):
        if self._auto_extend:
            self._extend_inv(N)
        return self._inv[N]

    # Nの逆元の階乗を取得
    def inv_fact(self, N):
        if self._auto_extend:
            self._extend_inv_fact(N)
        return self._inv_fact[N]

    # n 個から順序に関係なく r 個選ぶ組み合わせ数を計算
    def calc_comb(self, n, r):
        return (((self.fact(n) * self.inv_fact(n-r)) % self._MOD) * self.inv_fact(r)) % self._MOD

    # n 個から順序付きで r 個選ぶ組み合わせ数を計算
    def calc_perm(self, n, r):
        return (self.fact(n) * self.inv_fact(n-r)) % self._MOD

    # n 種類のものから重複ありで r 個選ぶ組み合わせ数を計算
    def calc_comb_with_repeat(self, n, r):
        return (((self.fact(n+r-1) * self.inv_fact(n-1)) % self._MOD) * self.inv_fact(r)) % self._MOD
