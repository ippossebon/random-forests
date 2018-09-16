
class Tree(object):
    def __init__(self, attributes, target_class, instances):
        self.attributes = attributes
        self.target_class = target_class
        self.instances = instances

    def createDecisionTree(self):
        decisionTree(self.instances, self.attributes, self.target_class)

    def getBestAttribute(self, attributes):
        #TODO usar gini index
        return attributes[0]

    def getMostFrequentClass(self, instances, target_class):
    """
    Retorna a classificação mais frequente para target_class entre as
    instances
    """
        class_values = {}

        for instance in instances:
            value = instance[target_class]

            if value in class_values:
                class_values[value] = class_values[value] + 1
            else:
                class_values[value] = 1

        return getItemWithMaxValue(class_values)


    def getItemWithMaxValue(self, items):
    """
    Retorna a chave do dicionário que possui o maior valor associado.
    Exemplo: {'a': 1, 'b': 2, 'c': 3} -> Retorna 'c'
    """
        return max(items, key=items.get)


    def haveSameClass(self, instances, class_to_check):
    """
    Retorna True se todos os elementos de instance têm a mesma classificação para
    class_to_check. False, caso contrário
    """
        class_value = instances[0][class_to_check]

        for instance in instances:
            if not instance[class_to_check] == class_value:
                return False

        return True


    def getDistinctValuesForAttribute(self, attribute, instances):
    """
    Retorna todos os valores distintos para um determinado atributo que estão
    presentes em instances
    """
        distinct_values = []
        for instance in instances:
            if instance[attribute] not in distinct_values:
                distinct_values.append(instance[attribute])

        return distinct_values

    def getSubsetWithAttributeValue(self, attribute, value, instances):
    """
    Retorna subconjunto com todas as intâncias que possuem o mesmo valor 'value'
    para o atributo 'attribute'
    """
        subset = []

        for instance in instances:
            if instance[attribute] == value:
                subset.append(instance)

        return subset

    def decisionTree(self, instances, attributes, target_class):
    """
    Função recursiva que cria uma árvore de decisão com base no conjunto
    'instances'
    """
        new_node = Node()

        if haveSameClass(instances, target_class):
            # Se todos os exemplos do conjunto possuem a mesma classificação,
            # retorna new_node como um nó folha rotulado com a classe
            new_node.value = instances[target_class]
            return new_node

        if len(attributes) == 0:
            # Se L é vazia, retorna new_node como um nó folha com a classe mais
            # frequente no conjunto de instancias
            value = getMostFrequentClass(instances, target_class)
            new_node.value = value
            return new_node
        else:
            # Seleciona atributo preditivo da lista de atributos que apresenta melhor critério de divisão
            attribute = getBestAttribute(attributes)
            new_node.value = attribute

            attributes.remove(attribute)

            # Para cada valor V distinto do atributo em questão, considerando os exemplos da lista de instancias:
            distinct_attribute_values = getDistinctValuesForAttribute(attribute, instances)

            for attribute_value in distinct_attribute_values:
                subset = getSubsetWithAttributeValue(attribute, attribute_value, instances)

                if len(subset) == 0:
                # Se esse subset for vazio, retorna new_node como nó folha rotulado
                # com a classe mais frequente no conjunto
                    pass
                else:
                    new_node.children = createDecisionTree(subset, attributes, target_class)
