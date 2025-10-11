import unittest

from parentnode import ParentNode
from leafnode import LeafNode


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

    def test_to_html_with_no_chilren(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", []).to_html()
        self.assertEqual(str(cm.exception), "parent does not have children")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"class": "child"})
        parent_node = ParentNode("div", [child_node], {"class": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent"><span class="child">child</span></div>',
        )


if __name__ == "__main__":
    unittest.main()
