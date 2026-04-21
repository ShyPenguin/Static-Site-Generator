from enum import Enum

from htmlnodes.htmlnode import HTMLNode
from htmlnodes.leafnode import LeafNode
from htmlnodes.parentnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        node = block_type_to_HTMLNode(type, block)
        nodes.append(node)
    result = ParentNode("div", nodes)
    return result

def block_type_to_HTMLNode(type, text):
    match type:
        case BlockType.PARAGRAPH:
            text = text.replace("\n", " ")
            return determine_type_node(HTMLNode("p", text), type)
        case BlockType.HEADING:
            heading = determine_heading(text)
            text = text.replace(f"{heading[1]} ", "")
            return determine_type_node(HTMLNode(heading[0], text), type)
        case BlockType.CODE:
            text = text.replace("```\n", "")
            text = text.replace("```", "")
            return determine_type_node(HTMLNode("code", text), type)
        case BlockType.QUOTE:
            text = text.replace("\n", " ")
            text = text.replace("> ", "")
            return determine_type_node(HTMLNode("blockquote", text), type)
        case BlockType.UNORDERED_LIST:
            text = text.replace("\n", "")
            return determine_type_node(HTMLNode("ul", text), type)
        case BlockType.ORDERED_LIST:
            text = text.replace("\n", "")
            return determine_type_node(HTMLNode("ol", text), type)

def determine_type_node(node, type): 
    children_nodes = []

    match type:
        case BlockType.CODE:
            child_node = text_node_to_html_node(TextNode(node.value, TextType.CODE))
            children_nodes = [child_node]
        case BlockType.UNORDERED_LIST:
            children_nodes = unordered_items(node.value)
        case BlockType.ORDERED_LIST:
            children_nodes = ordered_items(node.value)
        case _:
            children_nodes = text_to_children(node.value)
    if len(children_nodes) > 0:
        node = parent_block(type, children_nodes, node)
    else:
        node = LeafNode(node.tag, node.value)

    return node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def parent_block(type, nodes, parent_node):
    match type:
        case BlockType.CODE:
            return ParentNode("pre", nodes)
        case _:
            return ParentNode(parent_node.tag, nodes)

def unordered_items(text):
    blocks = text.split("- ")
    children_nodes = []
    for block in blocks:
        if block == "":
            continue
        item_children_nodes = text_to_children(block)
        if len(item_children_nodes) > 0:
            children_nodes.append(ParentNode("li", item_children_nodes))
        else:
            children_nodes.append(LeafNode("li", block))
    return children_nodes

def ordered_items(text):
    blocks = re.split(r"\d\.\s", text)
    children_nodes = []
    for block in blocks:
        if block == "":
            continue
        item_children_nodes = text_to_children(block)
        if len(item_children_nodes) > 0:
            children_nodes.append(ParentNode("li", item_children_nodes))
        else:
            children_nodes.append(LeafNode("li", block))
    return children_nodes

def determine_heading(text):
    count = 0
    for c in text:
        if c != "#":
            break
        count += 1
    return (f"h{count}", "#" * count)       

def extract_title(markdown):
    title = re.findall(r"(\<h1>.*?\</h1>)", markdown)[0]
    title = title.replace("<h1>", "")
    title = title.replace("</h1>", "")
    return title.strip()