import json
import pydot
import math
import os

import numpy as np
import matplotlib.pyplot as plt

from typing import List
from dataclasses import dataclass

@dataclass
class Cluster:
    name: str

    # list index connects both lists
    nodes: List
    coordinates: List

@dataclass
class Ellipse:
    name: str
    width: int
    height: int
    x_center: int
    y_center: int
    angle: int

# combines cluster json files into one
def combineJSON(path):
    nodes_dict = {}
    file_name = path.split("/")[-1]

    offset_x = 0
    offset_y = 0

    # combine all clusters into one dict again
    for positions_path in os.listdir(path):
        with open(os.path.join(path, positions_path)) as json_file:
            json_file_dict = json.load(json_file)

            max_x, max_y = 0, 0
            min_x, min_y = 0, 0
            for name, coords in json_file_dict.items():
                nodes_dict[name] = [coords[0] + offset_x, coords[1] + offset_y]

                if coords[0] > max_x:
                    max_x = coords[0]
                elif coords[0] < min_x:
                    min_x = coords[0]

                if coords[1] > max_y:
                    max_y = coords[1]
                elif coords[1] < min_y:
                    min_y = coords[1]

            height = max_y - min_y
            width = max_x - min_x

        if offset_x > 300:
            offset_x = 0
            offset_y += height
        else:
            offset_x += width
            offset_y += height

    output_path = f"Assignments/Assignment 5/nodePositions/Overall/{file_name}.json"
    with open(output_path, 'w') as fp:
        json.dump(nodes_dict, fp, indent=3)

    return output_path

"""
- get node coords
- group every node within their corresponding clusters
- find min and max x and y to gain box dimensions
- return box dimensions
"""

# positions json file, graph --> list of clusters
def getClusters(positions_path, G):
    with open(positions_path) as json_file:
        positions_dict = json.load(json_file)

        # create a list of clusters
        clusters = []
        for cluster in G.get_subgraphs():
            cluster_nodes = [point.get_name() for point in cluster.get_node_list()]

            # get coords for each cluster node
            cluster_nodes_coords = []
            for cluster_node in cluster_nodes:
                cluster_nodes_coords.append(positions_dict[cluster_node])

            # append cluster to clusters list
            clusters.append(Cluster(cluster.obj_dict['name'], cluster_nodes, cluster_nodes_coords))

    return clusters

# list of clusters --> list of ellipses
def getClusterBoxCoords(clusters):

    # returns angle from a list of x's and y's
    def linearRegression(xs, ys):
        x_mean = sum(xs) / len(xs)
        y_mean = sum(ys) / len(ys)

        # get offsets from mean
        x_mean_offsets = [x - x_mean for x in xs]
        y_mean_offsets = [y - y_mean for y in ys]

        # get angle
        xy_offsets = [x_mean_offset * y_mean_offset for x_mean_offset, y_mean_offset in zip(x_mean_offsets, y_mean_offsets)]
        x_squared_mean_offsets = [x_mean_offset ** 2 for x_mean_offset in x_mean_offsets]

        angle = sum(xy_offsets) / sum(x_squared_mean_offsets)

        # print(angle, "--->", math.degrees(angle))

        return angle, x_mean, y_mean

    ellipses = []
    for cluster in clusters:
        
        # get list of all x's and y's
        xs = [coord[0] for coord in cluster.coordinates]
        ys = [coord[1] for coord in cluster.coordinates]

        # get cluster width and height
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        # print(xs, "\n", max(xs), min(xs), width, "\n\n\n")

        # get cluster angle
        angle, x_mean, y_mean = linearRegression(xs, ys)

        # Account for multiple solutions of arctan
        # if angle < -45: angle += 90
        # elif angle > 45: angle -= 90

        # print(f"w: {width*2.5}, h: {height*2.5}, a:{angle}")
        ellipses.append(Ellipse(cluster.name, width, height, x_mean, y_mean, angle))

    return ellipses

# configure the input so that it can be used for matplotlib
def drawEllipse(x, y, width, height, angle):
    t = np.linspace(0, 2*math.pi, 100)
    Ell = np.array([width * np.cos(t) , height * np.sin(t)])  
    
    # center x and y removed to keep the same center location
    R_rot = np.array([[math.cos(angle) , -math.sin(angle)],[math.sin(angle) , math.cos(angle)]])  

    Ell_rot = np.zeros((2,Ell.shape[1]))
    for i in range(Ell.shape[1]):
        Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])

    return x+Ell_rot[0,:], y+Ell_rot[1,:]

def drawGraph(G, clusters, ellipses, circlesize=100, fontsize=6):
    colors = ["#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6", "#325A9B", "#EECA3B", "#FECB52", "#00CC96", "#636EFA", "#19D3F3", "#0D2A63", "#AB63FA", "#FF6692", "#BAB0AC", "#EF553B", "#6A76FC", "#E45756", "#479B55", "#72B7B2", "#1CBE4F", "#FF97FF", "#FF8000", "#B82E2E", "#FFA15A", "#54A24B", "#1C8356", "#FBE426", "#B6E880", "#AF0033", "#0099C6"]
    edge_list = G.get_edge_list()

    # draw all nodes
    coords_dict = {}
    for idx, cluster in enumerate(clusters):

        # group node with corresponding coord and draw it
        for node, position in zip(cluster.nodes, cluster.coordinates):
            plt.scatter(position[0], position[1], color=colors[idx], zorder=3, s=circlesize, alpha=0.7)
            # plt.text(position[0], position[1]-0.02, node, fontsize=fontsize, ha='center', va='bottom', zorder=4, color='black')

            coords_dict[node] = position

    # draw all edges
    for edge in edge_list:

        plt.plot([coords_dict[edge.get_source()][0], coords_dict[edge.get_destination()][0]],
                [coords_dict[edge.get_source()][1], coords_dict[edge.get_destination()][1]], color="black", zorder=2, alpha=0.1)
        
    # draw ellipses
    for ellipse in ellipses:

        # if ellipse.name == '"Youngest Devonian Strata"' or ellipse.name == '"Gap in the Sequence of Devonshi"':
            l, r = drawEllipse(ellipse.x_center, ellipse.y_center, ellipse.width / 2, ellipse.height / 2, ellipse.angle)
        
            plt.plot(l, r, 'darkorange')

    plt.title('Clustered Visualization')
    plt.xticks([])
    plt.yticks([])

    plt.show()

if __name__ == "__main__":
    # TODO: get this one to work
    FILE_NAME = "Networks/newBlogosphere.dot"

    # combine all cluster json files into one and get the filepath
    # FILE_NAME = "Networks/ArgumentationNetwork.dot"
    # path = combineJSON("Assignments/Assignment 5/nodePositions/ArgumentationNetwork")
    path = combineJSON("Assignments/Assignment 5/nodePositions/newBlogosphere")

    # path = "Assignments/Assignment 5/nodePositions/Overall/ArgumentationNetwork.json"

    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    clusters = getClusters(path, G)
    ellipses = getClusterBoxCoords(clusters)

    drawGraph(G, clusters, ellipses)