import pydot
# from collections import defaultdict

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]  
    
def find_key(adjacency_list, item):
    for key, value_list in adjacency_list.items():
        for value in value_list:
            if item in value[0]:
                return key
    return None 


def CreateAdjacencyList(nodes, edges):

    adjacencyList = {}
    
    for edge in edges:
        if 'weight' in edge.get_attributes():
            if edge.get_source() in adjacencyList.keys():
                adjacencyList[edge.get_source()].append((edge.get_destination(), edge.get_attributes()['weight']))
            else:
                adjacencyList[edge.get_source()] = [(edge.get_destination(), edge.get_attributes()['weight'])]
        else:
            if edge.get_source() in adjacencyList.keys():
                adjacencyList[edge.get_source()].append((edge.get_destination()))
            else:
                adjacencyList[edge.get_source()] = [(edge.get_destination())]
    for node in nodes:
        if node.get_name() not in adjacencyList.keys():
            #should ask if the same weight should be there otherway around
            adjacencyList[node.get_name()] = [(find_key(adjacencyList, node.get_name()), 0)]
    
    return adjacencyList

# print(CreateAdjacencyList(G.get_node_list(), G.get_edge_list()))