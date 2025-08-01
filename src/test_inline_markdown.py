import unittest
from textnode import TextNode, TextType
from Inline_markdown import extract_markdown_images, extract_markdown_links,split_nodes_image, split_nodes_link,split_nodes_delimiter,markdown_to_blocks     # adjust import path

class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "![one](url1) some text ![two](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_special_chars(self):
        text = "![alt text!@#](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt text!@#", "https://example.com/img.png")], matches)

    def test_extract_markdown_links(self):
        text = "Link to [Google](https://google.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Google", "https://google.com")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "Links: [A](urlA) and [B](urlB)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("A", "urlA"), ("B", "urlB")], matches)

    def test_extract_markdown_links_no_links(self):
        text = "No links here"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignore_images(self):
        text = "Image ![img](url1) and link [link](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "url2")], matches)

    def test_extract_markdown_links_with_special_chars(self):
        text = "Check [my link!@#](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("my link!@#", "https://example.com")], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("No images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_multiple_adjacent(self):
        node = TextNode("![a](url1)![b](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("a", TextType.IMAGE, "url1"),
            TextNode("b", TextType.IMAGE, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_with_non_text_nodes(self):
        nodes = [
            TextNode("Start ![img](url)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_text_before_and_after(self):
        node = TextNode("Hello ![img](url) world", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" world", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_image_at_start(self):
        node = TextNode("![img](url) is here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" is here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_image_at_end(self):
        node = TextNode("Image here ![img](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image here ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(expected, new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_images(self):
        node = TextNode(
            "![img](url) and [link](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("![img](url) and ", TextType.TEXT),  # image syntax left as text here
            TextNode("link", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_multiple_adjacent(self):
        node = TextNode("[A](urlA)[B](urlB)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("A", TextType.LINK, "urlA"),
            TextNode("B", TextType.LINK, "urlB"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_text_before_and_after(self):
        node = TextNode("Start [link](url) end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_link_at_start(self):
        node = TextNode("[link](url) is here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" is here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_link_at_end(self):
        node = TextNode("Here is a [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_with_non_text_nodes(self):
        nodes = [
            TextNode("Start [link](url)", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertListEqual(expected, new_nodes)



class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_bold_delimiter(self):
        node = TextNode("Make this **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Make this ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_italic_delimiter(self):
        node = TextNode("Some _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No delimiters here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("No delimiters here", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("**bold** and **strong**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("strong", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_consecutive_delimiters(self):
        node = TextNode("Empty `` code", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Empty ", TextType.TEXT),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("Here is **bold**", TextType.TEXT),
            TextNode("And `code` here", TextType.TEXT),
        ]
        # First split bold, then code
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("And ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_non_text_node_unchanged(self):
        node = TextNode("bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

class TestMarkdownToBlocks(unittest.TestCase):

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

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n  \n\n \n"), [])

    def test_single_block(self):
        md = "# Just a header"
        self.assertEqual(markdown_to_blocks(md), ["# Just a header"])

    def test_extra_newlines(self):
        md = """

This is a paragraph


Another one

"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is a paragraph",
                "Another one"
            ]
        )

    def test_mixed_content(self):
        md = """# Header

Paragraph text

- List item 1
- List item 2

Another paragraph"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Header",
                "Paragraph text",
                "- List item 1\n- List item 2",
                "Another paragraph"
            ]
        )

if __name__ == "__main__":
    unittest.main()
