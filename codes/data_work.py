import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json


def read_instance(instance_file):
    with open(instance_file, 'r') as json_file:
        data = json.load(json_file)
    environment = data.get('environment')
    fleet = data.get('fleet').get('aircraft')
    tasks = data.get('tasks')
    points = {point["id"]: point for point in environment.get('points')}
    # Create Graph
    G = nx.DiGraph()
    for node in tasks:
        if node.startswith('Depot'):
            if node.startswith('Depot_s'):
                string = 'departure'
            else:
                string = 'arrival'
        else:
            string = 'waypoint'
        waypoint = tasks[node][string]['point']
        duration = tasks[node][string]['duration']
        pos = points[waypoint].get('position_xy_m')
        G.add_node(node, pos=pos, duration=duration)
    for node1 in tasks:
        for node2 in tasks:
            if node1 != node2:
                distance, energyconsumption = heuristic_calculations(node1, node2, G)
                G.add_edge(node1, node2, distance=distance)

    position = nx.get_node_attributes(G, 'pos')
    nx.draw(G, position, with_labels=True, node_size=100, node_color='skyblue', font_size=10)
    # plt.show()
    plt.savefig('Graph.pdf')

    return G, fleet


def heuristic_calculations(node1, node2, G):
    pos1 = G.nodes[node1]['pos']
    pos2 = G.nodes[node2]['pos']
    distance = np.linalg.norm(np.array(pos1) - np.array(pos2))

    return distance, 0


def write_missions(missions_file, all_paths):
    missions = {}
    for i in list(all_paths.keys()):
        name = f"{i}-mission-1"
        missions[name] = {"aircraft_id": i, "mission": {"tasks": all_paths[i]}}
    with open(missions_file, 'w') as file:
        json.dump(missions, file, indent=2)


def generate_task(point, duration):
    return {
        "waypoint": {"point": point,
                     "duration": duration}
    }


def write_instance(instance_str, N_missions, orig_instance_str='instance.json'):
    with open(orig_instance_str, 'r') as json_file:
        data = json.load(json_file)
    environment = data.get('environment')
    fleet = data.get('fleet').get('aircraft')
    old_tasks = data.get('tasks')
    points = {point["id"]: point for point in environment.get('points')}
    feasible_ports = [key for key in points if key.startswith('verti')]
    depot = random.sample(feasible_ports, 2)
    tasks = {"Depot_s": {
        "departure": {
            "point": depot[0],
            "duration": 0
        }
    },
        "Depot_t": {
            "arrival": {
                "point": depot[1],
                "duration": 0
            }
        }}
    points.pop(depot[0])
    points.pop(depot[1])
    sample_points = random.sample(list(points), N_missions)
    for ind, p in enumerate(sample_points):
        tasks[chr(ord('A') + ind)] = generate_task(p, random.randint(0, 20) * 100)
    data['tasks'] = tasks
    with open(instance_str, 'w') as file:
        json.dump(data, file, indent=2)


if __name__ == "__main__":
    write_instance('instance.json', 5)

    '''
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
'''
