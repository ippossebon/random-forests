from tree import Node


class DecisionTree:

    def __init__(self, attributes, instances):
        self.attributes = attributes
        self.instances = instances # lista de dicionários
        self.tree = None
        self.is_tree_initialized = False

    def initializeTree(self, value):
        self.tree = Node(value)
        self.is_tree_initialized = True

    def createTree():
        instances_copy = list(self.instances)
        # Construção top-down - recursivo

        # Quando parar?
        # 1. Todos os exemplos na partição resultante pertencem à mesma classe (nó puro): cria-se uma folha com a classe correspondente
        # 2. Não há mais atributos para escolher ou uma partição resultante é vazia: cria-se uma folha com a classe majoritária dentre as instâncias


        # Escolehr um atributo para adicionar à árvore (iniciando pela raiz)
        attribute_index = 0
        for attribute in self.attributes:
            if not self.is_tree_initialized:
                self.initializeTree(attribute)

            # Estender a árvore, adicionando um ramo para cada valor do atributo selecionado
            for instance in self.instances_copy:
                if instance[attribute_index] in self.tree.children:
                    # Este valor de atributo já tem uma árvore associada
                    pass
                else:
                    # Valor de atributo não tem árvore associada. Cria
                    self.tree.data = instance[attribute_index]
                    self.tree.addChild(instance)

        # Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valores do atributo testado
        # Para cada partição de exemplos resultante, repetir este procedimento recursivamente
