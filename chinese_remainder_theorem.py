# 中国剰余定理 in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# 拡張ユークリッドの互除法を使用する
def gcd_by_ex_ea(a, b):
    if b == 0:
        return (1, 0, a)
    s, t, d = gcd_by_ex_ea(b, a % b)
    return (t, s - (a//b) * t, d)

# a, p, b, q が与えられた時、
# x = a (mod p) = b (mod q)
# であるような x を求める。
# 文章で書くと、p で割って a 余り、q で割って b 余るような
# 数を求める、ということになる。

# 前提条件としては、d = gcd(p, q) としたとき、
# a = b (mod d) 
# また、このとき (b - a) = 0 (mod d) となる。つまり
# (b - a) は d で割り切れるので、
# s = (b - a) // d としておく。 

# py + qz = d
# となる y, z を求める（拡張ユークリッドの互除法）。
# すると、両辺に s を掛けて
# psy + qsz = b - a
# a + psy = b - qsz 
# すると、この両辺は、その形から
# x = a + psy = a (mod p)
# x = b - qsz = b (mod q)
# であるため、この x が求める数字となる。
# x は lcm(p, q) 周期で現れるので、最後にこの剰余を取る

def crt(a, p, b, q):
    y, z, d = gcd_by_ex_ea(p, q)
    if a % d != b % d:
        return None
    s = (b - a) // d
    return (a + p * s * y) % (p * q // d)
