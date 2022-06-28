# Z-Algorithm
# ある文字列 S と、その連続部分文字列 S[i:] との
# 共通接頭辞の文字数の配列、Z を返す

# 例：
# abracadabra
# -> [11, 0, 0, 1, 0, 1, 0, 4, 0, 0, 1]

# Manacher に近い発想になる。
# すなわち、大きな共通接頭辞が発見されたとき、
# そこに含まれる配列については、Z の該当場所を
# 参照することで探索をサボることができる……みたいな。

def z_algorithm(S):
    Z = [0] * len(S)
    Z[0] = len(S)

    # 現在確認中の開始場所
    now = 1

    # now 地点から伸ばしている文字数
    ext = 0

    # この now, ext については、

    while now < len(S):
        # 確認できていない地点から確認を開始する
        while (now + ext < len(S) and S[now+ext] == S[ext]):
            ext += 1
        
        # 現在地の Z を更新
        Z[now] = ext

        # Z の値が 0 の場合、つまり伸ばせた文字数が 0 のときは、
        # 利用できるデータが無いのでそのまま次に進む
        if ext == 0:
            now += 1
            continue

        # もしも Z の値が 0 でないならばデータを流用できるので、
        # 該当するところをコピーする
        # ただし、ext 文字より多くは利用できないので注意
        rep = 1
        while now + rep < len(S) and rep + Z[rep] < ext:
            Z[now+rep] = Z[rep]
            rep += 1
        
        # コピーが終了するのは、文字列が終了したとき、もしくは
        # 使用できる文字列をはみ出した時になる
        
        # 現在位置をコピー終了地点へ
        now += rep

        # 全体で ext の長さの文字列の rep 番目を見ている時の、
        # さっきはみ出た地点、つまり後端までの距離から
        # 探索を再開することになる
        ext -= rep

    return Z

def main():
    S = input()
    print(*z_algorithm(S))

main()