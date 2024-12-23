"""A class representing a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key is not None

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.root = None
        self.size = 0

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        current = self.root
        edges = 0

        while current is not None:
            if key == current.key:
                return current, edges + 1
            elif key < current.key:
                current = current.left
            else:
                current = current.right
            edges += 1

        return None, edges

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type value: string
    @param value: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, value):
        if self.root is None:
            self.root = AVLNode(key, value)
            self.size += 1
            return self.root, 0, 0

        current = self.root
        parent = None
        edges = 0

        # Traverse to find the insertion point
        while current is not None:
            parent = current
            if key < current.key:
                if current.left is None:
                    current.left = AVLNode(key, value)
                    current.left.parent = current
                    self.size += 1
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = AVLNode(key, value)
                    current.right.parent = current
                    self.size += 1
                    break
                current = current.right
            edges += 1

        # Update heights and rebalance
        node = parent.left if parent.left and parent.left.key == key else parent.right
        promote_cases = self._rebalance(node)
        return node, edges + 1, promote_cases

    """Rebalances the tree starting from a given node

    @type node: AVLNode
    @param node: the node from which to start rebalancing
    @rtype: int
    @returns: the number of PROMOTE cases during the AVL rebalancing
    """
    def _rebalance(self, node):
        promote_cases = 0
        current = node
        while current is not None:
            old_height = current.height
            self._update_height(current)

            if abs(self._balance_factor(current)) > 1:
                promote_cases += 1
                current = self._rotate(current)

            if current.height == old_height:
                break

            current = current.parent

        return promote_cases

    """Updates the height of a node based on its children

    @type node: AVLNode
    @param node: the node whose height to update
    """
    def _update_height(self, node):
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        node.height = max(left_height, right_height) + 1

    """Calculates the balance factor of a node

    @type node: AVLNode
    @param node: the node whose balance factor to calculate
    @rtype: int
    @returns: the balance factor of the node
    """
    def _balance_factor(self, node):
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        return left_height - right_height

    """Performs rotations to rebalance the tree

    @type node: AVLNode
    @param node: the node to rebalance
    @rtype: AVLNode
    @returns: the new root of the subtree
    """
    def _rotate(self, node):
        if self._balance_factor(node) > 1:
            if self._balance_factor(node.left) < 0:
                self._rotate_left(node.left)
            return self._rotate_right(node)
        elif self._balance_factor(node) < -1:
            if self._balance_factor(node.right) > 0:
                self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    """Performs a left rotation on a subtree

    @type node: AVLNode
    @param node: the root of the subtree to rotate
    @rtype: AVLNode
    @returns: the new root of the subtree
    """
    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.left = node

        new_root.parent = node.parent
        if node.parent is None:
            self.root = new_root
        elif node.parent.left == node:
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        node.parent = new_root
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    """Performs a right rotation on a subtree

    @type node: AVLNode
    @param node: the root of the subtree to rotate
    @rtype: AVLNode
    @returns: the new root of the subtree
    """
    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.right = node

        new_root.parent = node.parent
        if node.parent is None:
            self.root = new_root
        elif node.parent.left == node:
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        node.parent = new_root
        self._update_height(node)
        self._update_height(new_root)
        return new_root
