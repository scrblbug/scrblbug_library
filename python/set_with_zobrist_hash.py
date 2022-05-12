# Zobrist bits を利用して O(1) で確率的一致判定可能な set

# 値ごとのランダムハッシュ（ビット列）を
# 生成・保持しておくためのクラス
from random import Random
class Zobrist_Bits_Generator:
    def __init__(this, seed=42):
        this._value_to_bits = dict()
        this._bits_set = set()
        this.random = Random().seed(seed)

    def get_bits(this, value):
        if value in this._value_to_bits:
            return this._value_to_bits[value]
        else:
            while True:
                _bits = this.random.randint(0, 1<<63-1)
                if _bits in this._bits_set:
                    continue
                this._value_to_bits[value] = _bits
                this._bits_set.add(_bits)
                return _bits

# 本体。
# 上記の Zobrist_Bits_Generator を引き渡して作成する。
class Set_with_Zobrist_Hash:
    def __init__(this, bits_gen):
        this._set = set()
        this._bits_gen = bits_gen
        this.hash = 0

    def add(this, value):
        if value in this._set:
            return (this.hash, this.len)
        else:
            _bits = this._bits_gen.get_bits(value)
            this._set.add(value)
            this.hash = this.hash ^ _bits
            return (this.hash, this.len)
    
    def remove(this, value):
        if value not in this._set:
            raise ValueError("The value is not in the set")
        
        _bits = this._bits_gen.get_bits(value)
        this._set.remove(value)
        this.hash = this.hash ^ _bits
        return (this.hash, this.len)
    
    def has(this, value):
        return value in this._set
    
    @property
    def len(this):
        return len(this._set)
