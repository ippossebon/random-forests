class Node(object):

    def __init__(self, node_value=None, node_top_edge=None):
        self.value = node_value
        self.top_edge = node_top_edge
        self.children = []

    def hasChild(self, c):
        for child in self.children:
            if child.value == c:
                return True

        return False
