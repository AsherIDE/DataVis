import numpy as np
import matplotlib.pyplot as plt
from ReadDotFile import CreateAdjacencyList

def UnpackAdjacencyList(adjacency_list: dict)->tuple[np.ndarray, np.ndarray]:
    verts = np.array([int(key) for key in adjacency_list])
    edges = []
    for key, edge_list in adjacency_list.items():
        for edge in edge_list:
            edges.append([key, edge])
    return verts, np.array(edges)

def CreateSubtree(verts: np.ndarray, edges:np.ndarray)-> dict:
    cleared_nodes = []
    subtree_edges = {}
    
    for edge in edges:
        if edge[0] in cleared_nodes and edge[1] in cleared_nodes:
            continue
        elif edge[0] in cleared_nodes: 
            cleared_nodes.append(edge[1])
        elif edge[1] in cleared_nodes:
            cleared_nodes.append(edge[0])
        else:
            cleared_nodes.append(edge[0])
            cleared_nodes.append(edge[1])
            
        if edge[0] not in subtree_edges:
            subtree_edges[edge[0]] = edge[1]
        else:
            subtree_edges[edge[1]] = edge[0]

    return verts, subtree_edges

def findDFSOrder(edges:np.ndarray, node:str, mode:str='pre')->np.ndarray:
    subtree_verts, subtree_edges = CreateSubtree(*UnpackAdjacencyList(edges))
    
    visited_nodes = []
    # depth_list = []
    backtrack = []
    out_list = []
    selected_node = node
    found_child = False
    depth=0
    
    def find_connected(edges, node, parent_nodes):
        if len(parent_nodes) == 0:
            parent_nodes = [0]
            
        connected_nodes = []
        for node_current, neighbor in edges.items():
            if node_current  == node and neighbor != parent_nodes[-1]:
                connected_nodes.append(neighbor)
            elif neighbor == node and node_current != parent_nodes[-1]:
                connected_nodes.append(node_current)
        return connected_nodes
    
    if mode == 'pre':
        while len(visited_nodes) < len(subtree_edges) + 1:
            found_child = False
            if selected_node not in visited_nodes:
                visited_nodes.append(selected_node)
                # depth_list.append(depth)
            if selected_node in subtree_edges:
                child_nodes = find_connected(subtree_edges, selected_node, backtrack)
            # if len(child_nodes) > 0:
                for child_node in child_nodes:
                    if child_node in visited_nodes:
                        continue
                    out_list.append((selected_node, child_node))
                    backtrack.append(selected_node)
                    selected_node = child_node
                    depth += 1
                    found_child = True
                    break
                if not found_child:
                    selected_node = backtrack[-1]
                    depth -= 1
                    backtrack.pop(-1)
            else:
                selected_node = backtrack[-1]
                depth -= 1
                backtrack.pop(-1)
    return out_list
                
def RadialGraph(DFS_order, subtree_edges, mode='pre'):
    coords = {}
    spiral_count = 0
    depth_angle_dict = {}
    for i, node in enumerate(DFS_order):
        sub_nodes = []
        subtree_len = 0
        for next_node in DFS_order[i:]:
            # print(next_node, node)
            if next_node[0] == node[0]:
                continue
            if next_node[1]  <= node[1]:
                break
            if next_node[1] == node[1] + 1:
                sub_nodes.append(next_node)
            if next_node[1] > node[1]:
                subtree_len += 1
        if len(sub_nodes) > 0:
            if node[1] == 0:
                coords[node[0]] = (0.0,0.0)
                arc = [0, 2*np.pi]
                angle_distr = np.linspace(arc[0], arc[1], len(sub_nodes), endpoint=False)
                node_angle = 0
            else:
                node_angle = np.arctan2(coords[node[0]][1], coords[node[0]][0])
                if node_angle < 0:
                    node_angle = 2*np.pi + node_angle
                print(node_angle)
                if node[1] not in depth_angle_dict:
                    right_bound = node_angle -np.pi/7
                else:
                    right_bound = depth_angle_dict[node[1]]
                left_bound = node_angle + np.arccos(node[1] / (node[1]+1)) * 0.9
                right_tangent = node_angle - np.arccos(node[1] / (node[1]+1))
                right_bound = max(right_bound, right_tangent)
                depth_angle_dict[node[1]] = left_bound
                # tau1 = np.arccos(node[1] / (node[1]+1))
                # tau2 = subtree_len / (coords[node[0]][2] - 1)
                # tau = min(tau1, tau2)
                angle_distr = np.linspace(right_bound, left_bound, len(sub_nodes), endpoint=False)
                
            for j, (angle, child_node) in enumerate(zip(angle_distr, sub_nodes)):
                coords[child_node[0]] = (np.cos(angle) * (node[1]*5+10), 
                                      np.sin(angle) * (node[1]*5+10),
                                      subtree_len)
                spiral_count += 1
            #  else:
    
    return coords

def PlotRadialGraph(coords, subtree_edges):
    fig, ax = plt.subplots(figsize=(8,8))
    coords_array = np.array([item for key, item in coords.items()])
    ax.set_aspect('equal')
    for edge, (neighbor, weight) in subtree_edges.items():
        coord1 = coords[edge]
        coord2 = coords[neighbor]
        ax.plot([coord1[0], coord2[0]], [coord1[1], coord2[1]], c='black', alpha=0.6)
    ax.scatter(coords_array[:,0], coords_array[:,1], zorder=2, s = 200)
    for key in coords:
        ax.text(coords[key][0], coords[key][1], key, zorder=3)

    

# if __name__ == "__main__":
    # central_node = 11
    # mode= 'pre'
    
    # adjacency_list = CreateAdjacencyList(G.get_node_list(), G.get_edge_list())

    # verts, edges = UnpackAdjacencyList(adjacency_list)
    
    # # Remove edges if their weight is zero
    # edges = np.squeeze([edge for edge in edges if edge[2]>0])
        
    # subtree_edges = CreateSubtree(verts, edges)

    # DFS_order = findDFSOrder(subtree_edges, central_node, mode)

    # radial_graph = RadialGraph(DFS_order, subtree_edges)
    
    # PlotRadialGraph(radial_graph, subtree_edges)
    