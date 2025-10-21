import unittest

from converters import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)


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
        blocks = [
                "This is **bolded** paragraph",
                "# h1",
                "## h2",
                "### h3",
                "#### h4",
                "##### h5",
                "###### h6",
                "- This is a list\n- with items",
                "``` This is a code block\n- with multiple lines```",
                "1. This is an ordered list\n2. with items\n3. and more items",
                ">This is a quote\n>spanning\n>multiple lines",
            ]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.UNORDERED_LIST,
                BlockType.CODE,
                BlockType.ORDERED_LIST,
                BlockType.QUOTE,
            ],
        )
