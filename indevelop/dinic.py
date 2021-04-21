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

    # bfsに基づき、source → sink 間の最短ルートを構成
    def _make_route(self, source, sink):
        self._dist = [-1] * self._N
        self._dist[source] = 0
        queue = [source]
        self._rev_paths = [[] for _ in range(N)]
        while queue:
            now = queue.pop()
            for nxt in self._caps[now]:
                self._rev_paths[nxt].append(now)
                if self._dist[nxt] != -1:
                    continue
                self._dist[nxt] = self._dist[now] + 1
                if nxt == sink:
                    break
                queue.append(nxt)

            else: continue
            break

        self._on_route = [False] * self._N
        self._on_route[sink] = True

        queue = [sink]
        while queue:
            now = queue.pop()
            for nxt in self._rev_paths[now]:
                if self._dist[nxt] >= self._dist[now] or self._on_route[nxt] == True:
                    continue
                self._on_route[nxt] = True
                if nxt == source:
                    break
                queue.append(nxt)

