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

    # BFS で距離を測定しておく
    def _make_dist_info(self, source, sink):
        self._dist = [-1] * self._N
        self._dist[source] = 0
        queue = [source]
        self._rev_paths = [[] for _ in range(self._N)]
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

            else:
                continue
            break
        if self._dist[sink] == -1:
            return False
        else:
            return True

    # # bfsで構築したルートに従い、流せるだけ流す
    # ######## 改善の余地あり！！ というか流せるだけ流せてない気が……########
    # def _plan_flow(self, source, sink):
    #     result = 0
    #     order = [0] * (self._dist[sink] + 1)
    #     queue = [sink]
    #     while queue:
    #         now = queue.pop()
    #         order[self._dist[now]] = now
            
    #         if now == source:
    #             max_flow = self.INF
    #             for u, v in zip(order[:-1], order[1:]):
    #                 if self._caps[u][v] < max_flow:
    #                     max_flow = self._caps[u][v]
    #                     if max_flow == 0:
    #                         break
    #             else:
    #                 for u, v in zip(order[:-1], order[1:]):
    #                     self._flow(u, v, max_flow)
    #                 result += max_flow

    #         for nxt in self._rev_paths[now]:
    #             if self._dist[nxt] >= self._dist[now] or now not in self._caps[nxt]:
    #                 continue
    #             queue.append(nxt)
    #     return result

    def plan_flow(self, source, sink):
        if self._make_dist_info(source, sink) == False:
            return 0
        
        result = 0

        # 以下の配列は、silf._dist[node] のインデックスによって位置を決定する

        # 現在考慮中のフローのノードを保持
        # [source, ... , sink]
        flow_nodes = [0] * (self._dist[sink] + 1)

        # 現在考慮中の流量の上限を保持 [from_source, ... , to_sink, self.INF]
        # DFS は sink 側から掛けるので、終端に流量の上限 INF を置いておく
        limit = [0] * (self._dist[sink] + 1)
        limit[-1] = self.INF

        # 流すべき流量の保留分を保持 [to_source(使わない), ..., to_sink]
        suspend = [0] * (self._dist[sink] + 1)


        # DFS で流せるだけ流す
        queue = [sink]

        # 前回見ていた深さ（行きがけ、帰りがけの判別のため）
        prev_dist = self._dist[sink] + 1

        while queue:
            now = queue.pop()
            flow_nodes[self._dist[now]] = now
            prev = flow_nodes[self._dist[now]+1]

            # 行きがけの場合
            if prev_dist > self._dist[now]:
                pass
            # 帰りがけの場合
            else:
                pass
            
            for nxt in self._caps[now]:
                queue.append(now)
                queue.append(nxt)

            prev_dist = self._dist[now]




    def get_max_flow(self, source, sink):
        result = 0
        while True:
            if self._make_route(source, sink):
                result += self._plan_flow(source, sink)
            else:
                break
        return result
