import math

class Tree(object):
    def __init__(self, attributes, target_class, instances):
        self.attributes = attributes
        self.target_class = target_class
        self.instances = instances

    def createDecisionTree(self):
        decisionTree(self.instances, self.attributes, self.target_class)

    def getBestAttribute(self, attributes, instances):
        """
        Retorna o atributo com o maior ganho de informação, seguindo o algoritmo ID3.
        """
        # Remove a classificação de cada instância
        attributes.remove(self.target_class)

        original_set_entropy = self.entropy(instances, self.target_class)
        attributes_information_gain = [0 for i in range(len(attributes))]

        for i in range(len(attributes)):
            # Pega todos os valores possíveis para o atributo em questão
            possible_values = self.getDistinctValuesForAttribute(attributes[i], instances)
            avg_entropy = 0

            # Calcula entropia ponderada para cada subset originado a partir do atributo
            for value in possible_values:
                subset = self.getSubsetWithAttributeValue(attributes[i], value, instances)
                entropy = self.entropy(subset, self.target_class)
                weighted_entropy = float(entropy * (len(subset)/len(instances)))
                avg_entropy = avg_entropy + weighted_entropy

            info_gain = original_set_entropy - avg_entropy
            attributes_information_gain[i] = info_gain

        best_attribute_index = attributes_information_gain.index(max(attributes_information_gain))

        return attributes[best_attribute_index]

    def entropy(self, instances, target_class):
        # Medida do grau de aleatoriedade de uma variável, dada em bits
        # Está associada à dificuldade de predizer o atributo alvo a partir
        # do atributo preditivo analisadoself.
        possible_values = self.getDistinctValuesForAttribute(target_class, instances)
        possible_values_count = [0 for i in range(len(possible_values))]

        for i in range(len(possible_values)):
            for j in range(len(instances)):
                if instances[j][target_class] == possible_values[i]:
                    possible_values_count[i] = possible_values_count[i] + 1

        entropy = 0
        for v in possible_values_count:
            percentage_of_values = float(v/len(instances))
            partial_result = float(-1 * percentage_of_values * math.log2(percentage_of_values))
            entropy = float(entropy + partial_result)

        return entropy


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