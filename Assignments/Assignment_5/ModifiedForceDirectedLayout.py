import matplotlib.pyplot as plt
import pydot
import numpy as np
import json


class Point:
    """A point located at (x,y) in 2D space.
    """

    def __init__(self, x, y, payload=None):
        self.x, self.y = x, y
        self.payload = payload

    def __repr__(self):
        return "{}: {}".format(str((self.x, self.y)), repr(self.payload))

    def __str__(self):
        return "P({:.2f}, {:.2f})".format(self.x, self.y)

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            other_x, other_y = other
        return np.hypot(self.x - other_x, self.y - other_y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __truediv__(self, other: float):
        return Point(self.x / other, self.y / other, self.payload)
    
    def __mul__(self, other:float|int):
        return Point(self.x * other, self.y * other, self.payload)
    
    def __rmul__(self, other:float|int):
        return self * other

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    

class Node:

    def __init__(self, name, pos) -> None:
        self.name = name
        self.pos = Point(pos[0], pos[1])
        self.adjacent_nodes = {}
        self.weight = 1
        self.quadtree_pos = ""

    def add_adjacent(self, node_name, attrs=[None]):
        self.adjacent_nodes[node_name] = {}

        for attr in attrs:
            self.adjacent_nodes[node_name][attr] = attrs[attr]

    def calc_own_weight(self):
        self.weight = 1 + len(self.adjacent_nodes) / 2
        self.pos.payload = self.weight

    def print_self(self):
        print(f"Node {self.name} at position: \nx={self.pos[0]} \ny={self.pos[1]}")
        print(
            f"Connected to nodes: {list([key for key in self.adjacent_nodes.keys()])}"
        )
        print(f"Using weights: {[item for key, item in self.adjacent_nodes.items()]}")
        print("\n")

    def set_quad_pos(self, quad_pos: str):
        self.quadtree_pos = quad_pos


"""
Below all force-directed functions
"""


def plot_graph(nodes_dict: dict[str, Node], edge_list, ax, force_plot):
    x_poss = np.array([node.pos.x for name, node in nodes_dict.items()])
    y_poss = np.array([node.pos.y for name, node in nodes_dict.items()])
    names = np.array([name for name in nodes_dict.keys()])

    ax[0].set_title(f"Force directed graph, iteration {len(force_plot)}")
    ax[1].set_title("Total movement")
    ax[1].set_ylim(bottom=0.001, top=np.max(force_plot))
    ax[1].set_xlabel("Iterations")
    ax[1].set_ylabel("Sum speed of all particles")
    # ax[1].set_xscale("log")
    # ax[1].set_yscale("log")

    ax[0].set_xticks([])
    ax[0].set_yticks([])

    ax[0].scatter(x_poss, y_poss, c="red", s=100, zorder=3, alpha=0.7)

    # for xpos, ypos, name in zip(x_poss, y_poss, names):
    # ax[0].text(
    #     xpos, ypos - 0.04, name, c="black", fontsize=8, ha="center", va="center"
    # )

    for edge in edge_list:
        if (
            edge.get_source() not in nodes_dict
            or edge.get_destination() not in nodes_dict
        ):
            continue

        source_pos = nodes_dict[edge.get_source()].pos
        dest_pos = nodes_dict[edge.get_destination()].pos
        ax[0].plot(
            [source_pos.x, dest_pos.x],
            [source_pos.y, dest_pos.y],
            c="black",
            zorder=2,
            alpha=0.1,
        )

    ax[1].plot(range(len(force_plot)), np.array(force_plot), c="tab:blue")


def spring_embed_repulse(node1: Point, node2: Point, c_rep: float):
    point_vec = node1 - node2
    point_dist = node1.distance_to(node2)

    f_rep = c_rep / (point_dist * point_dist) * (point_vec / point_dist)
    return f_rep


def spring_embed_spring(node1: Point, node2: Point, c_spring: float, length: float):
    point_vec = node2 - node1
    point_dist = node1.distance_to(node2)

    f_spring = c_spring * point_dist * point_dist / length * (point_vec / point_dist)
    return f_spring


def frucht_rein_attract(node1: Point, node2: Point, length: float):
    point_vec = node2 - node1
    point_dist = node1.distance_to(node2)

    f_attract = point_dist * point_dist / length * (point_vec / point_dist)
    return f_attract


def frucht_rein_repulse(node1: Point, node2: Point, length: float):
    point_vec = node1 - node2
    point_dist = node1.distance_to(node2)

    f_repulse = length * length / point_dist * (point_vec / point_dist)
    return f_repulse


def update_sim(
    node_dict: dict[str, Node],
    c_spring: float = 2,
    length: float = .01,
    c_rep: float = 5,
    c_FP: float = 1,
    c_grav: float = .01,
    delta: float = 1,
):
    total_total_force = 0
    poss = np.array([[node.pos.x, node.pos.y] for name, node in node_dict.items()])
    area = 5 * 5
    cent_mass = Point(*np.array([np.mean(poss[0]), np.mean(poss[1])]))
    FP_length = abs(c_FP * np.sqrt(area / len(node_dict)) - length)

    for name, node in node_dict.items():
        total_force = Point(0.0, 0.0)
        for name_2 in node_dict.keys():
            if name_2 == name:
                continue
            if MODE == "SE":
                # if name_2 not in node.adjacent_nodes:
                total_force = total_force + spring_embed_repulse(
                    node_dict[name].pos, node_dict[name_2].pos, c_rep
                )
                if name_2 in node.adjacent_nodes:
                    total_force += total_force + spring_embed_spring(
                        node_dict[name].pos, node_dict[name_2].pos, c_spring, length
                    )
            elif MODE == "FR":
                if name_2 in node.adjacent_nodes:
                    total_force = total_force + frucht_rein_attract(
                        node_dict[name].pos, node_dict[name_2].pos, FP_length
                    )
                total_force = total_force + frucht_rein_repulse(
                    node_dict[name].pos, node_dict[name_2].pos, FP_length
                )
            else:
                raise NotImplementedError(f"Mode {MODE} does not exist!")

            if GRAVITY:
                grav_force = (
                    c_grav
                    * node.weight
                    * (cent_mass - node.pos)
                    / node.pos.distance_to(cent_mass)
                )
                total_force += grav_force
            if INERTIA:
                total_force /= node.weight**2
            node.pos += total_force * delta
            total_total_force = (
                total_total_force + total_force.distance_to(Point(0, 0)) * delta
            )
    return node_dict, total_total_force


def init_sim(G: pydot.Dot, cluster, init_mode="stoch") -> tuple[dict[str:Node], list]:

    print("Initializing nodes...")

    # # TODO: check whether we are working with a cluster or not (FOR NOW THIS CODE ASSUMES WE ALWAYS WORK WITH A CLUSTER)
    # node_list = []
    # edge_list = G.get_edge_list()
    # for cluster in G.get_subgraphs():
    #     node_list += [point.get_name() for point in cluster.get_node_list()]

    node_list = [point.get_name() for point in cluster.get_node_list()]
    edge_list = G.get_edge_list()

    # Initialize node positions
    start_poss = {}
    angle_list = np.linspace(0, 2 * np.pi - 0.05, len(node_list), endpoint=False)
    for i, node in enumerate(node_list):
        if init_mode == "stoch":
            x = np.random.rand() * 100
            y = np.random.rand() * 100
        elif init_mode == "circle":
            x = 10 * np.cos(angle_list[i])
            y = 10 * np.sin(angle_list[i])
        start_poss[node] = np.array([x, y])

    nodes_dict = {name: Node(name, start_poss[name]) for name in node_list}

    remaining_node_list = [point.get_name() for point in cluster.get_node_list()]
    temporal_binding_node_name = ""
    for edge in edge_list:
        source = edge.get_source()
        dest = edge.get_destination()
        attr = edge.get_attributes()

        # prevent non existing nodes from being processed
        if source not in node_list or dest not in node_list:
            continue

        nodes_dict[source].add_adjacent(dest, attr)
        nodes_dict[dest].add_adjacent(source, attr)

        temporal_binding_node_name = source

        # remove nodes that have edges
        if source in remaining_node_list:
            remaining_node_list.remove(source)
        if dest in remaining_node_list:
            remaining_node_list.remove(dest)

    # add temportal edges to get them to stay near the other nodes
    if len(remaining_node_list) > 0:
        # no nodes are bound, so pick random node to bind to
        if len(remaining_node_list) == len(node_list):
            temporal_binding_node_name = node_list[0]
            remaining_node_list.pop(0)

        for node_to_bind in remaining_node_list:
            nodes_dict[temporal_binding_node_name].add_adjacent(
                node_to_bind, {"edge_type": "support"}
            )

        temporal_nodes_to_bind = []
        temporal_binding_node = None
        for node in cluster.get_node_list():
            # node to bind to temporal binding node
            if node.get_name() in remaining_node_list:
                temporal_nodes_to_bind.append(node)
            # temporal binding node
            elif node.get_name() == temporal_binding_node_name:
                temporal_binding_node = node

        temporal_edges = []
        for temporal_node_to_bind in temporal_nodes_to_bind:
            temporal_edges.append(
                pydot.Edge(
                    temporal_binding_node,
                    temporal_node_to_bind,
                    ltail=temporal_binding_node.get_name(),
                    lhead=temporal_node_to_bind.get_name(),
                )
            )

        edge_list = edge_list + temporal_edges
        print(f"+{cluster.obj_dict['name']} [{remaining_node_list}]")

    for name, node in nodes_dict.items():
        node.calc_own_weight()

    return nodes_dict, edge_list


def export_node_positions(nodes_dict: dict[str, Node], path):
    export_dict = {
        node_name: [node.pos.x, node.pos.y] for node_name, node in nodes_dict.items()
    }
    with open(path, "w") as fp:
        json.dump(export_dict, fp, indent=3)


def renderNodePositions(FILE_NAME, number_of_sims):
    if __name__ == "__main__":

        print("Reading file...")

        
        print("Read file")
        for cluster in G.get_subgraphs():
            nodes_dict, edges_list = init_sim(G, cluster, init_mode="stoch")

            file_name = cluster.obj_dict["name"].replace('"', "").replace(" ", "_")
            folder = FILE_NAME.split(".")[0].split("/")[1]
            
            print(folder, file_name)
            
            path = f"Assignments/Assignment 5/nodePositions/{folder}/{file_name}.json"

            fig, ax = plt.subplots(1, 2, figsize=(10, 6))
            tot_force_plot = []

            for i in range(number_of_sims):
                delta_t = 1 / (i * i * i + 100) + 0.001
                delta = [DT, delta_t][DELTA_TIME]

                # if i == 0:
                #     fig.savefig("Assignments/Assignment 3/StartPosition.png")

                node_positions, tot_force = update_sim(
                    nodes_dict,
                    c_rep=4,
                    c_spring=4,
                    length=10,
                    c_grav=0.001,
                    delta=delta,
                )
                tot_force_plot.append(tot_force / len(nodes_dict))
                ax[0].cla()
                ax[1].cla()
                plot_graph(nodes_dict, edges_list, ax, tot_force_plot)

                fig.tight_layout()
                plt.pause(0.01)
                if i % 50 == 0:
                    # fig.savefig(f"Assignments/Assignment 3/Iteration{i}.png")
                    # export_node_positions(nodes_dict, path)
                    print(f"+{cluster.obj_dict['name']} [JSON]")
                if tot_force / len(nodes_dict) < .1:
                    # fig.savefig(f"Assignments/Assignment 3/FinalPosition.png")
                    print(f"+{cluster.obj_dict['name']} [JSON][end]")
                    break
            export_node_positions(nodes_dict, path)
        plt.show()


DELTA_TIME = False
MODE = "SE"  # Out of SE (Spring-Embedder), FR (Fruchterman and Reingold)
INERTIA = True
GRAVITY = True

DT = .01

# generates a subfolder with json clusters
FILE_NAME = "Networks/ArgumentationNetwork.dot"

# TODO: get this one to work
# FILE_NAME = "Networks/newBlogosphere.dot"

G = pydot.graph_from_dot_file(FILE_NAME)[0]

number_of_sims = 200  # 5000

renderNodePositions(FILE_NAME, number_of_sims)