import unittest
from src.textnode import TextType, TextNode, textnode_to_htmlnode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

class TestTextNode(unittest.TestCase):
    # Test: TextNode(Class)
    def test_eq(self):
        node1 = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node1, node2)
    def test_not_eq(self):
        node1 = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    def test_url_is_None(self):
        node = TextNode("This is a test node", TextType.BOLD)
        self.assertIsNone(node.url)
    def test_is_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "www.google.com")
        self.assertIsNotNone(node.url)
    def test_valid_text_type(self):
        node = TextNode("This is a test node", TextType.BOLD)
        self.assertTrue(node.text_type in TextType)
    def test_invalid_text_type(self):
        with self.assertRaises(AttributeError):
            TextType.Curve
    # Test: textnode_to_htmlnode
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        htmlnode = textnode_to_htmlnode(node)
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, "This is a text node")
        self.assertEqual(htmlnode.to_html(), "This is a text node")
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        htmlnode = textnode_to_htmlnode(node)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, "This is a text node")
        self.assertEqual(htmlnode.to_html(), "<b>This is a text node</b>")
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        htmlnode = textnode_to_htmlnode(node)
        self.assertEqual(htmlnode.tag, "i")
        self.assertEqual(htmlnode.value, "This is a text node")
        self.assertEqual(htmlnode.to_html(), "<i>This is a text node</i>")
    def test_coded(self):
        node = TextNode("This is a text node", TextType.CODE)
        htmlnode = textnode_to_htmlnode(node)
        self.assertEqual(htmlnode.tag, "code")
        self.assertEqual(htmlnode.value, "This is a text node")
        self.assertEqual(htmlnode.to_html(), "<code>This is a text node</code>")
    def test_link(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
        htmlnode = textnode_to_htmlnode(node)
        self.assertEqual(htmlnode.tag, "a")
        self.assertEqual(htmlnode.value, "This is some anchor text")
        self.assertEqual(htmlnode.props, {"href": "https://boot.dev"})
        self.assertEqual(htmlnode.to_html(), '<a href="https://boot.dev">This is some anchor text</a>')
    def test_image(self):
        node = TextNode("This is some anchor text", TextType.IMAGE, "url/of/image.jpg")
        htmlnode = textnode_to_htmlnode(node)
        self.assertEqual(htmlnode.tag, "img")
        self.assertEqual(htmlnode.props, {"src": "url/of/image.jpg", "alt": "This is some anchor text"})
        self.assertEqual(htmlnode.to_html(), '<img src="url/of/image.jpg" alt="This is some anchor text"></img>')
    # Test: split_nodes_delimiter
    def test_delimiter_split(self):
        node = TextNode("This is text with a `code` block word", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_node, [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code", TextType.CODE, None), TextNode(" block word", TextType.TEXT, None)])
    def test_multiple_delimiter(self):
        node = TextNode("This is text with a `code` **block** word", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        newer_node = newer_node = split_nodes_delimiter(new_node, "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code", TextType.CODE, None), TextNode(" **block** word", TextType.TEXT, None)])
        self.assertEqual(newer_node, [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code", TextType.CODE, None), TextNode(" ", TextType.TEXT, None), TextNode("block", TextType.BOLD, None), TextNode(" word", TextType.TEXT, None)])
    def test_missing_delimeter_pair(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_node = split_nodes_delimiter([node], "`", TextType.TEXT)
    # Test: markdown link, image match
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        text = "This is text with an [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://boot.dev")], matches)
    def test_multiple_matches(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        matches_img = extract_markdown_images(text)
        matches_link = extract_markdown_links(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches_img)
        self.assertListEqual([("link", "https://boot.dev")], matches_link)
    def test_no_match_images_and_link(self):
        text = "This is a statement with no image or link markdowns"
        matches_img = extract_markdown_images(text)
        matches_link = extract_markdown_links(text)
        self.assertListEqual([], matches_img)
        self.assertListEqual([], matches_link)
    # Test split image, link
    def test_split_link_trailing(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev)",
        TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes)
    def test_split_link_leading(self):
        node = TextNode(
        "[to boot dev](https://www.boot.dev) is a text with a link",
        TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" is a text with a link" , TextType.TEXT, None)], new_nodes)
    def test_split_image(self):
        node = TextNode(
        "This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an image ", TextType.TEXT, None), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)
        pass
    def test_no_image_or_link(self):
        node = TextNode(
        "This is a text with no image or link",
        TextType.TEXT,)
        image_node = split_nodes_image([node])
        link_node = split_nodes_link([node])
        self.assertEqual([TextNode("This is a text with no image or link", TextType.TEXT, None)], image_node)
        self.assertEqual([TextNode("This is a text with no image or link", TextType.TEXT, None)], link_node)
        pass
    def test_no_text(self):
        node1 = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        image_node = split_nodes_image([node1])
        link_node = split_nodes_link([node2])
        self.assertEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], image_node)
        self.assertEqual([TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], link_node)
        pass
    # test text_to_textnode
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_node = text_to_textnodes(text)
        self.assertListEqual([TextNode("This is ", TextType.TEXT, None), TextNode("text", TextType.BOLD, None), TextNode(" with an ", TextType.TEXT, None),
        TextNode("italic", TextType.ITALIC, None), TextNode(" word and a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None),
        TextNode(" and an ", TextType.TEXT, None), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT, None),
        TextNode("link", TextType.LINK, "https://boot.dev")], text_node)
        pass
     
if __name__ == "__main__":
    unittest.main()