# 加算クエリ用Binary Indexed Tree(フェニック木)クラス
# 内部処理は 1-indexed だが、引数・返り値は 0-indexed に統一。

class Binary_Indexed_Tree_Sum:
    def __init__(self, N):
        self._len = 1 << ((N-1).bit_length())
        self._tree = [0] * (self._len + 1)
        self.total = 0

    # pos に対して x を加える。
    def add_to(self, pos, x):
        pos += 1
        while pos <= self._len:
            self._tree[pos] += x
            pos = pos + (pos & -pos)
        self.total += x

    # pos までの累積和を返す。
    def get_csum(self, pos):
        pos += 1
        result = 0
        while pos > 0:
            result += self._tree[pos]
            pos = pos - (pos & -pos)
        return result
    
    # 累積和が value となる最小のインデックスを返す。
    # value > self.total の場合は右端のインデックスが返る
    # ことになるので、事前チェック推奨。
    def lower_bound(self, value):
        if value <= 0:
            return 0

        result = 0
        check = self._len // 2

        # ここからBIT上で直接二分探索を行っているような感じ。
        while check > 0:
            if value > self._tree[result + check]:
                value -= self._tree[result + check]
                result += check
            check //= 2

        return result
