# Manacher's Algorithm を用いて、
# 与えられた文字列の連続部分文字列で
# 回文となる最長のものを返す。

def manacher(s, border='$'):
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
        if k > maxr:
            maxi, maxr = i, k

        if i + k > r:
            c, r = i, k

    return ''.join(c for c in s[maxi-maxr:maxi+maxr+1] if c != border)
