# Segment_Treeクラス in Python3
# 書いた人：scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug
# とりあえず基本的なところだけを分かりやすい形で組んでみたもの
# 初期化 (arg1, op, ie):arg1=初期要素or初期要素数
#       op=演算内容(初期値min的動作) ie=単位元(初期値math.inf)
# .length:データ部の長さ
# .offset:上部構造の長さ
# .tree:セグメント木全体のリスト
# .op:演算内容
# .ie:単位元
# .set(index, value):値をセットするとともに、必要な部分を再計算する。
# .get(index):値を取得する。
# .rangeq(left, right):半開放区間[left, right)での演算結果を取得
# .allq():全領域での演算結果を取得する。

class Segment_Tree:
    # リストもしくは要素数にて初期化を行う。
    # デフォルトでは最小値を求めるが、op(operation=演算内容、デフォルトはmin的関数)、
    # ie(identity element単位元)を指定することも可能(f.e: op=operator.add, ie=0)
    def __init__(self, arg1, op=lambda x, y:x if x < y else y, ie=float('inf')):
        self.op = op
        self.ie = ie

        if type(arg1) == int:
            default_list = []
            self.length = arg1
        else:
            default_list = list(arg1)
            self.length = len(arg1)

        # 上部構造分の配列個数(オフセット)を求める
        self.offset = 2 ** ((self.length - 1).bit_length())

        # 木の初期化。上部構造は1-indexedで使用していくことにする
        self.tree = [self.ie] * (self.offset * 2)
        if default_list:
            self.tree[self.offset:self.offset+self.length] = default_list
            self.refresh()

    # 全体の再計算(愚直に下から……)
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

    # データ領域の値をindexに応じて返す
    def get(self, x):
        return self.tree[x+self.offset]
        
    # 半開区間[left, right)における欲しい値(アレっすよ、アレ)を求める
    # 一番下の階層からボトムアップ的に必要な部分を見ていく
    def rangeq(self, left, right):
        # 区間がおかしなときは、エラー代わりに単位元でも返しておく？
        if left >= right:
            return self.ie
        
        # 左端と右端から上位を見ていく
        result = self.ie
        left = left + self.offset
        right = right + self.offset - 1

        # 左端と右端が重なるとこまで演算
        # 最後に重なった場合も、下記の条件分けから一度しか演算されない(念の為)
        while left <= right:
            # 左端は、自身が親の右側の子の時(=ノード番号が奇数のとき)にだけ
            # (自分が左側の時は次の演算に含まれるため)演算する
            if left % 2 == 1:
                result = self.op(result, self.tree[left])
            # 一段上に移動
            left = (left + 1) // 2

            # 右端は、自身が親の左側の(以下略
            # C++だとみんな半開放の値を生かして--rightとかエレガントに書いてるけど……
            if right % 2 == 0:
                result = self.op(result, self.tree[right])
            right = (right - 1) // 2
       
        return result
    
    # 全領域を対象にした計算値を返す
    def allq(self):
        return self.tree[1]



def segfunc(x,y):
    return x+y
class LazySegTree_RAQ:
    def __init__(self,init_val,segfunc,ide_ele):
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1<<(n-1).bit_length()
        self.tree = [ide_ele]*2*self.num
        self.lazy = [0]*2*self.num
        for i in range(n):
            self.tree[self.num+i] = init_val[i]
        for i in range(self.num-1,0,-1):
            self.tree[i] = self.segfunc(self.tree[2*i], self.tree[2*i+1])
    def gindex(self,l,r):
        l += self.num
        r += self.num
        lm = l>>(l&-l).bit_length()
        rm = r>>(r&-r).bit_length()
        while r>l:
            if l<=lm:
                yield l
            if r<=rm:
                yield r
            r >>= 1
            l >>= 1
        while l:
            yield l
            l >>= 1
    def propagates(self,*ids):
        for i in reversed(ids):
            v = self.lazy[i]
            if v==0:
                continue
            self.lazy[i] = 0
            self.lazy[2*i] += v
            self.lazy[2*i+1] += v
            self.tree[2*i] += v
            self.tree[2*i+1] += v
    def add(self,l,r,x):
        ids = self.gindex(l,r)
        l += self.num
        r += self.num
        while l<r:
            if l&1:
                self.lazy[l] += x
                self.tree[l] += x
                l += 1
            if r&1:
                self.lazy[r-1] += x
                self.tree[r-1] += x
            r >>= 1
            l >>= 1
        for i in ids:
            self.tree[i] = self.segfunc(self.tree[2*i], self.tree[2*i+1]) + self.lazy[i]
    def query(self,l,r):
        self.propagates(*self.gindex(l,r))
        res = self.ide_ele
        l += self.num
        r += self.num
        while l<r:
            if l&1:
                res = self.segfunc(res,self.tree[l])
                l += 1
            if r&1:
                res = self.segfunc(res,self.tree[r-1])
            l >>= 1
            r >>= 1
        return res
    
def segfunc(x,y):
    return min(x,y)
class LazySegTree_RUQ:
    def __init__(self,init_val,segfunc,ide_ele):
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1<<(n-1).bit_length()
        self.tree = [ide_ele]*2*self.num
        self.lazy = [None]*2*self.num
        for i in range(n):
            self.tree[self.num+i] = init_val[i]
        for i in range(self.num-1,0,-1):
            self.tree[i] = self.segfunc(self.tree[2*i],self.tree[2*i+1])
    def gindex(self,l,r):
        l += self.num
        r += self.num
        lm = l>>(l&-l).bit_length()
        rm = r>>(r&-r).bit_length()
        while r>l:
            if l<=lm:
                yield l
            if r<=rm:
                yield r
            r >>= 1
            l >>= 1
        while l:
            yield l
            l >>= 1
    def propagates(self,*ids):
        for i in reversed(ids):
            v = self.lazy[i]
            if v is None:
                continue
            self.lazy[i] = None
            self.lazy[2*i] = v
            self.lazy[2*i+1] = v
            self.tree[2*i] = v
            self.tree[2*i+1] = v
    def update(self,l,r,x):
        ids = self.gindex(l,r)
        self.propagates(*self.gindex(l,r))
        l += self.num
        r += self.num
        while l<r:
            if l&1:
                self.lazy[l] = x
                self.tree[l] = x
                l += 1
            if r&1:
                self.lazy[r-1] = x
                self.tree[r-1] = x
            r >>= 1
            l >>= 1
        for i in ids:
            self.tree[i] = self.segfunc(self.tree[2*i], self.tree[2*i+1])
    def query(self,l,r):
        ids = self.gindex(l,r)
        self.propagates(*self.gindex(l,r))
        res = self.ide_ele
        l += self.num
        r += self.num
        while l<r:
            if l&1:
                res = self.segfunc(res,self.tree[l])
                l += 1
            if r&1:
                res = self.segfunc(res,self.tree[r-1])
            l >>= 1
            r >>= 1
        return res
