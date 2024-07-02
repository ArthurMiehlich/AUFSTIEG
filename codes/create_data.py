import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json


def create_graph(missions):
    G = nx.DiGraph()
    for key, value in missions.items():
        G.add_node(key, pos=value[0], duration=value[1], energy_consumption=value[2])
    nodes = list(missions.keys())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            pos1 = missions[node1][0]
            pos2 = missions[node2][0]
            distance = np.linalg.norm(np.array(pos1) - np.array(pos2))
            G.add_edge(node1, node2, distance=distance, energy_consumption=distance)
            G.add_edge(node2, node1, distance=distance, energy_consumption=distance)

    save_graph_data(G)
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'weight')
    for ind in labels:
        labels[ind] = round(labels[ind], 2)
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=10)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.show()
    plt.savefig('Graph.pdf')


def save_drone_data(drones):
    with open('drone_data.json', 'w') as json_file:
        json.dump(drones, json_file, indent=4)


def save_graph_data(Graph):
    data = nx.node_link_data(Graph)
    with open('graph.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def is_valid_point(point, existing_points, min_distance=0.3):
    for p in existing_points:
        distance = math.sqrt((point[0] - p[0])**2 + (point[1] - p[1])**2)
        if distance < min_distance:
            return False
    return True

def get_random_instance(N_nodes, randomized=True):
    # missions = {'Depot': [(0, 0), 0]}
    missions = {'Depot_s': [(0, 0), 0, 0], 'Depot_t': [(0, 0), 0, 0]}
    existing_points = [(0, 0)]
    if randomized:
        for i in range(N_nodes):
            while True:
                new_point = (random.uniform(-10, 10), random.uniform(-10, 10))
                if is_valid_point(new_point, existing_points):
                    missions[i] = [new_point, 2, 2]
                    existing_points.append(new_point)
                    break
    else:
        for i in range(N_nodes):
            while True:
                if i % 3 == 0:
                    new_point = (random.uniform(-10, -5), random.uniform(-10, -5))
                elif i % 3 == 1:
                    new_point = (random.uniform(-8, 0), random.uniform(2, 10))
                else:
                    new_point = (random.uniform(1, 10), random.uniform(-5, 5))

                if is_valid_point(new_point, existing_points):
                    missions[i] = [new_point, 2, 2]
                    existing_points.append(new_point)
                    break
    return missions


if __name__ == "__main__":
    # [position, duration, energy_consumption]
    # missions = {'Depot': [(0, 0), 0,0], 'A': [(1, 4), 2,2], 'B': [(2, 3,), 2,2], 'C': [(4, 3), 2,2], 'D': [(3, -3), 2,2],
    #             'E': [(1, -3), 2,2], 'F': [(-3, -1), 2,2], 'G': [(-4, 0), 2,2]}
    missions = {'Depot_s': [(0, 0), 0, 0], 'Depot_t': [(0, 0), 0, 0], 'A': [(1, 4), 2, 2], 'B': [(2, 3,), 2, 2],
                'C': [(4, 3), 2, 2], 'D': [(3, -3), 2, 2], 'E': [(1, -3), 2, 2], 'F': [(-3, -1), 2, 2],
                'G': [(-4, 0), 2, 2]}

    #missions=get_random_instance(20,True)

    # [velocity, max energy, route]
    drones = {'quadro1': {'velocity': 1, 'energy_capacity': 30, 'current_optimal_path': [], 'total_travel_time': None},
              'quadro2': {'velocity': 1, 'energy_capacity': 30, 'current_optimal_path': [], 'total_travel_time': None},
              'quadro3': {'velocity': 1, 'energy_capacity': 30, 'current_optimal_path': [], 'total_travel_time': None}}
    # ,'quadro4':{'velocity':5, 'energy_capacity':30, 'current_optimal_path':[], 'total_travel_time':None}}

    create_graph(missions)
    save_drone_data(drones)
