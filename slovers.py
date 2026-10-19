TIME_LIMIT = 60


def solve_cpsat(n):
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    q = [model.NewIntVar(0, n - 1, f"q_{i}") for i in range(n)]

    model.AddAllDifferent(q)
    model.AddAllDifferent([q[i] + i for i in range(n)])
    model.AddAllDifferent([q[i] - i for i in range(n)])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = TIME_LIMIT

    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return [solver.Value(q[i]) for i in range(n)]

    if status == cp_model.INFEASIBLE:
        return "UNSAT"

    return "TIMEOUT"


def solve_gurobi(n):
    import gurobipy as gp
    from gurobipy import GRB

    try:
        m = gp.Model("nqueens")
        m.setParam("OutputFlag", 0)
        m.setParam("TimeLimit", TIME_LIMIT)

        x = m.addVars(n, n, vtype=GRB.BINARY, name="x")

        m.addConstrs(
            (x.sum(i, "*") == 1 for i in range(n))
        )

        m.addConstrs(
            (x.sum("*", j) == 1 for j in range(n))
        )

        for k in range(-n + 1, n):
            m.addConstr(
                gp.quicksum(
                    x[i, i-k]
                    for i in range(n)
                    if 0 <= i-k < n
                ) <= 1
            )

            m.addConstr(
                gp.quicksum(
                    x[i, n-1-i-k]
                    for i in range(n)
                    if 0 <= n-1-i-k < n
                ) <= 1
            )

        m.optimize()

        if m.status == GRB.OPTIMAL:
            return [
                [int(x[i, j].X > 0.5) for j in range(n)]
                for i in range(n)
            ]

        if m.status == GRB.TIME_LIMIT:
            return "TIMEOUT"

        if m.status == GRB.INFEASIBLE:
            return "UNSAT"

        return "LIMIT"

    except gp.GurobiError as e:
        msg = str(e).lower()

        # Gurobi license / model-size limitation
        if (
            "size-limited license" in msg
            or "model too large" in msg
            or "restricted license" in msg
            or "license" in msg
        ):
            return "LIMIT"

        print(f"Gurobi error: {e}")
        return "ERROR"

    except Exception as e:
        print(f"Gurobi error: {e}")
        return "ERROR"


def solve_cplex_mip(n):
    import docplex.mp.model as cpx

    try:
        mdl = cpx.Model(name="nqueens")
        mdl.context.solver.log_output = False
        mdl.parameters.timelimit = TIME_LIMIT

        x = mdl.binary_var_matrix(n, n, name="x")

        for i in range(n):
            mdl.add_constraint(
                mdl.sum(x[i, j] for j in range(n)) == 1
            )

        for j in range(n):
            mdl.add_constraint(
                mdl.sum(x[i, j] for i in range(n)) == 1
            )

        for k in range(-n + 1, n):
            mdl.add_constraint(
                mdl.sum(
                    x[i, i-k]
                    for i in range(n)
                    if 0 <= i-k < n
                ) <= 1
            )

            mdl.add_constraint(
                mdl.sum(
                    x[i, n-1-i-k]
                    for i in range(n)
                    if 0 <= n-1-i-k < n
                ) <= 1
            )

        sol = mdl.solve()

        if sol:
            return [
                [
                    int(sol.get_value(x[i, j]) > 0.5)
                    for j in range(n)
                ]
                for i in range(n)
            ]

        return "TIMEOUT"

    except Exception as e:
        msg = str(e).lower()

        # CPLEX license / model-size limitation
        if (
            "license" in msg
            or "limit" in msg
            or "community edition" in msg
            or "size" in msg
        ):
            return "LIMIT"

        print(f"CPLEX MIP error: {e}")
        return "ERROR"


def solve_cplex_cp(n):
    from docplex.cp.model import CpoModel

    try:
        mdl = CpoModel(name="nqueens")

        q = mdl.integer_var_list(
            n,
            0,
            n - 1,
            "q"
        )

        mdl.add(mdl.all_diff(q))

        mdl.add(
            mdl.all_diff(
                [q[i] + i for i in range(n)]
            )
        )

        mdl.add(
            mdl.all_diff(
                [q[i] - i for i in range(n)]
            )
        )

        sol = mdl.solve(
            TimeLimit=TIME_LIMIT,
            LogVerbosity="Quiet"
        )

        if sol:
            return [
                sol[q[i]]
                for i in range(n)
            ]

        return "TIMEOUT"

    except Exception as e:
        msg = str(e).lower()

        # CPLEX license / model-size limitation
        if (
            "license" in msg
            or "limit" in msg
            or "community edition" in msg
            or "size" in msg
        ):
            return "LIMIT"

        print(f"CPLEX CP error: {e}")
        return "ERROR"