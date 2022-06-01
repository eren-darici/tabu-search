from solver import TabuSearchSolver

solver = TabuSearchSolver('data.json', taboo_list_size=2)
solver.solve(iteration=300)
