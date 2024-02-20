import pydot

from nodeSorting import bfs, removeAdjacencyListWeights, getStartNode
from ReadDotFile import CreateAdjacencyList


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
# TODO: take care of unconnected nodes
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


# Determine node offsets for each node
# Input --> levels output from organizeBfsOutput function
# Ouput --> [{levels}, {node: {bottom_node: offset}}]
def getOffsets(levels):
    output = []

    for level in levels:
        output_level = {}
        for top_node, bottom_nodes in level.items():
            max_offset = (len(bottom_nodes) / 2) - 1 #-1 because 1 max_offset = 0 idx
            left_offset = 1
            right_offset = -1
            
            output_node_offsets = {}
            for idx, bottom_node in enumerate(bottom_nodes):

                # left
                if idx > max_offset:
                    output_node_offsets[bottom_node] = left_offset
                    left_offset += 1

                # right
                else:
                    output_node_offsets[bottom_node] = right_offset
                    right_offset -= 1

            output_level[top_node] = output_node_offsets

        output.append(output_level)

    return output

'''
Below is where we actually start visualizing the tree
'''

# Define the adjacency list
FILE_NAME = 'Networks/LesMiserables.dot'
G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Bfs tree
adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())
bfs_list = bfs(removeAdjacencyListWeights(adjacency_list), '11')
top_node = getStartNode(adjacency_list)

levels_list = organizeBfsOutput(bfs_list)

for i in getOffsets(levels_list):
    print(i)