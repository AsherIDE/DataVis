import pydot

from removeCycles import CreateDirectedAcyclicAdjacencyList, CreateDirectedAdjacencyList





# testing
FILE_NAME = 'Networks/SmallDirectedNetwork.dot'
G = pydot.graph_from_dot_file(FILE_NAME)[0]

# FILE_NAME = 'Networks/LeagueNetwork.dot'
# G = pydot.graph_from_dot_file(FILE_NAME)[0]

adj_test_list = CreateDirectedAdjacencyList(G.get_edge_list())

print(f"-------------------------------\n removed loops: {CreateDirectedAcyclicAdjacencyList(adj_test_list)} \n-------------------------------\n")
