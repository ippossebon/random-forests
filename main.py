import csv

from node import Node
from tree import Tree


def main():
    file_name = './data/test.csv'
    attributes, instances = getDataFromFile(file_name)

    tree = Tree(attributes, 'Joga', instances)
    tree.createDecisionTree()


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

    return attributes, instances

if __name__ == '__main__':
    main()
