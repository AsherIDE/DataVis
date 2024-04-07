import pydot
import matplotlib.pyplot as plt

from floyd_warshall import floyd_warshall
from sklearn.manifold import TSNE

# testing 
FILE_NAME = 'Networks/LesMiserables.dot'
# FILE_NAME = 'Networks/JazzNetwork.dot'
# FILE_NAME = 'Networks/LeagueNetwork.dot'

G = pydot.graph_from_dot_file(FILE_NAME)[0]

X = floyd_warshall(G)
perpl = 5

embedding = TSNE(n_components=2, perplexity = perpl, metric = 'precomputed', init = 'random')

X_transformed = embedding.fit_transform(X)

# simple way to scatter
# plt.scatter(*zip(*X_transformed))

# scatter nice plot
already_seen = {}  


# for i in range(len(X_transformed)):
#     x,y = X_transformed[i]
#     xy_str = str(x)+str(y)
#     if xy_str in already_seen:
#          continue
#     else:
#         plt.scatter(x, y, color="#EECA3B", zorder=2, s=50)
#         plt.text(x, y, i, fontsize=5, ha='center', va='center', zorder=3, color='black')
#         already_seen[xy_str] = 0

for i in range(len(X_transformed)):
    x,y = X_transformed[i]
    plt.scatter(x, y, color="#EECA3B", zorder=2, s=50)
    plt.text(x, y, i+1, fontsize=5, ha='center', va='center', zorder=3, color='black')

# draw edges
for edge in G.get_edge_list():
    source, sink = X_transformed[int(edge.get_source()) - 1], X_transformed[int(edge.get_destination()) - 1]

    plt.plot([source[0], sink[0]],
            [source[1], sink[1]], color="black", zorder=1, alpha=0.1)

plt.title('t-SNE, perplexity = ' + str(perpl))
plt.xticks([])
plt.yticks([])

plt.show()

print(X_transformed)