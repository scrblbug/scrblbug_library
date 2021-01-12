# 書きかけ
class Lazy_Segment_Tree:
    def __init__(self, init_arg, 
                 op=lambda x,y:x+y, 
                 ie=0, 
                 reflect_op=lambda x,y,rng:x+y*rng, 
                 update_op=lambda x,y:x+y, 
                 update_ie=0):
        self.op = op
        self.ie = ie
        self.refop = reflect_op
        self.udop = update_op
        self.udie = update_ie

        if type(init_arg) == int:
            self.length = init_arg
            default_list = None
        elif type(init_arg) == list:
            default_list = init_arg
            self.length = len(init_arg)
            
        self.depth = (self.length-1).bit_length()
        self.offset = 2**self.depth
        
        self.tree = [ie] * (self.offset * 2)

        if default_list:
            self.tree[self.offset:self.offset+self.length] = default_list
            self.init_tree()
        
        self.udtree = [self.udie] * (self.offset * 2)

    def init_tree(self):
        for i in range(self.offset-1, 0, -1):
            self.tree[i] = self.op(self.tree[i * 2], self.tree[i * 2 + 1])
    
    def generate_op_index(self, left, right):
        if not (0 <= left < right <= self.length):
            raise IndexError(f'left:{left}, right:{right}, length:{self.length}')
        left += self.offset
        right += self.offset
        while left < right:
            if right & 1:
                yield right - 1
            if left & 1:
                yield left
            left = (left + 1) >> 1
            right = (right - 1) >> 1

    def get_ud_index(self, left, right):
        if not (0 <= left < right <= self.length):
            raise IndexError(f'left:{left}, right:{right}, length:{self.length}')
        left += self.offset
        right += self.offset
        left = left // ((left & -left) * 2)
        right = (right - 1) // ((right & -right) * 2)
        result = []
        while left != right:
            if left < right:
                result.append(right)
                right = right >> 1
            else:
                result.append(left)
                left = left >> 1
        while left:
            result.append(left)
            left //= 2
        return result

    def update_value(self, x, left, right=None):
        if right == None:
            right = left + 1
        to_be_updated = self.get_ud_index(left, right)
        for idx in to_be_updated[::-1]:
            self.propagate(idx)

        for idx in self.generate_op_index(left, right):
            self.udtree[idx] = self.udop(self.udtree[idx], x)
            self.propagate(idx)
        
        for idx in to_be_updated:
            self.tree[idx] = self.op(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def propagate(self, idx):
        if self.udtree[idx] == self.udie:
            return
        self.tree[idx] = self.refop(self.tree[idx], self.udtree[idx], 2**(self.depth - idx.bit_length() + 1))
        self.udtree[idx] = self.udie
        if idx.bit_length() != self.depth + 1:
            self.udtree[idx * 2] = self.udop(self.udtree[idx * 2], self.udtree[idx])
            self.udtree[idx * 2 + 1] = self.udop(self.udtree[idx * 2 + 1], self.udtree[idx])
