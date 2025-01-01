def _search_from_node(self, start_node, key):
    """
    Core search logic that can start from any node.
    Returns (x, e), where:
      x = the node whose key == key, or EXT if not found
      e = number of edges on the path + 1
    """
    if start_node is EXT:
        return (EXT, 1)  # empty tree => path length = 1

    current = start_node
    edges = 1  # as per instructions: "edges on path + 1"
    while current is not EXT:
        if key == current.key:
            return (current, edges)
        elif key < current.key:
            current = current.left
        else:
            current = current.right
        edges += 1

    return (EXT, edges)


def search(self, key):
    """
    Searches for 'key' in the AVL tree, starting at the root.
    Returns (x, e), where:
      x = the node whose key == key, or EXT if not found
      e = number of edges on the path + 1
    """
    return self._search_from_node(self.root, key)


def finger_search(self, key):
    """
    Searches for 'key' in the AVL tree, starting from the maximum node.
    Handles movement up the tree when the key is less than the maximum key.
    Returns (x, e), where:
      x = the node whose key == key, or EXT if not found
      e = number of edges on the path + 1
    """
    if self.max_node is EXT:
        return (EXT, 1)

    current = self.max_node
    edges = 1

    while current is not EXT and key < current.key:
        current = current.parent
        edges += 1

    result_node, additional_edges = self._search_from_node(current, key)
    return (result_node, edges + additional_edges - 1)