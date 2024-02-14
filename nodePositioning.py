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

# def return_gravity_displacement(coord, cent=np.array([0.5, 0.5]), gravity_str = 0.02):
#     vec_to_center = cent - coord
#     vec_to_center = vec_to_center 
#     ds = vec_to_center * gravity_str
#     return ds

# def return_coulombs_displacement(coord, node_list, adjacency_list, node_id, threshold_value):
#     disp = np.array([0.0, 0.0])
#     for (node_id, node) in node_list.items():
#         ds = coord - node
#         if np.array_equal(ds, [0,0]):
#             continue
#         elif(np.linalg.norm(ds) < threshold_value):
#             ds_unit = ds / np.linalg.norm(ds)
#             repel_strength = np.power(np.linalg.norm(ds), -2)
#             if repel_strength>100:
#                 repel_strength = 100
#             disp += ds_unit * repel_strength 
#         else:
#             continue
#     return disp 

# def return_spring_displacement(coord, node_id, coord_list, adjacency_list:dict, spring_coeff, ideal_dist):
#     disp = np.array([0.0,0.0])
#     if len(adjacency_list[node_id]) == 0:
#         return disp
#     for neighbor in adjacency_list[node_id]:
#         neighbor_coord = coord_list[neighbor[0]]
#         point_vector = neighbor_coord - coord
#         point_vector_unit = point_vector / np.linalg.norm(point_vector)
#         disp += point_vector - point_vector_unit *ideal_dist
#     return disp * spring_coeff 

# def update_simulation(
#     adjacency_list:dict, coords_list:dict, 
#     grav_coeff = .0001, 
#     spring_coeff = 0.02, 
#     coulomb_thresh = 1.25,
#     coulomb_coeff = 0.00005,
#     ideal_spring_dist = 0.2
#     ):
#     gravity_displacements = np.array([return_gravity_displacement(np.array(coord), gravity_str=grav_coeff) for _, coord in coords_list.items()])
#     coulomb_displacements = np.array([return_coulombs_displacement(np.array(coord), coords_list, adjacency_list, node_id, coulomb_thresh) for node_id, coord in coords_list.items()])
#     spring_displacements = np.array([return_spring_displacement(np.array(coord), node_id, coords_list, adjacency_list, spring_coeff, ideal_spring_dist) for node_id, coord in coords_list.items()])
    
#     total_displacements = np.zeros((len(coords_list), 2))
#     total_displacements += gravity_displacements 
#     total_displacements += coulomb_displacements*coulomb_coeff
#     total_displacements += spring_displacements
    
#     for node, disp in zip(coords_list.keys(), total_displacements):
#         coords_list[node] += disp
#     return coords_list

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

def update_physics_sim(
    node_positions:dict, 
    adjacency_list:dict,
    velocity_list: dict  = None,
    grav_coeff=0.01,
    coulomb_coeff = .001,
    spring_const = 0.1,
    ideal_dist = 5.0,
    drag=0.9,
    dt=0.01
    ):
    total_forces = {}
    if velocity_list is None:
        velocity_list = {}
        for node in node_positions:
            velocity_list[node] = [0.0,0.0]
    for node in node_positions:
        total_forces[node] = [0.0,0.0]

    grav_forces = np.array([return_gravity_force(np.array(coord), 1, grav_coeff) for _, coord in node_positions.items()])
    coulomb_forces = np.array([return_coulomb_force(np.array(coord), node_positions, coulomb_coeff) for _, coord in node_positions.items()])
    spring_forces = np.array([return_spring_force(np.array(coord), node, node_positions, adjacency_list, spring_const, ideal_dist) for node, coord in node_positions.items()])
        
    for i, node in enumerate(total_forces):
        total_forces[node] += grav_forces[i]
        total_forces[node] += coulomb_forces[i]
        total_forces[node] += spring_forces[i]
    
    for node_key, node_vel_key, force_key in zip(node_positions, velocity_list, total_forces):
        new_pos, new_vel = apply_force_on_node(node_positions[node_key], velocity_list[node_vel_key], total_forces[force_key], drag=drag, dt=dt)
        node_positions[node_key] = new_pos
        velocity_list[node_vel_key] = new_vel
    
    return node_positions, velocity_list
    
    
    

FILE_NAME = 'Networks/LesMiserables.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

# Define the adjacency list
adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())

node_positions = {}
angle_list = np.linspace(0, 2*np.pi - 0.05, len(adjacency_list.keys()))
for i, node in enumerate(adjacency_list.keys()):
    # x = random.uniform(0, 1)  
    # y = random.uniform(0, 1)
    
    x = np.cos(angle_list[i])
    y = np.sin(angle_list[i])
    
    node_positions[node] = (x, y)

number_of_sims = 5000
velocities = None

# fig, ax = plt.subplots(number_of_sims, figsize=(3, 3*number_of_sims))
fig, ax = plt.subplots()
for i in range(number_of_sims):
    ax.clear()
    node_positions, velocities = update_physics_sim(node_positions, adjacency_list, velocities)
    if i%10 == 0:
        plot_graph(ax, node_positions, adjacency_list)
        plt.pause(0.01)

plt.show()