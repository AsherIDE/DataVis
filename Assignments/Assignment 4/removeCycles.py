import pydot
import copy

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
        

# Returns directed acyclic graph (Heuristic with guarantees by Eades et al. (1993))
# NOTE: add changed_nodes_dict to the return to see which nodes were reversed
def CreateDirectedAcyclicAdjacencyList(adjacency_list):
    adjacency_list_copy = copy.deepcopy(adjacency_list)
    acyclic_adjacency_list = {}

    # list of lists --> list
    def flatten(matrix):
        flat_list = []
        for row in matrix:
            flat_list.extend(row)
        return list(set(flat_list))
    
    # remove a sink from all adjacency_list values
    def remove_sink(sink):
        removed_items_counter = 0
        nodes_that_became_sink = []

        # remove sink from the list
        for node, neighbors in adjacency_list_copy.items():
            if sink in neighbors:
                neighbors.remove(sink)

                # node lost its neighbors and has become a sink (thus remove it)
                if len(neighbors) == 0:
                    # print(f"Sink (remove_sink function): {node}")
                    nodes_that_became_sink.append(node)

                # save the node again but without the sink neighbor
                else:
                    adjacency_list_copy[node] = neighbors
                    removed_items_counter += 1

        # remove nodes that became a sink
        for sink_node in nodes_that_became_sink:
            adjacency_list_copy.pop(sink_node)

        # return that progress is still being made
        return removed_items_counter + len(nodes_that_became_sink)


    """
    1. remove sinks
    2. remove sources
    3. remove the loop itself
    """

    # print(f"-------------------------------\n original: {adjacency_list} \n-------------------------------\n")

    changed_nodes_dict = {} # append value to list of original node values, remove key from values from other keys
    while True:

        # remove sinks (nodes without outging edges)
        while True:
            sink_removed_items_counter = 0

            nodes = adjacency_list_copy.keys()
            neighbors = flatten(adjacency_list_copy.values())
            
            # loop every potential sink
            for potential_sink in neighbors:
                # sink found --> remove it
                if potential_sink not in nodes:
                    # print(f"Sink: {potential_sink}")
                    sink_removed_items_counter += remove_sink(potential_sink)

            # break the loop when nothing is removed anymore
            if sink_removed_items_counter == 0:
                break

        # print(f"-------------------------------\n removed sinks: {adjacency_list_copy} \n-------------------------------\n")

        # remove sources without incoming edges
        while True:
            sources_to_remove = []

            nodes = adjacency_list_copy.keys()
            neighbors = flatten(adjacency_list_copy.values())

            # loop every potential source
            for potential_source in nodes:
                # source found --> remove it
                if potential_source not in neighbors:
                    # print(f"Source: {potential_source}")
                    sources_to_remove.append(potential_source)

            # remove found sources from adjacency_list_copy
            for source in sources_to_remove:
                adjacency_list_copy.pop(source)

            # break the loop if nothing is removed
            if len(sources_to_remove) == 0:
                break

        # print(f"-------------------------------\n removed sources: {adjacency_list_copy} \n-------------------------------\n")

        # select node with most edges, otherwise random node
        change_node, change_values = "", []
        for k, v in adjacency_list_copy.items():
            if change_node == {} or len(v) > len(change_values):
                change_node = k
                change_values = v

        # remove selected node and add it to changed_nodes_dict
        vertices_to_change_node = []
        for k2, v2 in adjacency_list_copy.items():
            if change_node in v2:
                vertices_to_change_node.append(k2)

        # break the loop when everything is filtered
        if adjacency_list_copy == {}:
            break

        changed_nodes_dict[change_node] = vertices_to_change_node
        print(f"Acycled connection: {change_node} --> {vertices_to_change_node}")
        adjacency_list_copy.pop(change_node)

    # update the return adjacency_list
    for changed_node, changed_values in changed_nodes_dict.items():
        
        for changed_value in changed_values:
            # prevent duplicates from being added
            if changed_value not in adjacency_list[changed_node]:
                adjacency_list[changed_node] += changed_values

            # remove the vertices that were the other way around
            adjacency_list[changed_value].remove(changed_node)

            if len(adjacency_list[changed_value]) == 0:
                adjacency_list.pop(changed_value)

    return adjacency_list


# testing
# FILE_NAME = 'Networks/SmallDirectedNetwork.dot'
# G = pydot.graph_from_dot_file(FILE_NAME)[0]

# FILE_NAME = 'Networks/LeagueNetwork.dot'
# G = pydot.graph_from_dot_file(FILE_NAME)[0]

# adj_test_list = CreateDirectedAdjacencyList(G.get_edge_list())

# print(f"-------------------------------\n removed loops: {CreateDirectedAcyclicAdjacencyList(adj_test_list)} \n-------------------------------\n")
