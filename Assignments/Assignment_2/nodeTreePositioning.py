import pydot
import matplotlib.pyplot as plt

from Assignments.Assignment_2.nodeSorting import bfs, removeAdjacencyListWeights, getStartNode
from Assignments.Assignment_2.ReadDotFile import CreateAdjacencyList
from Assignments.Assignment_2.DFSImplementation import findDFSOrder

from typing import List
from dataclasses import dataclass

@dataclass
class Node:
    id: str
    children: List
    leaf_count: int

# Create easy to interpret list with tree depth levels
# Input --> Bfs output
# Output --> Tree class, connections dict
def organizeBfsOutput(input):
    connections = {}

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
            connections.update(level)
            level = {}
            lower_level_nodes = []

            # add the current top node to the next level already (in the next iteration it will otherwise be forgotten)
            level[top_node] = [bottom_node]

    # add the last level after the last iteration
    connections.update(level)
    
    # Creates a tree out of a dict with connections
    # id = first node, connections
    def makeTree(id, connections):
        child_ids = connections.get(id, [])
        children = []
        leaf_count = 0
        for child_id in child_ids:
            child = makeTree(child_id, connections)
            children.append(child)
            if len(child.children) == 0:
                leaf_count += 1
            else:
                leaf_count += child.leaf_count

        return Node(id, children, leaf_count)

    tree = makeTree(list(connections.keys())[0], connections)

    return tree, connections

def organizeDFSOutput(order_list):
    connections = {}
    for edge in order_list:
        top_node, bottom_node = edge[0], edge[1]
        if top_node not in connections:
            connections[top_node] = []
        connections[top_node].append(bottom_node)
    # Creates a tree out of a dict with connections
    # id = first node, connections
    def makeTree(id, connections):
        child_ids = connections.get(id, [])
        children = []
        leaf_count = 0
        for child_id in child_ids:
            child = makeTree(child_id, connections)
            children.append(child)
            if len(child.children) == 0:
                leaf_count += 1
            else:
                leaf_count += child.leaf_count

        return Node(id, children, leaf_count)

    tree = makeTree(list(connections.keys())[0], connections)
    
    return tree, connections

# Recursive function to iterate the tree and get all coords
def buildTreeCoords(tree, x = 0, y = 0):
    Coords = {tree.id: (x + tree.leaf_count / 2, y)}

    # get coords from children and childrens children and so on
    for child in tree.children:
        Coords.update(buildTreeCoords(child, x, y - 0.3))

        x += max(child.leaf_count, 1)

    return Coords

# Returns a list of nodes that are missing in a network tree
def getMissingNodes(nodes_tree, adjacency_list):
    nodes_missing = []
    
    # get list of all existing nodes in .dot file
    nodes_adjacency_list = []
    for adjacency_node, adjacency_neighbors in adjacency_list.items():
        if adjacency_node not in nodes_adjacency_list:
            nodes_adjacency_list.append(adjacency_node)

        for adjacency_neighbor in adjacency_neighbors:
            if adjacency_neighbor not in nodes_adjacency_list:
                nodes_adjacency_list.append(adjacency_neighbor)
    
    # compare both lists and add missing nodes to missing list
    for node in nodes_adjacency_list:
        if node not in nodes_tree:
            nodes_missing.append(node)
    
    return nodes_missing

# Draw the actual tree from a file and some settings (xy being the left out nodes positions)
def drawTree(FILE_NAME, fontsize, circlesize, xy, MODE='bfs', START_NODE=None):
    FILE_NAME = f'Networks/{FILE_NAME}.dot'
    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    # bfs tree
    adjacency_list = removeAdjacencyListWeights(CreateAdjacencyList(G.get_node_list(), G.get_edge_list()))
    total_nodes = [node.get_name() for node in G.get_node_list()]
    
    if START_NODE is None:
        top_node = getStartNode(adjacency_list, total_nodes)[0]
    else:
        top_node = START_NODE
    
    match MODE:
        case 'bfs':
            order_list = bfs(adjacency_list, top_node)
            tree, connections = organizeBfsOutput(order_list)
        case 'dfs':
            order_list = findDFSOrder(adjacency_list, top_node)
            tree, connections = organizeDFSOutput(order_list)
        case _:
            raise ValueError()

    # put bfs into tree format
    # print(tree, connections)

    # retrieve coords
    coords = buildTreeCoords(tree)


    # get missing nodes
    missing_nodes_list = getMissingNodes(coords.keys(), adjacency_list)

    # add coords to missing nodes
    y_missing = xy[1]
    x_missing = xy[0]
    step = 0
    for missing_node in missing_nodes_list:
        coords[missing_node] = (x_missing, y_missing)

        if step <= 3:
            y_missing += 0.05
            step += 1
        else: 
            y_missing -= 0.1
            step -= 3

        x_missing += 3

    # add missing nodes to list of connections
    for missing_node1 in missing_nodes_list:
        for missing_node2 in missing_nodes_list:
            if missing_node1 in adjacency_list[missing_node2] and missing_node2 not in connections:
                if missing_node1 not in connections:
                    connections[missing_node1] = [missing_node2]
                else:
                    connections[missing_node1].append(missing_node2)

    
    # draw the nodes and edges (based on tree connections)
    drawn_edges = []
    for node, position in coords.items():
        plt.scatter(position[0], position[1], color='red', zorder=3, s=circlesize)
        # plt.text(position[0], position[1]-0.02, node, fontsize=fontsize, ha='center', va='bottom', zorder=4, color='black')

        if node in connections:
            for child in connections[node]:
                plt.plot([position[0], coords[child][0]],
                        [position[1], coords[child][1]], color="black", zorder=2, alpha=0.4)
                
                drawn_edges.append((node, child))
                
    # draw edges (based on all connections from adjacency list)
    # for node, neighbors in adjacency_list.items():
        
    #     for neighbor in neighbors:

    #         # prevent already drawn vertices from being drawn again
    #         if (node, neighbor) in drawn_edges or (neighbor, node) in drawn_edges:
    #             continue
            
    #         plt.plot([coords[node][0], coords[neighbor[0]][0]],
    #                  [coords[node][1], coords[neighbor[0]][1]], color='black', zorder=1, alpha=0.4)

    plt.title('Tree Visualization')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    plt.xticks([])
    plt.yticks([])

    plt.show()


# TODO: find recursive time complecity O(n + v)

# TEST (MODE='dfs', START_NODE= '1' otherwise dont specify)
# jazz network
# FILE_NAME = 'JazzNetwork'
# drawTree(FILE_NAME, 5, 30, (110, -1.4))

# les miserables
# FILE_NAME = 'LesMiserables'
# drawTree(FILE_NAME, 12, 100, (4, -0.9), MODE='dfs', START_NODE= '1')






























"""

Wall of torture below...

"""

# # Returns a new dict with altered offsets
# def moveOffset(nodes, amount):
#             new_nodes = {}

#             for node, offset in nodes.items():
#                 new_nodes[node] = offset + amount

#             return new_nodes

# # list of lists --> list
# def flatten(matrix):
#     flat_list = []
#     for row in matrix:
#         flat_list.extend(row)
#     return list(set(flat_list))

# # Determine node offsets for each node
# # Input --> levels output from organizeBfsOutput function
# # Ouput --> [{levels}, {node: {bottom_node: offset}}]
# def getOffsets(levels):
#     output = []

#     for idx, level in enumerate(levels):
#         output_level = {}

#         # create a dict to easily find relative starting positions
#         elevated_dict = {}
#         if idx > 0:
#             elevated_level = list(output[idx - 1].values())
#             for elevated_node in elevated_level:
#                 elevated_dict.update(elevated_node)

#         for top_node, bottom_nodes in level.items():
#             max_offset = (len(bottom_nodes) / 2) - 1 #-1 because 1 max_offset = 0 idx
#             left_offset = 1
#             right_offset = -1

#             # determine the offset from the top node
#             if idx > 0:

#                 # find top_node in current level if its not in elevated_dict
#                 if top_node not in elevated_dict.keys():
#                     # assign a position to nodes connected to the same line manually
#                     for output_node in output_level.values():
#                         if top_node in output_node.keys():
#                             top_node_offset = output_node[top_node]
                
#                 else:
#                     top_node_offset = elevated_dict[top_node]

#                 left_offset = top_node_offset + 1
#                 right_offset = top_node_offset - 1
            
#             # assign a position to every bottom node
#             output_node_offsets = {}
#             for idx2, bottom_node in enumerate(bottom_nodes):

#                 # assign left offset
#                 if idx2 > max_offset:
#                     output_node_offsets[bottom_node] = left_offset
#                     left_offset += 1

#                 # assign right offset
#                 else:
#                     output_node_offsets[bottom_node] = right_offset
#                     right_offset -= 1

#             output_level[top_node] = output_node_offsets

#         output.append(output_level)

#     # sort output dict to avoid line crossing at lower levels
#     # sorted_output = []
#     # 
#     # for unsorted_level in output:
#     #     unsorted_level_values = {}
#     #     for children in unsorted_level.values():
#     #         unsorted_level_values.update(children)
#         # print(list(reversed(list({k: v for k, v in sorted(unsorted_level_values.items(), key=lambda item: item[1])}.keys()))), "\n")
#         # print(dict(reversed({k: v for k, v in sorted(unsorted_level_values.items(), key=lambda item: item[1])}.items())), "\n")

#     # iter levels
#     # for id3, unsorted_level in enumerate(output):
#     #     # first iteration cannot be sorted
#     #     if id3 == 0:
#     #         continue

#     #     # iter nodes on level
#     #     # for parent, children in unsorted_level.items():
#     #     previous_level_children = flatten(list(item.keys() for item in output[id3 - 1].values()))
#     #     sorted_level = {}
#     #     print(previous_level_children, "\n")
#     #     # print(list(unsorted_level.keys()), "\n", list(unsorted_level.values()), "\n", previous_level_children, "\n\n\n")

#     return output

# # Returns a list of nodes that are missing in a network tree
# def getMissingNodes(levels, adjacency_list):
#     nodes_missing = []
    
#     # get list of all existing nodes in .dot file
#     nodes_adjacency_list = []
#     for adjacency_node, adjacency_neighbors in adjacency_list.items():
#         if adjacency_node not in nodes_adjacency_list:
#             nodes_adjacency_list.append(adjacency_node)

#         for adjacency_neighbor in adjacency_neighbors:
#             if adjacency_neighbor not in nodes_adjacency_list:
#                 nodes_adjacency_list.append(adjacency_neighbor)
    
#     # get list of all nodes from all levels
#     nodes_levels = []
#     for level in levels:
#         for top_node, bottom_nodes in level.items():
#             if top_node not in nodes_levels:
#                 nodes_levels.append(top_node)
            
#             for bottom_node in bottom_nodes:
#                 if bottom_node not in nodes_levels:
#                     nodes_levels.append(bottom_node)
    
#     # compare both lists and add missing nodes to missing list
#     for node in nodes_adjacency_list:
#         if node not in nodes_levels:
#             nodes_missing.append(node)
    
#     return nodes_missing


# # Get a dict with node coordinates
# def getCoordinates(offsets, missing_nodes_list):
#     output = {}
#     loose_nodes = []

#     # get first node position
#     output[list(offsets[0].keys())[0]] = (0, 0)

#     # get lower level node positions
#     node_order = {} # {level: [nodes]}
#     for idy, level in enumerate(offsets):
#         y = idy + 1
#         node_order[idy] = []

#         left_occupied_offsets = []
#         right_occupied_offsets = []
#         # use suggested offsets, since there is no overlap
#         if idy == 0:
#             for bottom_nodes in level.values():
#                 # assign coordinates to every node
#                 for node, offset in bottom_nodes.items():
#                     output[node] = (offset, -y)

#         # recalculate every other offset from other levels
#         else:
#             for top_node, bottom_nodes in level.items():
#                 parent_node_offset = bottom_nodes[next(iter(bottom_nodes))] + 1

#                 # will be adjusted if things overlap or cross x=0
#                 modified_bottom_nodes = bottom_nodes

#                 # append to left
#                 if parent_node_offset <= 0:

#                     # bottom_nodes are moved to new parent node offset
#                     if top_node in output.keys():
#                         new_parent_node_offset = output[top_node][0]
#                         modified_bottom_nodes = moveOffset(bottom_nodes, new_parent_node_offset - parent_node_offset)
#                         # print(top_node, output[top_node][0], bottom_nodes)

#                     # bottom_nodes surpass x=0 border
#                     if max(modified_bottom_nodes.values()) > 0:
#                         modified_bottom_nodes = moveOffset(modified_bottom_nodes, -max(bottom_nodes.values()) - 1)

#                     # bottom_nodes overlaps with other stack of bottom_nodes
#                     if len(list(set(modified_bottom_nodes.values()) & set(left_occupied_offsets))) > 0:
#                         free_offsets = min(left_occupied_offsets) - 1
#                         modified_bottom_nodes = moveOffset(bottom_nodes, int(free_offsets + (max(bottom_nodes.values()) / -1)))

#                 # append to right
#                 else:
#                     # bottom_nodes surpass x=0 border
#                     if min(bottom_nodes.values()) < 0:
#                         modified_bottom_nodes = moveOffset(bottom_nodes, min(bottom_nodes.values()) + 1)

#                     # bottom_nodes overlaps with other stack of bottom_nodes
#                     if len(list(set(modified_bottom_nodes.values()) & set(right_occupied_offsets))) > 0:
#                         free_offsets = max(right_occupied_offsets) + 1
#                         modified_bottom_nodes = moveOffset(bottom_nodes, int(free_offsets - min(bottom_nodes.values())))

#                 # save order
#                 node_order[idy] += list(dict(reversed({k: v for k, v in sorted(modified_bottom_nodes.items(), key=lambda item: item[1])}.items())).keys())
#                 # print(f"modified: {list(dict(reversed({k: v for k, v in sorted(modified_bottom_nodes.items(), key=lambda item: item[1])}.items())).keys())}")
#                 # print(modified_bottom_nodes)
#                 # def Convert(tup):
#                 #     di = dict(tup)
#                 #     return di

#                 # index_map = {v: i for i, v in enumerate(list(dict(reversed({k: v for k, v in sorted(modified_bottom_nodes.items(), key=lambda item: item[1])}.items())).keys()))}
#                 # modified_bottom_nodes = Convert(sorted(modified_bottom_nodes.items(), key=lambda pair: index_map[pair[0]]))
#                 # print(modified_bottom_nodes)

#                 # exclude parent node offset (to leave an empty space between left and right)
#                 if bottom_nodes != modified_bottom_nodes and len(bottom_nodes.values()) > 1:
#                     # print(modified_bottom_nodes, "<----- modified")
#                     # print(bottom_nodes, "<----- unmodified")
#                     parent_node_offset = modified_bottom_nodes[next(iter(modified_bottom_nodes))] + 1
#                 # else:
#                 #     print(bottom_nodes)
#                 if parent_node_offset <= 0:
#                     left_occupied_offsets.append(parent_node_offset)

#                     # assign coordinates to every node
#                     for node, offset in modified_bottom_nodes.items():
#                         output[node] = (offset, -y)
#                         left_occupied_offsets.append(offset)
#                         # print(node)
#                 else:
#                     right_occupied_offsets.append(parent_node_offset)

#                     # assign coordinates to every node
#                     for node, offset in modified_bottom_nodes.items():
#                         output[node] = (offset, -y)
#                         right_occupied_offsets.append(offset)
#                         # print(node)




#         # occupied_offsets = []
#         # for bottom_nodes in level.values():
#         #     parent_node_offset = bottom_nodes[next(iter(bottom_nodes))] + 1
            
#         #     # TODO: DIT WEL ECHT TOEPASSEN REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#         #     #  TODO: DYNAMISCH MAKEN
#         #     if len(bottom_nodes.keys()) > 1 and parent_node_offset not in occupied_offsets:
#         #             # avoid duplicates
#         #             occupied_offsets.append(parent_node_offset)
#         #             # print(f"mid pos: {parent_node_offset}")

#         #     # assign coordinates to every node
#         #     for node, offset in bottom_nodes.items():

#         #         # prevent node collision
#         #         if offset not in occupied_offsets:
#         #             output[node] = (offset, -y)
                    
#         #             occupied_offsets.append(offset)

#         #         else:
#         #             move = -1

#         #             # find out if we have to move the node to the left or right
#         #             if offset > 0:
#         #                 move = 1

#         #             # find new position for node
#         #             manual_offset = offset
#         #             while True:
#         #                 manual_offset = manual_offset + move

#         #                 if manual_offset not in occupied_offsets:
#         #                     output[node] = (manual_offset, -y)
#         #                     break

#         #             occupied_offsets.append(manual_offset)

    

#     for idz, level in enumerate(offsets):
#         if idz < 2:
#             continue

#         # print(level)
#         # print(node_order)

#         sorted_node_index = None
#         for level_node in level.keys():
#             if level_node not in node_order[idz - 1]:
#                 continue

#             if sorted_node_index is not None and node_order[idz - 1].index(level_node) < sorted_node_index:
#                 print(f"{node_order[idz - 1].index(level_node)} came before {sorted_node_index}")

#             sorted_node_index = node_order[idz - 1].index(level_node)


#     # get missing node positions
#     missing_nodes_count = (len(missing_nodes_list) / 2) - 1
#     yl = y + 1
#     yr = y + 1

#     left_offset = -1
#     right_offset = 1
#     for idx, missing_node in enumerate(missing_nodes_list):
#         loose_nodes.append(missing_node)

#         # left
#         if idx <= missing_nodes_count:
#             output[missing_node] = (left_offset, -yl)
#             left_offset -= 1
#             yl += 0.2
#         # right
#         else:
#             output[missing_node] = (right_offset, -yr)
#             right_offset += 1
#             yr += 0.2

#     return output, loose_nodes


# # Input --> file, fontsize, circlesize
# def drawVisualization(FILE_NAME, fontsize, circlesize):

#     # define the adjacency list
#     G = pydot.graph_from_dot_file(FILE_NAME)[0]

#     # bfs tree
#     adjacency_list = removeAdjacencyListWeights(CreateAdjacencyList(G.get_node_list(), G.get_edge_list()))
#     top_node = getStartNode(adjacency_list)
#     bfs_list = bfs(adjacency_list, top_node)

#     # put bfs into levels format
#     levels_list = organizeBfsOutput(bfs_list)
#     offsets_list = getOffsets(levels_list)

#     print("------------------------------------------------------\n")
#     for offset in levels_list:
#         print(offset, "\n")
#     print("------------------------------------------------------\n")

#     # get coords form levels
#     missing_nodes_list = getMissingNodes(levels_list, adjacency_list)
#     coordinates_dict, loose_nodes = getCoordinates(offsets_list, missing_nodes_list)

#     for node, position in coordinates_dict.items():
#         plt.scatter(position[0], position[1], color='#808080', zorder=2, s=circlesize)
#         plt.text(position[0], position[1]-0.05, node, fontsize=fontsize, ha='center', va='bottom', zorder=3, color='black')

#     # draw edges (only draw edges that come forth from the bfs output)
#     colors = ["#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B", "#325A9B"]
#     # colors = ["#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6", "#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6"]
#     color_index = 0
#     for level in levels_list:
#         for top_node, bottom_nodes in level.items():
#             for node in bottom_nodes:
#                 plt.plot([coordinates_dict[node][0], coordinates_dict[top_node][0]],
#                         [coordinates_dict[node][1], coordinates_dict[top_node][1]], color=colors[color_index], zorder=1, alpha=0.8)
                
#             color_index += 1

#     # draw edges (all edges according to adjacency list)
#     # for node, neighbors in adjacency_list.items():
        
#     #     for neighbor in neighbors:

#     #         # prevent node not found from bvs output
#     #         if neighbor[0] not in coordinates_dict.keys() or node not in coordinates_dict.keys():
#     #             continue
            
#     #         plt.plot([coordinates_dict[node][0], coordinates_dict[neighbor[0]][0]],
#     #                  [coordinates_dict[node][1], coordinates_dict[neighbor[0]][1]], color='black', zorder=1, alpha=0.5)
            
#     # draw lines between loose nodes
#     connected = {}
#     for node1 in loose_nodes:
#         for node2 in loose_nodes:
#             if node1 in adjacency_list.keys() and node2 in adjacency_list[node1]:
#                 plt.plot([coordinates_dict[node1][0], coordinates_dict[node2][0]],
#                         [coordinates_dict[node1][1], coordinates_dict[node2][1]], color=colors[color_index], zorder=1, alpha=0.8)


#     plt.title('Graph Visualization')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.xticks([])
#     plt.yticks([])

#     return plt.show()


# '''
# Below is where we actually start visualizing the tree
# '''

# # FILE_NAME = 'Networks/LesMiserables.dot'
# # drawVisualization(FILE_NAME, 12, 350)

# # FILE_NAME = 'Networks/JazzNetwork.dot'
# # drawVisualization(FILE_NAME, 6, 50)

# # Data_path = Path.cwd()
# # Data_path = Data_path.parent.parent / 'Networks' / 'LesMiserables.dot'
# # FILE_NAME = str(Data_path)
# # drawVisualization(FILE_NAME, 6, 50)

# # FILE_NAME = 'Networks/LeagueNetwork.dot'
# # drawVisualization(FILE_NAME, 20, 500)

