import csv
import random
import math
import statistics
import jsonpickle

# import matplotlib.pyplot as plt
# import numpy as np

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

    tree = Tree(attributes, attributes_types, target_class, instances)
    tree.createDecisionTree()

    results_accuracy = []
    results_precision = []
    results_recall = []
    results_f1measure = []

    k = 10

    for n_trees in range(1,51):
        accuracy = []
        precision = []
        recall = []
        f1 = []

        folds = getKStratifiedFolds(instances, target_class, k=k)
        results = crossValidation(attributes,
                            attributes_types,
                            target_class,
                            folds,
                            b=n_trees,
                            k=k)
        print(results)

        results_accuracy.append(results[0])
        results_precision.append(results[1])
        results_recall.append(results[2])
        results_f1measure.append(results[3])

    # plt.xticks(np.arange(min(range(10, 51)), max(range(10, 51))+1, 5.0))
    # plt.plot(range(10,51), results_accuracy, label = "Accuracy")
    # plt.plot(range(10,51), results_precision, label = "Precision")
    # plt.plot(range(10,51), results_recall, label = "Recall")
    # plt.plot(range(10,51), results_f1measure, label = "F1-Measure")
    # plt.ylabel('Values')
    # plt.xlabel('Number of trees')
    # plt.title('Results for' + file_name)
    # plt.legend()
    # plt.show()

def getBootstrap(data_set, size):
    bootstrap = []

    for i in range(size):
        index = random.randint(0, len(data_set)-1)
        bootstrap.append(data_set[index])

    return bootstrap

def getClassDistinctValues(target_class, data):
    distinct_values = []
    for instance in data:
        if instance[target_class] not in distinct_values:
            distinct_values.append(instance[target_class])
    return distinct_values


def getClassesSubsets(target_class, data):
    distinct_values = getClassDistinctValues(target_class, data)

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


def crossValidation(attributes, attributes_types, target_class, folds, b, k):
    accuracy_values = []
    precision_values = []
    recall_values = []
    fmeasure_values = []


    for i in range(k):
        training_set_folds = list(folds)
        training_set_folds.remove(folds[i])
        training_set = transformToList(training_set_folds)

        # bootstrap tem o tamanho de um fold
        bootstrap_size = len(training_set)

        # test_set = folds[i]
        test_set = list(training_set)
        forest = []

        for j in range(b):
            bootstrap = getBootstrap(training_set, bootstrap_size)
            tree = Tree(attributes, attributes_types, target_class, bootstrap)
            tree.createDecisionTree()

            forest.append(tree)

        # Usa o ensemble de B arvores para prever as instancias do fold i
        # (fold de teste) e avaliar desempenho do algoritmo (calcular Fmeasure)
        true_positives, false_positives, false_negatives, true_negatives = evaluateForest(forest, test_set, target_class)

        accuracy_values.append(calculateAccuracy(true_positives, true_negatives, false_positives, false_negatives))

        precision_value = calculatePrecision(true_positives, false_positives)
        precision_values.append(precision_value)

        recall_value = calculateRecall(true_positives, false_negatives)
        recall_values.append(recall_value)
        fmeasure_values.append(calculateF1Measure(precision_value, recall_value))

    accuracy = sum(accuracy_values)/len(accuracy_values)
    precision = sum(precision_values)/len(precision_values)
    recall = sum(recall_values)/len(recall_values)
    fmeasure = sum(fmeasure_values)/len(fmeasure_values)

    return accuracy, precision, recall, fmeasure

def evaluateForest(forest, test_set, target_class):
    instances_copy = list(test_set)

    class_distinct_values = getClassDistinctValues(target_class, test_set)

    true_positives = 0
    false_positives = {}
    true_negatives = {}
    false_negatives = {}

    for value in class_distinct_values:
        false_positives[value] = 0
        true_negatives[value] = 0
        false_negatives[value] = 0

    predictions = []
    correct_classes = []

    # Para cada instância do conjunto de validação
    for instance in instances_copy:
        correct_class = instance[target_class]
        correct_classes.append(correct_class)

        predicted_class = forestPredict(forest, instance)

        predictions.append(predicted_class)

    for i in range(len(predictions)):
        if predictions[i] == correct_classes[i]:
            true_positives = true_positives + 1
        else:
            for value in class_distinct_values:
                if correct_classes[i] == value and predictions[i] != value:
                    # falso negativo
                    false_negatives[value] = false_negatives[value] + 1
                elif correct_classes[i] != value and predictions[i] == value:
                    # falso positivo
                    false_positives[value] = false_positives[value]  + 1
                elif correct_classes[i] != value and predictions[i] != value:
                    # verdadeiro negativo
                    true_negatives[value] = true_negatives[value] + 1


    avg_false_positives = getAverageValue(false_positives)
    avg_false_negatives = getAverageValue(false_negatives)
    avg_true_negatives = getAverageValue(true_negatives)

    return true_positives, avg_false_positives, avg_false_negatives, avg_true_negatives


def getAverageValue(values_dict):
    values_list = []
    classes_count = 0

    for value in values_dict:
        values_list.append(values_dict[value])
        classes_count = classes_count + 1

    avg_value = float(sum(values_list) / classes_count)
    return avg_value

def forestPredict(forest, instance):
    predictions = []

    for tree in forest:
        predictions.append(tree.classify(instance))

    most_frequent_class = max(set(predictions), key=predictions.count)

    return most_frequent_class


def calculateAccuracy(true_positives, true_negatives, false_positives, false_negatives):
    return float((true_positives + true_negatives)/(true_positives + true_negatives + false_positives + false_negatives))

def calculateRecall(true_positives, false_negatives):
    return float((true_positives)/(true_positives + false_negatives))

def calculatePrecision(true_positives, false_positives):
    return float((true_positives)/(true_positives + false_positives))

def calculateF1Measure(precision, recall):
    return float((2*precision*recall)/(precision+recall))


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
