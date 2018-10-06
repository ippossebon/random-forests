import math
import random

from node import Node

class Tree(object):
    def __init__(self, attributes, attributes_types, target_class, instances):
        self.attributes_types = attributes_types
        self.attributes = attributes
        self.target_class = target_class
        self.instances = instances
        self.decision_tree = None
        self.predicted_class = None

    def createDecisionTree(self):
        if self.target_class in self.attributes:
            self.attributes.remove(self.target_class)

        self.decision_tree = self.decisionTree(self.instances, self.attributes, self.target_class)

    def getBestAttribute(self, attributes, instances):
        """
        Retorna o atributo com o maior ganho de informação, seguindo o algoritmo ID3.
        """

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
        # do atributo preditivo analisado.
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

        return self.getItemWithMaxValue(class_values)


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

    def getRandomAttributes(self, attributes, m=None):
        """
        Retorna m atributos aleatórios da lista de atributos
        valor default de m = sqrt(len(attributes))
        """
        random_attributes = []
        random_attributes_count = m or int(math.sqrt(len(attributes)))

        for x in range(random_attributes_count):
            index = random.randint(0, len(attributes)-1)
            random_attributes.append(attributes[index])

        return random_attributes

    def decisionTree(self, instances, attributes, target_class, top_edge=None):
        """
        Função recursiva que cria uma árvore de decisão com base no conjunto
        'instances'
        """
        node = Node()
        node.top_edge = top_edge

        # if len(instances) == 0:
        #     import ipdb; ipdb.set_trace()
        #     print('a')

        if self.haveSameClass(instances, target_class):
            # Se todos os exemplos do conjunto possuem a mesma classificação,
            # retorna node como um nó folha rotulado com a classe

            # Pega a classe da primeira instância. Tanto faz, pois todos têm a mesma classe.
            node.value = instances[0][target_class]
            return node

        if len(attributes) == 0:
            # Se L é vazia, retorna node como um nó folha com a classe mais
            # frequente no conjunto de instancias
            value = self.getMostFrequentClass(instances, target_class)
            node.value = value
            return node
        else:
            # Seleciona m atributos aleatórios e escolhe o melhor
            # ! IMPORTANTE: para demonstrar que o algoritmo de indução de árvores funciona,
            # deve selecionar entre TODOS os atributos, e não apenas entre aleatórios

            random_attributes = self.getRandomAttributes(attributes)
            attribute = self.getBestAttribute(random_attributes, instances)
            # attribute = self.getBestAttribute(attributes, instances)
            node.value = attribute

            attributes.remove(attribute)

            # considerando attributes como um dict
            if self.attributes_types[attribute] == 'n':
                # atributo numerico
                values_sum = 0
                for instance in instances:
                    values_sum = values_sum + float(instance[attribute])

                avg_value = values_sum / len(instances)
                subset_A, subset_B = self.getSubsetsForNumericAttribute(attribute, avg_value, instances)

                subset_A_attribute_value = '<= ' + str(avg_value)
                subset_B_attribute_value = '> ' + str(avg_value)

                node.children.append(self.decisionTree(subset_A, attributes, target_class, subset_A_attribute_value))
                node.children.append(self.decisionTree(subset_B, attributes, target_class, subset_B_attribute_value))
            else:
                # Para cada valor V distinto do atributo em questão, considerando os exemplos da lista de instancias:
                distinct_attribute_values = self.getDistinctValuesForAttribute(attribute, instances)

                for attribute_value in distinct_attribute_values:
                    subset = self.getSubsetWithAttributeValue(attribute, attribute_value, instances)

                    if len(subset) == 0:
                        # Se esse subset for vazio, retorna node como nó folha rotulado
                        # com a classe mais frequente no conjunto
                        node.value = self.getMostFrequentClass(instances, target_class)
                        return node
                    else:
                        node.children.append(self.decisionTree(subset, attributes, target_class, attribute_value))
        return node

    def getSubsetsForNumericAttribute(self, attribute, split_value, instances):
        subset_A = []
        subset_B = []

        for instance in instances:
            if float(instance[attribute]) <= split_value:
                subset_A.append(instance)
            else:
                subset_B.append(instance)

        return subset_A, subset_B

    def printDecisionTree(self):
        self.printTree(self.decision_tree)


    def printTree(self, tree, level=0):
        if tree.top_edge:
            print('    ' * (level - 1) + '+---' * (level > 0) + '[' + tree.top_edge + ']' + tree.value)
        else:
            print('    ' * (level - 1) + '+---' * (level > 0) + tree.value)


        for i in range(len(tree.children)):
            if type(tree.children[i]) is Node:
                self.printTree(tree.children[i], level + 1)
            else:
                print('    ' * level + '+---' + tree.children[i].value)


    def classify(self, instance):
        return self.predict(self.decision_tree, instance)


    def predict(self, tree, instance):
        if len(tree.children) > 0:
            for i in range(len(tree.children)):
                attribute = tree.value
                attribute_value = tree.children[i].top_edge

                if self.attributes_types[attribute] == 'n':
                    # atributo numerico
                    operator, num = attribute_value.split(' ')

                    if operator == '<=':
                        if instance[attribute] <= num:
                            return self.predict(tree.children[0], instance)

                    else:
                        if instance[attribute] > num:
                            return self.predict(tree.children[1], instance)
                else:
                    # atributo categórico
                    if instance[attribute] == attribute_value:
                        return self.predict(tree.children[i], instance)
        else:
            return tree.value
