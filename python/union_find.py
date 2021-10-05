# Union_Findクラス in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug
# なんにせよ分かりやすさ重視で……コメントは過剰につけています
# Union_Find(N):要素数NのUnion_Find木を作成
# .parent:親要素管理リスト
# .rank:木の高さ管理リスト
# .group_count:現在のグループ数
# .N:全体の要素数
# .find(x):最上位の親(グループリーダー)を取得
# .unite(x, y):xとyのグループを統合しつつ、
#   (統合先リーダー, 統合元リーダー) or 統合不要なら(-1, -1)を返す
# .samep(x, y):xとyが同じグループかどうかを判定
# .get_member_count(x):xの所属するグループのメンバー数を取得
# .get_group_members(x):xの所属するグループのメンバーをリストで取得
# .get_all_member_count():全てのリーダー:グループメンバー数を辞書形式で取得
# .get_all_group_members():全てのリーダー:[メンバー一覧]を辞書形式で取得

class Union_Find:
    # 親管理リストと高さ管理リストを初期化し、
    # 要素N個のUnion-Find森を作成する。
    # 親管理リストは、基本的には自分のひとつ上の親を表すが、
    # 値が負の場合には、自身が最上位の親(リーダー)であることを表し、
    # 自分を含めたグループの人数を管理することとする
    def __init__(self, N):
        self.parent = [-1] * N
        self.rank = [0] * N
        self.group_count = N
        self.N = N

    # xの所属するグループのリーダーを返す
    def find(self, x):
        # 自分自身がリーダーなら、自分を返す
        if self.parent[x] < 0:
            return x

        # 再帰的に捜索し、見つかれば繋ぎ変えておく
        # (計算量が増える＝面倒くさいので)高さ管理は行わない
        par = self.find(self.parent[x])
        self.parent[x] = par
        return par

    # xとyのグループを統合する
    def unite(self, x, y):
        # それぞれのリーダーに対する操作を行うことになる
        x = self.find(x)
        y = self.find(y)

        # リーダーが同じなら何もする必要がない
        if x == y:
            return (-1, -1)

        # 木の高さが同じ場合：
        # グループの人数を合計しつつ適当に繋ぎ、繋げられた方の高さを1増やす
        if self.rank[x] == self.rank[y]:
            self.parent[x] += self.parent[y]
            self.parent[y] = x
            self.rank[x] += 1
            self.group_count -= 1
            return (x, y)

        # 木の高さが違うなら、低い方を高い方につなぐ
        if self.rank[x] < self.rank[y]:
            x, y = y, x
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        self.group_count -= 1
        return (x, y)

    # xとyが同じグループかどうかを調べる
    def samep(self, x, y):
        return self.find(x) == self.find(y)

    # xの所属するグループのメンバー数を返す
    def get_member_count(self, x):
        x = self.find(x)
        return -self.parent[x]

    # xの所属するグループのメンバーをリストで返す
    def get_group_members(self, x):
        x = self.find(x)
        return [i for i in range(self.N) if self.find(i) == x]

    # 全ての{リーダー:グループメンバー数}を辞書形式で返す
    def get_all_member_count(self):
        return {idx:-n for idx, n in enumerate(self.parent) if n < 0}

    # 全ての{リーダー:[メンバー一覧]}を辞書形式で返す
    # もしもこれが欲しいだけなら、グラフ探索するほうが速いんじゃないかな……
    def get_all_group_members(self):
        agm_dic = {}
        for i in range(self.N):
            agm_dic.setdefault(self.find(i), [])
            agm_dic[self.find(i)].append(i)
        return agm_dic

# 以下はimmutableなオブジェクトをUnion_Findで扱う拡張クラス
# 適当にでっち上げたのでコメント無し＆不具合が多いかも……
class Union_Find_Objects(Union_Find):
    # 初期化は要素数0として行うので注意。
    def __init__(self):
        super().__init__(0)
        self.obj_to_idx = {}
        self.idx_to_obj = []
    
    # 新規オブジェクトをUnion Findに独立要素として追加する
    def obj_add(self, obj):
        self.parent.append(-1)
        self.rank.append(0)
        self.idx_to_obj.append(obj)
        self.obj_to_idx[obj] = self.N
        self.N += 1
        self.group_count += 1
    
    def obj_find(self, obj):
        x = self.obj_to_idx[obj]
        super().find(x)
        return self.idx_to_obj[x]
    
    def obj_unite(self, obj_x, obj_y):
        x = self.obj_to_idx[obj_x]
        y = self.obj_to_idx[obj_y]
        x, y = super().unite(x, y)
        if x != -1:
            return (self.idx_to_obj[x], self.idx_to_obj[y])
        else:
            return (-1, -1)
    
    def obj_samep(self, obj_x, obj_y):
        x = self.obj_to_idx[obj_x]
        y = self.obj_to_idx[obj_y]
        return super().samep(x, y)

    def obj_existp(self, obj_x):
        return obj_x in self.obj_to_idx
