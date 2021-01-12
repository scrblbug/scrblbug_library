class Lazy_Segment_Tree:
    def __init__(self, init_arg, op, ie, update_op, update_ie):
        self.op = op
        self.ie = ie
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
    



