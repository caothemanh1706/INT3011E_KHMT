import time
import csv
import multiprocessing
import sys
import os

def worker_task(solver_name, n, return_dict):
    sys.stdout = open(os.devnull, 'w')
    import time
    from pysat.solvers import Glucose3

    global solve_duration, nof_vars, nof_clauses
    solve_duration = 0.0
    nof_vars = 0
    nof_clauses = 0

    original_solve = Glucose3.solve

    def patched_solve(self, *args, **kwargs):
        global solve_duration, nof_vars, nof_clauses
        start = time.time()
        res = original_solve(self, *args, **kwargs)
        solve_duration = time.time() - start
        nof_vars = self.nof_vars()
        nof_clauses = self.nof_clauses()
        return res

    Glucose3.solve = patched_solve

    import binary, binomial, sequential
    binary.n = n
    binomial.n = n
    sequential.n = n

    from slovers import solve_gurobi, solve_cplex_cp, solve_cplex_mip, solve_cpsat

    solvers = {
        'SAT-Binary': binary.solve_n_queens,
        'SAT-Binomial': binomial.solve_n_queens,
        'SAT-Sequential': sequential.solve_n_queens,
        'Gurobi': solve_gurobi,
        'CPLEX-CP': solve_cplex_cp,
        'CPLEX-MIP': solve_cplex_mip,
        'CP-SAT': solve_cpsat
    }

    start_total = time.time()
    try:
        sol = solvers[solver_name](n)
        total_time = time.time() - start_total

        if sol == "LIMIT":
            status = "LIMIT"
        elif sol == "UNSAT":
            status = "UNSAT"
        else:
            status = "SAT"

    except Exception as e:
        total_time = time.time() - start_total
        status = f"Error: {e}"

    encoding_time = total_time - solve_duration
    if encoding_time < 0:
        encoding_time = 0.0

    if not solver_name.startswith('SAT'):
        encoding_time = 0.0
        solve_duration = total_time
        nof_vars = 0
        nof_clauses = 0

    return_dict['Variables'] = nof_vars
    return_dict['Clauses'] = nof_clauses
    return_dict['EncodingTime'] = encoding_time
    return_dict['SolveTime'] = solve_duration
    return_dict['TotalTime'] = total_time
    return_dict['Status'] = status

def run_experiments():
    ns = [8, 16, 32, 64, 100, 128, 256, 512]
    solvers = [
        'SAT-Binomial',
        'SAT-Binary',
        'SAT-Sequential',
        'Gurobi',
        'CPLEX-CP',
        'CPLEX-MIP',
        'CP-SAT'
    ]
    timeout_sec = 60

    print("N,Encoding,Variables,Clauses,EncodingTime,SolveTime,TotalTime,Status")

    with open("experiment_results_large3.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "N", "Encoding", "Variables", "Clauses",
            "EncodingTime", "SolveTime", "TotalTime", "Status"
        ])

        for n in ns:
            for solver in solvers:
                manager = multiprocessing.Manager()
                return_dict = manager.dict()

                p = multiprocessing.Process(
                    target=worker_task,
                    args=(solver, n, return_dict)
                )
                p.start()
                p.join(timeout_sec)

                if p.is_alive():
                    p.terminate()
                    p.join()
                    row = [
                        n, solver, "", "", "", "",
                        ">60s", "TIMEOUT"
                    ]

                elif 'Status' in return_dict:
                    row = [
                        n,
                        solver,
                        return_dict.get('Variables', ''),
                        return_dict.get('Clauses', ''),
                        f"{return_dict.get('EncodingTime', 0):.3f}",
                        f"{return_dict.get('SolveTime', 0):.3f}",
                        f"{return_dict.get('TotalTime', 0):.3f}",
                        return_dict.get('Status', 'Error')
                    ]

                else:
                    row = [
                        n, solver, "", "", "", "", "",
                        "Crash/Error"
                    ]

                writer.writerow(row)
                f.flush()
                print(",".join(map(str, row)))

if __name__ == '__main__':
    run_experiments()
