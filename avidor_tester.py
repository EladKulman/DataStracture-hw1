from AVLTree2 import AVLTree, EXT
import random

TREE_SIZE = 6
TEST_NUM = 15

nums = [i for i in range(2**15)]
L = random.sample(nums, TREE_SIZE)


def generate_tree(L1=L):
    T = AVLTree()
    for j in L1:
        T.insert(j, None)
    return T


def display_aux(T):
    """Returns list of strings, width, height, and horizontal coordinate of the root."""

    # No child.
    if T.right is None and T.left is None:
        line = '%s' % T.key
        width = len(line)
        height = 1
        middle = width // 2
        return [line], width, height, middle

    # Only left child.
    if T.right is None:
        lines, n, p, x = display_aux(T.left)
        s = '%s' % T.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
        second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
        shifted_lines = [line + u * ' ' for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

    # Only right child.
    if T.left is None:
        lines, n, p, x = display_aux(T.right)
        s = '%s' % T.key
        u = len(s)
        first_line = s + x * '_' + (n - x) * ' '
        second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
        shifted_lines = [u * ' ' + line for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

    # Two children.
    left, n, p, x = display_aux(T.left)
    right, m, q, y = display_aux(T.right)
    s = '%s' % T.key
    u = len(s)
    first_line = (x + 1) * ' ' + (n - x - 1) * \
        '_' + s + y * '_' + (m - y) * ' '
    second_line = x * ' ' + '/' + \
        (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '

    if p < q:
        left += [n * ' '] * (q - p)
    elif q < p:
        right += [m * ' '] * (p - q)

    zipped_lines = zip(left, right)
    lines = [first_line, second_line] + \
        [a + u * ' ' + b for a, b in zipped_lines]
    return lines, n + m + u, max(p, q) + 2, n + u // 2


def display(T):
    lines, *_ = display_aux(T.root)
    for line in lines:
        print(line)
    print("_" * 50)


def check_height(node):
    if not node.is_real_node():
        return True
    left = node.height - node.left.height
    right = node.height - node.right.height
    if set([left, right]) == set([1, 2]) or (left, right) == (1, 1):
        return check_height(node.left) and check_height(node.right)
    return False


def check_bst(self):
    def _check_bst(node):
        if node.key == None:
            return True
        if node.height == 0:
            return True
        if node.left.key != None:
            if node.left is not EXT:
                if node.key < node.left.key:
                    return False
        if node.right is not EXT:
            if node.right.key != None:
                if node.key > node.right.key:
                    return False
        return (_check_bst(node.left) and _check_bst(node.right))
    return _check_bst(self.root)


def test_suite():
    # Test 0 - test tree search
    for i in range(TEST_NUM):
        T = generate_tree()
        for j in range(TREE_SIZE):
            key = L[j]
            v = T.search(key)[0]
            assert v.key == key
            assert v.value == None
        
    # Test 1 - test tree insert
    for _ in range(TEST_NUM):
        T = generate_tree()
        assert check_height(T.root)
        assert T.size == TREE_SIZE
        assert T.max_node.key == max(L)
        assert T.max_node.right == EXT
        assert check_bst(T)

    # Test 2 - test tree join
    nums_small = nums[:2**6]
    nums_big = nums[2**8:]
    for i in range(TEST_NUM):
        if i % 3 == 0:
            L_small_tree_size = TREE_SIZE + int(TREE_SIZE/2)
            L_big_tree_size = TREE_SIZE
        else:
            L_small_tree_size = TREE_SIZE
            L_big_tree_size = TREE_SIZE + int(TREE_SIZE/2)
        L_small = random.sample(nums_small, L_small_tree_size)
        L_big = random.sample(nums_big, L_big_tree_size)
        T_small = generate_tree(L_small)
        T_big = generate_tree(L_big)
        key = 2**6
        val = None
        if i % 2 == 0:
            T_small.join(T_big, key, val)
            assert check_height(T_small.root)
            assert T_small.size == L_small_tree_size + L_big_tree_size + 1
            assert T_small.max_node.key == max(L_big)
            assert T_small.max_node.right == EXT
            assert check_bst(T_small)
            assert check_bst(T_small)
        else:
            T_big.join(T_small, key, val)
            assert check_height(T_big.root)
            assert T_big.size == L_small_tree_size + L_big_tree_size + 1
            assert T_big.max_node.key == max(L_big)
            assert T_big.max_node.right == EXT
            assert check_bst(T_big)
            assert check_bst(T_big)

    # Test 3 - test tree split
    for i in range(TEST_NUM):
        L1 = random.sample(nums, TREE_SIZE)
        T = generate_tree(L1)
        split_key = random.choice(L1)
        v = T.search(split_key)[0]
        t1, t2 = T.split(v)
        print("aaa")
        assert check_bst(t1)
        assert check_bst(t2)
        assert check_height(t1.root)
        assert check_height(t2.root)

if __name__ == "__main__":
    test_suite()
