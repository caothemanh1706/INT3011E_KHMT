import time

def solve_cpsat(n):
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    
    queens = [model.NewIntVar(0, n - 1, f'q_{i}') for i in range(n)]
    
    model.AddAllDifferent(queens)
    model.AddAllDifferent([queens[i] + i for i in range(n)])
    model.AddAllDifferent([queens[i] - i for i in range(n)])
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return [solver.Value(queens[i]) for i in range(n)]
    return None

def solve_gurobi(n):
    import gurobipy as gp
    from gurobipy import GRB
    try:
        # Create a new model
        m = gp.Model("nqueens")
        m.setParam('OutputFlag', 0)
        
        # Create variables
        x = m.addVars(n, n, vtype=GRB.BINARY, name="x")
        
        # Add constraints
        m.addConstrs((x.sum(i, '*') == 1 for i in range(n)), name="row")
        m.addConstrs((x.sum('*', j) == 1 for j in range(n)), name="col")
        
        for k in range(-n+1, n):
            m.addConstr(gp.quicksum(x[i, i-k] for i in range(n) if 0 <= i-k < n) <= 1, name=f"diag1_{k}")
            m.addConstr(gp.quicksum(x[i, n-1-i-k] for i in range(n) if 0 <= n-1-i-k < n) <= 1, name=f"diag2_{k}")
            
        m.optimize()
        if m.status == GRB.OPTIMAL:
            return [[int(x[i, j].X > 0.5) for j in range(n)] for i in range(n)]
        return None
    except Exception as e:
        print(f"Gurobi error: {e}")
        return None

def solve_cplex_mip(n):
    import docplex.mp.model as cpx
    try:
        mdl = cpx.Model(name="nqueens")
        mdl.context.solver.log_output = False
        
        x = mdl.binary_var_matrix(n, n, name="x")
        
        for i in range(n):
            mdl.add_constraint(mdl.sum(x[i, j] for j in range(n)) == 1)
        for j in range(n):
            mdl.add_constraint(mdl.sum(x[i, j] for i in range(n)) == 1)
            
        for k in range(-n+1, n):
            mdl.add_constraint(mdl.sum(x[i, i-k] for i in range(n) if 0 <= i-k < n) <= 1)
            mdl.add_constraint(mdl.sum(x[i, n-1-i-k] for i in range(n) if 0 <= n-1-i-k < n) <= 1)
            
        sol = mdl.solve()
        if sol:
            return [[int(sol.get_value(x[i, j]) > 0.5) for j in range(n)] for i in range(n)]
        return None
    except Exception as e:
        print(f"Cplex error: {e}")
        return None
        
def solve_cplex_cp(n):
    try:
        from docplex.cp.model import CpoModel
        mdl = CpoModel(name="nqueens")
        
        queens = mdl.integer_var_list(n, 0, n - 1, "q")
        
        mdl.add(mdl.all_diff(queens))
        mdl.add(mdl.all_diff([queens[i] + i for i in range(n)]))
        mdl.add(mdl.all_diff([queens[i] - i for i in range(n)]))
        
        sol = mdl.solve(LogVerbosity="Quiet")
        if sol:
            return [sol[queens[i]] for i in range(n)]
        return None
    except Exception as e:
        print(f"Cplex CP error: {e}")
        return None

