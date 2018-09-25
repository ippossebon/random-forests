import csv

from node import Node
from tree import Tree

"""
attributes_type = 'num' se os atributos são numéricos
attributes_type = 'cat' se os atributos são categóricos

"""

def main():
    file_name = './data/joga.csv'
    attributes, instances = getDataFromFile(file_name)

    tree = Tree('cat', attributes, 'Joga', instances)
    tree.createDecisionTree()
    tree.printDecisionTree()
    
    new_file_name = './data/new_data.csv'    
    attributes, new_instances = getDataFromFile(new_file_name)
    
    # Preve a classe de cada nova instancia informada
    for instance in range(len(new_instances)):
		predict(attributes, instance, tree)
	
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
  
 # Classifica uma nova instancia de acordo com a arvore de decisao   
 def predict(attributes, instance, tree, default_class = None):
	 if not tree:
		 return default_class
      
     attribute_index = list(tree.keys())[0]
     attribute_values = list(tree.values())[0]
     instance_attribute_value = instance[attribute_index]
      
     if instance_attribute_value not in attribute_values:
		 return default_class
     
     return self._predict(attribute_values[instance_attribute_value],
                          instance, default_class)
    

if __name__ == '__main__':
    main()
