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
def organizeBfsOutput(input):
    output = []
    level = {}
    lower_level_nodes = []
    
    for edge in input:
        top_node, bottom_node = edge[0], edge[1]
        
        # check if a new node has to be added to the list of nodes for the current level
        if top_node not in lower_level_nodes:
            if top_node in level.keys():
                level[top_node] = level[top_node] + [bottom_node]

            else:
                level[top_node] = [bottom_node]
            
            # list of nodes that shouldnt be on the current level
            lower_level_nodes.append(bottom_node)
        
        # descend to new level
        else:
            output.append(level)
            level = {}
            lower_level_nodes = []

            # add the current top node to the next level already (in the next iteration it will otherwise be forgotten)
            level[top_node] = [bottom_node]

    # add the last level after the last iteration
    output.append(level)

    return output

def organizeDFSoutput(DFSorder):
    last_depth = 0
    parent_node = DFS_order[0][0]
    last_node = DFS_order[0][0]
    depth_last_added_node_dict = {}
    output = []
    for (node, depth) in DFSorder:
        if node == parent_node:
            output.append({
                node: []
            })
            last_depth = 0
            last_node = node
        elif depth == (last_depth + 1):
            if len(output) - 1 < depth:
                output.append({node: []})
            else:
                output[depth][node] = []
            parent_node = last_node
            output[depth-1][parent_node].append(node)
            last_depth = depth
            last_node = node
        elif depth == last_depth:
            output[depth][node] = []
            output[depth-1][parent_node].append(node)
            last_node = node
        elif depth == (last_depth - 1):
            parent_node = depth_last_added_node_dict[depth-1]
            output[depth][node] =[]
            output[depth-1][parent_node].append(node)
            last_depth = depth
            last_node = node
        depth_last_added_node_dict[depth] = node
    return output


# Determine node offsets for each node
# Input --> levels output from organizeBfsOutput function
# Ouput --> [{levels}, {node: {bottom_node: offset}}]
def getOffsets(levels):
    output = []

    for idx, level in enumerate(levels):
        output_level = {}

        # create a dict to easily find relative starting positions
        elevated_dict = {}
        if idx > 0:
            elevated_level = list(output[idx - 1].values())
            for elevated_node in elevated_level:
                elevated_dict.update(elevated_node)

        for top_node, bottom_nodes in level.items():
            max_offset = (len(bottom_nodes) / 2) - 1 #-1 because 1 max_offset = 0 idx
            left_offset = 1
            right_offset = -1

            # determine the offset from the top node
            if idx > 0:
                top_node_offset = elevated_dict[top_node]

                left_offset = top_node_offset + 1
                right_offset = top_node_offset - 1
            
            # assign a position to every bottom node
            output_node_offsets = {}
            for idx2, bottom_node in enumerate(bottom_nodes):

                # assign left offset
                if idx2 > max_offset:
                    output_node_offsets[bottom_node] = left_offset
                    left_offset += 1

                # assign right offset
                else:
                    output_node_offsets[bottom_node] = right_offset
                    right_offset -= 1

            output_level[top_node] = output_node_offsets

        output.append(output_level)

    return output


# Get a dict with node coordinates
def getCoordinates(offsets):
    output = {}

    # get first node position
    output[list(offsets[0].keys())[0]] = (0, 0)

    # get other node positions
    for idy, level in enumerate(offsets):
        y = idy + 1
        # x = 1

        for bottom_nodes in level.values():
            for node, offset in bottom_nodes.items():
                output[node] = (offset, -y)

    # TODO: offset compensation

    return output


'''
Below is where we actually start visualizing the tree
'''

# Define the adjacency list
# FILE_NAME = '../Networks/LesMiserables.dot'
Data_path = Path.cwd()
Data_path = Data_path.parent.parent / 'Networks' / 'LesMiserables.dot'
FILE_NAME = str(Data_path)
G = pydot.graph_from_dot_file(FILE_NAME)[0]
central_node = 11
mode= 'pre'

# Bfs tree
adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())
top_node = getStartNode(adjacency_list)
verts, edges = UnpackAdjacencyList(adjacency_list)
edges = np.squeeze([edge for edge in edges if edge[2]>0])
subtree_edges = CreateSubtree(verts, edges)
DFS_order = findDFSOrder(subtree_edges, central_node, mode)


levels_list = organizeDFSoutput(DFS_order)

offsets_list = getOffsets(levels_list)

coordinates_dict = getCoordinates(offsets_list)

# print("\n\n--------------results---------------")
# for k, v in coordinates_dict.items():
#     print(k, v)

# print(f"adj: {removeAdjacencyListWeights(adjacency_list)} \n\n bfs: {bfs_list}   \n\n lvls: {levels_list}")

# Draw nodes
for node, position in coordinates_dict.items():
    plt.scatter(position[0], position[1], color='blue', zorder=2)
    plt.text(position[0], position[1]+0.02, node, fontsize=12, ha='center', va='bottom', zorder=3, color='red')

print(coordinates_dict.keys())
# Draw edges
for node, neighbors in adjacency_list.items():
    print(node, neighbors)
    
    for neighbor_w in neighbors:
        neighbor, weight = neighbor_w
        neighbor = int(neighbor)
        print(neighbor, weight)
        # TODO: fixt bfs so that nodes wont randomly vanish
        # if neighbor not in coordinates_dict.keys() or node not in coordinates_dict.keys():
        #     continue
        
        plt.plot([coordinates_dict[node][0], coordinates_dict[neighbor][0]],
                 [coordinates_dict[node][1], coordinates_dict[neighbor][1]], color='black', zorder=1)


plt.title('Graph Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks([])
plt.yticks([])

plt.show()