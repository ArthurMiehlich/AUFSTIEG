import gurobipy as gp
from gurobipy import GRB

def solve_vrp():
    # Create a new model
    m = gp.Model('VRP')

    # Create variables
    t={}
    for i in range(3):
        t[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=100, name='t')
    maxTime = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name='maxTime')

    # Set objective
    m.setObjective(maxTime, GRB.MINIMIZE)

    # Add constraint
    for i in range(3):
        m.addConstr(t[i] <= maxTime, name='max_time_constraint')

    # Optimize model
    m.optimize()

    # Print solution
    for i in range(3):
        print(f"Optimal solution: t = {t[i].X}, maxTime = {maxTime.X}")

solve_vrp()
