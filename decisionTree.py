from tree import Node


class DecisionTree:

    def __init__(self, attributes, instances):
        self.attributes = attributes
        self.instances = instances # lista de dicionários
        self.tree = None
        self.is_tree_initialized = False

    def initializeTree(self, root):
        self.tree = Node(root)
        self.is_tree_initialized = True

    def newDictWithoutKey(self, d, key):
        r = dict(d)
        del r[key]
        return r

    def splitTree(self, attribute, instances):
        for instance in instances:
            if self.tree.hasChild(instance[attribute]):
                # Adiciona instancia com o valor deste atributo
                for index in range(len(self.tree.children)):
                    if attribute in instance:
                        if self.tree.children[index].value == instance[attribute]:
                            new_instance = self.newDictWithoutKey(instance, attribute)
                            self.tree.children[index].children.append(new_instance)
            else:
                # Cria novo nodo com o valor do atributo dessa instância
                new_node = Node(instance[attribute])
                new_instance = self.newDictWithoutKey(instance, attribute)
                new_node.children.append(new_instance)
                self.tree.children.append(new_node)

        return instances

    def createTree(self):
        instances_copy = list(self.instances)
        # Construção top-down - recursivo

        # Quando parar?
        # 1. Todos os exemplos na partição resultante pertencem à mesma classe (nó puro): cria-se uma folha com a classe correspondente
        # 2. Não há mais atributos para escolher ou uma partição resultante é vazia: cria-se uma folha com a classe majoritária dentre as instâncias


        # Escolher um atributo para adicionar à árvore (iniciando pela raiz)
        for attribute in self.attributes:
            if not self.is_tree_initialized:
                self.initializeTree(attribute)

            instances_copy = self.splitTree(attribute, instances_copy)
        self.tree.printTree()

        # Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valores do atributo testado
        # Para cada partição de exemplos resultante, repetir este procedimento recursivamente
