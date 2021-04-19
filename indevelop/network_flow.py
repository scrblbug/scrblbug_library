import sys
sys.setrecursionlimit(10**9)
from collections import defaultdict
from copy import deepcopy
import math
class Network_Flow:
    def __init__(self, N):
        self.N = N
        self.edges = [defaultdict(int) for _ in range(N)]
        self.rev_edges = [defaultdict(int) for _ in range(N)]
        self.INF = 10**18
        self.caps = []

    def prepare_caps(self):
        self.caps = deepcopy(self.edges)

    def add_edge(self, frm, to, cap):
        self.edges[frm][to] += cap
        self.rev_edges[to][frm] += cap

    def add_flow(self, frm, to, vol):
        self.caps[frm][to] -= vol
        self.caps[to][frm] += vol
        if to in self.caps[frm] and self.caps[frm][to] == 0:
            del self.caps[frm][to]
        if frm in self.caps[to] and self.caps[to][frm] == 0:
            del self.caps[to][frm]

    def ford_fulkerson(self, start, goal):
        self.prepare_caps()
        def find_stream(start, goal):
            route = []
            visited = set()

            def dfs(now):
                route.append(now)
                visited.add(now)
                if now == goal:
                    return route
                for nxt in self.caps[now]:
                    if nxt in visited:
                        continue
                    res = dfs(nxt)
                    if res:
                        return res
                route.pop()
            
            return dfs(start)

        result = 0
        while True:
            stream = find_stream(start, goal)
            if stream:
                rt = stream
                vol = min(self.caps[rt[i]][rt[i+1]] for i in range(len(rt)-1))
                for i in range(len(rt)-1):
                    self.add_flow(rt[i], rt[i+1], vol)
                result += vol
            else:
                break
        return result

