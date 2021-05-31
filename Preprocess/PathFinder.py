import json
import networkx as nx

INPUT = '../Samples/sample_c.json'
MAX_NUM_ITERATION = 200
ROUTERS = []
CHARGES = {}

G = nx.DiGraph()

def init_graph():
    global CHARGES, G
    with open(INPUT) as json_file:
        data = json.load(json_file)
        CHARGES = data['charges']
            
        for router in data['routers']:
            ROUTERS.append(router)
            G.add_node(router, h_n = 1, p_n = 1, total = 1 * 1, selected = 0)

        for edge in data['edges']:
            G.add_edge(edge['from'], edge['to'], weight=1, b_n=edge['init'])

def find_non_disjoint_states(paths):
    vistied_nodes = {}
    for path in paths:
        for node in path:
            if node in vistied_nodes.keys():
                vistied_nodes[node] = vistied_nodes[node] + 1
            else:
                vistied_nodes[node] = 1
    return dict(filter(lambda elem: elem[1] > 1,vistied_nodes.items()))

def execute_shortest_path():
    global CHARGES, G
    for key in G.nodes:
        if(key in ROUTERS):
            node = G.nodes[key]
            node['selected'] = 0
            node['total'] = node['h_n'] * node['p_n']
    
    for key in G.edges:
        dest = key[1]
        if(dest in ROUTERS):
            dest_node = G.nodes[key[1]]
            G[key[0]][key[1]]['weight'] = dest_node['total'] + dest_node['p_n'] * G[key[0]][key[1]]['b_n']
    
    paths = []
    for charge, dest in CHARGES.items():
        paths.append(nx.shortest_path(G, charge, dest, weight='weight'))
    return paths   

def update_graph(non_disjoint_nodes):
    for key in G.nodes:
        node = G.nodes[key]
        if key in non_disjoint_nodes.keys():
            node['p_n'] = non_disjoint_nodes[key] + 1
            node['h_n'] = node['h_n'] + 1
        else:
            node['p_n'] = 1

init_graph()
paths = []
for i in range(0, MAX_NUM_ITERATION):
    paths = execute_shortest_path()
    print("Iteration {}: {}".format(i + 1, paths))
    non_disjoint_nodes = find_non_disjoint_states(paths)
    if(len(non_disjoint_nodes) == 0):
        break
    update_graph(non_disjoint_nodes)

print("Final Answer: " + str(paths))