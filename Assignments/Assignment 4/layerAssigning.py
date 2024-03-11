import pydot

from removeCycles import CreateDirectedAcyclicAdjacencyList, CreateDirectedAdjacencyList, flatten

# Creates a layer assignment from an acyclic adjacency list
def CreateLayerAssignment(input, all_nodes):
    levels = {}
    iteration = 0

    while True:
        sources = []
        iteration += 1

        nodes = input.keys()
        neighbors = flatten(input.values())

        # find all sources
        for potential_source in nodes:
            # source found --> remove it
            if potential_source not in neighbors:
                # print(f"{potential_source} not in {neighbors}")
                sources.append(potential_source)

        # iterate every starting point
        levels[iteration] = {}
        for source in sources:
            source_descendents = input[source]
            
            levels[iteration][source] = source_descendents
            input.pop(source)

        if input == {}:
            break
    
    # find missing nodes
    levels_nodes = flatten(levels.values())
    missing_nodes = []
    for potential_missing_node in all_nodes:
        if potential_missing_node not in levels_nodes:
            missing_nodes.append(potential_missing_node)
    
    # add missing nodes to levels_to_append to assert the correct order
    levels_to_append = {}
    for level, level_nodes in reversed(levels.items()):
        levels_to_append[level + 1] = []

        found_nodes = []
        for missing_node in missing_nodes:
            if missing_node in flatten(level_nodes.values()):
                
                levels_to_append[level + 1].append(missing_node)

                found_nodes.append(missing_node)

        missing_nodes = [missing_node for missing_node in missing_nodes if missing_node not in found_nodes]

    # insert levels_to_append (missing nodes) into levels
    for missing_level, previously_missing_nodes in levels_to_append.items():
        if missing_level not in levels.keys():
            levels[missing_level] = {}

        for previously_missing_node in previously_missing_nodes:
            levels[missing_level][previously_missing_node] = []

    return levels



# testing
FILE_NAME = 'Networks/SmallDirectedNetwork.dot'
G = pydot.graph_from_dot_file(FILE_NAME)[0]

# FILE_NAME = 'Networks/LeagueNetwork.dot'
# G = pydot.graph_from_dot_file(FILE_NAME)[0]
adj_test_list = CreateDirectedAdjacencyList(G.get_edge_list())

# print(adj_test_list)
total_nodes = [node.get_name() for node in G.get_node_list()]
acyclic_adj_test_list, changed_nodes = CreateDirectedAcyclicAdjacencyList(adj_test_list)

# print(f"-------------------------------\n in: {acyclic_adj_test_list} \n-------------------------------\n")

# print("-------------------------------\n out: \n-------------------------------\n")
# for l, v in CreateLayerAssignment(acyclic_adj_test_list, total_nodes).items():
#         print(f"level: {l} \n items: {v}")

# print("\n-------------------------------\n")

result = CreateLayerAssignment(acyclic_adj_test_list, total_nodes)

