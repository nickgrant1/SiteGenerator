from enum import Enum
import re
from htmlnode import *
from textnode import *
class BlockType(Enum):
    PARAGRAPH = 'p'
    HEADING = 'h{}'
    CODE = 'code'
    QUOTE = 'blockquote'
    UL = 'ul'
    OL = 'ol'

def markdown_to_blocks(md):
    blocks = md.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    linesplit = block.splitlines()
    if bool(re.match(r"#{1,6} .*?", block)):
        return BlockType.HEADING
    elif block[:3] == '```' and block[-3:] == '```':
        return BlockType.CODE
    elif all(line.startswith('>') for line in linesplit):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in linesplit):
        return BlockType.UL
    elif all(line.startswith(f'{i+1}. ') for i, line in enumerate(linesplit)):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH  

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children=[]
    for block in blocks:
        code_block = block
        block = re.sub(r"\s+", " ", block)
        block_type = block_to_block_type(block)
        block_node = HTMLNode(block_type.value)
        if block_type == BlockType.HEADING:
            headingLevel = len(re.match(r"#{1,6}", block)[0])
            block_node.tag = BlockType.HEADING.value.format(headingLevel)
            block_node.value = block[headingLevel+1:]
        elif block_type == BlockType.PARAGRAPH:
            block_node.value = block
        elif block_type == BlockType.CODE:
            code_text = code_block[3:-3].lstrip()
            code_node = LeafNode('code', code_text)
            block_node = ParentNode('pre', [code_node])
        elif block_type == BlockType.QUOTE:
            lines = [line.lstrip('>') for line in block.splitlines()]
            block_node.value = "\n".join(lines)
        elif block_type == BlockType.UL:
            lines = [line.lstrip('- ') for line in block.splitlines()]
            lines = [f'<li>{line}</li>' for line in lines]
            block_node.value = "\n".join(lines)
        elif block_type == BlockType.OL:
            lines = [re.sub(r"^\d+\. ", "", line) for line in block.splitlines()]
            lines = [f'<li>{line}</li>' for line in lines]
            block_node.value = '\n'.join(lines)
        else:
            raise ValueError("block_type isn't a BlockType")
        if block_type != BlockType.CODE:
            children_nodes = text_to_children(block_node.value)
            if not children_nodes:
                children_nodes = [LeafNode(None, block_node.value)]
            block_node = ParentNode(block_type.value, children_nodes)
        children.append(block_node)

    return ParentNode('div', children)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes