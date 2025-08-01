import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_single(self):
        node = HTMLNode(
            tag="img",
            props={"alt": "An image"}
        )
        expected = ' alt="An image"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Hello world")
        expected = ''
        self.assertEqual(node.props_to_html(), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3"),
        ]
        parent_node = ParentNode("ul", children)
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        )

    def test_to_html_no_children_error(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", None)
        self.assertEqual(str(cm.exception), "ParentNode must have children.")

    def test_init_no_tag_error(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [])
        self.assertEqual(str(cm.exception), "ParentNode must have a tag.")

    def test_to_html_no_tag_error(self):
        parent_node = ParentNode("div", [LeafNode("p", "text")])
        parent_node.tag = None  # manually remove tag to test error in to_html
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have a tag to render HTML.")

    def test_nested_parentnodes(self):
        # Nest three levels deep
        leaf = LeafNode("em", "deep")
        child = ParentNode("span", [leaf])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><em>deep</em></span></div>"
        )

    def test_props_in_parentnode(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode("section", [child], props={"class": "my-section"})
        self.assertEqual(
            parent.to_html(),
            '<section class="my-section"><p>Hello</p></section>'
        )

    
if __name__ == "__main__":
    unittest.main()
