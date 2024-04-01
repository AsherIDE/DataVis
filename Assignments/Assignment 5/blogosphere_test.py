import matplotlib.pyplot as plt
import pydot
import numpy as np
import json

# FILE_NAME = "Networks/ArgumentationNetwork.dot"

FILE_NAME = "Networks/BlogosphereNetwork.dot"
G = pydot.graph_from_dot_file(FILE_NAME)[0]

nodes_list = G.get_node_list()
edges_list = G.get_edge_list()

print(nodes_list)

new_G = pydot.Dot(graph_type='digraph', compound='true')

cluster_left=pydot.Cluster('Left',label='Left')
cluster_right=pydot.Cluster('right', label='right')
new_G.add_subgraph(cluster_left)
new_G.add_subgraph(cluster_right)

for node in nodes_list:
    match node.get_attributes()['value']:
        case '0':
            cluster_left.add_node(node)
        case '1':
            cluster_right.add_node(node) 
            
def find_clusters(edge):
    cluster_dict = {
        '0' : cluster_left,
        '1' : cluster_right
    }
    
    start_value = edge.get_source()
    end_value = edge.get_destination().get_attributes()['value']
    return cluster_dict[start_value], cluster_dict[end_value]
    

for edge in edges_list:
    new_G.add_edge(pydot.Edge(edge.get_source(), edge.get_destination()))

new_G.write("newBlogosphere.dot")        
# for subgraph in new_G.get_subgraphs():
#     print(subgraph)