import pydot
import matplotlib.pyplot as plt
import numpy as np

from nodeSorting import bfs, removeAdjacencyListWeights, getStartNode
from ReadDotFile import CreateAdjacencyList
from DFSImplementation import UnpackAdjacencyList, findDFSOrder, CreateSubtree

from pathlib import Path

'''
- Define minimum distance

1. Create node tree structure
2. Calculate node offsets for each level
3. Calculate actual positions
4. Draw graph

'''

# Create easy to interpret list with tree depth levels
# Input --> Bfs output
# Output --> List of levels: [{node: [children]}, {node: [children]}]
# def organizeBfsOutput(input):
#     output = []
#     level = {}
#     lower_level_nodes = []
    
#     for edge in input:
#         top_node, bottom_node = edge[0], edge[1]
        
#         # check if a new node has to be added to the list of nodes for the current level
#         if top_node not in lower_level_nodes:
#             if top_node in level.keys():
#                 level[top_node] = level[top_node] + [bottom_node]

#             else:
#                 level[top_node] = [bottom_node]
            
#             # list of nodes that shouldnt be on the current level
#             lower_level_nodes.append(bottom_node)
        
#         # descend to new level
#         else:
#             output.append(level)
#             level = {}
#             lower_level_nodes = []

#             # add the current top node to the next level already (in the next iteration it will otherwise be forgotten)
#             level[top_node] = [bottom_node]

#     # add the last level after the last iteration
#     output.append(level)

#     return output

# def organizeDFSoutput(DFSorder):
#     last_depth = 0
#     parent_node = DFS_order[0][0]
#     last_node = DFS_order[0][0]
#     depth_last_added_node_dict = {}
#     output = []
#     for (node, depth) in DFSorder:
#         if node == parent_node:
#             output.append({
#                 node: []
#             })
#             last_depth = 0
#             last_node = node
#         elif depth == (last_depth + 1):
#             if len(output) - 1 < depth:
#                 output.append({node: []})
#             else:
#                 output[depth][node] = []
#             parent_node = last_node
#             output[depth-1][parent_node].append(node)
#             last_depth = depth
#             last_node = node
#         elif depth == last_depth:
#             output[depth][node] = []
#             output[depth-1][parent_node].append(node)
#             last_node = node
#         elif depth == (last_depth - 1):
#             parent_node = depth_last_added_node_dict[depth-1]
#             output[depth][node] =[]
#             output[depth-1][parent_node].append(node)
#             last_depth = depth
#             last_node = node
#         depth_last_added_node_dict[depth] = node
#     return output

def get_dfs_coords(DFS_order):
    output = {}
    depth_dict = {}
    for node, depth in DFS_order:
        if depth not in depth_dict:
            depth_dict[depth] = [node]
            output[node] = [0, -depth]
        else:
            depth_dict[depth].append(node)
            output[node] = [len(depth_dict[depth])-1, -depth]
    return output

'''
Below is where we actually start visualizing the tree
'''

# Define the adjacency list
# FILE_NAME = '../Networks/LesMiserables.dot'
Data_path = Path.cwd()
Data_path = Data_path / 'Networks' / 'LesMiserables.dot'
FILE_NAME = str(Data_path)
G = pydot.graph_from_dot_file(FILE_NAME)[0]
central_node = 11
mode= 'pre'

# Bfs tree
adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())
verts, edges = UnpackAdjacencyList(adjacency_list)

adjacency_sans_weights = removeAdjacencyListWeights(adjacency_list)
edges = np.squeeze([edge for edge in edges if edge[2]>0])
subtree_edges = CreateSubtree(verts, edges)
DFS_order = findDFSOrder(subtree_edges, central_node, mode)

print(DFS_order)

node_coords = get_dfs_coords(DFS_order)

colors = ["#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6", "#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6"]

fig, ax = plt.subplots(figsize=(7,7))

for node, coord in node_coords.items():
    ax.scatter(coord[0], coord[1], c='blue')
    ax.text(coord[0], coord[1], node)
    
last_depth = 0
color_index = 0

# print(DFS_order)

for entry in subtree_edges:
    node = entry
    neighbor, weight = subtree_edges[entry]
    
    depth = min(node_coords[node][1], node_coords[neighbor][1])
    # print(node, neighbor, depth)
    
    ax.plot([node_coords[node][0], node_coords[neighbor][0]],
            [node_coords[node][1], node_coords[neighbor][1]], color=colors[color_index], zorder=1)
   
ax.set_title('Graph Visualization')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_xticks([])
ax.set_yticks([])

plt.show()