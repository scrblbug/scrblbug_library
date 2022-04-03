# Manacher's Algorithm を用いて、
# 与えられた文字列の連続部分文字列で
# 回文となる最長のもの、
# もしくは return_rad = True で
# 区切り文字を含めた（注意！）各文字の回文半径を返す。

# 考え方の肝は、長回文の中に短回文が含まれている場合、
# その短回文は長回文の反対側にもあるはずなので、その分の
# 探索を省くことが可能……みたいな感じ（伝われ！

def manacher(s, border='$', return_rad=False):
    # 区切り文字を挿入しておく
    s = [c for a, b in zip([border] * len(s), s) for c in (a, b)] + [border]
    N = len(s)

    # 各文字を中心とした最大の半径
    rad = [0] * N

    # 現在考慮すべき右端を含む回文の中心と半径
    c, r = 0, 0

    # 現在見つかっている最長の回文の中心と半径
    maxi, maxr = 1, 0

    # 現在の中心を i としてループ開始
    for i in range(N):
        # 現在の中心の鏡点
        mc = 2 * c - i

        # 現在の中心から確認可能な回文の半径
        k = min(rad[mc], max(0, c + r - i))

        # 回文を広げる
        while i+k+1 < N and i-k-1 >= 0 and s[i+k+1] == s[i-k-1]:
            k += 1
        rad[i] = k

        # 最大値更新
        if k > maxr:
            maxi, maxr = i, k

        # 右端を含む回文の更新
        if i + k > r:
            c, r = i, k

    if return_rad:
        return rad
    else:
        return ''.join(c for c in s[maxi-maxr:maxi+maxr+1] if c != border)
