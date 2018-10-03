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


    folds = getKStratifiedFolds(original_data_set, k)
    crossValidation(attributes, attributes_types, target_class, folds, bootstrap_size, b, k)


def getBootstrap(data_set, size):
    validation_set = list(data_set)
    training_set = []

    for i in range(size):
        index = random.randint(0, len(data_set)-1)
        training_set.append(data_set[index])

        # todas as instâncias não selecionadas são usadas como conjunto de teste
        validation_set.remove(data_set[index])

    return training_set, validation_set


def randomForest(trees_count, bootstrap_size, training_data):
    forest = []

    for i in range(trees_count):
        training_set, validation_set = getBootstrap(training_data, bootstrap_size)
        tree = Tree(attributes, 'class', training_set)
        tree.createDecisionTree()
        forest.append(tree)

    return forest

def getClassesSubsets(target_class, data):
    distinct_values = []
    for instance in data:
        if instance[target_class] not in distinct_values:
            distinct_values.append(instance[target_class])


    class_subsets = {}
    for value in distinct_values:
        for instance in data:
            if instance[target_class] == value:
                class_subsets[value].append(instance)

    return class_subsets



def getKStratifiedFolds(original_data_set, target_class, k):
    instances_by_class = getClassesSubsets(target_class, data)
    



def crossValidation(attributes, attributes_types, target_class, folds, bootstrap_size, b, k):
    for i in range(k):
        training_set = list(folds)
        training_set.remove(folds[i])

        test_test = folds[i]
        forest = []

        for b in range(b):
            bootstrap = getBootstrap(training_set, bootstrap_size)
            tree = Tree(attributes, attributes_types, target_class, bootstrap)
            tree.createDecisionTree()

            forest.append(tree)

        # Usa o ensemble de B arvores para prever as instancias do fold i
        # (fold de teste) e avaliar desempenho do algoritmo (calcular Fmeasure)
        evaluateForest(forest, test_test)


def evaluateForest(forest, test_test, target_class):
    instances_copy = list(test_test)

    for instance in instances_copy:
        correct_class = test_test[target_class]
        test_test.pop(target_class)
        predicted_class = forestPredict(forest, instance)
        print('Predição: ' + predicted_class + ' -- Classe correta: ' + correct_class)


def forestPredict(instance, forest):
    predictions = []

    for tree in forest:
        predictions.append(tree.classify(instance))

    most_frequent_class = max(set(predictions), key=predictions.count)
    return most_frequent_class


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
