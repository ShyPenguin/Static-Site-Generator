from htmlnodes.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No Children")
        
        full_text = ""
        for child in self.children:
            full_text += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{full_text}</{self.tag}>"
    
    def __repr__(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No Children")
        
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
