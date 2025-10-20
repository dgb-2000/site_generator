import re
from textnode import TextNode, TextType
from leafnode import LeafNode


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
