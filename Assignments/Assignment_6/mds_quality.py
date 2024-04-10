from MDS import drawMDS
import matplotlib.pyplot as plt
from scipy import stats
from shapely import LineString
import math

def calculate_angle(edge1, edge2):
    e1_new = [(edge1[0][0]-edge1[1][0]), (edge1[0][1]-edge1[1][1])]
    e2_new = [(edge2[0][0]-edge2[1][0]), (edge2[0][1]-edge2[1][1])]
    dot_product = (e1_new[0]*e2_new[0]) + (e1_new[1]*e2_new[1])
    len_e1 = ((e1_new[0]*e1_new[0]) + (e1_new[1]*e1_new[1]))**0.5
    len_e2 = ((e2_new[0]*e2_new[0]) + (e2_new[1]*e2_new[1]))**0.5
    cos_angle = dot_product/(len_e1*len_e2)
    angle = math.acos(cos_angle)
    angle_deg = math.degrees(angle)
    return angle_deg

def drawMDSQuality(FILE_NAME):
    FILE_NAME = f'Networks/{FILE_NAME}.dot'

    coords_list = []
    crossing_count = 0
    smallest_angle = 360
    data_dist_list = []
    graph_dist_list = []
    stress = 0 
    normalization = 0

    G, X, X_transformed = drawMDS(FILE_NAME, False)

    # calculate crossing number and smallest angle 
    for edge in G.get_edge_list():
            source, dest = X_transformed[int(edge.get_source()) - 1], X_transformed[int(edge.get_destination()) - 1]
            #print(source, dest)
            current_coord = [(source[0], source[1]), (dest[0], dest[1])]
            for coord in coords_list: 
                # crossings
                if LineString(current_coord).crosses(LineString(coord)):
                    crossing_count += 1
                    angle = calculate_angle(current_coord, coord)
                    
                    # smallest angle
                    if angle < smallest_angle:
                            smallest_angle = angle
                # stress

            coords_list += [current_coord]


    # calculate stress
    for i in range(len(X_transformed)):
        for j in range(i+1, len(X_transformed)):
            [x1, y1] = X_transformed[i]
            [x2, y2] = X_transformed[j]
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
# FILE_NAME = 'LesMiserables' #Most suitable, other ones are bad

drawMDSQuality('JazzNetwork')