import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import json



def VRP(Graph, drone_data):
    pass


if __name__ == "__main__":

    #reading in data
    Graph = nx.read_gml("graph.gml")
    with open('drone_data.json', 'r') as json_file:
        drones = json.load(json_file)

    print('Hi. Done!')