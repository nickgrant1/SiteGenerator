import re
from textnode import TextNode, TextType
def extract_markdown_images(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return extract_markdown_images(text)

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        parts = re.split(r"(\[.*?\])(\(.*?\))", node.text)
        text, url = "", ""
        for val in parts:
            if val == "":
                continue
            if val[0] == '[' and val[-1] == ']':
                text = val[1:-1]
            elif val[0] == '(' and val[-1] == ')':
                url = val[1:-1]
                result.append(TextNode(text, TextType.LINK, url))
            else:
                result.append(TextNode(val, TextType.TEXT))
    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        parts = re.split(r"(!\[.*?\])(\(.*?\))", node.text)
        text, url = "", ""
        for val in parts:
            if val == "":
                continue
            if val[0] == '!':
                text = val[2:-1]
            elif val[0] == '(' and val[-1] == ')':
                url = val[1:-1]
                result.append(TextNode(text, TextType.IMAGE, url))
            else:
                result.append(TextNode(val, TextType.TEXT))
    return result
        


