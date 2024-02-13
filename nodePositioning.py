import matplotlib.pyplot as plt
from ReadDotFile import  CreateAdjacencyList
import random
import pydot
import numpy as np

""" def get_node_degree(adjacency_list, all_nodes):
    out_list = np.zeros((len(all_nodes), 2))
    out_list[:,0] = all_nodes
    for node, neighbors in adjacency_list.items():
        if(node in all_nodes)
        out_list[int(node) - 1,1] = len(neighbors)
        for neighbor in neighbors:
            out_list[int(neighbor)-1,1]+= 1
    
    return out_list """

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Define the adjacency list
adjacency_list = CreateAdjacencyList(G.get_edge_list())

all_nodes = sorted(set(adjacency_list.keys()).union(*adjacency_list.values()))

# print('adjacency_list', adjacency_list)
# print('all_nodes', all_nodes)

""" print(get_node_degree(adjacency_list, all_nodes)) """

node_positions = {}

# circ_ang_list = np.linspace(0, 2*np.pi, len(all_nodes))

node_positions = {}
for node in all_nodes:
    x = random.uniform(0, 1)  
    y = random.uniform(0, 1) 
    node_positions[node] = (x, y)


plt.figure()

for node, position in node_positions.items():
    plt.scatter(position[0], position[1], color='blue', zorder=2)
    plt.text(position[0], position[1]+0.02, node, fontsize=12, ha='center', va='bottom')

# Draw edges
for node, neighbors in adjacency_list.items():
    for neighbor in neighbors:
        plt.plot([node_positions[node][0], node_positions[neighbor][0]],
                 [node_positions[node][1], node_positions[neighbor][1]], color='black', zorder=1)


plt.title('Graph Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks([])
plt.yticks([])

plt.show()