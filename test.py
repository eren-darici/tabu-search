from solver import TabooSearchSolver

solver = TabooSearchSolver('data.json', taboo_list_size=2, seed=1)
solver.solve(iteration=300)
