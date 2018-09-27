import csv

from node import Node
from tree import Tree

"""
attributes_type = 'num' se os atributos são numéricos
attributes_type = 'cat' se os atributos são categóricos

"""

def main():
    file_name = './data/joga.csv'
    attributes, attributes_types, instances = getDataFromFile(file_name)

    tree = Tree(attributes, attributes_types, 'Joga', instances)
    tree.createDecisionTree()
    tree.printDecisionTree()

    #new_instance_file = './data/new_data.csv'

    #attributes, attributes_types, new_instances = getDataFromFile(new_instance_file)

    #print(new_instance)

    # Preve a classe de cada nova instancia informada
    for instance in range(len(instances)):
        predict(attributes, instance, tree)

def getBootstrap(training_data, size):
    pass


def generateRandomForest(trees_count, bootstrap_size, training_data):
    forest = []

    for i in range(trees_count):
        bootstrap = getBootstrap(training_data, bootstrap_size)
        tree = Tree(attributes, 'class', bootstrap)
        tree.createDecisionTree()
        forest.append(tree)

    return forest


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


# Classifica uma nova instancia de acordo com a arvore de decisao
def predict(tree, instance):
    # Precisa verificar se um nodo filho ou eh um terminal com a classe para retornar
    # ou se eh um nodo dicionario com outro nivel da arvore para explorar

    # O index e valor de um nodo eh usado para verificar se a informacao da instancia
    # vai para o lado esquerdo ou direito da divisao da arvore

    # Verifica se o valor da instancia eh menor que o nodo atual (atributos numericos)
    # ou se o valor da instancia eh diferente do nodo atual (atributos categoricos)

    if (instance[tree.node[index]] < tree.node[value]) || (instance[tree.node[index]] != tree.node[value]):
		if isinstance(tree.node[left], dict):
			return predict(tree.node[left], instance)
		else:
			return tree.node[left]
	else:
		if isinstance(tree.node[right], dict):
			return predict(tree.node[right], instance)
		else:
			return tree.node[right]

if __name__ == '__main__':
    main()
