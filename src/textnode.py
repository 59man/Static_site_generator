from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"  # for plain text and other block-level content

class TextNode:
        def __init__(self, text: str, text_type: TextType, url: str = None):
            self.text = text
            self.text_type = text_type
            self.url = url

        def __eq__(self, other):
            if not isinstance(other, TextNode):
                return False
            return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
            )

        def __repr__(self):
            return f"TextNode({self.text}, {self.text_type}, {self.url})"



def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node, TextNode):
        raise TypeError("Input must be a TextNode instance.")
    
    ttype = text_node.text_type
    text = text_node.text
    url = text_node.url

    if ttype == TextType.TEXT:
        # raw text, no tag
        return LeafNode(tag=None, value=text)

    elif ttype == TextType.BOLD:
        return LeafNode(tag="b", value=text)

    elif ttype == TextType.ITALIC:
        return LeafNode(tag="i", value=text)

    elif ttype == TextType.CODE:
        return LeafNode(tag="code", value=text)

    elif ttype == TextType.LINK:
        if not url:
            raise ValueError("Link TextNode must have a URL.")
        return LeafNode(tag="a", value=text, props={"href": url})

    elif ttype == TextType.IMAGE:
        if not url:
            raise ValueError("Image TextNode must have a URL for 'src'.")
        # alt text is the text content
        return LeafNode(tag="img", value="", props={"src": url, "alt": text or ""})

    else:
        raise ValueError(f"Unsupported TextType: {ttype}")