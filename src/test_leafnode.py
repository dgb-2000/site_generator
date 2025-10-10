import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            '<p>This is a paragraph of text.</p>'
        )

    def test_leaf_to_html_with_props(self):
        node = LeafNode(
            "a",
            "This is link text",
            {'href': 'https://boot.dev', 'target': '_blank'}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">This is link text</a>'
        )


if __name__ == "__main__":
    unittest.main()
