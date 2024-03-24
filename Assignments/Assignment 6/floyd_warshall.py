import pydot
import numpy as np

def floyd_warshall(G):
    # vertices
    V = G.get_node_list()

    dim = len(V)
    D = np.ones((dim,dim)) * np.inf

    # redefine existing edge weight values
    for edge in G.get_edge_list():
        
        # assume weight of 1 if weights arent available
        if edge.get_weight() == None:
            D[int(edge.get_source()) - 1, int(edge.get_destination()) - 1] = 1
            D[int(edge.get_destination()) - 1, int(edge.get_source()) - 1] = 1
        else:
            D[int(edge.get_source()) - 1, int(edge.get_destination()) - 1] = edge.get_weight()
            D[int(edge.get_destination()) - 1, int(edge.get_source()) - 1] = edge.get_weight()

    # set diagonals to 0
    for i in range(len(V)):
        D[i, i] = 0

    # find paths with smaller weights
    for k in range(dim): 
        for i in range(dim): 
            for j in range(dim):
                if D[i, j] > D[i, k] + D[k, j]:
                    D[i, j] = D[i, k] + D[k, j]

    return D

# testing 
# FILE_NAME = 'Networks/LesMiserables.dot'
# G = pydot.graph_from_dot_file(FILE_NAME)[0]

# print(floyd_warshall(G))