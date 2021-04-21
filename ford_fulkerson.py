# Ford_Fulkerson法による最大流量計算 in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# そこそこ動くけど速くはない。
# コンテスト用というより、学習用ということで。

# Ford_Fulkerson(N): 頂点数Nで初期化
# .add_edge(u, v, cap): 頂点u → v に容量capの辺を張る
# .get_max_flow(source, sink): source → sinkの最大流量を求める

class Ford_Fulkerson:
    def __init__(self, N):
        self._N = N
        self._caps = [dict() for _ in range(N)]
        self.INF = 10**18

    # 残余グラフに辺を張る
    def add_edge(self, u, v, cap):
        if cap == 0 or u == v:
            return
        if v not in self._caps[u]:
            self._caps[u][v] = 0
        self._caps[u][v] += cap
    
    # 残余グラフ書き換え（双方向）
    def _make_flow(self, u, v, volume):
        self._caps[u][v] -= volume
        if self._caps[u][v] == 0:
            del self._caps[u][v]

        if u not in self._caps[v]:
            self._caps[v][u] = 0
        self._caps[v][u] += volume

    # dfsで適当な経路を求め、[逆経路, 容量] を返す
    def _plan_route(self, source, sink):
        # 訪問済みチェック 兼 経路の一つ前の頂点を保持するリスト
        prev = [-1] * self._N
        prev[source] = source
        queue = [source]

        while queue:
            now = queue.pop()

            # ゴールに到着してたら終了
            if now == sink:
                break

            # 訪問済みでなければ経路を更新してキューに入れる
            for nxt in self._caps[now]:
                if prev[nxt] != -1:
                    continue
                prev[nxt] = now
                queue.append(nxt)

        # 経路が見つからなかったら、[[], 0] を返す
        if prev[sink] == -1:
            return [[], 0]

        # 逆順で経路を復元しつつ、最大容量を確認
        rev_route = [sink]
        now = sink
        max_cap = self.INF
        while now != source:
            if self._caps[prev[now]][now] < max_cap:
                max_cap = self._caps[prev[now]][now]
            now = prev[now]
            rev_route.append(now)

        # [逆順経路, 最大容量] を返す
        return [rev_route, max_cap]

    # 最大流量計算
    def get_max_flow(self, source, sink):
        result = 0

        # 経路が見つかる間は頑張って流す
        while True:
            route, volume = self._plan_route(source, sink)
            if volume == 0:
                break
            result += volume

            # 残余グラフ更新
            for u, v in zip(route[1:], route[:-1]):
                self._make_flow(u, v, volume)

        return result
