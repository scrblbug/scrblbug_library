# 加算クエリ用Binary Indexed Tree(フェニック木)クラス
# 内部処理は 1-indexed だが、引数・返り値は 0-indexed に統一。

class Binary_Indexed_Tree_Sum:
    def __init__(self, N):
        self._len = 1 << ((N-1).bit_length())
        self._tree = [0] * (self._len + 1)
        self._list = [0] * (self._len)
        self.total = 0
        self.N = N

    # pos に対して x を加える。
    def add_to(self, pos, x):
        self._list[pos] += x
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

    # pos の値を返す。
    def get_value(self, pos):
        return self._list[pos]

    # 累積和が value となる最小のインデックスを返す。
    # value > self.total の場合は Nを返す（存在しないインデックス）
    # ことになるので、事後チェック推奨。
    def lower_bound(self, value):
        if value <= 0:
            return 0
        if value > self.total:
            return self.N

        result = 0
        check = self._len // 2

        # ここからBIT上で直接二分探索を行っているような感じ。
        while check > 0:
            if value > self._tree[result + check]:
                value -= self._tree[result + check]
                result += check
            check //= 2

        return result


# OrderedMultiSet
from bisect import bisect_right
class Ordered_Set:
    def __init__(self, target):
        if type(target) is int:
            self.get_value = lambda x: x
            self.get_index = lambda x: x
            self.N = target + 1
            self.total = 0
        else:
            self.values = sorted(list(set(target)))
            v_to_i = {v:i for i, v in enumerate(self.values)}
            self.get_value = lambda x: self.values[x] if x < len(self.values) else None
            self.get_index = lambda x: v_to_i[x] if x in v_to_i else None
            self.N = len(self.values)
            self.total = 0
    
        self.bit = Binary_Indexed_Tree_Sum(self.N)

    @property
    def count(self):
        return self.bit.total

    # 指定した値の個数を返す。
    def get_value_count(self, value):
        index = self.get_index(value)
        return self.bit.get_value(index) if index != None else 0
    
    # 指定した値を格納する。単一の値を複数個同時に入れられる。
    def add(self, value, count=1):
        index = self.get_index(value)
        self.bit.add_to(index, count)
        self.total += value * count
    
    # 指定した値を取り出す。もしも個数が足りなければ None を返す
    def pop(self, value, count=1):
        if self.get_value_count(value) < count:
            return None
        self.add(value, -count)
        return value

    # 指定した値以下のものの個数を返す。
    def get_value_count_le(self, value):
        index = self.get_index(value)
        return self.bit.get_csum(index)
    
    # 指定した値未満のものの個数を返す。
    def get_value_count_lt(self, value):
        index = self.get_index(value) - 1
        if index < 0:
            return 0
        return self.bit.get_csum(index)
    
    # 指定した値以上のものの個数を返す。
    def get_value_count_ge(self, value):
        return self.count - self.get_value_count_lt(value)
    
    # 指定した値より大きいものの個数を返す。
    def get_value_count_gt(self, value):
        return self.count - self.get_value_count_le(value)

    # 小さい方から数えて合計個数が n 個以上になる、最小の値を返す。
    def lower_bound(self, count):
        index = self.bit.lower_bound(count)
        return self.get_value(index)
    
    # 格納されている一番大きな値を返す
    def get_max(self):
        if self.bit.total == 0:
            return None
        index = self.bit.lower_bound(self.bit.total)
        return self.get_value(index)
    
    def pop_max(self):
        if self.bit.total == 0:
            return None
        index = self.bit.lower_bound(self.bit.total)
        self.bit.add_to(index, -1)
        self.total -= self.get_value(index)
        return self.get_value(index)
    
    # 格納されている一番小さな値を返す
    def get_min(self):
        if self.bit.total == 0:
            return None
        index = self.bit.lower_bound(1)
        return self.get_value(index)
    
    def pop_min(self):
        if self.bit.total == 0:
            return None
        index = self.bit.lower_bound(1)
        self.bit.add_to(index, -1)
        self.total -= self.get_value(index)
        return self.get_value(index)
