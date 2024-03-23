import pydot
import numpy as np
import matplotlib.pyplot as plt
from ReadDotFile import CreateAdjacencyList

def create_connections_list(adjacency_list): 
    connections_list = []
    for i in adjacency_list:
        for j in adjacency_list[str(i)]:
            connections_list.append((i, j[0], j[1]))
    return connections_list
    

def create_matrix_undirected(adjacency_list):
    conn_list = create_connections_list(adjacency_list)
    dim = len(adjacency_list)
    matrix = np.ones((dim,dim)) * np.inf
    for i in conn_list:
        if int(i[2]) == 0:
            matrix[int(i[0]) - 1][int(i[1]) - 1] = 0
            matrix[int(i[1]) - 1][int(i[0]) - 1] = 0
        else:
            matrix[int(i[0]) - 1][int(i[1]) - 1] = 1/int(i[2])
            matrix[int(i[1]) - 1][int(i[0]) - 1] = 1/int(i[2])
    for i in adjacency_list:
        matrix[int(i)-1][int(i)-1] = 0
    for k in range(5): 
        for i in range(5): 
            for j in range(5): 
                if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    matrix[j][i] = matrix[i][k] + matrix[k][j]
    return matrix


# testing 

FILE_NAME = 'Networks/LesMiserables.dot'
G = pydot.graph_from_dot_file(FILE_NAME)[0]

adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())
print(create_matrix_undirected(adjacency_list)[10])