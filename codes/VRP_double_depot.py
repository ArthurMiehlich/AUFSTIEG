from data_work import *
from plot import *
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import json


########################################################################################################################
##                                                                                                                    ##
##                                              VRP generell funktioniert                                             ##
##                                evtl zu viele constraints, Zeit und energie gehen noch nicht                        ##
##                                                                                                                    ##
########################################################################################################################


def VRP(Graph, drone_data):
    drone_names = drone_data.keys()
    m = gp.Model('VRP')

    # variable denotes if edge (u,v) is taken by drone d
    x = {}
    for d in drone_names:
        for (u, v) in Graph.edges:
            x[d, u, v] = m.addVar(vtype=GRB.BINARY, name=f'x_{d}_{u}_{v}')
            x[d, v, u] = m.addVar(vtype=GRB.BINARY, name=f'x_{d}_{v}_{u}')

    # variable denotes the current energy consumption of drone d at node n
    y = {}
    for d in drone_names:
        for n in Graph.nodes:
            y[d, n] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f'y_{d}_{n}')
        # y[d, 'Depot_s'] = 0

    # variable denoting time of drone d at node n
    t = {}
    for d in drone_names:
        for n in Graph.nodes:
            t[d, n] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f't_{d}_{n}')
        # t[d, 'Depot_s'] = 0

    maxTime = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name='maxTime')

    # objective function: minimize total flight time
    obj = (gp.quicksum(
        gp.quicksum(
            gp.quicksum(
                Graph.get_edge_data(u, v)['distance'] * 1 / drone_data[d]['performance']['multicopter'][
                    'cruise_speed_mDs'] * (x[d, u, v])
                for u in Graph.nodes if u != v)
            for v in Graph.nodes)
        for d in drone_names)
           + maxTime)
    m.setObjective(obj, GRB.MINIMIZE)

    # customer constraints
    for j in Graph.nodes:
        if j not in ['Depot_s', 'Depot_t']:
            m.addConstr(
                1 == gp.quicksum(gp.quicksum(x[d, i, j] for i in Graph.nodes if i != j) for d in drone_names),
                name=f'visit_{j}')
            m.addConstr(
                1 == gp.quicksum(gp.quicksum(x[d, j, i] for i in Graph.nodes if i != j) for d in drone_names),
                name=f'leave_{j}')

    # flow constraints
    for d in drone_names:
        for u in Graph.nodes:
            if u not in ['Depot_s', 'Depot_t']:
                m.addConstr(0 == gp.quicksum(x[d, u, v] for v in Graph.nodes if u != v) - gp.quicksum(
                    x[d, v, u] for v in Graph.nodes if u != v), name=f'flow_{d}_{u}')

    # Depot constraints
    for d in drone_names:
        m.addConstr(1 == gp.quicksum(x[d, i, 'Depot_t'] for i in Graph.nodes if i not in ['Depot_s', 'Depot_t']),
                    name=f"drone_{d}_depot_arrival")
        m.addConstr(1 == gp.quicksum(x[d, 'Depot_s', i] for i in Graph.nodes if i not in ['Depot_s', 'Depot_t']),
                    name=f"drone_{d}_leaves_depot")

    # time constraint (klappt noch nicht korrekt)
    M = 1000000
    for d in drone_names:
        for u in Graph.nodes:
            for v in Graph.nodes:
                if u != v:
                    m.addConstr(
                        t[d, u] - t[d, v] + Graph.nodes[v]['duration'] + Graph.get_edge_data(u, v)['distance'] * 1 /
                        drone_data[d]['performance']['multicopter']['cruise_speed_mDs'] <= M * (1 - x[d, u, v]),
                        name=f"Time_constr_{d}_{u}_{v}")

    # # energy constraint (klappt noch nicht korrekt)
    # for d in drone_names:
    #     for u in Graph.nodes:
    #         for v in Graph.nodes:
    #             if u != v:
    #                 m.addConstr(y[d, u] - y[d,v] + Graph.get_edge_data(u, v)['energy_consumption'] * x[d, u, v] <=
    #                             1000, name=f"Energy_constr_{d}_{u}_{v}")

    for d in drone_names:
        m.addConstr(t[d, 'Depot_t'] <= maxTime, name=f'max_Time_{d}')

    m.write("test.lp")
    m.setParam('TimeLimit', 30)
    m.optimize()
    # m.write("test.sol")
    # os.system("gedit test.lp &")
    # os.system("gedit test.sol &")

    print(f"Gesamtzeit ist {maxTime.x}.")
    depot = 'Depot_s'
    all_paths = {}
    for d in drone_names:
        current_node = depot
        path = [depot]
        while True:
            next_node = None
            for v in Graph.nodes:
                if v != current_node:
                    if round(x[d, current_node, v].x) == 1:
                        next_node = v
                        break

            if next_node is None or next_node == 'Depot_t':
                path.append('Depot_t')
                break
            path.append(next_node)
            current_node = next_node
        all_paths[d] = path
        print(f'Drohne {d} Pfad: {" -> ".join(map(str, path))}')
    write_missions('missions1.json', all_paths)
    for d in drone_names:
        for n in all_paths[d]:
            rest_energy = round(drone_data[d]['performance']['multicopter']['energy_capacity_J'] - t[d, n].x, 1)
            print(f'Drohne {d} ist zu Zeitpunkt {round(t[d, n].x, 1)} an Knoten {n}.')
            # mit verbleibenden Energiereserven von {rest_energy}.')
        drone_data[d]['current_optimal_path'] = all_paths[d]
        drone_data[d]['total_travel_time'] = t[d, 'Depot_t'].x

    x_values = {}
    for d in drone_names:
        for (u, v) in Graph.edges:
            x_values[d, u, v] = round(x[d, u, v].X)
            x_values[d, v, u] = round(x[d, v, u].X)

    plot_sol(Graph, x_values, drone_names)


if __name__ == "__main__":
    # reading in data
    Graph, drones = read_instance('instance1.json')
    VRP(Graph, drones)
