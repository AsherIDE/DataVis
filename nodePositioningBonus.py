import matplotlib.pyplot as plt
from ReadDotFile import  CreateAdjacencyList
import pydot
import numpy as np

from points_on_circle import points_on_circle

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Define the adjacency list
adjacency_list = CreateAdjacencyList(G.get_edge_list())


# Bonus node positions
node_positions = {}

# determine node with most edges
node_edges_amount, node_max = 0, 0
for n, e in adjacency_list.items():
    if len(e) > node_edges_amount:
        node_edges_amount = len(e)
        node_max = str(n)

# start determining positions
node_positions[node_max] = (0,0)
node_edges = adjacency_list[node_max].copy()

# generate the first circle
xs, ys = points_on_circle(node_edges_amount, 5, 0, 0)
for x, y in zip(xs, ys):
    node_positions[node_edges.pop(0)] = (x, y)

# generate the rest
"""

1. for each adjacency_list item in the first circle, check their neighbors
2. 

"""
print(adjacency_list.keys())
# for processed_node in adjacency_list.keys:
#     if processed_node in adjacency_list.keys():

# for node in adjacency_list[node_max]:
#     if node in adjacency_list.keys():
#         new_neighbors = adjacency_list[node].copy()

#         xs, ys = points_on_circle(len(new_neighbors), 5, node_positions[node][0], node_positions[node][1])
#         for x, y in zip(xs, ys):
#             new_node = new_neighbors.pop(0)
#             if new_node not in node_positions:

#                 node_positions[new_node] = (x, y)
#                 break
#         break

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