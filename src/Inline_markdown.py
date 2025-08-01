from textnode import TextNode, TextType
from htmlnode import HTMLNode,LeafNode,ParentNode
import re


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        # Only split nodes of type TEXT
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        
        # If no delimiter found, just keep the node as is
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        
        # We alternate parts: even indices = TEXT, odd indices = delimiter wrapped nodes
        for i, part in enumerate(parts):
            if part == "":
                # Skip empty parts (e.g., consecutive delimiters)
                continue
            
            if i % 2 == 0:
                # Even index = plain text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index = wrapped with the given text_type
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes




def extract_markdown_images(text):
    """
    Extracts markdown images of the form ![alt text](url)
    Returns a list of tuples: (alt_text, url)
    """
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    """
    Extracts markdown links of the form [anchor text](url)
    Returns a list of tuples: (anchor_text, url)
    """
    # We want to exclude image markdown (which starts with !), so negative lookbehind for '!'
    pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        matches = list(pattern.finditer(text))

        if not matches:
            # No matches: just append original node once
            new_nodes.append(node)
            continue

        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()

            if start > last_index:
                before_text = text[last_index:start]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = end

        if last_index < len(text):
            after_text = text[last_index:]
            if after_text:
                new_nodes.append(TextNode(after_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)')
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        matches = list(pattern.finditer(text))

        if not matches:
            new_nodes.append(node)
            continue  # skip leftover text logic since no matches

        for match in matches:
            start, end = match.span()
            anchor_text, url = match.groups()

            if start > last_index:
                before_text = text[last_index:start]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            last_index = end

        # Only execute this if matches were found
        if last_index < len(text):
            after_text = text[last_index:]
            if after_text:
                new_nodes.append(TextNode(after_text, TextType.TEXT))

    return new_nodes


def markdown_to_blocks(markdown):
    # Step 1: Split by double newlines
    raw_blocks = markdown.split("\n\n")
    
    # Step 2: Strip each block and remove empty ones
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    
    return blocks
