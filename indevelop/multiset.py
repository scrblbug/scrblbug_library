import heapq
class Multiset:
    def __init__(self):
        self.cnt = dict()
        self.hq = []
    
    def push(self, x):
        if x in self.cnt:
            self.cnt[x] += 1
        else:
            self.cnt[x] = 1
        heapq.heappush(self.hq, x)
 
    def remove(self, x):
        if x in self.cnt and self.cnt[x] > 0:
            self.cnt[x] -= 1
        else:
            raise ValueError(f'{x} not in set')
    
    def pop(self, x):
        while True:
            tmp = heapq.heappop(self.hq)
            if self.cnt[tmp] > 0:
                self.cnt[tmp] -= 1
                return tmp
    
    def get_min(self):
        while True:
            tmp = self.hq[0]
            if self.cnt[tmp] > 0:
                return tmp
            else:
                heapq.heappop(self.hq)
    