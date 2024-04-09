import pydot
import statistics
import matplotlib.pyplot as plt
from Assignments.Assignment_4.removeCycles import CreateDirectedAcyclicAdjacencyList, CreateDirectedAdjacencyList, flatten
from Assignments.Assignment_4.layerAssigning import CreateLayerAssignment
from shapely import LineString
import math
from floyd_warshall import floyd_warshall
from scipy import stats


def create_dummies_and_lists(result):

    connections_list = []

    for l, v in result.items():
        if l != (len(result)):
            next_layer = result[l+1]
            for j in v.items():
                if len(j[1])>0:
                    for k in j[1]:
                        connections_list += [(j[0], (str(k)))]

    coords = {}
    for l, v in result.items():
        current_layer = list(result[l].keys())
        breadth = len(current_layer)
        if l > 1:
            previous_aims = sorted(flatten(result[l-1].values()))
            #previous_aims = [x for xs in list(result[l-1].values()) for x in xs]
        else:
            previous_aims = []
        for i in previous_aims:
            if i not in current_layer:
                breadth+=1
                current_layer.append('d'+i+'.'+str(l))
                result[l]['d'+i+'.'+str(l)] = [i]
        b = 1/breadth
        d = 0
        for i in current_layer:
            c = 0.5*b + d*b
            if i.startswith('d'):
                continue
                #plt.plot(c, l, 's', color = 'black', zorder = 2)
                #plt.text(c+0.01, l, i, zorder = 3)
            else:
                continue
                #plt.scatter(c, l, color = 'purple', zorder = 2)
                #plt.text(c+0.01, l, i, zorder = 3)
            coords[i] = [c,l]
            d +=1


    connections_list = []

    for l, v in result.items():
        if l != (len(result)):
            next_layer = result[l+1]
            for j in v.items():
                if len(j[1])>0:
                    for k in j[1]:
                        if k in next_layer:
                            #plt.plot([coords[j[0]][0],coords[str(k)][0]] , [coords[j[0]][1],coords[str(k)][1]], zorder = 1, color = 'violet', alpha = 0.7)
                            #plt.annotate('', xy = coords[str(k)], xytext = coords[j[0]], arrowprops=dict(arrowstyle="->", color='violet'), zorder = 1, alpha = 0.7)
                            connections_list += [(j[0], (str(k)))]
                        else:
                            #plt.plot([coords[j[0]][0],coords['d'+str(k)+str(l+1)][0]] , [coords[j[0]][1],coords['d'+str(k)+str(l+1)][1]], zorder = 1, color = 'violet', alpha = 0.7)
                            #result[l+1][j[0]] = result[l][j[0]] + ['d'+str(k)+str(l+1)]
                            #plt.annotate('', xy = coords['d'+str(k)+'.'+str(l+1)], xytext = coords[j[0]], arrowprops=dict(arrowstyle="->", color='violet'), zorder = 1, alpha = 0.7)
                            connections_list += [(j[0], 'd'+str(k)+'.'+str(l+1))]
    
    #plt.show()

    return connections_list, coords


def count_crossings(layer_list, connections_list):

    crossings = 0 

    for i in range(len(layer_list)-1):
        layer_1 = layer_list[i]
        layer_2 = layer_list[i+1]

        for node_1 in layer_2: 
            node_1_order = layer_2.index(node_1)
            node_1_edges = [ x for x, y in connections_list if (y == node_1)]

            for node_2 in layer_2:
                node_2_order = layer_2.index(node_2)
                node_2_edges = [ x for x, y in connections_list if (y == node_2)]
                if node_2_order > node_1_order:
                    list_list = [(layer_1.index(x),layer_1.index(y)) for x in node_1_edges for y in node_2_edges]
                    crossings += sum(1 if int(x) > int(y)  else 0 for x, y in list_list)

    return crossings

# BARYCENTER 


def create_layer_list(result):
    layer_list = [list(result[i].keys()) for i in range(1, len(result)+1)]
    return layer_list


def reduce_crossings_barycenter(result, layer_list, connections_list):
    
    crossing_number = count_crossings(layer_list, connections_list)
    new_crossing_number = 0
    crossing_number_list = [crossing_number]

    while crossing_number != new_crossing_number:
        crossing_number = count_crossings(layer_list, connections_list)
        for i in range(len(result)-1):
            layer_1 = layer_list[i]
            layer_2 = layer_list[i+1]
            barycenter_list = []
            for node in layer_2: 
                no_conn = len([ (x,y) for x, y in connections_list if (y == node)])
                conn_in_order = sum([ layer_1.index(x)+1 for x, y in connections_list if y  == node ])
                barycenter = conn_in_order/no_conn
                barycenter_list += [(node, barycenter)]
            barycenter_list = sorted(barycenter_list, key=lambda bc: bc[1]) 
            layer_2_new = list(list(zip(*barycenter_list))[0])
            layer_2 = layer_2_new
            layer_list[i+1] = layer_2


        for i in range(1, len(result)):
            layer_1 = layer_list[-i]
            layer_2 = layer_list[-(i+1)]
            barycenter_list = []
            for node in layer_2: 
                no_conn = len([ (x,y) for x, y in connections_list if (x == node)])
                conn_in_order = sum([ layer_1.index(y)+1 for x, y in connections_list if x  == node ])
                if no_conn > 0:
                    barycenter = conn_in_order/no_conn
                else:
                    barycenter = 0
                barycenter_list += [(node, barycenter)]
            barycenter_list = sorted(barycenter_list, key=lambda bc: bc[1]) 
            layer_2_new = list(list(zip(*barycenter_list))[0])
            layer_2 = layer_2_new
            layer_list[-(i+1)] = layer_2

        new_crossing_number = count_crossings(layer_list, connections_list)
        crossing_number_list += [new_crossing_number]
    
    return layer_list, crossing_number_list

# MEDIAN 

def reduce_crossings_median(result, layer_list, connections_list):
    
    crossing_number = count_crossings(layer_list, connections_list)
    new_crossing_number = 0
    crossing_number_list = [crossing_number]

    while crossing_number != new_crossing_number:
        crossing_number = count_crossings(layer_list, connections_list)
        for i in range(len(result)-1):
            layer_1 = layer_list[i]
            layer_2 = layer_list[i+1]
            median_list = []
            for node in layer_2: 
                conn_coords = [ layer_1.index(x) for x, y in connections_list if (y == node)]
                if len(conn_coords) > 0:
                    median_coords = statistics.median(conn_coords)
                else:
                    median_coords = 0
                median_list += [(node, median_coords)]
            median_list = sorted(median_list, key=lambda med: med[1]) 
            layer_2_new = list(list(zip(*median_list))[0])
            layer_2 = layer_2_new
            layer_list[i+1] = layer_2


        for i in range(1, len(result)):
            layer_1 = layer_list[-i]
            layer_2 = layer_list[-(i+1)]
            median_list = []
            for node in layer_2: 
                conn_coords = [ layer_1.index(y) for x, y in connections_list if (x == node)]
                if len(conn_coords) > 0:
                    median_coords = statistics.median(conn_coords)
                else:
                    median_coords = 0
                median_list += [(node, median_coords)]
            median_list = sorted(median_list, key=lambda med: med[1]) 
            layer_2_new = list(list(zip(*median_list))[0])
            layer_2 = layer_2_new
            layer_list[-(i+1)] = layer_2

        new_crossing_number = count_crossings(layer_list, connections_list)
        crossing_number_list += [new_crossing_number]
    
    return layer_list, crossing_number_list



def reverse_edges(connections_list, reversed_edges):
    storage = []
    for i in connections_list:
        if (i[0] in reversed_edges.keys()):
            if i[1] in reversed_edges[i[0]]:
                connections_list[connections_list.index(i)] = (i[1], i[0], 'r')
            elif i[1][1:-2] in reversed_edges[i[0]]:
                connections_list[connections_list.index(i)] = (i[1], i[0], 'r')
                storage += [i[1][1:-2]]
        if i[0][1:-2] in storage:
            connections_list[connections_list.index(i)] = (i[1], i[0], 'r')

    return connections_list

def reverse_edges_no_dummies(connections_list, reversed_edges):
    raw_conn = []
    new_connections_list = []
    for i in connections_list:
        if (i[0].startswith('d') and i[1].startswith('d')) or i[0].startswith('d'):
            continue
        elif i[1].startswith('d'):
            raw_conn += [(i[0], i[1][1:].split('.')[0])]
        else:
            raw_conn += [(i[0], i[1])]
    for i in raw_conn:
        if (i[0] in reversed_edges.keys()) and i[1] in reversed_edges[i[0]]:
            new_connections_list += [(i[1], i[0], 'r')]
        else:
            new_connections_list += [(i[0], i[1])]
            
    return new_connections_list



def plot_final_graph(result, layer_list, connections_list, dummy_variables, draw_graph=True):

    coords = {}
    edge_coords = []
    for l, v in result.items():
        current_layer = layer_list[l-1]
        breadth = len(current_layer)
        b = 1/breadth
        d = 0
        for i in current_layer:
            c = 0.5*b + d*b
            if i.startswith('d'):
                plt.plot(c, l, 's', color = 'white', zorder = 0)
                #plt.text(c+0.01, l, i, zorder = 3)
            else:
                plt.scatter(c, l, color = 'red', zorder = 2)
                #plt.text(c+0.01, l, i, zorder = 3)
            coords[i] = [c,l]
            d +=1
    if not dummy_variables:
        for i in connections_list:
            if len(i) == 2:
                plt.annotate('', xy = coords[i[1]], xytext = coords[i[0]], arrowprops=dict(arrowstyle="->", color='black', alpha = 0.7), zorder = 1)
            else:
                plt.annotate('', xy = coords[i[1]], xytext = coords[i[0]], arrowprops=dict(arrowstyle="->", color='indigo', alpha = 0.7), zorder = 1)
    else: 
        for i in connections_list:
            if (i[1].startswith('d') and i[0].startswith('d')) or (i[0].startswith('d')):
               continue
            elif i[1].startswith('d'):
               plt.annotate('', xy = coords[i[1][1:].split('.')[0]], xytext = coords[i[0]], arrowprops=dict(arrowstyle="->", color='black', alpha = 0.7), zorder = 1)
            else:
                edge_coords.append([(coords[i[1]][0],coords[i[1]][1]), (coords[i[0]][0], coords[i[0]][1])])
                if len(i) == 2:
                    plt.annotate('', xy = coords[i[1]], xytext = coords[i[0]], arrowprops=dict(arrowstyle="->", color='black', alpha = 0.7), zorder = 1)
                else:
                    plt.annotate('', xy = coords[i[1]], xytext = coords[i[0]], arrowprops=dict(arrowstyle="->", color='indigo', alpha = 0.7), zorder = 1)

    for i in list(result.keys()):
        plt.axhline(y = i, color = 'black', linestyle = '-', linewidth = 0.3, zorder = 0) 
    
    if draw_graph == True:
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xticks([])
        #plt.yticks([])
        plt.show()
    else:
        plt.clf()
    return edge_coords, coords

def drawLayered(FILE_NAME, draw_graph=True, nodummies=False, median=False):
    if draw_graph:
        FILE_NAME = f'Networks/{FILE_NAME}.dot'

    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    adj_test_list = CreateDirectedAdjacencyList(G.get_edge_list())
    total_nodes = [node.get_name() for node in G.get_node_list()]
    acyclic_adj_test_list, reversed_edges = CreateDirectedAcyclicAdjacencyList(adj_test_list)
    result = CreateLayerAssignment(acyclic_adj_test_list, total_nodes)


    connections_list, coords = create_dummies_and_lists(result)
    layer_list = create_layer_list(result)
    
    # settings
    if median:
        new_layer_list, crossing_list = reduce_crossings_median(result, layer_list, connections_list)
    else:
        new_layer_list, crossing_list = reduce_crossings_barycenter(result, layer_list, connections_list)

    if nodummies:
        connections_list_new = reverse_edges_no_dummies(connections_list, reversed_edges)
    else:
        connections_list_new = reverse_edges(connections_list, reversed_edges)
    
    coords, node_coords = plot_final_graph(result, new_layer_list, connections_list_new, nodummies, draw_graph)
    # print(crossing_list)

    return coords, node_coords, new_layer_list

### ---- QUALITY METRICS ---- ###


def calculate_angle(edge1, edge2, layer_count):
    e1_new = [(edge1[0][0]-edge1[1][0]), (edge1[0][1]/layer_count-edge1[1][1]/layer_count)]
    e2_new = [(edge2[0][0]-edge2[1][0]), (edge2[0][1]/layer_count-edge2[1][1]/layer_count)]
    dot_product = (e1_new[0]*e2_new[0]) + (e1_new[1]*e2_new[1])
    len_e1 = ((e1_new[0]*e1_new[0]) + (e1_new[1]*e1_new[1]))**0.5
    len_e2 = ((e2_new[0]*e2_new[0]) + (e2_new[1]*e2_new[1]))**0.5
    cos_angle = dot_product/(len_e1*len_e2)
    angle = math.acos(cos_angle)
    angle_deg = math.degrees(angle)
    return angle_deg

def drawLayeredQuality(FILE_NAME):
    FILE_NAME = f'Networks/{FILE_NAME}.dot'

    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    # drawleyered part
    # ---------------------------------------------------------------------------------------------
    coords, node_coords, new_layer_list = drawLayered(FILE_NAME, draw_graph=False)
    # ---------------------------------------------------------------------------------------------

    X = floyd_warshall(G)

    coords_list = []
    smallest_angle = 360
    crossing_count = 0
    pairs_list = []
    data_dist_list = []
    graph_dist_list = []
    stress = 0 
    normalization = 0


    # calculate number of crossings and smallest angle
    for edge in coords:
        current_coord = edge

        for coord in coords_list: 

            if LineString(current_coord).crosses(LineString(coord)):
                crossing_count += 1
                angle = calculate_angle(current_coord, coord, len(new_layer_list))
            
                if angle < smallest_angle:
                    smallest_angle = angle
                    print(angle)
            
        coords_list += [current_coord]


    # calculate stress
    for i in range(1, 78):
        pairs_list.append(node_coords[str(i)])


    for i in range(len(pairs_list)):
        for j in range(i+1, len(pairs_list)):
            [x1, y1] = pairs_list[i]
            [x2, y2] = pairs_list[j]
            data_distance = X[i][j]
            graph_distance = math.dist([x1, y1], [x2, y2])
            data_dist_list.append(data_distance)
            graph_dist_list.append(graph_distance)
            stress += (data_distance - graph_distance)**2
            normalization += data_distance**2
        

    # plot shepard
    plt.scatter(data_dist_list, graph_dist_list, c="red", s=100, zorder=3, alpha=0.4)
    plt.show()
    spearman_rank = stats.spearmanr(data_dist_list, graph_dist_list)

    # normalized stress
    norm_stress = stress/normalization

    # results
    print("crossing count: ", crossing_count, "smallest angle: ", smallest_angle, "normalized stress: ", norm_stress, 'spearman rank correlation:', spearman_rank.statistic)

# TEST
# FILE_NAME = 'SmallDirectedNetwork'
# FILE_NAME = 'LeagueNetwork'
# FILE_NAME = 'LesMiserables'

# drawLayered(FILE_NAME) 
# drawLayeredQuality(FILE_NAME)


