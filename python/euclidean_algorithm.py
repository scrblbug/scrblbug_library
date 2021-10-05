# ユークリッドの互除法・拡張ユークリッドの互除法 in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# gcd_by_ea(a, b)
# a, b 二つの数が与えられた時、ユークリッドの互除法を用いて
# 最大公約数を求める。
def gcd_by_ea(a, b):
    if a % b == 0:
        return b
    return gcd_by_ea(b, a % b)

# 再帰無しの場合
def gcd_by_ea_without_recursion(a, b):
    while b:
        a, b = b, a % b
    return a

# gcd_by_ex_ea(a, b)
# a, b 二つの数が与えられた時、拡張ユークリッドの互除法を用いて
# ax + by = gcd(a, b) となる x, y, gcd(a, b) を求める。

# 以下、ざっくりとした動きの説明。
# 分かりやすいように定数を大文字で書く。
# D = gcd(A, B)とする (A >= B)
# Ax + By = D
# ここで、A を B で割った商を Q、余りを R とする
# A = BQ + R
# (BQ + R)x + By = D
# B(Qx + y) + Rx = D
# これで (A, B) の問題を (B, R) に還元したことになる(A >= B, B > R)
# なお、この還元はユークリッドの互除法そのもののため、
# 最終的には (D, 0) で終了する。
# Bs + Rt = D となる s, t が決定された時、
# s = Qx + y, t = x
# x = t, y = s - Qt
# 以下再帰的に問題を解決していくが、終了は
# Ds + 0t = D で (s, t) = (1, 0) となる
def gcd_by_ex_ea(a, b):
    if b == 0:
        return (1, 0, a)
    s, t, d = gcd_by_ex_ea(b, a % b)
    return (t, s - (a//b) * t, d)
