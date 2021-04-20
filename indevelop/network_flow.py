import sys
sys.setrecursionlimit(10**9)
from collections import defaultdict, deque
from copy import deepcopy
import math
class Network_Flow:
    def __init__(self, N):
        self.N = N
        self.edges = [defaultdict(int) for _ in range(N)]
        self.INF = 10**18
        self.caps = []

    def prepare_caps(self):
        self.caps = deepcopy(self.edges)

    def add_edge(self, frm, to, cap):
        if cap != 0:
            self.edges[frm][to] += cap

    def add_flow(self, frm, to, vol):
        self.caps[frm][to] -= vol
        self.caps[to][frm] += vol
        if to in self.caps[frm] and self.caps[frm][to] == 0:
            del self.caps[frm][to]
        if frm in self.caps[to] and self.caps[to][frm] == 0:
            del self.caps[to][frm]

    def dinic(self, start, goal):
        def make_route():
            self.dist = [-1] * self.N
            self.dist[start] = 0
            queue = deque([start])
            while queue:
                now = queue.popleft()
                if now == goal:
                    break
                for nxt in self.caps[now]:
                    if self.dist[nxt] != -1:
                        continue
                    self.dist[nxt] = self.dist[now] + 1
                    queue.append(nxt)

            rev_caps = [[] for _ in range(self.N)]
            for u in range(self.N):
                if self.dist[u] == -1:
                    continue
                for v in self.caps[u]:
                    if self.dist[v] == -1:
                        continue
                    rev_caps[v].append(u)
            self.on_route = [0] * self.N
            self.on_route[goal] = 1
            queue = deque([goal])
            while queue:
                now = queue.popleft()
                if now == start:
                    break
                for nxt in rev_caps[now]:
                    if self.on_route[nxt] != 0:
                        continue
                    if self.dist[nxt] != self.dist[now] - 1:
                        self.on_route[nxt] = -1
                        continue
                    self.on_route[nxt] = 1
                    queue.append(nxt)
    
        def plan_flow(now, volume):
            flown = []
            for nxt in self.caps[now]:
                p_cap = self.caps[now][nxt]
                tf = volume if volume < p_cap else p_cap
                if self.on_route[nxt] != 1:
                    continue
                if self.dist[nxt] != self.dist[now] + 1:
                    continue
                if nxt == goal:
                    flown = [[now, nxt, tf]]
                    self.caps[now][nxt] -= tf
                    self.caps[nxt][now] += tf
                    break
                rf = plan_flow(nxt, tf)
                flown.append([now, nxt, rf])
                self.caps[now][nxt] -= rf
                self.caps[nxt][now] += rf
                volume -= rf
                if volume == 0:
                    break
            flown_route.extend(flown)
            return sum(f for u, v, f in flown)

        self.prepare_caps()
        result = 0
        while True:
            flown_route = []
            make_route()
            tmp_r = plan_flow(start, self.INF)
            if tmp_r == 0:
                break
            result += tmp_r
            for u, v, f in flown_route:
                if self.caps[u][v] == 0:
                    del self.caps[u][v]
                if self.caps[v][u] == 0:
                    del self.caps[v][u]

        return result
