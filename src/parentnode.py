from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError

        if not self.children:
            raise ValueError("parent does not have children")

        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            output += child.to_html()
        output = output + f"</{self.tag}>"
        return output
