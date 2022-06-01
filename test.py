from solver import TabuSearchSolver

solver = TabuSearchSolver('data.json', taboo_list_size=3)
solver.solve(iteration=300)
solver.show_results_as_graph()
