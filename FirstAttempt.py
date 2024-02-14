import matplotlib.pyplot as plt
from ReadDotFile import  CreateAdjacencyList
import random
import pydot
import numpy as np

def plot_graph(ax:plt.Axes, coords_list:dict, adjacency_list:dict):
    for node, position in coords_list.items():
        ax.scatter(position[0], position[1], color='red', zorder=2, s=130)
        ax.text(position[0], position[1]-0.04, node, c='black', fontsize=8, ha='center', va='bottom')

    # Draw edges
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            ax.plot([node_positions[node][0], node_positions[neighbor[0]][0]],
                    [node_positions[node][1], node_positions[neighbor[0]][1]], color='black', zorder=1)
    ax.set_title('Graph Visualization')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    # ax.set_xlim(0, 1)
    # ax.set_ylim(0, 1)
    # ax.set_xticks([])
    # ax.set_yticks([])
    return None

def return_gravity_force(coord:np.ndarray, mass, grav_coeff):
    coord_unit = coord / np.linalg.norm(coord)
    return mass * grav_coeff * -1 * coord_unit

def return_coulomb_force(coord, node_positions, coulomb_coeff):
    force = [0.0,0.0]
    for _, node_coord in node_positions.items():
        vec_pos = coord - node_coord
        if np.linalg.norm(vec_pos) < 1e-5:
            continue
        force += (np.power(np.linalg.norm(vec_pos), -2)) * coulomb_coeff * (vec_pos/np.linalg.norm(vec_pos))
    return force

def return_spring_force(coord, node_id, node_positions, adjacency_list, spring_const, ideal_dist):
    force = [0.0,0.0]
    for neighbor in adjacency_list[node_id]:
        neighbor_coord = node_positions[neighbor[0]]
        point_vector = neighbor_coord - coord
        point_vector_unit = point_vector / np.linalg.norm(point_vector)
        force += (point_vector - point_vector_unit *ideal_dist) * spring_const
    return  force

def apply_force_on_node(coord, velocity, force, drag, dt, mass=1):
    acceleration = force / mass
    velocity = (acceleration * dt + velocity) * drag
    coord += velocity*dt
    return coord, velocity
    
FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Define the adjacency list
adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())

node_positions = {}
for i, node in enumerate(adjacency_list.keys()):
    x = random.uniform(0, 1)  
    y = random.uniform(0, 1)
    
    node_positions[node] = (x, y)

fig, ax = plt.subplots()
plot_graph(ax, node_positions, adjacency_list)

plt.show()