import csv
import random

from node import Node
from tree import Tree

"""
attributes_type = 'n' se os atributos são numéricos
attributes_type = 'c' se os atributos são categóricos

"""

def main():
    file_name = './data/wine.csv'
    target_class = 'class'
    attributes, attributes_types, instances = getDataFromFile(file_name)

    folds = getKStratifiedFolds(instances, 'class', k=10)
    crossValidation(attributes, attributes_types, target_class, folds, bootstrap_size=10, b=5, k=10)


def getBootstrap(data_set, size):
    bootstrap = []

    for i in range(size):
        index = random.randint(0, len(data_set)-1)
        bootstrap.append(data_set[index])

    return bootstrap


def getClassesSubsets(target_class, data):
    distinct_values = []
    for instance in data:
        if instance[target_class] not in distinct_values:
            distinct_values.append(instance[target_class])

    class_subsets = {}
    for value in distinct_values:
        for instance in data:
            if instance[target_class] == value:
                if value not in class_subsets:
                    class_subsets[value] = []
                class_subsets[value].append(instance)

    return class_subsets


def getKStratifiedFolds(data_set, target_class, k):
    instances_by_class = getClassesSubsets(target_class, data_set)
    folds = [None] * k

    # Inicializa a lista de folds
    for i in range(k):
        folds[i] = []

    for class_value in instances_by_class:
        # pega K valores deste subset
        instance_index = 0
        for instance in instances_by_class[class_value]:
            fold_index = instance_index % k
            folds[fold_index].append(instance)
            instance_index = instance_index + 1

    return folds


def transformToList(list_of_lists):
    new_list = []
    for l in list_of_lists:
        for value in l:
            new_list.append(value)

    return new_list


def crossValidation(attributes, attributes_types, target_class, folds, bootstrap_size, b, k):
    for i in range(k):
        training_set_folds = list(folds)
        training_set_folds.remove(folds[i])
        training_set = transformToList(training_set_folds)

        test_set = folds[i]
        forest = []

        for b in range(b):
            bootstrap = getBootstrap(training_set, bootstrap_size)
            tree = Tree(attributes, attributes_types, target_class, bootstrap)
            tree.createDecisionTree()

            forest.append(tree)

        # Usa o ensemble de B arvores para prever as instancias do fold i
        # (fold de teste) e avaliar desempenho do algoritmo (calcular Fmeasure)
        evaluateForest(forest, test_set, target_class)


def evaluateForest(forest, test_set, target_class):
    instances_copy = list(test_set)

    for instance in instances_copy:
        correct_class = instance[target_class]
        instance.pop(target_class)
        predicted_class = forestPredict(forest, instance)
        print('Predição: ' + predicted_class + ' -- Classe correta: ' + correct_class)


def forestPredict(forest, instance):
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
