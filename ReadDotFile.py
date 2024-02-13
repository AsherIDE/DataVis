import pydot
# from collections import defaultdict

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

#for n in G.get_node_list():
    #print(f"Found node with id {n.get_name()}")
#for e in G.get_edge_list():
    #print(f"Edge from {e.get_source()} to {e.get_destination()}")
    
def find_key(adjacency_list, item):
    for key, value_list in adjacency_list.items():
        if item in value_list:
            return key
    return None 


def CreateAdjacencyList(nodes, edges):

    adjacencyList = {}
    
    for edge in edges:
        if edge.get_source() in adjacencyList.keys():
            adjacencyList[edge.get_source()].append(edge.get_destination())
        else:
            adjacencyList[edge.get_source()] = [edge.get_destination()]
    
    for node in nodes:
        if node.get_name() not in adjacencyList.keys():
            adjacencyList[node.get_name()] = [find_key(adjacencyList, node.get_name())]
    
    return adjacencyList

print(CreateAdjacencyList(G.get_node_list(), G.get_edge_list()))