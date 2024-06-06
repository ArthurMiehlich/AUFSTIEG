from plot import *
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import json
import os


def VRP(Graph, drone_data):
    N_drones = len(drone_data)
    m = gp.Model('VRP')

    # variable denotes if edge (u,v) is taken by drone d
    x = {}
    for d in range(N_drones):
        for (u, v) in Graph.edges:
            x[d, u, v] = m.addVar(vtype=GRB.BINARY, name=f'x_{d}_{u}_{v}')
            x[d, v, u] = m.addVar(vtype=GRB.BINARY, name=f'x_{d}_{v}_{u}')

    # variable denotes the current energy consumption of drone d at node n
    y = {}
    for d in range(N_drones):
        for n in Graph.nodes:
            y[d, n] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f'y_{d}_{n}')

    # variable denoting time of drone d at node n
    t = {}
    for d in range(N_drones):
        for n in Graph.nodes:
            t[d, n] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f't_{d}_{n}')

    # objective function: minimize total flight time
    obj = gp.quicksum(
        gp.quicksum(
            gp.quicksum(
                Graph.get_edge_data(u, v)['weight'] * (x[d, u, v])
            for u in Graph.nodes if u!=v)
            for v in Graph.nodes)
        for d in range(N_drones))
    m.setObjective(obj, GRB.MINIMIZE)

    # customer constraints
    for j in Graph.nodes:
        if j != 'Depot':
            m.addConstr(
                1 == gp.quicksum(gp.quicksum(x[d, i, j] for i in Graph.nodes if i != j) for d in range(N_drones)),
                name=f'visit_{j}')
            m.addConstr(
                1 == gp.quicksum(gp.quicksum(x[d, j, i] for i in Graph.nodes if i != j) for d in range(N_drones)),
                name=f'leave_{j}')

    # flow constraints
    for d in range(N_drones):
        for u in Graph.nodes:
            m.addConstr(0==gp.quicksum(x[d,u,v] for v in Graph.nodes if u!=v)-gp.quicksum(x[d,v,u] for v in Graph.nodes if u!=v), name=f'flow_{d}_{u}')

    # Depot constraints

    for d in range(N_drones):
        m.addConstr(1 == gp.quicksum(x[d, i, 'Depot'] for i in Graph.nodes if i != 'Depot'), name=f"drone_{d}_depot_arrival")
        m.addConstr(1 == gp.quicksum(x[d, 'Depot', i] for i in Graph.nodes if i != 'Depot'), name=f"drone_{d}_leaves_depot")

    # time constraint
    M = 1000
    for d in range(N_drones):
        for u in Graph.nodes:
            for v in Graph.nodes:
                if u!=v and v!='Depot':
                    m.addConstr(t[d, u] - t[d, v] + Graph.nodes[v]['duration'] + Graph.get_edge_data(u, v)['weight'] <= M * (
                        1 - x[d, u, v]), name=f"Time_constr_{d}_{u}_{v}")

    m.write("test.lp")
    m.optimize()
    #m.write("test.sol")
    #os.system("gedit test.lp &")
    #os.system("gedit test.sol &")

    for d in range(N_drones):
        for (u, v) in Graph.edges:
            if round(x[d, u, v].x) == 1:
                print(f'Drohne {d} fliegt von {u} nach {v}.')
            if round(x[d, v, u].x) == 1:
                print(f'Drohne {d} fliegt von {v} nach {u}.')

    for d in range(N_drones):
        for n in Graph.nodes:
            if round(t[d, n].x) != 0:
                print(f'Drohne {d} ist zu Zeitpunkt {t[d, n].x} an Knoten {n}.')

    x_values = {}
    if m.status == GRB.OPTIMAL:
        for d in range(N_drones):
            for (u, v) in Graph.edges:
                x_values[d, u, v] = round(x[d, u, v].X)
                x_values[d, v, u] = round(x[d, v, u].X)

    plot_sol(Graph,x_values)


if __name__ == "__main__":
    # reading in data
    Graph = nx.read_gml("graph.gml")
    with open('drone_data.json', 'r') as json_file:
        drones = json.load(json_file)
    VRP(Graph, drones)
