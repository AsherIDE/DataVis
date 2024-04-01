import numpy as np
import matplotlib.pyplot as plt
from clusterMarking import getClusters, combineJSON
import pydot
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.measurement import distance
from tqdm import tqdm

colors = [
    "#325A9B",
    "#EECA3B",
    "#FECB52",
    "#00CC96",
    "#636EFA",
    "#19D3F3",
    "#0D2A63",
    "#AB63FA",
    "#FF6692",
    "#BAB0AC",
    "#EF553B",
    "#6A76FC",
    "#E45756",
    "#479B55",
    "#72B7B2",
    "#1CBE4F",
    "#FF97FF",
    "#FF8000",
    "#B82E2E",
    "#FFA15A",
    "#54A24B",
    "#1C8356",
    "#FBE426",
    "#B6E880",
    "#AF0033",
    "#0099C6",
    "#325A9B",
    "#EECA3B",
    "#FECB52",
    "#00CC96",
    "#636EFA",
    "#19D3F3",
    "#0D2A63",
    "#AB63FA",
    "#FF6692",
    "#BAB0AC",
    "#EF553B",
    "#6A76FC",
    "#E45756",
    "#479B55",
    "#72B7B2",
    "#1CBE4F",
    "#FF97FF",
    "#FF8000",
    "#B82E2E",
    "#FFA15A",
    "#54A24B",
    "#1C8356",
    "#FBE426",
    "#B6E880",
    "#AF0033",
    "#0099C6",
]

# Edge = (n, (x,y))


def subdivide(edge, n):
    line = LineString(edge)
    distances = np.linspace(0, line.length, n)
    points = [line.interpolate(distance) for distance in distances]
    edge = np.array([point.xy for point in points])
    return np.squeeze(edge)


def merge_clusters(clusters):
    coords_dict = {}
    for cluster in clusters:
        for node, position in zip(cluster.nodes, cluster.coordinates):
            coords_dict[node] = position
    return coords_dict


def plot_straight_graph(ax, clusters: dict, edges_list):
    coords_dict = merge_clusters(clusters)
    for idx, cluster in enumerate(clusters):
        for node, coord in zip(cluster.nodes, cluster.coordinates):
            ax.scatter(coord[0], coord[1], alpha=0.7, color=colors[idx], zorder=3)
    for edge in edge_list:
        ax.plot(
            [coords_dict[edge.get_source()][0], coords_dict[edge.get_destination()][0]],
            [coords_dict[edge.get_source()][1], coords_dict[edge.get_destination()][1]],
            color="black",
            zorder=2,
            alpha=0.1,
        )


def plot_curve_graph(ax, clusters: dict, edge_obj_list: np.ndarray):
    for idx, cluster in enumerate(clusters):
        for node, coord in zip(cluster.nodes, cluster.coordinates):
            ax.scatter(coord[0], coord[1], alpha=0.7, color=colors[idx], zorder=3)
    for edge in edge_obj_list:
        ax.plot(
            [point[0] for point in edge],
            [point[1] for point in edge],
            color="black",
            zorder=2,
            alpha=0.1,
        )
        # ax.scatter(
        #     [point[0] for point in edge[1:-1]],
        #     [point[1] for point in edge[1:-1]],
        #     color="green",
        #     zorder=3,
        #     alpha=0.7,
        # )


def edge_as_vector(edge):
    return Point(
        edge.end_pos[0] - edge.start_pos[0], edge.end_pos[1] - edge.start_pos[1]
    )


def comp_dist(edge_1, edge_2, avg_len: float):
    midP = Point(
        (edge_1[0][0] + edge_1[-1][0]) / 2.0, (edge_1[0][1] + edge_1[0][1]) / 2.0
    )
    midQ = Point(
        (edge_2.start_pos[0] + edge_2.end_pos[0]) / 2.0,
        (edge_2.start_pos[1] + edge_2.end_pos[1]) / 2.0,
    )
    return avg_len / (avg_len + distance(midP, midQ))


def calc_compatibility(edge_1, edge_2):

    avg_len = (edge_1.length + edge_2.length) / 2

    # Angle compatibility
    comp_angle = abs(np.cos(np.arccos(edge_1.unit_vector.dot(edge_2.unit_vector))))

    # Scale compatibility
    comp_scale = 2 / (
        avg_len * min(edge_1.length, edge_2.length)
        + max(edge_1.length, edge_2.length) / avg_len
    )

    # Distance compatibility
    comp_dist_coeff = comp_dist(edge_1, edge_2, avg_len)

    return comp_angle * comp_scale * comp_dist_coeff


def construct_compatibility_matrix(
    edge_list: np.ndarray,
) -> dict[str, dict[str, float]]:
    vector_array = edge_list[:, -1] - edge_list[:, 0]
    unit_vector_array = np.linalg.norm(vector_array, axis=1, keepdims=True)

    midpoint_matrix = (unit_vector_array + unit_vector_array.T) / 2
    midpoint_array = (edge_list[:, 0] + edge_list[:, -1]) / 2
    midpoint_dist = np.linalg.norm(
        midpoint_array[None, :] - midpoint_array[:, None], axis=-1
    )

    # Angle compatibility
    angle_comp = np.abs(
        (vector_array @ vector_array.T)
        / (unit_vector_array @ unit_vector_array.T + 1e-8)
    )
    scale_comp = 2 / (
        midpoint_matrix / (np.minimum(unit_vector_array, unit_vector_array.T) + 1e-8)
        + np.maximum(unit_vector_array, unit_vector_array.T) / (midpoint_matrix + 1e-8)
        + 1e-8
    )
    dists_comp = midpoint_matrix / (midpoint_matrix + midpoint_dist + 1e-8)

    # No visibility compatibility, sorry
    print(np.sum(angle_comp), np.sum(scale_comp), np.sum(dists_comp))

    return angle_comp * scale_comp * dists_comp


def calc_spring_forces(edge, k_c) -> list[Point]:
    edge_midpoints_array = np.squeeze(np.array([point.xy for point in edge.points]))
    force_per_point = []
    for idx, point in enumerate(edge_midpoints_array[1:-1]):
        i = idx + 1
        force_vec = (edge_midpoints_array[i] - edge_midpoints_array[i - 1]) + (
            edge_midpoints_array[i] - edge_midpoints_array[i + 1]
        )
        force = force_vec / 2 * k_c
        force_per_point.append(force)
    return np.array(force_per_point)


def calc_attr_forces(point1: Point, point2: Point):
    point1_arr = np.array(point1.xy)
    point2_arr = np.array(point2.xy)

    unit_vec = (point2_arr - point1_arr) / distance(point1, point2)

    if distance(point1, point2) > 10:
        return np.squeeze(unit_vec)
    else:
        return np.array([0.0, 0.0])


def calc_update(edge_list: list, comp_matrix, spring_const):
    spring_dist_l = edge_list[:, :-1] - edge_list[:, 1:]
    spring_dist_l = np.concatenate(
        [np.zeros((spring_dist_l.shape[0], 1, spring_dist_l.shape[-1])), spring_dist_l],
        axis=1,
    )
    spring_dist_r = edge_list[:, 1:] - edge_list[:, :-1]
    spring_dist_r = np.concatenate(
        [spring_dist_r, np.zeros((spring_dist_l.shape[0], 1, spring_dist_l.shape[-1]))],
        axis=1,
    )

    spring_force_l = np.sum(spring_dist_l**2, axis=-1, keepdims=True)
    spring_force_r = np.sum(spring_dist_r**2, axis=-1, keepdims=True)
    
    SPRING_FORCE = spring_const * (spring_force_l * spring_dist_l + spring_force_r * spring_dist_r)
    
    electro_dist = edge_list[:, None, ...] - edge_list[None, ...]
    electro_force = comp_matrix[..., None] / (np.linalg.norm(electro_dist, axis=-1) + 1e-8)
    
    ELECTRO_FORCE = np.sum(electro_force[..., None] * electro_dist, axis=0)
    
    FORCE_FORCE = SPRING_FORCE + ELECTRO_FORCE
    
    FORCE_FORCE[:,0,:] = FORCE_FORCE[:,-1,:] = 0

    return FORCE_FORCE


def return_intra_cluster_edges(edge_list, clusters):
    all_edge_list = []
    comp_edge_list = []

    for idx, pydot_edge in enumerate(edge_list):
        source_node, dest_node = pydot_edge.get_source(), pydot_edge.get_destination()
        all_edge_list.append([coords_dict[source_node], coords_dict[dest_node]])

        # print(pydot_edge.get_source(), pydot_edge.get_destination())
        for cluster in clusters:
            if source_node in cluster.nodes:
                if dest_node in cluster.nodes:
                    pass
                else:
                    comp_edge_list.append(
                        [coords_dict[source_node], coords_dict[dest_node]]
                    )
            else:
                continue
            # print("No cluster found!!!")

    return np.array(comp_edge_list), np.array(all_edge_list)


FILE_NAME = "Networks/ArgumentationNetwork.dot"
# FILE_NAME = "Networks/newBlogosphere.dot"
path = combineJSON("Assignments/Assignment 5/nodePositions/ArgumentationNetwork")
G = pydot.graph_from_dot_file(FILE_NAME)[0]
DT = .004

edge_list = G.get_edge_list()

clusters = getClusters(path, G)

coords_dict = merge_clusters(clusters)

comp_edge_list, curve_edge_list = return_intra_cluster_edges(edge_list, clusters)
comp_edge_list = np.array([subdivide(edge, 5) for edge in comp_edge_list])

comp_matrix = construct_compatibility_matrix(comp_edge_list)

comp_matrix = (comp_matrix > .2).astype(np.float32)

print(np.sum(comp_matrix))

fig, ax = plt.subplots()

plot_curve_graph(ax, clusters, curve_edge_list)

fig.savefig("FirstFrame")
plt.pause(0.1)

for iteration in range(100):
    DT = DT * .5
    print(f"Iteration {iteration}")
    ax.cla()
    comp_edge_list = np.array([subdivide(edge, 5 + iteration) for edge in comp_edge_list])

    for j in range(50):
        FORCES = calc_update(comp_edge_list, comp_matrix, 0.0004)
        comp_edge_list += FORCES * DT
    plot_curve_graph(ax, clusters, comp_edge_list)
    fig.savefig("CurrentFrame")
    plt.pause(0.1)


plt.show()
