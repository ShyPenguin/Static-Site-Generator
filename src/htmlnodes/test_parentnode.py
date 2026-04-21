import unittest

from htmlnodes.parentnode import ParentNode
from htmlnodes.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_none(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_leaf_node = LeafNode("div", "Child Leaf")
        parent_node = ParentNode("div", [child_node, child_leaf_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><div>Child Leaf</div></div>",
        )
    