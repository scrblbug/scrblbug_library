class BTNode:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

class Binary_Tree:
    def __init__(self):
        self.root = None
        self.value_cnt = dict()

    def _get_partial_max_node(p_root):
        now = p_root
        while p_root.right != None:
            now = p_root.right
        return now

    def _get_partial_min_node(p_root):
        now = p_root
        while p_root.left != None:
            now = p_root.left
        return now

    def add(self, value):
        if value in self.value_cnt and self.value_cnt[value] > 0:
            self.value_cnt[value] += 1
            return self.value_cnt[value]
        else:
            self.value_cnt[value] = 1

        if self.root == None:
            self.root = BTNode(value)

        else:
            new = BTNode(value)
            now = self.root
            while True:
                if value < now.value:
                    if now.left == None:
                        now.left = new
                        new.parent = now
                        return 1
                    else:
                        now = now.left
                        continue
                else:
                    if now.right == None:
                        now.right = new
                        new.parent = now
                        return 1
                    else:
                        now = now.right
                        continue

    def _get_eq_or_min_larger_node(self, value):
        now = self.root
        result = None
        while True:
            if now.value == value:
                return now
            elif now.value < value:
                if now.right != None:
                    now = now.right
                else:
                    break
            else:
                if result == None or result.value > now.value:
                    result = now
                if now.left != None:
                    now = now.left
                else:
                    break
        return result

    def _get_min_larger_node(self, value):
        now = self.root
        result = None
        while True:
            if now.value <= value:
                if now.right != None:
                    now = now.right
                else:
                    break
            else:
                if result == None or result.value > now.value:
                    result = now
                if now.left != None:
                    now = now.left
                else:
                    break
        return result
    
    def _get_eq_or_max_smaller_node(self, value):
        now = self.root
        result = None
        while True:
            if now.value == value:
                return now
            elif now.value > value:
                if now.left != None:
                    now = now.left
                else:
                    break
            else:
                if result == None or result.value < now.value:
                    result = now
                if now.right != None:
                    now = now.right
                else:
                    break
        return result
    
    def _get_max_smaller_node(self, value):
        now = self.root
        result = None
        while True:
            if now.value >= value:
                if now.left != None:
                    now = now.left
                else:
                    break
            else:
                if result == None or result.value < now.value:
                    result = now
                if now.right != None:
                    now = now.right
                else:
                    break
        return result

    def _remove_node(self, node):
        if node.left != None:
            alt = self._get_partial_max_node(node.left)
        elif node.right != None:
            alt = self._get_partial_min_node(node.right)
        else:
            alt = None

        if node.parent != None:
            if node.parent.right == node:
                node.parent.right = alt
            else:
                node.parent.left = alt

        if alt != None:
            alt.parent = node.parent
            alt.left = node.left
            alt.right = node.right

            if alt.parent.right == alt:
                alt.parent.right = None
            else:
                alt.parent.left = None

        del self.value_cnt[node.value]

