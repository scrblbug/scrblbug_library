# 区間加算クエリ用Binary Indexed Tree(フェニック木)クラス
# とりあえず最低限動作するものを……
class BITsum:
    # 1-indexedにするため、N+1の配列を作成し、0で初期化
    def __init__(self, N):
        self.tree = [0] * (N+1)
        self.N = N
    
    # 指定インデックスに値を加算
    def add(self, x, value):
        while x < self.N + 1:
            self.tree[x] += value
            x += x & -x
    
    # 1~xまでの合計を求める
    def sum_to(self, x):
        if x == 0:
            return 0
        result = 0
        while x > 0:
            result += self.tree[x]
            x -= x & -x
        return result
    
    # 指定範囲[x,y]の合計を求める(x, y > 0)
    def sum_from_to(self, x, y):
        return self.sum_to(y) - self.sum_to(x-1)

# 同じく最大値用BITクラス
class BITmax:
    def __init__(self, N, init=0):
        self.tree = [init] * (N+1)
        self.N = N
        self.init = init
    
    def set(self, x, value):
        while x < self.N + 1:
            old = self.tree[x]
            if value <= old:
                break
            self.tree[x] = value
            x += x & -x
    
    def find_max_to(self, x):
        result = self.init
        while x < self.N + 1:
            result = max(result, self.tree[x])
            x -= x & -x
        return result

