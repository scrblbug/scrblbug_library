# popcount
# value を二進法で表した時に 1 が現れる回数を返す
# ただし、value は 64bit 整数以下でなければならない

def popcount(value):
    value = ((value >> 1) & 0x5555555555555555) + (value & 0x5555555555555555)
    value = ((value >> 2) & 0x3333333333333333) + (value & 0x3333333333333333)
    value = (value + (value >> 4)) & 0x0f0f0f0f0f0f0f0f
    value = value + (value >> 8)
    value = value + (value >> 16)
    value = value + (value >> 32)
    return value & 0x7f
