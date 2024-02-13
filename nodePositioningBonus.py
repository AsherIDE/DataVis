import matplotlib.pyplot as plt
from ReadDotFile import  CreateAdjacencyList
import math
import pydot
import numpy as np

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Define the adjacency list
adjacency_list = CreateAdjacencyList(G.get_edge_list())

# all_nodes = sorted(set(adjacency_list.keys()).union(*adjacency_list.values()))

# Random node positions {node, (x, y)}
node_positions = {}
# for node in all_nodes:
#     x = random.uniform(0, 1)  
#     y = random.uniform(0, 1) 
#     node_positions[node] = (x, y)

# Bonus node positions

# determine node with most edges
node_edges_amount, node_max = 0, 0
for n, e in adjacency_list.items():
    if len(e) > node_edges_amount:
        node_edges_amount = len(e)
        node_max = str(n)

# start determining positions
node_positions[node_max] = (0,0)

node_edges = adjacency_list[node_max]

print(360 / node_edges_amount)
print(math.sin(360 / node_edges_amount) * 5)

angle = 360 / node_edges_amount
for neighbor in node_edges:
     node_positions[neighbor] = (math.sin(angle) * 1, math.cos(angle) * 1)

     angle += angle

plt.figure()

# Draw nodes
for node, position in node_positions.items():
    plt.scatter(position[0], position[1], color='blue', zorder=2)
    plt.text(position[0], position[1]+0.02, node, fontsize=12, ha='center', va='bottom')

# # Draw edges
# for node, neighbors in adjacency_list.items():
#     for neighbor in neighbors:
#         plt.plot([node_positions[node][0], node_positions[neighbor][0]],
#                  [node_positions[node][1], node_positions[neighbor][1]], color='black', zorder=1)


plt.title('Graph Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks([])
plt.yticks([])

plt.show()