import pydot

# Returns directed adjacency list
def CreateDirectedAdjacencyList(edges):
    output = {}

    for edge in edges:
        source = edge.get_source()
        target = edge.get_destination()

        if source not in output.keys():
            output[source] = [target]
        else:
            output[source] += [target]

    return output

# TODO: finish this function
def CreateDirectedAcyclicAdjacencyList(adjacency_list):
    adjacency_list_copy = adjacency_list.copy()
    indexed_adjacency_list = {}

    
    for source, targets in adjacency_list_copy.items():
        indexed_adjacency_list_len = len(indexed_adjacency_list)

        # first iteration
        if indexed_adjacency_list_len == 0:
            indexed_adjacency_list[indexed_adjacency_list_len] = {source: targets}
        
        # check if previous node is connected to current node
        elif source in list(indexed_adjacency_list[indexed_adjacency_list_len - 1].values())[0]:
            indexed_adjacency_list[indexed_adjacency_list_len] = {source: targets}

        
        

    return indexed_adjacency_list


# testing
FILE_NAME = 'Networks/SmallDirectedNetwork.dot'
G = pydot.graph_from_dot_file(FILE_NAME)[0]

adj_test_list = CreateDirectedAdjacencyList(G.get_edge_list())
# print(adj_test_list)

print(CreateDirectedAcyclicAdjacencyList(adj_test_list))