import csv
import random

from node import Node
from tree import Tree

"""
attributes_type = 'num' se os atributos são numéricos
attributes_type = 'cat' se os atributos são categóricos

"""

def main():
    file_name = './data/wine.csv'
    attributes, attributes_types, instances = getDataFromFile(file_name)

    tree = Tree(attributes, attributes_types, 'class', instances)
    tree.createDecisionTree()
    # tree.printDecisionTree()

    instances_copy = list(instances)

    for instance in instances_copy:
        correct_class = instance['class']
        instance.pop('class')
        predicted_class = tree.classify(instance)
        print('Predição: ' + predicted_class + ' -- Classe correta: ' + correct_class)


def getBootstrap(original_data_set, size):
    validation_set = list(original_data_set)
    training_set = []

    for i in range(size):
        index = random.randint(0, len(original_data_set)-1)
        training_set.append(original_data_set[index])

        # todas as instâncias não selecionadas são usadas como conjunto de teste
        validation_set.remove(original_data_set[index])

    return training_set, validation_set


def randomForest(trees_count, bootstrap_size, training_data):
    forest = []

    for i in range(trees_count):
        training_set, validation_set = getBootstrap(training_data, bootstrap_size)
        tree = Tree(attributes, 'class', training_set)
        tree.createDecisionTree()
        forest.append(tree)

    return forest


def stratifiedCrossValidation(original_data_set):
    pass


def majorityVoting(instance, forest):
    # retorna a classe predita pela maioria das árvores
    predictions = {}

    for i in range(len(forest)):
        predicted_class = forest[i].classify(instance)

        if predicted_class not in predictions.keys():
            predictions[predicted_class] = 1
        else:
            predictions[predicted_class] = predictions[predicted_class] + 1

    return max(predictions, key=predictions.get)


# Retorna a lista de atributos e um dicionário de instâncias do problema
def getDataFromFile(file_name):
    instances = []

    with open(file_name) as csvfile:
        data = csv.reader(csvfile, delimiter=';')

        line_count = 0
        attributes = []

        for row in data:
            if line_count == 0:
                types = row
            elif line_count == 1:
                attributes = row
            else:
                instance = {}
                for i in range(len(attributes)):
                    instance[attributes[i]] = row[i]

                instances.append(instance)
            line_count = line_count + 1

    # Gera o dicionario com o tipo de cada atributo
    attributes_types = {}
    for i in range(len(attributes)):
        attributes_types[attributes[i]] = types[i]

    return attributes, attributes_types, instances


if __name__ == '__main__':
    main()
