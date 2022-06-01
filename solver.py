import json
import random
from termcolor import colored


class TabooSearchSolver(object):
    def __init__(self, data_path: str,  taboo_list_size, seed=None) -> None:
        self.data = self.__load_data(data_path)
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(0, 10000)

        self.initial_solution = self.__create_initial_solution(
            self.data, seed=seed, show=True)

        self.current_solution = self.initial_solution.copy()

        self.best_solution = self.initial_solution.copy()
        self.best_solution_value = self.__calculate_value()

        self.taboo_list = []
        self.taboo_list_size = taboo_list_size

    def __load_data(self, json_path: str):
        """
        Loads data from a JSON file.
        """
        with open(json_path, "r") as f:
            data = json.load(f)

            try:
                data = {int(key): {int(key2): value2 for key2, value2 in value.items()}
                        for key, value in data.items()}
            except:
                pass

        return data

    def __swap(self, solution: list, i, j) -> list:
        """
        Takes a list and swaps the elements at index i and j.
        """
        solution_copy = solution.copy()

        solution_copy[i], solution_copy[j] = solution_copy[j], solution_copy[i]

        return solution_copy

    def __create_initial_solution(self, instances: dict, seed: int, show: bool = False) -> list:
        """
        Creates a random initial solution.
        """
        n_jobs = len(instances)
        initial_solution = list(range(1, n_jobs + 1))

        random.seed(seed)

        random.shuffle(initial_solution)

        if show:
            print("Initial solution:", initial_solution)

        return initial_solution

    def __calculate_value(self):
        """
        Calculates the value of the current solution.
        """
        value = 0

        for first_node_idx in range(len(self.current_solution) - 1):
            first_node = self.current_solution[first_node_idx]
            second_node = self.current_solution[first_node_idx + 1]

            lowest_node = min(first_node, second_node)
            highest_node = max(first_node, second_node)

            temp_value = self.data[lowest_node][highest_node]
            value += temp_value

        return value

    def __calculate_neighbor_value(self, neighbor: list) -> int:
        """
        Calculates the value of a neighbor.
        """
        neighbor_value = 0

        for first_node_idx in range(len(neighbor) - 1):
            first_node = neighbor[first_node_idx]
            second_node = neighbor[first_node_idx + 1]

            lowest_node = min(first_node, second_node)
            highest_node = max(first_node, second_node)

            if lowest_node == highest_node:
                continue

            temp_value = self.data[lowest_node][highest_node]
            neighbor_value += temp_value

        return_cost = self.data[min(
            neighbor[0], neighbor[-1])][max(neighbor[0], neighbor[-1])]

        return neighbor_value + return_cost

    def __is_taboo(self, node_idx: int) -> bool:
        """
        Checks if a node is taboo.
        """
        return node_idx in self.taboo_list

    def __is_solution_better(self, solution: list) -> bool:
        """
        Checks if a solution is better than the current best solution.
        """
        solution_value = self.__calculate_neighbor_value(solution)

        if solution_value < self.best_solution_value:
            return True

        return False

    def __generate_neighbors(self, solution: list) -> list:
        """
        Generates neighbors of a solution.
        """
        neighbors = []

        for i in range(len(solution) - 1):
            for j in range(i + 1, len(solution)):
                neighbor = self.__swap(solution, i, j)

                if not self.__is_taboo(neighbor):
                    neighbors.append(neighbor)

        return neighbors

    def __get_best_neighbor(self, neighbors: list) -> list:
        """
        Returns the best neighbor of a solution.
        """
        best_neighbor = None
        best_neighbor_value = float("inf")

        for neighbor in neighbors:
            neighbor_value = self.__calculate_neighbor_value(neighbor)

            if neighbor_value < best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value

        return best_neighbor

    def solve(self, iteration: int) -> list:
        """
        Solves the TSP problem using Taboo Search.
        """
        for i in range(iteration):
            neighbors = self.__generate_neighbors(self.current_solution)
            # print(colored("Iteration:", "green"), i)

            best_neighbor = self.__get_best_neighbor(neighbors)

            if self.__is_solution_better(best_neighbor):

                self.current_solution = best_neighbor
                self.best_solution = best_neighbor
                self.best_solution_value = self.__calculate_neighbor_value(
                    best_neighbor)
                temp_neighbor = best_neighbor.copy()
                temp_neighbor.append(temp_neighbor[0])
                print("Iteration:", i, "Best neighbor:", temp_neighbor,
                      "Value:", self.best_solution_value)

            self.taboo_list.append(self.current_solution[0])

            if len(self.taboo_list) > self.taboo_list_size:
                self.taboo_list.pop(0)

        return self.best_solution
