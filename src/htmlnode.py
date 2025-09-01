

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag, self.value, self.children, self.props = tag, value, children, props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return None
        x = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return x

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value and self.tag != 'img' and self.tag != 'a':
            print(f"LeafNode tag={self.tag}, value={self.value}, props={self.props_to_html()}")
            raise ValueError("Missing content")
        elif not self.tag:
            return self.value
        
        if self.tag == 'a':
            return f'<a href="{self.props['href']}">{self.value}</a>'
        elif self.tag == 'img':
            return f'<img src="{self.props['src']}" alt="{self.props['alt']}">'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children)

    def to_html(self):
        if not self.tag:
            raise ValueError('Missing Tag')
        elif not self.children:
            raise ValueError('Missing Children')
        
        result = f'<{self.tag}>'
        for child in self.children:
            result += child.to_html()
        result += f'</{self.tag}>'
        return result