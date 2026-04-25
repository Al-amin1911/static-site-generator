from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_to_textnodes, textnode_to_htmlnode

def markdown_to_blocks(markdown) -> list:
    blocks = markdown.strip().split("\n\n")
    format = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        format.append(block)
    return format

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered list"

def block_to_block_type(markdown_block):
    # heading block
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # code block
    if markdown_block.startswith("```\n"):
        lines = markdown_block.split("\n")
        if len(lines) <= 2 or lines[-1] != "```":
            return BlockType.PARAGRAPH
        return BlockType.CODE
    #  quotes block
    if markdown_block.startswith(">"):
        lines = markdown_block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # unordered list block
    if markdown_block.startswith("- "):
        lines = markdown_block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    # ordered list
    if markdown_block.startswith("1. "):
        lines = markdown_block.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "): 
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH  
    pass


def text_to_children(text):
    textnode_list = text_to_textnodes(text)
    htmlnode_list = []
    for text_node in textnode_list:
        html_node = textnode_to_htmlnode(text_node)
        htmlnode_list.append(html_node)
    return htmlnode_list
    pass

def paragraph_to_html_node(markdown_block):
    formatted = " ".join(markdown_block.split("\n"))
    children = text_to_children(formatted)
    return ParentNode("p", children)

def heading_to_html_node(markdown_block):
    level = 0
    for char in markdown_block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 > len(markdown_block):
        raise ValueError(f"Invalid heading level: {level}")
    children = text_to_children(markdown_block[level:].strip())
    return ParentNode(f"h{level}", children)

def quote_to_html_node(markdown_block):
    lines = markdown_block.split("\n")
    new_line = []
    for line in lines:
        text = line.lstrip(">").strip()
        new_line.append(text)
    new_text = " ".join(new_line)
    children = text_to_children(new_text)
    return ParentNode("blockquote", children)

def code_to_html_node(markdown_block):
    lines = markdown_block.split("\n")
    text = "\n".join(lines[1:-1]) + "\n"
    code_node = TextNode(text, TextType.CODE)
    htmlnode = textnode_to_htmlnode(code_node)
    return ParentNode("pre", [htmlnode])

def unordered_list_to_html(markdown_block):
    lines = markdown_block.split("\n")
    parent_list = []
    for line in lines:
        line = line[2:]
        children = text_to_children(line)
        parent = ParentNode("li", children)
        parent_list.append(parent)
    return ParentNode("ul", parent_list)

def ordered_list_to_html(markdown_block):
    lines = markdown_block.split("\n")
    parent_list = []
    for line in lines:
        line = line.split(". ",1)[1]
        children = text_to_children(line)
        parent = ParentNode("li", children)
        parent_list.append(parent)
    return ParentNode("ol", parent_list)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.ULIST:
            node = unordered_list_to_html(block)
        elif block_type == BlockType.OLIST:
            node = ordered_list_to_html(block)
        else:
            raise TypeError(f"{block} not a block type")
        parent_list.append(node)
    return ParentNode("div", parent_list)
    pass