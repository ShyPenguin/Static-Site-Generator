import unittest

from htmlnodes.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        mockdata = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, mockdata)
        props = node.props_to_html()
        self.assertEqual(props, ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_class(self):
        mockdata = {
            "href": "https://www.google.com",
            "target": "_blank",
            "class": "container"
        }
        node = HTMLNode(None, None, None, mockdata)
        props = node.props_to_html()
        self.assertEqual(props, ' href="https://www.google.com" target="_blank" class="container"')

    def test_props_to_html_data(self):
        mockdata = {
            "href": "https://www.google.com",
            "target": "_blank",
            "class": "container",
            "data-modified": "True"
        }
        node = HTMLNode(None, None, None, mockdata)
        props = node.props_to_html()
        self.assertEqual(props, ' href="https://www.google.com" target="_blank" class="container" data-modified="True"')

if __name__ == "__main__":
    unittest.main()