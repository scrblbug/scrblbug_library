# サンダラムの篩を用いて、素数リストを作成する
# 書いた人：scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug
# そこまで速くもないが、学習用ということで。

def get_prime_list_sundaram(limit):
    limit = (limit - 1) // 2
    ing = [True] * (limit+1)
    ing[0] = False
    i = 1

    # ing[n]==Trueのとき、2 * n + 1は素数
    # 奇数*奇数 = (2p + 1) * (2q + 1)
    #          = 2p + 2q + 4pq + 1
    #          = 2(p + q + pq) + 1
    # により、
    # i + j + 2 * i * jで作成される合成数を取り除けば、
    # すべての奇数の合成数が取り除かれるという仕組み

    # おぞましい式が入っているが、単に下記のwhileと同じ
    # while 2 * i**2 + 2 * i < limit + 1:
    for i in range(1, (((4 + 8 * limit) ** 0.5 - 2) // 4) + 1):
        j = i
        while i + j + 2 * i * j < limit + 1:
            ing[i + j + 2 * i * j] = False
            j += 1
        i += 1
    return [2] + [2 * n + 1 for n in range(limit+1) if ing[n]==True]
