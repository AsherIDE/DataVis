from ReadDotFile import CreateAdjacencyList

import pydot

test_adjacency_list_weighted = {'1': [('2', '1')], '2': [('3', '8'), ('4', '10'), ('5', '1'), ('6', '1'), ('7', '1'), ('8', '1'), ('9', '2'), ('10', '1'), ('11', '5')], '3': [('4', '6'), ('11', '3')], '4': [('11', '3')], '11': [('12', '1'), ('13', '1'), ('14', '1'), ('15', '1'), ('16', '1'), ('24', '9'), ('25', '7'), ('26', '12'), ('27', '31'), ('28', '17'), ('29', '8'), ('30', '2'), ('32', '3'), ('33', '1'), ('34', '2'), ('35', '3'), ('36', '3'), ('37', '2'), ('38', '2'), ('39', '2'), ('44', '3'), ('45', '1'), ('49', '1'), ('50', '2'), ('52', '2'), ('56', '19'), ('59', '4'), ('65', '1'), ('69', '1'), ('70', '1'), ('71', '1'), ('72', '1'), ('73', '1')], '13': [('24', '2')], '24': [('17', '3'), ('18', '3'), ('19', '3'), ('20', '3'), ('21', '4'), ('22', '4'), ('23', '4'), ('25', '2'), ('26', '1'), ('28', '5'), ('30', '1'), ('31', '1'), ('32', '2')], '25': [('26', '13'), ('27', '4'), ('28', '1'), ('42', '2'), ('43', '1'), ('51', '1'), ('69', '1'), ('70', '1'), ('71', '1')], '26': [('27', '1'), ('28', '5'), ('40', '1'), ('41', '1'), ('42', '3'), ('43', '2'), ('49', '1'), ('56', '2'), ('69', '5'), ('70', '6'), ('71', '4'), ('72', '1'), ('76', 
'3')], '27': [('18', '1'), ('28', '1'), ('44', '1'), ('50', '3'), ('52', '2'), ('55', '1'), ('56', '21'), ('73', '2')], '28': [('29', '1'), ('30', '1'), ('32', '1'), ('34', '1'), ('44', '1'), ('49', '1'), ('59', '6'), ('69', 
'1'), ('70', '2'), ('71', '1'), ('72', '1'), ('73', '1')], '29': [('45', '3'), ('46', '2')], '30': [('35', '2'), ('36', '2'), ('37', '1'), ('38', '1'), ('39', '1')], '32': [('31', '2')], '35': [('36', '3'), ('37', '2'), ('38', '2'), ('39', '2')], '36': [('37', '2'), ('38', '2'), ('39', '2')], '37': [('38', '2'), ('39', '2')], '38': [('39', '2')], '49': [('47', '2'), ('56', '4'), ('58', '1'), ('59', '7'), ('60', '6'), ('61', '1'), ('62', '2'), ('63', '7'), ('64', '5'), ('65', '5'), ('66', '3'), ('67', '1'), ('69', '1'), ('70', '1'), ('72', '1'), ('74', '2'), ('75', '2'), ('76', '1'), ('77', '1')], '50': [('51', '1'), ('52', '9'), ('55', '1'), ('56', '12'), ('57', '1')], '52': [('53', '1'), ('54', '1'), ('55', '2'), ('56', '6')], '56': [('18', '1'), ('40', '1'), ('42', '5'), ('55', '1'), ('57', '1'), ('58', '1'), ('59', '7'), ('60', '5'), ('62', '1'), ('63', '9'), ('64', '1'), ('65', '5'), ('66', '2')], '59': [('58', '1'), ('60', '15'), ('61', '4'), ('62', '6'), ('63', '17'), ('64', '4'), ('65', '10'), ('66', '5'), ('67', '3'), ('71', '1'), ('77', '1')], '65': [('58', '1'), ('60', '9'), ('61', '2'), ('62', '6'), ('63', '12'), ('64', '4'), ('66', '7'), ('67', '3'), ('77', '1')], '69': [('42', '1'), ('70', '6'), ('71', '4'), ('72', '2'), ('76', '3')], '70': [('42', '1'), ('71', '4'), ('72', '2'), ('76', '3')], '71': [('42', '1'), ('72', '2'), ('76', '1')], '72': [('42', '1'), ('76', '1')], '17': [('18', '4'), ('19', '4'), ('20', '4'), ('21', '3'), ('22', '3'), ('23', '3')], '18': [('19', '4'), ('20', '4'), ('21', '3'), ('22', '3'), ('23', '3')], '19': [('20', '4'), ('21', '3'), ('22', '3'), ('23', '3')], '20': [('21', '4'), ('22', '3'), ('23', '3')], '21': [('22', '5'), ('23', '4')], '22': [('23', '4')], '42': [('43', '2'), ('58', '1'), ('63', '1'), ('76', '1')], '40': [('53', '1')], '58': [('60', '2'), ('62', '1'), ('63', '2'), ('64', '2'), ('66', '1'), ('68', '3')], '63': [('60', '13'), ('61', '3'), ('62', '6'), ('64', '6'), ('66', '5'), ('67', '2'), ('77', '1')], '47': [('48', '1')], '60': [('61', '2'), ('62', '5'), ('64', '5'), ('66', '5'), ('67', '1')], '61': [('62', '2'), ('64', '2'), ('66', '2'), ('67', '1')], '62': [('64', '3'), ('66', '5'), ('67', '1')], '64': [('66', '5'), ('67', '1'), ('77', '1')], '66': [('67', '2'), ('77', '1')], '67': [('77', '1')], '74': [('75', '3')], '5': [('2', 0)], '6': [('2', 0)], '7': [('2', 0)], '8': [('2', 0)], '9': [('2', 0)], '10': [('2', 0)], '12': [('11', 0)], '14': [('11', 0)], '15': [('11', 0)], '16': [('11', 0)], '33': [('11', 0)], '34': [('11', 0)], '39': [('11', 0)], '44': [('11', 0)], '45': [('11', 0)], '73': [('11', 0)], '23': [('24', 0)], '31': [('24', 0)], '43': [('25', 0)], '51': [('25', 0)], '41': [('26', 0)], '76': [('26', 0)], '55': [('27', 0)], '46': [('29', 0)], '53': [('52', 0)], '48': [('47', 0)], '75': [('49', 0)], '77': [('49', 0)], '57': [('50', 0)], '54': [('52', 0)], '68': [('58', 0)]}

test_adjacency_list = {'1': ['2'], '2': ['3', '4', '5', '6', '7', '8', '9', '10', '11'], '3': ['4', '11'], '4': ['11'], '11': ['12', '13', '14', '15', '16', '24', '25', '26', '27', '28', '29', '30', '32', '33', '34', '35', '36', '37', '38', '39', 
'44', '45', '49', '50', '52', '56', '59', '65', '69', '70', '71', '72', '73'], '13': ['24'], '24': ['17', '18', '19', '20', '21', '22', '23', '25', '26', '28', '30', '31', '32'], '25': ['26', '27', '28', '42', '43', '51', '69', '70', '71'], '26': ['27', '28', '40', '41', '42', '43', '49', '56', '69', '70', '71', '72', '76'], '27': ['18', '28', '44', '50', '52', '55', '56', '73'], '28': ['29', '30', '32', '34', '44', '49', '59', '69', '70', '71', 
'72', '73'], '29': ['45', '46'], '30': ['35', '36', '37', '38', '39'], '32': ['31'], '35': ['36', '37', '38', '39'], '36': ['37', '38', '39'], '37': ['38', '39'], '38': ['39'], '49': ['47', '56', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '69', '70', '72', '74', '75', '76', '77'], '50': ['51', '52', '55', '56', '57'], '52': ['53', '54', '55', '56'], '56': ['18', '40', '42', '55', '57', '58', '59', '60', '62', '63', '64', '65', '66'], '59': ['58', '60', '61', '62', '63', '64', '65', '66', '67', '71', '77'], '65': ['58', '60', '61', '62', '63', '64', '66', '67', '77'], '69': ['42', '70', '71', '72', '76'], '70': ['42', '71', '72', '76'], '71': ['42', '72', '76'], '72': ['42', '76'], '17': ['18', '19', '20', '21', '22', '23'], '18': ['19', '20', '21', '22', '23'], '19': ['20', '21', '22', '23'], '20': ['21', '22', '23'], '21': ['22', '23'], '22': ['23'], '42': ['43', '58', 
'63', '76'], '40': ['53'], '58': ['60', '62', '63', '64', '66', '68'], '63': ['60', '61', '62', '64', '66', '67', '77'], '47': ['48'], '60': ['61', '62', '64', '66', '67'], '61': ['62', '64', '66', '67'], '62': ['64', '66', '67'], '64': ['66', '67', '77'], '66': ['67', '77'], '67': ['77'], '74': ['75'], '5': ['2'], '6': ['2'], '7': ['2'], '8': ['2'], '9': ['2'], '10': ['2'], '12': ['11'], '14': ['11'], '15': ['11'], '16': ['11'], '33': ['11'], '34': ['11'], '39': ['11'], '44': ['11'], '45': ['11'], '73': ['11'], '23': ['24'], '31': ['24'], '43': ['25'], '51': ['25'], '41': ['26'], '76': ['26'], '55': ['27'], '46': ['29'], '53': ['52'], '48': ['47'], '75': ['49'], '77': ['49'], '57': ['50'], '54': ['52'], '68': ['58']}

# Remove weights to make adjacency list readable for 
def removeAdjacencyListWeights(adjacency_list_weighted):
    adjacency_list = {}

    for node in adjacency_list_weighted:
        adjacency_list[node] = [node[0] for node in adjacency_list_weighted[node]]

    return adjacency_list
# print(removeAdjacencyListWeights(test_adjacency_list_weighted))

# NOTE: deprecated function
# Get a list of possible starting nodes
# def getStartNode(adjacency_list):
#     # determine node with most edges
#     node_edges_amount, node_max = 0, 0
#     for n, e in adjacency_list.items():
#         if len(e) > node_edges_amount:
#             node_edges_amount = len(e)
#             node_max = str(n)

#     return node_max

# 
# Breath first search (from tutorial slides week 1)
# 
# g is an adjacency list.
# g[u] == [v1, v2, v3, ...] means edges (u, v1), (u, v2), (u, v3), ... are in the graph
def bfs(g, start_node):
    out = []
    to_visit = [start_node]
    visited = {v: False for v in g}
    visited[start_node] = True
    while to_visit:
        x = to_visit.pop(0)
        for child in g[x]:
            if visited[child]:
                continue
            visited[child] = True
            out.append((x, child))
            to_visit.append(child)
    return out




# Breath first search to find suitable starting nodes
visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue
def bfs_start_finder(visited, graph, total_nodes_amount, node):
  nodes_iterated = 0

  visited.append(node)
  queue.append(node)

  while queue:
    s = queue.pop(0)
    nodes_iterated += 1

    for neighbour in graph[s]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

  # check if current start position is suitable (no missing nodes)
  if nodes_iterated == len(total_nodes_amount):
     return True
  
  return False

# find suitable bfs starting nodes
def getStartNode(adjacency_list, total_nodes):
  visited = []
  queue = [] 
  
  suitable_nodes = []
  for node in total_nodes:
    potential_node = bfs_start_finder(visited, adjacency_list, total_nodes, node)

    if potential_node == True:
        suitable_nodes.append(node)

  return suitable_nodes

# find suitable node testing
# FILE_NAME = 'Networks/LesMiserables.dot'
# FILE_NAME = 'Networks/JazzNetwork.dot'

# G = pydot.graph_from_dot_file(FILE_NAME)[0]
# G_total_nodes = [node.get_name() for node in G.get_node_list()]
# G_adjacency_list = removeAdjacencyListWeights(CreateAdjacencyList(G.get_node_list(), G.get_edge_list()))

# print(getStartNode(G_adjacency_list, G_total_nodes))

