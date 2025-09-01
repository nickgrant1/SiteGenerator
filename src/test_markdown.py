import unittest

from blocks import *
from main import extract_title

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            )

    def test_block_to_block_type(self):
        block = '### heading today'
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = '```this is some code```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = '>this is\n>a quote of\n>the day'
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = '- this is\n- an unordered\n- list\n- for your\n- information'
        self.assertEqual(block_to_block_type(block), BlockType.UL)

        block = '1. this is\n2. a quote of\n3. the day\n4. lolol'
        self.assertEqual(block_to_block_type(block), BlockType.OL)

        block = 'This is a regular **bolded** paragraph'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        md = """
This is **bolded** paragraph

```This is a code paragraph with _italic_ text and link here: [src](url)
This is the same paragraph on a new line```

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.CODE)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UL)
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        block = markdown_to_blocks(md)
        block = block_to_block_type(block[0])
        self.assertEqual(block, BlockType.CODE)

    '''def test_markdown_to_html_node(self):
        md = """
This is **bolded** paragraph

```This is a code paragraph with _italic_ text and link here: [src](url)
This is the same paragraph on a new line```

- This is a list
- with items
"""
        print(repr(markdown_to_html_node(md)))'''



    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        title = extract_title('# This is the heading\nnew line')
        self.assertEqual(title, 'This is the heading')
        
        with self.assertRaises(Exception):
            extract_title('## This is not the heading\nnew line')


if __name__ == "__main__":
    unittest.main()
    