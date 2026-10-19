from pysat.solvers import Glucose3

new_variables_count = 0

# khơi tạo bàn cờ
def genarate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

# khởi tạo biến phụ

def genarate_new_variables(new_variables_count, length):
    start = n ** 2 + new_variables_count
    return [i for i in range(start + 1, start + length)]

# most one queen

def at_most_one(clauses, variables):
    global new_variables_count 
    new_variables = genarate_new_variables(new_variables_count, len(variables))
    new_variables_count += (len(new_variables))
    clauses.append([-variables[0], new_variables[0]])
    for i in range(1, len(variables) - 1):
        clauses.append([-variables[i], new_variables[i]])
        clauses.append([-new_variables[i - 1], new_variables[i]])
        clauses.append([-new_variables[i - 1], -variables[i]])
    clauses.append([-new_variables[len(variables) - 2], -variables[len(variables) - 1]])

# exactly one queen

def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)

# check

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

# solve

def solve_n_queens(n):
    variables = genarate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()

    for clause in clauses :
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j]) > 0 for j in range(n)] for i in range(n)]
    else :
        return None

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))

if __name__ == "__main__":
    n = 128  # Change this value to solve for different sizes of the N-Queens problem
    solution = solve_n_queens(n)
    print_solution(solution)
