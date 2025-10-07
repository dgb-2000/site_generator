import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            "p",
            "test",
            None,
            {"class": "test", "style": "display: none;"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="test" style="display: none;"'
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "test",
            None,
            {"class": "test"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag: p, value: test, children: None, props: {'class': 'test'})"
        )

    def test_nested(self):
        children = []
        children.append(HTMLNode("p", "test1", None, {}))
        children.append(HTMLNode("p", "test2", None, {"class": "custom"}))
        node = HTMLNode("p", "test", children, {"class": "test"})
        self.assertEqual(
            repr(node.children[0]),
            "HTMLNode(tag: p, value: test1, children: None, props: {})"
        )
        self.assertEqual(
            repr(node.children[1]),
            "HTMLNode(tag: p, value: test2, children: None, props: {'class': 'custom'})"
        )

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )


if __name__ == "__main__":
    unittest.main()
