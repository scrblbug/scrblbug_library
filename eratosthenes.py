# エラトステネスの篩を用いて素数列を作成する関数
# 書いた人：scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug
# get_prime_list: 素朴な実装
# get_prime_list_ex, ex2: 奇数のみを走査する版
# 実行速度は概ね ex > ex2 > normal
# function(limit): 上限limitまでの素数を列挙したリストを返す

# エラトステネスの篩を使い、上限limitまでの素数列を取得する
# もっとも素朴な実装
def get_prime_list(limit):
    # nが素数なら、primep[n]==Trueとする配列を準備
    primep = [True] * (limit + 1)

    # 0, 1は素数から除外
    primep[0], primep[1] = False, False

    # 2～limitの平方根まで順番に見ていく
    for n in range(2, int(limit ** 0.5) + 1):
        # nが素数と確定したら、その倍数を全て素数から除外
        if primep[n] == True:
            for p in range(n * 2, limit + 1, n):
                primep[p] = False

    # 最後に素数だけを取り出す
    return [p for p in range(limit + 1) if primep[p]==True]

# エラトステネスの篩を使うが、2の倍数をあらかじめ除いておく
def get_prime_list_ex(limit):
    if limit < 2:
        return []

    # primep[n]==Trueのとき、(2 * n) + 1 が素数とする
    primep = [True] * ((limit - 1) // 2 + 1)

    primep[0] = False

    # 少しややこしく見えるが、やっていることは同じ
    # f.e. primep[3](=7)の場合、primep[10](=21), primep[17](=35)と
    # 素数から除外されていくことになる
    for n in range(1, int((limit ** 0.5) - 1) // 2 + 1):
        if primep[n] == True:
            p = 2 * n + 1
            for i in range(n + p, len(primep), p):
                primep[i] = False

    # 2だけはしょうがないので最後に追加する
    return [2] + [2 * p + 1 for p in range(len(primep)) if primep[p]==True]

# エラトステネスの篩を使うが、2の倍数をあらかじめ除いておく（見通し良い版）
def get_prime_list_ex2(limit):
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
