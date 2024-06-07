import random

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json

def create_graph(missions):
    G=nx.Graph()
    for key, value in missions.items():
        G.add_node(key, pos=value[0], duration=value[1])
    nodes = list(missions.keys())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            pos1 = missions[node1][0]
            pos2 = missions[node2][0]
            distance = np.linalg.norm(np.array(pos1) - np.array(pos2))
            G.add_edge(node1, node2, weight=distance)
    nx.write_gml(G, "graph.gml")
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'weight')
    for ind in labels:
        labels[ind]=round(labels[ind],2)
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=10)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    #plt.show()
    plt.savefig('Graph.pdf')

def save_drone_data(drones):
    with open('drone_data.json', 'w') as json_file:
        json.dump(drones, json_file)

def get_random_instance(N_nodes, randomized=True):
    missions={'Depot': [(0, 0), 0]}
    if randomized:
        for i in range(N_nodes):
            missions[i]=[(random.randrange(-10,10),random.randrange(-10,10)),2]
    else:
        for i in range(N_nodes):
            if i%3==0:
                missions[i] = [(random.randrange(-10, -5), random.randrange(-10, -5)), 2]
            elif i%3==1:
                missions[i] = [(random.randrange(-8, 0), random.randrange(2, 10)), 2]
            else:
                missions[i] = [(random.randrange(1, 10), random.randrange(-5, 5)), 2]
    return missions



if __name__ == "__main__":
    # [position, duration]
    missions = {'Depot': [(0, 0), 0], 'A': [(1, 4), 2], 'B': [(2, 3,), 2], 'C': [(4, 3), 2], 'D': [(3, -3), 2],
                'E': [(1, -3), 2], 'F': [(-3, -1), 2], 'G': [(-4, 0), 2]}

    missions=get_random_instance(40,True)

    # [velocity, max energy]
    drones = {'quadro1':[5,30], 'quadro2':[5,30],'quadro3':[5,30],'quadro4':[5,30]}



    create_graph(missions)
    save_drone_data(drones)


