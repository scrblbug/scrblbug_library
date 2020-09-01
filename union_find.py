# Union_Findクラス
# なんにせよ分かりやすさ重視で……
# parent:親要素管理リスト rank:木の高さ管理リスト

class Union_Find:
    # コンストラクタ。親管理リストと高さ管理リストを初期化し、
    # 要素N個のUnion-Find木を作る
    def __init__(self, N):
        self.parent = [i for i in range(N)]
        self.rank = [0] * N
    
    # 最上位の親を探す
    def find(self, x):
        # 自分自身が親なら、自分を返す
        if x == self.parent[x]:
            return x

        # 再帰的に捜索し、見つかれば繋ぎ変えておく
        # (面倒くさいので)高さ管理は行わない
        par = self.find(self.parent[x])
        self.parent[x] = par
        return par

    # xとyのグループを統合する
    def unite(self, x, y):
        # それぞれの最上位の親に対する操作を行うことになる
        x = self.find(x)
        y = self.find(y)

        # 木の高さが同じ→適当に繋ぎ、繋げられた方の高さを1増やす
        if self.rank[x] == self.rank[y]:
            self.parent[y] = x
            self.rank[x] += 1
        
        # 木の高さが違うなら、低い方を高い方につなぐ
        elif self.rank[x] > self.rank[y]:
            self.parent[y] = x
        else:
            self.parent[x] = y
    
    # xとyが同じグループかどうかを調べる
    def same(self, x, y):
        return self.find(x) == self.find(y)
    
    # 全てのグループの人数を辞書形式で返す
    def get_groups(self):
        g_dic = {}
        for i in range(len(self.parent)):
            p = self.find(i)
            g_dic.setdefault(p, 0)
            g_dic[p] += 1  
        return g_dic
