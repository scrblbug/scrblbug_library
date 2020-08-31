# 演算内容、単位元の必要に応じて(コンストラクタ参照)
import math

# セグメント木のクラス
# 後日遅延評価なども取り入れていきたいが、とりあえず
# 基本的なところだけを分かりやすい形で組んでみたもの
# length:データ部の長さ depth:構造全体の深さ
# offset:上位構造の長さ tree:全体リスト

class Segment_Tree:
    # コンストラクタ。リストもしくは要素数にて初期化。
    # デフォルトでは最小値を求めるが、op(operation=演算内容、デフォルトは最小値)、
    # ie(identity element単位元)を指定することも可能(f.e: op=operator.add, ie=0)
    def __init__(self, arg1, op=lambda x, y:x if x < y else y, ie=math.inf):
        self.op = op
        self.ie = ie

        if type(arg1) == int:
            default_list = []
            self.length = arg1
        else:
            default_list = list(arg1)
            self.length = len(arg1)

        # 全体の深さ、上位構造分のオフセットを求める
        self.depth = 0
        self.offset = 1
        while self.offset < self.length:
            self.depth += 1
            self.offset *= 2

        # 木の初期化。構造は1-indexedで使用していくことにする
        self.tree = [self.ie] * (self.offset * 2)
        if default_list:
            self.tree[self.offset:self.offset+self.length] = default_list
            self.refresh()

    # 全体の再計算(愚直に……)
    def refresh(self):
        for idx in range(self.offset - 1, 0, -1):
            self.tree[idx] = self.op(self.tree[idx*2], self.tree[idx*2+1])

    # 値のセット、及び関連する部分の再計算
    def set(self, idx, value):
        idx = idx + self.offset
        self.tree[idx] = value
        while idx > 1:
            idx //= 2
            old = self.tree[idx]
            new = self.op(self.tree[idx*2], self.tree[idx*2+1])
            if old == new:
                break
            else:
                self.tree[idx] = new
        
    # 半開区間[left, right)における欲しい値(アレっすよ、アレ)を求める
    def find(self, left, right):
        # 区間がおかしなときは、エラー代わりに単位元とかでも返しておく
        if left >= right:
            return self.ie
        
        # 左端と右端から上位を見ていく
        result = self.ie
        left = left + self.offset
        right = right + self.offset - 1

        # 左端と右端が重なるとこまで演算
        while left <= right:
            # 左端は、自身が親の右側の子の時(=ノード番号が奇数のとき)にだけ演算する
            if left % 2 == 1:
                result = self.op(result, self.tree[left])
            # 一段上に移動
            left = (left + 1) // 2

            # 右端は、自身が親の左側の(以下略
            if right % 2 == 0:
                result = self.op(result, self.tree[right])
            right = (right - 1) // 2
       
        return result
    
    # データ領域の値をindexに応じて返す
    def get(self, x):
        return self.tree[x+self.offset]

    # 全領域を対象にした計算値を返す
    def find_all(self):
        return self.tree[1]
    
    # 保持している値全体を返す（デバッグ用？）
    def show_tree(self):
        print(self.tree)
