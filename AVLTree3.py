###################################
#  Single SENTINEL Node Instance  #
###################################

class AVLNode:
    """
    Represents a node in an AVL Tree.
    If key is None, this node is the sentinel (EXT).
    Otherwise, it is a real node.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.height = -1 if key is None else 0
        # By default, pointers are self (for the sentinel) or set properly in real nodes
        self.left = None
        self.right = None
        self.parent = None

    def is_real_node(self):
        """
        Returns True if this node is a real node (key != None).
        Returns False if this node is the sentinel (key == None).
        """
        return self.key is not None

    def get_balance_factor(self):
        """
        Returns (left.height - right.height) if real,
        or 0 if sentinel.
        """
        if not self.is_real_node():
            return 0
        return self.left.height - self.right.height

    def update_height(self):
        """
        Recomputes the node's height: 1 + max(left.height, right.height).
        For sentinel, height stays -1.
        """
        if not self.is_real_node():
            self.height = -1
        else:
            self.height = 1 + max(self.left.height, self.right.height)

# Create ONE global sentinel node EXT.
EXT = AVLNode(None, None)
# Make all its pointers reference itself
EXT.left = EXT
EXT.right = EXT
EXT.parent = EXT
# Height is -1 (already set in constructor).


class AVLTree:
    """
    An AVL Tree using a single sentinel node (EXT) for all external pointers.
    """

    def __init__(self):
        # Required fields (per your instructions):
        self._root = EXT
        self._size = 0
        self._max = EXT

    ##########################
    #       BASIC GETTERS    #
    ##########################

    def get_root(self):
        """Return the tree's root (EXT if empty)."""
        return self._root

    def size(self):
        """Return the number of real nodes in the tree."""
        return self._size

    def max_node(self):
        """Return the node with the maximal key, or None if empty."""
        if self._max.is_real_node():
            return self._max
        return None

    ##########################
    #        SEARCH          #
    ##########################

    def search(self, key):
        """
        Search for 'key' in the tree (from self._root).
        Returns (found_node, e), where:
          found_node: the AVLNode with key=key, or None if not found
          e: number of edges traveled + 1
        """
        if not self._root.is_real_node():
            return (None, 1)  # empty => path length 1

        current = self._root
        edges = 1
        while current.is_real_node():
            if key == current.key:
                return (current, edges)
            elif key < current.key:
                current = current.left
            else:
                current = current.right
            edges += 1

        # if we reached EXT, not found
        return (None, edges)

    def finger_search(self, key):
        """
        Search for 'key' starting from the maximum node instead of the root.
        Returns (found_node, e).
        """
        if not self._max.is_real_node():
            return (None, 1)  # empty tree

        current = self._max
        edges = 1
        while current.is_real_node():
            if key == current.key:
                return (current, edges)
            elif key < current.key:
                if current.left.is_real_node():
                    current = current.left
                else:
                    current = current.parent
            else:
                # key > current.key
                if current.right.is_real_node():
                    current = current.right
                else:
                    current = current.parent
            edges += 1

        return (None, edges)

    ##########################
    #       INSERT           #
    ##########################

    def insert(self, key, value):
        """
        Insert (key, value) into the tree (from _root).
        Returns (x, e, h):
          x = newly inserted node
          e = # of edges traveled + 1 (before rebalance)
          h = # of "PROMOTE" (implementation-specific)
        """
        if not self._root.is_real_node():
            # Tree is empty
            new_node = AVLNode(key, value)
            self._connect_as_root(new_node)
            return (new_node, 1, 0)

        current = self._root
        edges = 1
        while True:
            edges += 1
            if key < current.key:
                if not current.left.is_real_node():  
                    # current.left == EXT => place new node here
                    new_node = AVLNode(key, value)
                    self._connect_child(current, new_node, is_left=True)
                    break
                else:
                    current = current.left
            else:
                # key > current.key (assuming no duplicates)
                if not current.right.is_real_node():
                    new_node = AVLNode(key, value)
                    self._connect_child(current, new_node, is_left=False)
                    break
                else:
                    current = current.right

        # Update size, potentially update _max
        self._size += 1
        if (self._max.is_real_node() and key > self._max.key) or (not self._max.is_real_node()):
            self._max = new_node

        # Rebalance from new_node upward
        promotes = self._rebalance_upwards(new_node)
        return (new_node, edges, promotes)

    def finger_insert(self, key, value):
        """
        Insert (key, value) starting from self._max instead of _root.
        Returns (x, e, h).
        """
        if not self._max.is_real_node():
            # Tree is empty
            new_node = AVLNode(key, value)
            self._connect_as_root(new_node)
            return (new_node, 1, 0)

        current = self._max
        edges = 1
        while True:
            edges += 1
            if key < current.key:
                if not current.left.is_real_node():
                    new_node = AVLNode(key, value)
                    self._connect_child(current, new_node, is_left=True)
                    break
                else:
                    current = current.left
            else:
                # key >= current.key
                if not current.right.is_real_node():
                    new_node = AVLNode(key, value)
                    self._connect_child(current, new_node, is_left=False)
                    break
                else:
                    current = current.right

        # Update size and possibly _max
        self._size += 1
        if (not self._max.is_real_node()) or (key > self._max.key):
            self._max = new_node

        promotes = self._rebalance_upwards(new_node)
        return (new_node, edges, promotes)

    ##########################
    #        DELETE          #
    ##########################

    def delete(self, node):
        """
        Delete 'node' (which is a real node) from the tree. Rebalance.
        """
        if node is None or (not node.is_real_node()):
            return  # not a real node => nothing

        # If node has ≤1 real child => remove directly
        if (not node.left.is_real_node()) or (not node.right.is_real_node()):
            self._delete_single_child(node)
        else:
            # 2 real children => swap with successor, then remove that
            successor = self._get_min_subtree(node.right)
            # swap key/value
            node.key, successor.key = successor.key, node.key
            node.value, successor.value = successor.value, node.value
            # remove successor
            self._delete_single_child(successor)

        # If we removed the max, recalc _max
        if node == self._max:
            self._max = self._find_new_max()

    def _delete_single_child(self, node):
        parent = node.parent
        child = node.left if node.left.is_real_node() else node.right

        # If node == _root
        if parent == EXT:  
            # node was the root
            if child.is_real_node():
                self._root = child
                child.parent = EXT
            else:
                self._root = EXT
            self._size -= 1
            self._rebalance_upwards(child)
            return

        # Otherwise, re-hook parent's pointer
        is_left_child = (parent.left == node)
        if is_left_child:
            parent.left = child
        else:
            parent.right = child
        child.parent = parent

        self._size -= 1
        self._rebalance_upwards(parent)

    ##########################
    #       JOIN / SPLIT     #
    ##########################

    def join(self, tree2, key, value):
        """
        Joins self with tree2 around a new item (key, value).
        Precondition: all keys in self < key < all keys in tree2 (or opposite).
        """
        # If self is empty, just insert into tree2
        if not self._root.is_real_node():
            _, _, _ = tree2.insert(key, value)
            self._root = tree2._root
            self._size = tree2._size
            self._max = tree2._max
            return

        # If tree2 is empty
        if not tree2._root.is_real_node():
            self.insert(key, value)
            return

        # We compare heights
        h1 = self._root.height
        h2 = tree2._root.height

        new_node = AVLNode(key, value)

        if h1 > h2:
            # attach tree2 under self
            curr = self._root
            while curr.is_real_node():
                if curr.height == h2:
                    break
                if curr.right.is_real_node() and (curr.right.height >= h2):
                    curr = curr.right
                else:
                    break

            new_node.left = curr.right
            new_node.left.parent = new_node
            new_node.right = tree2._root
            new_node.right.parent = new_node

            curr.right = new_node
            new_node.parent = curr

            self._size = self._size + tree2._size + 1
            # Rebalance
            self._rebalance_upwards(new_node)
        else:
            # attach self under tree2
            curr = tree2._root
            while curr.is_real_node():
                if curr.height == h1:
                    break
                if curr.left.is_real_node() and (curr.left.height >= h1):
                    curr = curr.left
                else:
                    break

            new_node.right = curr.left
            new_node.right.parent = new_node
            new_node.left = self._root
            new_node.left.parent = new_node

            curr.left = new_node
            new_node.parent = curr

            tree2._size = self._size + tree2._size + 1
            tree2._rebalance_upwards(new_node)
            # Now adopt tree2's structure
            self._root = tree2._root
            self._size = tree2._size

        # Update max
        self._max = self._find_new_max()

    def split(self, node):
        """
        Splits this tree at 'node'.
        Returns (left_tree, right_tree).
        All keys < node.key go to left_tree, all keys > node.key go to right_tree.
        'node' is removed in the process.
        """
        left_tree = AVLTree()
        right_tree = AVLTree()

        # 1) delete 'node'
        self.delete(node)
        # 2) transform to array and re-insert into left_tree / right_tree
        arr = self.avl_to_array()
        pivot = 0
        while pivot < len(arr) and arr[pivot][0] < node.key:
            pivot += 1
        left_part = arr[:pivot]
        right_part = arr[pivot:]  # node.key itself is removed

        for (k, v) in left_part:
            left_tree.insert(k, v)
        for (k, v) in right_part:
            right_tree.insert(k, v)

        return (left_tree, right_tree)

    ##########################
    #       UTILITIES        #
    ##########################

    def avl_to_array(self):
        """
        Returns an in-order traversal of (key, value) for all real nodes.
        """
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node, result):
        if not node.is_real_node():
            return
        self._inorder(node.left, result)
        result.append((node.key, node.value))
        self._inorder(node.right, result)

    ##########################
    #   ROTATION / REBALANCE #
    ##########################

    def _rebalance_upwards(self, start_node):
        """
        From start_node up to the root, do height updates and rotations.
        Returns number of "PROMOTE" operations (optional).
        """
        promotes = 0
        current = start_node
        while current.is_real_node():
            old_height = current.height
            current.update_height()
            # If height increased, consider that a "promote"
            if current.height > old_height:
                promotes += 1

            bf = current.get_balance_factor()
            if bf == 2:
                # left-heavy
                if current.left.get_balance_factor() < 0:
                    self._rotate_left(current.left)
                self._rotate_right(current)
            elif bf == -2:
                # right-heavy
                if current.right.get_balance_factor() > 0:
                    self._rotate_right(current.right)
                self._rotate_left(current)

            current = current.parent
        return promotes

    def _rotate_left(self, node):
        right_child = node.right
        if not right_child.is_real_node():
            return  # can't rotate with EXT

        # Turn right_child.left into node.right
        node.right = right_child.left
        node.right.parent = node

        # node goes to the left of right_child
        right_child.left = node
        parent = node.parent
        right_child.parent = parent
        node.parent = right_child

        # If node was root
        if parent == EXT:
            self._root = right_child
        else:
            if parent.left == node:
                parent.left = right_child
            else:
                parent.right = right_child

        node.update_height()
        right_child.update_height()

    def _rotate_right(self, node):
        left_child = node.left
        if not left_child.is_real_node():
            return

        node.left = left_child.right
        node.left.parent = node

        left_child.right = node
        parent = node.parent
        left_child.parent = parent
        node.parent = left_child

        if parent == EXT:
            self._root = left_child
        else:
            if parent.right == node:
                parent.right = left_child
            else:
                parent.left = left_child

        node.update_height()
        left_child.update_height()

    ##########################
    #   HELPER CONNECTIONS   #
    ##########################

    def _connect_as_root(self, new_node):
        """
        Helper to set a newly created node as the tree's root.
        """
        self._root = new_node
        new_node.parent = EXT
        new_node.left = EXT
        new_node.right = EXT
        self._size = 1
        self._max = new_node

    def _connect_child(self, parent_node, child_node, is_left):
        """
        Hook 'child_node' as either left or right child of 'parent_node'.
        Initialize pointers for the new child.
        """
        child_node.parent = parent_node
        child_node.left = EXT
        child_node.right = EXT
        if is_left:
            parent_node.left = child_node
        else:
            parent_node.right = child_node

    def _get_min_subtree(self, node):
        """
        Return the node with smallest key in subtree rooted at 'node'.
        """
        current = node
        while current.left.is_real_node():
            current = current.left
        return current

    def _find_new_max(self):
        """
        After deleting or splitting (if we lost the old max),
        find the new max in O(log n) by going right from root.
        Returns EXT if empty, or the rightmost real node.
        """
        if not self._root.is_real_node():
            return EXT
        current = self._root
        while current.right.is_real_node():
            current = current.right
        return current
