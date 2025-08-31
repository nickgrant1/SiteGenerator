import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_to_html(self):
        node2 = HTMLNode(props= {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        with self.assertRaises(NotImplementedError): 
            node2.to_html()

    def test_props_to_html(self):
        node2 = HTMLNode(props= {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node2.props_to_html(), f'href="https://www.google.com" target="_blank"')

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2= LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node3 = LeafNode("b", "Hello, world!")
        self.assertEqual(node3.to_html(), "<b>Hello, world!</b>")
        node3 = LeafNode("h1", "Hello, world!")
        self.assertEqual(node3.to_html(), "<h1>Hello, world!</h1>")

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


if __name__ == "__main__":
    unittest.main()
    