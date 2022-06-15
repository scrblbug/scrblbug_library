# Zobrist bits を利用して O(1) で確率的一致判定可能な set

# 値ごとのランダムハッシュ（ビット列）を
# 生成・保持しておくためのクラス
from random import Random
class Zobrist_Bits_Generator:
    def __init__(self, seed=42):
        self._value_to_bits = dict()
        self._bits_set = set()
        self.random = Random().seed(seed)

    def get_bits(self, value):
        if value in self._value_to_bits:
            return self._value_to_bits[value]
        else:
            while True:
                _bits = self.random.randint(0, (1<<63)-1)
                if _bits in self._bits_set:
                    continue
                self._value_to_bits[value] = _bits
                self._bits_set.add(_bits)
                return _bits

# 本体。
# 上記の Zobrist_Bits_Generator を引き渡して作成する。
class Set_with_Bits:
    def __init__(self, bits_gen):
        self._set = set()
        self._bits_gen = bits_gen
        self.hash = 0

    def add(self, value):
        if value in self._set:
            return (self.hash, self.len)
        else:
            _bits = self._bits_gen.get_bits(value)
            self._set.add(value)
            self.hash = self.hash ^ _bits
            return (self.hash, self.len)
    
    def remove(self, value):
        if value not in self._set:
            raise ValueError("The value is not in the set")
        
        _bits = self._bits_gen.get_bits(value)
        self._set.remove(value)
        self.hash = self.hash ^ _bits
        return (self.hash, self.len)
    
    def has(self, value):
        return value in self._set
    
    @property
    def len(self):
        return len(self._set)
