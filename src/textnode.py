from logging import raiseExceptions
from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    # cover all the inline text types:
    # text (plain)
    # **Bold text**
    # _Italic text_
    # `Code text`
    # Links, in this format: [anchor text](url)
    # Images, in this format: ![alt text](url)
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text 
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url ==other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        

def textnode_to_htmlnode(textnode):
    if textnode.text_type not in TextType:
        raise Exception("textnode.text_type not in TextType")
    else:
        textnode.text_type
        if textnode.text_type == TextType.TEXT:
            return LeafNode(None, textnode.text)
        if textnode.text_type == TextType.BOLD:
            return LeafNode("b", textnode.text)
        if textnode.text_type == TextType.ITALIC:
            return LeafNode("i", textnode.text)
        if textnode.text_type == TextType.CODE:
            return LeafNode("code", textnode.text)
        if textnode.text_type == TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        if textnode.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            s = old_node.text
            if s.count(delimiter) % 2 == 0:
                list_values = s.split(delimiter)
                for i in range(len(list_values)):
                    if i % 2 != 0:
                        new_nodes.append(TextNode(list_values[i], text_type))
                    else:
                        new_nodes.append(TextNode(list_values[i], TextType.TEXT))
            else:
                raise Exception("invalid Markdown syntax")
    return new_nodes
        # Next adjustments will be to cover cases such as nested text(text-type) such as:
        # - Bolded Italics **_word_**
        # - italicized code _`code`_

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes:list) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if len(old_node.text) <= 0:
            continue
        elif old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            link_match = extract_markdown_links(text)
            if not link_match:
                new_nodes.append(TextNode(text, TextType.TEXT, None))
            else:
                for match in link_match:
                    sections = text.split(f"[{match[0]}]({match[1]})", 1)
                    if len(sections[0]) > 0:     
                        new_nodes.append(TextNode(sections[0], TextType.TEXT, None))
                    new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
                    text = sections[1]
                if len(text) > 0:
                    new_nodes.append(TextNode(text, TextType.TEXT, None))
    return new_nodes

def split_nodes_image(old_nodes:list) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if len(old_node.text) <= 0:
            continue
        elif old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            img_match = extract_markdown_images(text)
            if not img_match:
                new_nodes.append(TextNode(text, TextType.TEXT, None))
            else:
                for match in img_match:
                    sections = text.split(f"![{match[0]}]({match[1]})", 1)
                    if len(sections[0]) > 0:     
                        new_nodes.append(TextNode(sections[0], TextType.TEXT, None))
                    new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
                    text = sections[1]
                if len(text) > 0:
                    new_nodes.append(TextNode(text, TextType.TEXT, None))
    return new_nodes    

def text_to_textnodes(text:str) -> list:
    node = TextNode(text, TextType.TEXT, None)
    sort_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    sort_italic = split_nodes_delimiter(sort_bold, "_", TextType.ITALIC)
    sort_code = split_nodes_delimiter(sort_italic, "`", TextType.CODE)
    sort_image = split_nodes_image(sort_code)
    sort_link = split_nodes_link(sort_image)
    return sort_link



