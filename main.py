import csv

from decisionTree import DecisionTree
from tree import Node


def main():
    file_name = './data/test.csv'
    attributes, instances = getDataFromFile(file_name)

    createDecisionTree(instances, attributes, 'Joga')

# Retorna a lista de atributos e um dicionário de instâncias do problema
def getDataFromFile(file_name):
    instances = []

    with open(file_name) as csvfile:
        data = csv.reader(csvfile, delimiter=';')

        first_line = True
        attributes = []

        for row in data:
            if first_line:
                attributes = row
                first_line = False
            else:
                instance = {}

                for i in range(len(attributes)):
                    instance[attributes[i]] = row[i]

                instances.append(instance)

    #print(instances)
    return attributes, instances


def getBestAttribute(attributes):
    return attributes[0]


def getMostFrequentClass(instances, target_class):
    class_values = {}

    for instance in instances:
        value = instance[target_class]

        if value in class_values:
            class_values[value] = class_values[value] + 1
        else:
            class_values[value] = 1

    return getItemWithMaxValue(class_values)


def getItemWithMaxValue(items):
    return max(items, key=items.get)



def haveSameClass(instances, class_to_check):
    class_value = instances[0][class_to_check]

    for instance in instances:
        if not instance[class_to_check] == class_value:
            return False

    return True


def getDistinctValuesForAttribute(attribute, instances):
    distinct_values = []
    for instance in instances:
        if instance[attribute] not in distinct_values:
            distinct_values.append(instance[attribute])

    return distinct_values

def getSubsetWithAttributeValue(attribute, value, instances):
    subset = []

    for instance in instances:
        if instance[attribute] == value:
            subset.append(instance)

    return subset


def createDecisionTree(instances, attributes, target_class):
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


if __name__ == '__main__':
    main()
