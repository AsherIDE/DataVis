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


def plot_graph(nodes_dict: dict[str, Node], edge_list, ax, force_plot):
    x_poss = np.array([node.pos.x for name, node in nodes_dict.items()])
    y_poss = np.array([node.pos.y for name, node in nodes_dict.items()])

    ax[0].set_title(f"Force directed graph, iteration {len(force_plot)}")
    ax[1].set_title("Total movement")
    ax[1].set_ylim(bottom=0.001, top=np.max(force_plot))
    ax[1].set_xlabel("Iterations")
    ax[1].set_ylabel("Sum speed of all particles")
    ax[1].set_xscale("log")
    ax[1].set_yscale("log")
    
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    ax[0].scatter(x_poss, y_poss, c="red", s=100, zorder=3)

    # for xpos, ypos, name in zip(x_poss, y_poss, names):
        # ax[0].text(
        #     xpos, ypos - 0.04, name, c="black", fontsize=8, ha="center", va="center"
        # )

    for edge in edge_list:
        source_pos = nodes_dict[edge.get_source()].pos
        dest_pos = nodes_dict[edge.get_destination()].pos
        ax[0].plot([source_pos.x, dest_pos.x], [source_pos.y, dest_pos.y], c="black", zorder=2, alpha=0.1)

    ax[1].plot(range(len(force_plot)), np.array(force_plot), c="tab:blue")


def spring_embed_repulse(node1: Point, node2: Point, c_rep: float):
    point_vec = node1 - node2
    point_dist = node1.distance_to(node2)

    f_rep = c_rep / (point_dist * point_dist) * (point_vec / point_dist)
    return f_rep


def spring_embed_spring(
    node1: Point, node2: Point, c_spring: float, length: float
):
    point_vec = node2 - node1
    point_dist = node1.distance_to(node2)

    f_spring = c_spring * np.log(point_dist / length) * (point_vec / point_dist)
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
    length: float = 2,
    c_rep: float = 1,
    c_FP: float = 1,
    c_grav: float = 1,
    delta: float = 1,
    MODE='FR'
):
    total_total_force = 0
    poss = np.array([[node.pos.x, node.pos.y] for name, node in node_dict.items()])
    area = 5 * 5
    cent_mass = Point(*np.array([np.mean(poss[0]), np.mean(poss[1])]))
    FP_length = abs(c_FP * np.sqrt(area / len(node_dict)) - length)

    for name, node in node_dict.items():
        total_force = Point(0.0,0.0)
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

            if GRAVITY:
                grav_force = (
                    c_grav
                    * node.weight
                    * (cent_mass - node.pos)
                    / node.pos.distance_to(cent_mass)
                )
                total_force += grav_force
            if INERTIA:
                total_force /= node.weight
            node.pos += total_force * delta
            total_total_force = total_total_force + total_force.distance_to(Point(0,0)) * delta
    return node_dict, total_total_force


def init_sim(G: pydot.Dot, init_mode="stoch") -> tuple[dict[str:Node], list]:

    print("Initializing nodes...")

    node_list = [point.get_name() for point in G.get_node_list()]
    edge_list = G.get_edge_list()

    # Initialize node positions
    start_poss = {}
    angle_list = np.linspace(0, 2 * np.pi - 0.05, len(node_list), endpoint=False)
    for i, node in enumerate(node_list):
        if init_mode == "stoch":
            x = np.random.rand() * 10
            y = np.random.rand() * 10
        elif init_mode == "circle":
            x = 10 * np.cos(angle_list[i])
            y = 10 * np.sin(angle_list[i])
        start_poss[node] = np.array([x, y])

    nodes_dict = {name: Node(name, start_poss[name]) for name in node_list}

    for edge in edge_list:
        source = edge.get_source()
        dest = edge.get_destination()
        attr = edge.get_attributes()

        nodes_dict[source].add_adjacent(dest, attr)
        nodes_dict[dest].add_adjacent(source, attr)

    for name, node in nodes_dict.items():
        node.calc_own_weight()

    return nodes_dict, edge_list

def export_node_positions(nodes_dict: dict[str, Node]):
    export_dict = {
        node_name: [node.pos.x, node.pos.y] for node_name, node in nodes_dict.items()
    }
    with open('node_positions.json', 'w') as fp:
        json.dump(export_dict, fp, indent=3)


# if __name__ == "__main__":
# MODE = "FR"  # Out of SE (Spring-Embedder), FR (Fruchterman and Reingold)
INERTIA = True
GRAVITY = True

def drawForceDirected(FILE_NAME, number_of_sims=5000, MODE='FR'):
    FILE_NAME = f'Networks/{FILE_NAME}.dot'

    DELTA_TIME = False

    match MODE:
        case "FR":
            DT = 0.01
        case "SE":
            DT = 1

    print("Reading file...")
    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    nodes_dict, edges_list = init_sim(G, init_mode="stoch")

    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    tot_force_plot = []

    for i in range(number_of_sims):
        delta_t = 1 / (i * i * i + 100) + 0.001
        delta = [DT, delta_t][DELTA_TIME]
        
        # if i == 0:
        #     fig.savefig("Assignments/Assignment 3/StartPosition.png")
        
        node_positions, tot_force = update_sim(
            nodes_dict, c_rep=1, c_spring=2, length=10, c_grav=0.0001, delta=delta, MODE=MODE
        )
        tot_force_plot.append(tot_force / len(nodes_dict))
        ax[0].cla()
        ax[1].cla()
        plot_graph(nodes_dict, edges_list, ax, tot_force_plot)
        # export_node_positions(nodes_dict)
        # fig.tight_layout()
        plt.pause(0.01)
        # if i % 50 == 0:
        #     fig.savefig(f"Assignments/Assignment 3/Iteration{i}.png")
        if tot_force / len(nodes_dict) < .42:
            # fig.savefig(f"Assignments/Assignment 3/FinalPosition.png")
            break

    plt.show()

# TEST
# FILE_NAME = "JazzNetwork"
# FILE_NAME = 'LeagueNetwork'
# FILE_NAME = "SmallDirectedNetwork"
# FILE_NAME = "LesMiserables"

# drawForceDirected(FILE_NAME)