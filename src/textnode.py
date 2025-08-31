from enum import Enum
import re
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text=text
        self.text_type=text_type
        self.url=url

    def __eq__(self, textNode: "TextNode") -> bool:
        if self.text == textNode.text and \
            self.text_type == textNode.text_type and \
            self.url == textNode.url:
            return True
        return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result=[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            result.append(node)
            continue

        lst = re.split(rf"({re.escape(delimiter)}.*?{re.escape(delimiter)})", node.text)
        text=""
        for val in lst:
            if val == "":
                continue
            if val.startswith(delimiter):
                if delimiter == '**':
                    text = val[2:-2]
                else:
                    text = val[1:-1]
                result.append(TextNode(text, text_type))
            else:
                result.append(TextNode(val, TextType.TEXT))            
    return result     

def text_to_textnodes(text):
    from extract import split_nodes_image, split_nodes_link
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    