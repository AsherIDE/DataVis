import pydot
from collections import defaultdict

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

#for n in G.get_node_list():
    #print(f"Found node with id {n.get_name()}")
#for e in G.get_edge_list():
    #print(f"Edge from {e.get_source()} to {e.get_destination()}")


def CreateAdjacencyList(edges):
    edge_list = []
    
    for edge in edges:
        edge_list.append((edge.get_source(), edge.get_destination()))

    adjacencyList = defaultdict(list)
    
    for start, end in edge_list:
        adjacencyList[start].append(end)
    
    print('adjacencyList', adjacencyList)
    
    return adjacencyList
    
    
CreateAdjacencyList(G.get_edge_list())