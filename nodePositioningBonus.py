import matplotlib.pyplot as plt
from ReadDotFile import  CreateAdjacencyList
import pydot
import time

from points_on_circle import points_on_circle

# timing start
start_time = time.time()

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Define the adjacency list
adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())


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

# assign every node into a circle layer, each one furthe away from the centre
circles = {1: [node_max], 2: adjacency_list[node_max].copy()}
circles_list = [node_max] + adjacency_list[node_max].copy()
nodes_non_categorized = [ele for ele in adjacency_list.keys() if ele not in circles_list]
while len(nodes_non_categorized) != 0:
    circles_next = []
    circles_number = len(circles.keys())
    for node in circles[circles_number]:
        for neighbor in adjacency_list[node]:
            if neighbor not in circles_list:
                circles_next.append(neighbor)

    circles_list += circles_next
    new_nodes_non_categorized = [ele for ele in nodes_non_categorized if ele not in circles_next]
    if new_nodes_non_categorized == nodes_non_categorized:
        circles[circles_number + 1] = nodes_non_categorized
        break

    else:
        circles[circles_number + 1] = circles_next
        nodes_non_categorized = new_nodes_non_categorized


# get the coordinates
radius = 5
for circle, nodes in circles.items():
    if circle > 2:
        radius = radius + 3
        xs, ys = points_on_circle(len(nodes), radius, 0, 0)

        for x, y in zip(xs, ys):
            node_positions[nodes.pop(0)] = (x, y)

plt.figure()

# Draw nodes
for node, position in node_positions.items():
    plt.scatter(position[0], position[1], color='blue', zorder=2)
    plt.text(position[0], position[1]+0.02, node, fontsize=12, ha='center', va='bottom', zorder=3, color='red')

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

# timing end
print("--- %s seconds ---" % (time.time() - start_time))

plt.show()