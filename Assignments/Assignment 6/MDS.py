import pydot
import matplotlib.pyplot as plt

from floyd_warshall import floyd_warshall
from sklearn.manifold import MDS

# testing 
FILE_NAME = 'Networks/LesMiserables.dot'
# FILE_NAME = 'Networks/JazzNetwork.dot'
# FILE_NAME = 'Networks/LeagueNetwork.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

X = floyd_warshall(G)

embedding = MDS(n_components=2, normalized_stress='auto', dissimilarity='precomputed')

X_transformed = embedding.fit_transform(X)

# simple way to scatter
# plt.scatter(*zip(*X_transformed))

# scatter nice plot
for i in range(len(X_transformed)):
    x, y = X_transformed[i]

    plt.scatter(x, y, color="#EECA3B", zorder=2, s=50)
    plt.text(x, y, i, fontsize=5, ha='center', va='center', zorder=3, color='black')

# draw edges
for edge in G.get_edge_list():
    source, sink = X_transformed[int(edge.get_source()) - 1], X_transformed[int(edge.get_destination()) - 1]

    plt.plot([source[0], sink[0]],
            [source[1], sink[1]], color="black", zorder=1, alpha=0.1)

plt.title('Multidimensional scaling')
plt.xticks([])
plt.yticks([])

plt.show()