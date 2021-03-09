# Weighted_Union_Findクラス in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug
# なんにせよ分かりやすさ重視で……コメントは過剰につけています
# Union_Find(N):要素数NのWeighted_Union_Find木を作成
# .parent:親要素管理リスト
# .rank:木の高さ管理リスト
# .group_count:現在のグループ数
# .N:全体の要素数
# .find(x):最上位の親(グループリーダー)を取得
# .unite(x, y):xとyのグループを統合しつつ、(統合先リーダー, 統合元リーダー)or統合不要なら(-1, -1)を返す
# .get_diff(x, y):xとyの距離を返す。距離が分からない場合はNone

# 必要最低限の実装
# やや再帰で遅くなっているようなので、後日書き直すかも……？

class Weighted_Union_Find:
    def __init__(self, N):
        self.parent = [-1] * N
        self.rank = [0] * N
        self.weight = [0] * N
        self.group_count = N
        self.N = N

    #最上位の親(グループリーダー)を取得
    def find(self, x):
        # parent が負数なら、自分がリーダー
        if self.parent[x] < 0:
            return x

        # 自分をリーダーの直下に置き直し、重み付けを更新するのを
        # 再帰で根本まで行う
        leader = self.find(self.parent[x])
        self.weight[x] += self.weight[self.parent[x]]
        self.parent[x] = leader

        return leader

    # xとyのグループを統合しつつ、(統合先リーダー, 統合元リーダー)を返す
    # 統合不要なら(-1, -1)を返し、矛盾する値が来たらエラーを返す
    def unite(self, x, y, w):
        lx, ly = self.find(x), self.find(y)

        # そもそも同じグループにいる場合、何もしない
        if lx == ly:
            # が、値が矛盾する場合はエラーを返す
            if self.weight[y] - self.weight[x] != w:
                raise ValueError ('value contradiction detected')
            else:
                return (-1, -1)
    
        lx_to_ly = self.weight[x] - self.weight[y] + w
        self.group_count -= 1

        # 同じ高さのときは、とりあえず x の下に y をつけ、高さを更新
        if self.rank[lx] == self.rank[ly]:
            self.parent[ly] = lx
            self.weight[ly] = lx_to_ly
            self.rank[x] += 1
            return (lx, ly)
        
        # 高さが違う場合は、高い方に低い方をつける
        if self.rank[lx] < self.rank[ly]:
            lx, ly = ly, lx
            lx_to_ly = - lx_to_ly
        
        self.parent[ly] = lx
        self.weight[ly] = lx_to_ly
        return (lx, ly)

    # 同じリーダーの下なら（＝比較可能なら）距離を返す
    # 違ったら None を投げておく
    def get_diff(self, x, y):
        if self.find(x) == self.find(y):
            return self.weight[y] - self.weight[x]
        else:
            return None
