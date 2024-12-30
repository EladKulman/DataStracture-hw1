#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

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
		self.height = -1
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None


"""
A class implementing an AVL tree.
"""
EXT = AVLNode(None, None)

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self._root = EXT
		self._size = 0
		self._max = EXT


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		return None, -1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		return None, -1

	def successor(self, node):
		if node is None:
			return None

		if node.right.is_real_node():
			current = node.right
			while current.left.is_real_node():
				current = current.left
			return current

		y = node.parent
		while y is not None and node == y.right:
			node = y
			y = y.parent
		return y

	def update_height(self, node):
		node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

	def get_height(self, node):
		if node is None:
			return -1
		return node.height

	def get_balance(self, node):
		if node is None:
			return 0
		return self.get_height(node.left) - self.get_height(node.right)

	def rotate_right(self, y):
		rotation_count = 1  # Count this rotation
		x = y.left
		T2 = x.right
		x.right = y
		y.left = T2
		if T2:
			T2.parent = y
		x.parent = y.parent
		if y.parent is None:
			self.root = x
		else:
			if y.parent.left == y:
				y.parent.left = x
			else:
				y.parent.right = x
		y.parent = x
		self.update_height(y)
		self.update_height(x)
		y.update_size()
		x.update_size()

		return rotation_count

	def rotate_left(self, x):
		rotation_count = 1  # Count this rotation
		y = x.right
		T2 = y.left
		y.left = x
		x.right = T2
		if T2:
			T2.parent = x
		y.parent = x.parent
		if x.parent is None:
			self.root = y
		else:
			if x.parent.left == x:
				x.parent.left = y
			else:
				x.parent.right = y
		x.parent = y
		self.update_height(x)
		self.update_height(y)
		y.update_size()
		x.update_size()

		return rotation_count

	def rebalance(self, node):
		rotations = 0
		while node is not None:
			old_height = node.height
			self.update_height(node)
			balance = self.get_balance(node)

			if balance > 1:
				if self.get_balance(node.left) < 0:
					self.rotate_left(node.left)
					rotations += 1
				self.rotate_right(node)
				rotations += 1
			elif balance < -1:
				if self.get_balance(node.right) > 0:
					self.rotate_right(node.right)
					rotations += 1
				self.rotate_left(node)
				rotations += 1
			if node.is_real_node:
				node.update_size()

			node = node.parent

		return rotations

	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""

	def insert(self, key, value):
		rotations = 0
		e = 0  # Count the number of edges traversed
		parent = None
		current = self._root

		if self._root is None or not self._root.is_real_node():
			self._root = AVLNode(key, value)
			self._max = self._root
			self._size += 1
			return self._root, e, rotations

		while current.is_real_node():
			parent = current
			e += 1
			if key < current.key:
				current = current.left
			else:
				current = current.right

		new_node = AVLNode(key, value)
		new_node.parent = parent
		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		if self._max is None or key > self._max.key:
			self._max = new_node

		current_node = parent
		while current_node is not None:
			self.update_height(current_node)
			balance = self.get_balance(current_node)

			if balance > 1:
				if key < current_node.left.key:
					rotations += self.rotate_right(current_node)
				else:
					self.rotate_left(current_node.left)
					rotations += self.rotate_right(current_node)
			elif balance < -1:
				if key > current_node.right.key:
					rotations += self.rotate_left(current_node)
				else:
					self.rotate_right(current_node.right)
					rotations += self.rotate_left(current_node)

			current_node = current_node.parent

		self._size += 1
		return new_node, e, rotations

	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""

	def finger_insert(self, key, value):
		rotations = 0
		e = 0
		parent = None
		current = self._max

		if not self._root or not self._root.is_real_node():
			self._root = AVLNode(key, value)
			self._max = self._root
			self._size += 1
			return self._root, e, rotations

		while current.is_real_node():
			parent = current
			e += 1
			if key < current.key:
				current = current.left
			else:
				current = current.right

		new_node = AVLNode(key, value)
		new_node.parent = parent
		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		if key > self._max.key:
			self._max = new_node

		current_node = parent
		while current_node is not None:
			self.update_height(current_node)
			balance = self.get_balance(current_node)

			if balance > 1:
				if key < current_node.left.key:
					rotations += self.rotate_right(current_node)
				else:
					self.rotate_left(current_node.left)
					rotations += self.rotate_right(current_node)
			elif balance < -1:
				if key > current_node.right.key:
					rotations += self.rotate_left(current_node)
				else:
					self.rotate_right(current_node.right)
					rotations += self.rotate_left(current_node)

			current_node = current_node.parent

		self._size += 1
		return new_node, e, rotations

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""

	def delete(self, node):
		if not node:
			return

		if node.left is None and node.right is None:
			if node == self._root:
				self._root = None
			elif node.parent and node.parent.left == node:
				node.parent.left = None
			elif node.parent and node.parent.right == node:
				node.parent.right = None
			if node == self._max:
				self._max = node.parent if node.parent and node.parent.is_real_node() else None
			if node.parent:
				node.parent.update_size()
			self.rebalance(node.parent)
			self._size -= 1
			return

		if node.left is None or node.right is None:
			child = node.left if node.left else node.right
			if node == self._root:
				self._root = child
			elif node.parent and node.parent.left == node:
				node.parent.left = child
			else:
				node.parent.right = child
			if child:
				child.parent = node.parent
			if node == self._max:
				self._max = child
			if node.parent:
				node.parent.update_size()
			self.rebalance(node.parent)
			self._size -= 1
			return

		successor_node = self.successor(node)
		if successor_node:
			node.key = successor_node.key
			node.value = successor_node.value
			self.delete(successor_node)

		if node == self._max:
			self._max = self._root  # Recompute the max after deletion

		self._size -= 1

	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self._size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None
