import unittest
import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class HTMLNodeTest(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode("p", "text in paragraph",[],{"href": "https://www.google.com", "target": "_blank",})
        node_joined = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node_joined, node.props_to_html())
    
    def test_to_html(self):
        node = HTMLNode("p", "text in paragraph",[],{"href": "https://www.google.com", "target": "_blank",})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_prop_to_html_empty(self):
        node = HTMLNode("p", "text in paragraph",[])
        self.assertEqual("", node.props_to_html())   

class LeafNodeTest(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_no_tag(self):
        node = LeafNode(None,"Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    def test_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click me!</a>')
    def test_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), 'LeafNode(p, Hello, world!, None)')

class ParentNodeTest(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span>child</span></div>')
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><b>grandchild</b></span></div>')
    def test_child_props(self):
        child_node = LeafNode("span", "child", {"href": "https://boot.dev"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span href="https://boot.dev">child</span></div>')
    def test_parent_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"href": "https://boot.dev"})
        self.assertEqual(parent_node.to_html(), '<div href="https://boot.dev"><span>child</span></div>')
    def test_no_tag(self):
        parentnode = ParentNode("",[LeafNode("b", "Bold text"),])
        with self.assertRaises(ValueError):
            parentnode.to_html()
    def test_no_child(self):
        parentnode = ParentNode("p",None)
        with self.assertRaises(ValueError):
            parentnode.to_html()

if __name__ == "__main__":
    unittest.main()