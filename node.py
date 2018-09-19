class Node(object):

    def __init__(self, node_value=None):
        self.value = node_value
        self.children = []

    def createChild(self, node_value):
        node = Node(node_value)
        self.children.append(node)
        return node

    def hasChild(self, c):
        for child in self.children:
            if child.value == c:
                return True

        return False

    def printValueAndChildren(self):
        print(self.value)

        for i in range(len(self.children)):
            print(self.children[i].value, end=" ")
