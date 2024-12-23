import unittest

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        # Import AVLTree and AVLNode from the file where they are implemented
        from AVLTree import AVLTree
        self.tree = AVLTree()

    def tearDown(self):
        self.tree = None

    def test_insert_single(self):
        node, edges, promotes = self.tree.insert(10, "value10")
        self.assertEqual(self.tree.get_root().key, 10)
        self.assertEqual(self.tree.get_root().value, "value10")
        self.assertEqual(edges, 0)
        self.assertEqual(promotes, 0)

    def test_insert_multiple(self):
        keys = [20, 10, 30]
        for key in keys:
            self.tree.insert(key, f"value{key}")
        root = self.tree.get_root()
        self.assertEqual(root.key, 20)
        self.assertEqual(root.left.key, 10)
        self.assertEqual(root.right.key, 30)

    def test_search_existing(self):
        self.tree.insert(10, "value10")
        self.tree.insert(20, "value20")
        node, edges = self.tree.search(20)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 20)
        self.assertEqual(edges, 2)

    def test_search_non_existing(self):
        self.tree.insert(10, "value10")
        self.tree.insert(20, "value20")
        node, edges = self.tree.search(15)
        self.assertIsNone(node)
        self.assertEqual(edges, 2)

    def test_balancing_after_insertions(self):
        keys = [30, 20, 40, 10, 25]
        for key in keys:
            self.tree.insert(key, f"value{key}")
        root = self.tree.get_root()
        self.assertEqual(root.key, 30)
        self.assertEqual(root.left.key, 20)
        self.assertEqual(root.right.key, 40)
        self.assertEqual(root.left.left.key, 10)
        self.assertEqual(root.left.right.key, 25)

    def test_height_update(self):
        keys = [10, 20, 30]
        for key in keys:
            self.tree.insert(key, f"value{key}")
        root = self.tree.get_root()
        self.assertEqual(root.height, 1)
        self.assertEqual(root.left.height, 0)
        self.assertEqual(root.right.height, 0)

    def test_insert_promote_cases(self):
        keys = [30, 20, 10]
        promote_counts = []
        for key in keys:
            _, _, promotes = self.tree.insert(key, f"value{key}")
            promote_counts.append(promotes)
        self.assertEqual(promote_counts, [0, 0, 1])

if __name__ == "__main__":
    unittest.main()
