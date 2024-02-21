import pydot
import matplotlib.pyplot as plt

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
def getOffsets(levels, distance=1):
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
            left_offset = distance
            right_offset = -distance

            # determine the offset from the top node
            if idx > 0:

                # find top_node in current level if its not in elevated_dict
                if top_node not in elevated_dict.keys():
                    # assign a position to nodes connected to the same line manually
                    for output_node in output_level.values():
                        if top_node in output_node.keys():
                            top_node_offset = output_node[top_node]
                
                else:
                    top_node_offset = elevated_dict[top_node]

                left_offset = top_node_offset + distance
                right_offset = top_node_offset - distance
            
            # assign a position to every bottom node
            output_node_offsets = {}
            for idx2, bottom_node in enumerate(bottom_nodes):

                # assign left offset
                if idx2 > max_offset:
                    output_node_offsets[bottom_node] = left_offset
                    left_offset += distance

                # assign right offset
                else:
                    output_node_offsets[bottom_node] = right_offset
                    right_offset -= distance

            output_level[top_node] = output_node_offsets

        output.append(output_level)

    return output


# Get a dict with node coordinates
def getCoordinates(offsets, distance=1):
    output = {}

    # get first node position
    output[list(offsets[0].keys())[0]] = (0, 0)

    # get other node positions
    for idy, level in enumerate(offsets):
        y = idy + 1

        occupied_offsets = []
        for bottom_nodes in level.values():
            for node, offset in bottom_nodes.items():

                # prevent node collision
                if offset not in occupied_offsets:
                    output[node] = (offset, -y)
                    
                    occupied_offsets.append(offset)

                else:
                    move = -1

                    # find out if we have to move the node to the left or right
                    if offset > 0:
                        move = 1

                    # find new position for node
                    manual_offset = offset
                    while True:
                        manual_offset = manual_offset + (move * distance)

                        if manual_offset not in occupied_offsets:
                            output[node] = (manual_offset, -y)
                            break

                    occupied_offsets.append(manual_offset)

    return output


# Input --> file, fontsize, circlesize
def drawVisualization(FILE_NAME, fontsize, circlesize):

    # Define the adjacency list
    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    # Bfs tree
    adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())
    top_node = getStartNode(adjacency_list)
    bfs_list = bfs(removeAdjacencyListWeights(adjacency_list), top_node)

    levels_list = organizeBfsOutput(bfs_list)
    # for l in levels_list:
    #     print(f"{l}\n")
    offsets_list = getOffsets(levels_list, distance=10)

    coordinates_dict = getCoordinates(offsets_list, distance=10)

    # Draw nodes
    # for node, position in coordinates_dict.items():
    #     plt.scatter(position[0], position[1], color='#808080', zorder=2, s=350)
    #     plt.text(position[0], position[1]-0.05, node, fontsize=12, ha='center', va='bottom', zorder=3, color='black')

    for node, position in coordinates_dict.items():
        plt.scatter(position[0], position[1], color='#808080', zorder=2, s=circlesize)
        plt.text(position[0], position[1]-0.05, node, fontsize=fontsize, ha='center', va='bottom', zorder=3, color='black')

    # Draw edges (only draw edges that come forth from the bfs output)
    colors = ["#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6", "#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6"]
    color_index = 0
    for level in levels_list:
        for top_node, bottom_nodes in level.items():
            for node in bottom_nodes:
                if node in coordinates_dict.keys() and top_node in coordinates_dict.keys():
                    plt.plot([coordinates_dict[node][0], coordinates_dict[top_node][0]],
                            [coordinates_dict[node][1], coordinates_dict[top_node][1]], color=colors[color_index], zorder=1, alpha=0.8)
                
            color_index += 1

    # Draw edges (all edges according to adjacency list)
    # for node, neighbors in adjacency_list.items():
        
    #     for neighbor in neighbors:

    #         # prevent node not found from bvs output
    #         if neighbor[0] not in coordinates_dict.keys() or node not in coordinates_dict.keys():
    #             continue
            
    #         plt.plot([coordinates_dict[node][0], coordinates_dict[neighbor[0]][0]],
    #                  [coordinates_dict[node][1], coordinates_dict[neighbor[0]][1]], color='black', zorder=1, alpha=0.5)


    plt.title('Graph Visualization')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xticks([])
    plt.yticks([])

    return plt.show()


'''
Below is where we actually start visualizing the tree
'''

# FILE_NAME = 'Networks/LesMiserables.dot'
# drawVisualization(FILE_NAME, 12, 350)

FILE_NAME = 'Networks/JazzNetwork.dot'
drawVisualization(FILE_NAME, 6, 50)

# FILE_NAME = 'Networks/LeagueNetwork.dot'
# drawVisualization(FILE_NAME, 20, 500)

