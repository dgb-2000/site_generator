import re
from textnode import TextNode, TextType
from leafnode import LeafNode
from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception(f"Expected text_node to be of type 'TextNode'. Found: {type(text_node)}")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception("text_node does not have a valid text_type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception(f"Invalid markdown syntax: Not every delimiter '{delimiter}' was matched!")
            else:
                for i in range(0, len(parts)):
                    if i % 2 == 0:
                        if len(parts[i]) > 0:
                            new_nodes.append(TextNode(parts[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for match in matches:
            parts = node_text.split(f"![{match[0]}]({match[1]})", 1)
            if len(parts[0]) > 0:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            node_text = parts[1]
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for match in matches:
            parts = node_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(parts[0]) > 0:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            node_text = parts[1]
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    new_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_nodes = []
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            new_nodes.append(block)
    return new_nodes


def block_to_block_type(markdown):
    if markdown.startswith(('# ', '## ', '### ', '#### ', '##### ', '##### ', '###### ')):
        return BlockType.HEADING
    if markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE
    if markdown.startswith('- '):
        ul = True
        for line in markdown.split('\n'):
            if not line.startswith('- '):
                ul = False
        if ul:
            return BlockType.UNORDERED_LIST
    if markdown.startswith('>'):
        quote = True
        for line in markdown.split('\n'):
            if not line.startswith('>'):
                quote = False
        if quote:
            return BlockType.QUOTE
    if markdown.startswith('1. '):
        ol = True
        count = 1
        for line in markdown.split('\n'):
            if not line.startswith(f'{count}. '):
                ol = False
            count += 1
        if ol:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_htmlnode(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            node = ParentNode("p", [])
            parts = []
            for line in block.split("\n"):
                parts.append(line.strip())
            textnodes = text_to_textnodes(" ".join(parts))
            for textnode in textnodes:
                node.children.append(text_node_to_html_node(textnode))
            return node
        case BlockType.UNORDERED_LIST:
            node = ParentNode("ul", [])
            for line in block.split("\n"):
                child = ParentNode("li", [])
                textnodes = text_to_textnodes(line[2:])
                for textnode in textnodes:
                    child.children.append(text_node_to_html_node(textnode))
                node.children.append(child)
            return node
        case BlockType.ORDERED_LIST:
            node = ParentNode("ol", [])
            for line in block.split("\n"):
                child = ParentNode("li", [])
                textnodes = text_to_textnodes(line.split('. ', 1)[1])
                for textnode in textnodes:
                    child.children.append(text_node_to_html_node(textnode))
                node.children.append(child)
            return node
        case BlockType.QUOTE:
            node = ParentNode("blockquote", [])
            for line in block.split("\n"):
                textnodes = text_to_textnodes(line[1:])
                for textnode in textnodes:
                    node.children.append(text_node_to_html_node(textnode))
            return node
        case BlockType.HEADING:
            node = ParentNode(None, [])
            if block.startswith("# "):
                node.tag = "h1"
            if block.startswith("## "):
                node.tag = "h2"
            if block.startswith("### "):
                node.tag = "h3"
            if block.startswith("#### "):
                node.tag = "h4"
            if block.startswith("##### "):
                node.tag = "h5"
            if block.startswith("###### "):
                node.tag = "h6"
            textnodes = text_to_textnodes(block.split(" ", 1)[1])
            for textnode in textnodes:
                node.append(text_node_to_html_node(textnode))
            return node
        case BlockType.CODE:
            node = ParentNode("pre", [])
            child = text_node_to_html_node(TextNode(block[3:-3].lstrip(), TextType.CODE))
            node.children.append(child)
            return node


def markdown_to_html_node(markdown):
    node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node.children.append(block_to_htmlnode(block))
    return node
