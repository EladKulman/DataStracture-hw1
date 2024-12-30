from AVLTree import AVLTree
import random

TREE_SIZE = 20

def generate_tree(size):
    nums = [i for i in range(2**15)]
    L = random.sample(nums, size)
    T = AVLTree()
    for j in L:
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
    first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
    second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '

    if p < q:
        left += [n * ' '] * (q - p)
    elif q < p:
        right += [m * ' '] * (p - q)

    zipped_lines = zip(left, right)
    lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
    return lines, n + m + u, max(p, q) + 2, n + u // 2

def display(T):
    lines, *_ = display_aux(T._root)
    for line in lines:
        print(line)


def check_height(node):
            if not node.is_real_node():
                return True
            left = node.height - node.left.height
            right = node.height - node.right.height
            if set([left, right]) == set([1, 2]) or (left, right) == (1, 1):
                return check_height(node.left) and check_height(node.right)
            return False

if __name__ == "__main__":
    T = generate_tree(TREE_SIZE)
    display(T)
    print(check_height(T._root))
    