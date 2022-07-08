# Dinic法による最大流量計算 in Python3
# 書いた人: scrblbug
# サイトURL: http://miaoued.net Twitter: @scrblbug

# そこそこ動くけど速くはない。
# コンテスト用というより、学習用ということで。

# Dinic(N): 頂点数Nで初期化
# .add_edge(u, v, cap): 頂点u → v に容量capの辺を張る
# .get_max_flow(source, sink): source → sinkの最大流量を求め、
#                              [最大流量, 残余グラフ] を返す
from collections import deque
class Dinic:
    def __init__(self, N):
        self._N = N
        self._caps = [dict() for _ in range(N)]
        self.INF = 10**18

    # 残余グラフに辺を追加
    def add_edge(self, u, v, cap):
        if cap == 0 or u == v:
            return

        if v not in self._caps[u]:
            self._caps[u][v] = 0
        self._caps[u][v] += cap

    # 残余グラフに流す
    def _flow(self, f, t, v):
        self._caps[f][t] -= v
        self._caps[t][f] = self._caps[t].setdefault(f, 0) + v
        if self._caps[f][t] == 0:
            del self._caps[f][t]

    # BFS で距離を測定し、最短ルート群を構築する
    def _make_dist(self, source, sink):
        rev_paths = [[] for _ in range(self._N)]
        # 距離を測定
        self._dist = [self.INF] * self._N
        self._dist[source] = 0

        queue = deque([source])
        found = self.INF
        while queue:
            now = queue.pop()
            if now == sink:
                found = self._dist[now]
            for nxt in self._caps[now]:
                if self._dist[nxt] != self.INF or self._dist[now] == found:
                    if self._dist[nxt] == self._dist[now] + 1:
                        rev_paths[nxt].append(now)
                    continue
                self._dist[nxt] = self._dist[now] + 1
                rev_paths[nxt].append(now)
                queue.appendleft(nxt)

        # sink へ到達不能なら、False を返す
        if self._dist[sink] == self.INF:
            return False

        # 通る可能性があるノードを確定
        self._in_use = [False] * self._N
        self._in_use[sink] = True

        queue = deque([sink])
        while queue:
            now = queue.pop()
            for nxt in rev_paths[now]:
                if self._dist[nxt] == self._dist[now] - 1:
                    if self._in_use[nxt] == True:
                        continue
                    self._in_use[nxt] = True
                    queue.appendleft(nxt)

        return found + 1

    # _make_dist に基づく最短ルート上を、DFS で流せるだけ流す
    def _route_flow(self, source, sink):
        _len = self._make_dist(source, sink)
        if _len == False:
            return 0

        # 現在考慮中のルート
        f_nodes = [0] * _len

        # 現在考慮中の流量の上限
        # [from_source, ..., to_sink, from_sink(INF)]
        f_limit = [self.INF] * _len

        # 現在保留中の流量
        # [to_source(ここに流量がまとまる), ..., to_sink]
        f_suspend = [0] * _len

        prev_dist = -1
        queue = [source]

        while queue:
            now = queue.pop()
            d = self._dist[now]

            # ルートの更新
            f_nodes[d] = now

            # 行きがけ
            if prev_dist < d:

                # 流量上限の更新
                if now != source:
                    prev_limit = f_limit[d-1]

                    # 一つ手前の流量上限が 0 なら、そのノードより下流を
                    # 見る必要がないので、queue を pop() してやる
                    if prev_limit == 0:
                        while queue and self._dist[queue[-1]] >= d - 1:
                            queue.pop()
                        continue

                    # 流せるなら、上限を更新
                    if prev_limit > self._caps[f_nodes[d-1]][now]:
                        f_limit[d] = self._caps[f_nodes[d-1]][now]
                    else:
                        f_limit[d] = prev_limit
                    
                # sink に到着していたら、流す準備をしておく
                if now == sink:
                    f_suspend[d] = f_limit[d]
                
                # 次のノードをキューに入れる
                for nxt in self._caps[now]:
                    if self._dist[nxt] == d+1 and self._in_use[nxt]:
                        queue.append(now)
                        queue.append(nxt)

            # 帰りがけ
            else:
                vol = f_suspend[d+1]
                if vol != 0:
                    f_suspend[d+1] = 0
                    f_suspend[d] += vol
                    self._flow(f_nodes[d], f_nodes[d+1], vol)
                    f_limit[d] -= vol
            
            prev_dist = d
        
        return f_suspend[0]

    def get_max_flow(self, source, sink):
        result = 0
        while True:
            flowed = self._route_flow(source, sink)
            if flowed != 0:
                result += flowed
            else:
                break
        return [result, self._caps]
