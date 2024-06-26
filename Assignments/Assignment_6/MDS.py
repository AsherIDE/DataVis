import pydot
import matplotlib.pyplot as plt
import math

from floyd_warshall import floyd_warshall
from sklearn.manifold import MDS
from shapely import LineString
from scipy import stats

def drawMDS(FILE_NAME, draw_graph=True):
    if draw_graph:
        FILE_NAME = f'Networks/{FILE_NAME}.dot'
    G = pydot.graph_from_dot_file(FILE_NAME)[0]

    X = floyd_warshall(G)

    embedding = MDS(n_components=2, normalized_stress='auto', dissimilarity='precomputed')

    X_transformed = embedding.fit_transform(X)

    # simple way to scatter
    # plt.scatter(*zip(*X_transformed))

    # scatter nice plot
    for i in range(len(X_transformed)):
        x, y = X_transformed[i]

        plt.scatter(x, y, color="red", zorder=2, s=50)
        plt.text(x, y, i, fontsize=5, ha='center', va='center', zorder=3, color='black')

    # draw edges
    for edge in G.get_edge_list():
        source, sink = X_transformed[int(edge.get_source()) - 1], X_transformed[int(edge.get_destination()) - 1]

        plt.plot([source[0], sink[0]],
                [source[1], sink[1]], color="black", zorder=1, alpha=0.4)

    if draw_graph:
        plt.title('Multidimensional scaling')
        plt.xticks([])
        plt.yticks([])

        plt.show()
    else:
        plt.clf()

    return G, X, X_transformed
# TEST
# FILE_NAME = 'LesMiserables'
# FILE_NAME = 'JazzNetwork'
# FILE_NAME = 'LeagueNetwork'

# drawMDS(FILE_NAME)