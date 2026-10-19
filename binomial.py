import time

from pysat.solvers import Glucose3

def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def at_most_one(clauses, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses

def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)

def generate_clauses(n, variables):
    clauses = []

    # check in row
    for i in range(n):
        exactly_one(clauses, variables[i])

    # check in column
    for j in range(n):
        exactly_one(clauses, [variables[i][j] for i in range(n)])

    # check in diagonal
    for i in range(1, n):
        diagonal = []
        row = i
        col = 0
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(clauses, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = n - 1
        col = j
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(clauses, diagonal)

    for i in range(n - 1):
        diagonal = []
        row = i
        col = 0
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(clauses, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = 0
        col = j
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(clauses, diagonal)

    return clauses

def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
       # print(solution)
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


if __name__ == '__main__':
        with open("size.txt", "r") as file:
            sizes = [int(line.strip()) for line in file if line.strip()]
        print(f"{'N':>8} {'Time (seconds)':>20}")
        print("-" * 50)
    
        for n in sizes:
            start_time = time.perf_counter()
            solution = solve_n_queens(n)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"{n:>8} {execution_time:>20.6f}")
    