import unittest

from textnode import *
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", TextType.BOLD, 'https:nickgg3')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("This is a text node", TextType.IMAGE, '../hello/folder')
        html_node = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['src'], '../hello/folder')
        self.assertEqual(html_node.props['alt'], 'This is a text node')

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode('This is text with a ', TextType.TEXT, None), \
                            TextNode('code block', TextType.BOLD, None), \
                            TextNode(' word', TextType.TEXT, None)], new_nodes)

        node2 = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        self.assertListEqual([node2], new_nodes2)

        node3 = TextNode("_This is text with a code block word_", TextType.ITALIC)
        new_nodes3 = split_nodes_delimiter([node3], "_", TextType.ITALIC)
        self.assertListEqual([node3], new_nodes3)

    def test_text_to_textnode(self):
        text=r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, result)

    def test_textnode_to_htmlnode(self):
        text=r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        #print(nodes[7])
        #print(text_node_to_html_node(nodes[7]))
        #self.assertEqual(text_node_to_html_node(nodes[7]), LeafNode('img', "", {'src': 'https://i.imgur.com/fJRm4Vk.jpeg', 'alt': 'obi wan image'}))

if __name__ == "__main__":
    unittest.main()