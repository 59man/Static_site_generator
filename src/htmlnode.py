from enum import Enum

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag                     # e.g., "p", "a", "h1", etc.
        self.value = value                 # e.g., inner text
        self.children = children or []     # list of HTMLNode objects
        self.props = props or {}           # e.g., {"href": "https://..."}
    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html()")
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    def __repr__(self):
        return (
            f"HTMLNode(tag={repr(self.tag)}, "
            f"value={repr(self.value)}, "
            f"children={repr(self.children)}, "
            f"props={repr(self.props)})"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to render as HTML.")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag.")
        if children is None:
            raise ValueError("ParentNode must have children.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to render HTML.")
        if self.children is None:
            raise ValueError("ParentNode must have children to render HTML.")
        
        # Recursively render children to HTML strings
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"