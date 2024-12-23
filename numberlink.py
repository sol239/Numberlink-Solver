import itertools
import os
import subprocess
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

class NumberlinkBoard:
    """
    Class for Numberlink board.
    """

    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.board = []
        self.all_clauses = {}
        self.clauses = []
        self.load_from_file(filename)
        self.number_of_paths = self.get_number_of_paths()
        self.paths = {}
        self.theory = ""
        self.start_end_points = {}
        self.start_end_points_locs = []
        self.direction_signs = ["│", "─", "┘", "└", "┐", "┌"]
        self.true_clauses = []
        self.result_board1 = []
        self.numbered_board = []
        self.direction_board_list = []
        self.direction_board_string = ""
        self.cnf_dir_name = "CNFS"
        self.results_dir_name = "RESULTS"

        self.sat_output = ""
        self.instance_result = 0
        self.model = ""

        self.sat_real_time = 0


        self.get_start_end_points()
        self.create_dirs()

        self.is_input_correct()

    def is_input_correct(self):

        correct_paths = [str(x) for x in range(1, self.number_of_paths + 1)]
        paths = []
        for key,values in self.start_end_points.items():
            paths.append(str(key))

        if correct_paths != paths:
            self.exit()

        for key,values in self.start_end_points.items():
            if len(values) != 2:
                self.exit()

        return True

    def create_dirs(self):
        """
        Create directories for CNF files and results
        :return: None
        """
        path = Path(self.cnf_dir_name)
        if not path.exists():
            path.mkdir()
        path = Path(self.results_dir_name)
        if not path.exists():
            path.mkdir()

    def load_from_file(self, filename):
        """
        Method for loading board from txt file
        """

        file = open(filename, "r", encoding="utf-8")
        file_lines = file.readlines()
        modified_lines = []
        for line in file_lines:
            line = line.strip()
            l = line.split(",")
            modified_lines.append(l)

        self.board = modified_lines
        self.height = len(modified_lines)
        self.width = len(modified_lines[0])
        file.close()

    def print_board(self, _board: []):
        """
        Method for printing numberlink board in list representation.
        :param _board:
        :return:
        """
        for line in _board:
            print(line)
        print()

    def print_board_info(self):
        """
        Method for printing board info.
        :return:
        """
        print(f"width = {self.width}")
        print(f"height = {self.height}")
        print(f"number of paths = {self.number_of_paths}")
        print(f"sat real time = {self.sat_real_time} s")
        print(f"number of variables = {len(self.all_clauses)}")
        print(f"number of clauses = {len(self.clauses)}")

    def get_cell(self, i, j):
        """
        Returns cell value on position i, j, where i is vertical and j is horizontal.
        :param i: vertical
        :param j: horizontal
        :return: cell value
        """
        return self.board[i][j]

    def get_number_of_paths(self) -> int:
        """
        Returns number of paths in the board.
        :return:
        """
        _numbers = set()
        for row in self.board:
            for cell in row:
                if cell != ".":
                    _numbers.add(int(cell))
        return len(_numbers)

    def get_start_end_points(self):
        """
        Method for getting starting and ending points of paths.
        :return:
        """
        for i in range(1, self.number_of_paths + 1):
            self.start_end_points[i] = []

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != ".":
                    try:
                        self.start_end_points[int(self.board[i][j])].append((i, j))
                    except:
                        self.exit()
                    self.start_end_points_locs.append((i, j))

    def generate_all_clauses_4D(self, echo=False):
        """
        Generates all combinations of clauses for 4D theory.
        :param echo: print status
        :return:
        """
        counter = 1
        for i in range(self.height):
            for j in range(self.width):
                for p in range(1, self.number_of_paths + 1):
                    for d in range(1, 7):
                        if (i, j) in self.start_end_points[p]:
                            if (i, j, p, 0) not in self.all_clauses:
                                self.all_clauses[(i, j, p, 0)] = counter
                                counter += 1
                        else:
                            if (i, j, p, d) not in self.all_clauses:
                                self.all_clauses[(i, j, p, d)] = counter
                                counter += 1
        if echo:
            print(f"All clauses generated. [{len(self.all_clauses)}]")

    def get_se_points_neigbors(self, i, j, p) -> []:
        """
        Returns neighbors of starting and ending points. They must match their path and direction.
        :param i: vertical
        :param j: horizontal
        :param p: path
        :return: neighbors
        """
        # i = vertical dimension
        # j = horizontal dimension
        # 1 = │, 2 = ─, 3 = ┘, 4 = └, 5 = ┐, 6 = ┌

        neighbors = []

        if i > 0:
            i1 = i - 1
            j1 = j

            possible_direction = [1, 5, 6]
            for d in possible_direction:
                if (i1, j1) not in self.start_end_points_locs:
                    neighbors.append((i1, j1, p, d))

        if i < self.height - 1:

            i1 = i + 1
            j1 = j

            possible_direction = [1, 3, 4]

            for d in possible_direction:
                if (i1, j1) not in self.start_end_points_locs:
                    neighbors.append((i1, j1, p, d))

        if j > 0:

            i1 = i
            j1 = j - 1

            possible_direction = [2, 4, 6]
            for d in possible_direction:
                if (i1, j1) not in self.start_end_points_locs:
                    neighbors.append((i1, j1, p, d))

        if j < self.width - 1:
            i1 = i
            j1 = j + 1

            possible_direction = [2, 3, 5]
            for d in possible_direction:
                if (i1, j1) not in self.start_end_points_locs:
                    neighbors.append((i1, j1, p, d))

        return neighbors

    def get_not_se_points_neighbours(self, i, j, direction) -> []:
        """
        Returns neighbors of non-starting and non-ending points. They must match their path and direction.
        :param i:
        :param j:
        :param direction:
        :return:
        """

        neighbors = []
        possible_direction = []
        if i > 0:
            i1 = i - 1
            j1 = j

            if direction == 1:
                possible_direction = [1, 5, 6]
                for d in possible_direction:
                    if (i1, j1) not in self.start_end_points_locs:
                        neighbors.append((i1, j1, d))
                    else:
                        neighbors.append((i1, j1, 0))

            elif direction == 3:
                possible_direction = [1, 5, 6]
                for d in possible_direction:
                    if (i1, j1) not in self.start_end_points_locs:
                        neighbors.append((i1, j1, d))
                    else:
                        neighbors.append((i1, j1, 0))

            elif direction == 4:
                possible_direction = [1, 5, 6]
                for d in possible_direction:
                    if (i1, j1) not in self.start_end_points_locs:
                        neighbors.append((i1, j1, d))
                    else:
                        neighbors.append((i1, j1, 0))

        if i < self.height - 1:

            i1 = i + 1
            j1 = j

            possible_direction = [1, 3, 4]

            if direction == 1 or direction == 5 or direction == 6:
                for d in possible_direction:
                    if (i1, j1) not in self.start_end_points_locs:
                        neighbors.append((i1, j1, d))
                    else:
                        neighbors.append((i1, j1, 0))

        if j > 0:

            i1 = i
            j1 = j - 1

            possible_direction = [2, 4, 6]

            if direction == 2 or direction == 3 or direction == 5:
                for d in possible_direction:
                    if (i1, j1) not in self.start_end_points_locs:
                        neighbors.append((i1, j1, d))
                    else:
                        neighbors.append((i1, j1, 0))

        if j < self.width - 1:
            i1 = i
            j1 = j + 1

            possible_direction = [2, 3, 5]

            if direction == 2 or direction == 4 or direction == 6:
                for d in possible_direction:
                    if (i1, j1) not in self.start_end_points_locs:
                        neighbors.append((i1, j1, d))
                    else:
                        neighbors.append((i1, j1, 0))

        # remove same neighbors
        neighbors = list(set(neighbors))
        return neighbors

    def generate_clauses_4D(self, echo=False, _extra_clauses = []):
        """
        Generates clauses for 4D theory.
        :param echo: print status
        :param _extra_clauses: extra clauses to eliminate cycles
        :return:
        """

        # 0. Add clauses to eliminate cycles
        if len(_extra_clauses) != 0:
            for cycle in _extra_clauses:
                cycle = set(cycle)
                for p in range(1, self.number_of_paths + 1):
                    clause = []
                    for extra_clause in cycle:
                        i1, j1, p1, d1 = extra_clause
                        clause.append(-self.all_clauses[(i1, j1, p, d1)])
                    self.clauses.append(clause)

        # Iterate over all cells in the number link board.
        for i in range(self.height):
            for j in range(self.width):

                # 1. All starting and ending points are fixed.
                if self.board[i][j] != "." :
                    path = int(self.board[i][j])
                    # starting and ending points have direction 0
                    self.clauses.append([self.all_clauses[(i, j, path, 0)]])
                    for variable in self.all_clauses.items():
                        if variable[0][0] == i and variable[0][1] == j and variable[0][2] != path:
                            self.clauses.append([-variable[1]])   # negating all other paths on the same position

                # 2. Every cell has exactly one path and direction.
                if (i, j) not in self.start_end_points_locs:
                    clause = []
                    combinations = []

                    # At least one is true.
                    for p in range(1, self.number_of_paths + 1):
                        for d in range(1, 7):
                            clause.append(self.all_clauses[(i, j, p, d)])
                            combinations.append((i, j, p, d))
                    self.clauses.append(clause)

                    # At most one is true.
                    for c1 in combinations:
                        for c2 in combinations:
                            if c1 != c2:
                                self.clauses.append([-self.all_clauses[c1], -self.all_clauses[c2]])

                # 3. Every starting and ending point has one neighbor with the same path and possible direction.
                if (i, j) in self.start_end_points_locs:
                    path = int(self.board[i][j])
                    neighbors = self.get_se_points_neigbors(i, j, path)
                    clause = []

                    # At least one neighbor is true.
                    for neighbor in neighbors:
                        clause.append(self.all_clauses[neighbor])
                        for p in range(1, self.number_of_paths + 1):
                            if p != path:
                                n1, n2, p1, d1 = neighbor
                                self.clauses.append([-self.all_clauses[(n1, n2, p, d1)]])
                    self.clauses.append(clause)

                    # At most one neighbor is true.
                    for c1 in neighbors:
                        for c2 in neighbors:
                            if c1 != c2:
                                self.clauses.append([-self.all_clauses[c1], -self.all_clauses[c2]])

                # 4. Every non-starting and non-ending point has exactly two neighbors with the same path and possible direction.
                if (i, j) not in self.start_end_points_locs:
                    for p in range(1, self.number_of_paths + 1):
                        for d in range(1, 7):
                            neighbors = self.get_not_se_points_neighbours(i, j, d)

                            # Adding path to neighbor tuple.
                            _ = []
                            for index in range(len(neighbors)):
                                i1, j1, d1 = neighbors[index]
                                _.append((i1, j1, p, d1))
                            neighbors = _

                            # If the cell is neighbor to the starting or ending point, it must have the same path.
                            for neighbor in neighbors:
                                i1, j1, p1, d1 = neighbor
                                if (i1, j1) in self.start_end_points_locs:
                                    if p != int(self.board[neighbor[0]][neighbor[1]]):
                                        neighbors.remove(neighbor)

                            current_cell = self.all_clauses[(i, j, p, d)]

                            # Unique combinations of neighbors.
                            # Basically each neighbor has to be connected to exactly two neighbors.
                            # And the two neighbors must have different locations.
                            # We will separate neighbors into two groups based on their (i,j) location.
                            # Exactly one neighbor from each group must be true when the current cell is true.

                            unique = set()
                            for neighbor in neighbors:
                                i1, j1, p1, d1 = neighbor
                                unique.add((i1, j1))
                            unique = list(unique)

                            g_1 = []
                            g_2 = []

                            for neighbor in neighbors:
                                i1, j1, p1, d1 = neighbor
                                if (i1, j1) == unique[0]:
                                    g_1.append(neighbor)
                                else:
                                    g_2.append(neighbor)

                            if len(g_1) > len(g_2):
                                g_1, g_2 = g_2, g_1

                            if len(g_1) == 0 or len(g_2) == 0:
                                self.clauses.append([-self.all_clauses[(i, j, p, d)]])
                                continue

                            # At least one neighbor from g_1 is true when current_cell is true.
                            g_1_clause = [-current_cell] + [self.all_clauses[var] for var in g_1]
                            self.clauses.append(g_1_clause)

                            # At least one neighbor from g_2 is true when current_cell is true.
                            g_2_clause = [-current_cell] + [self.all_clauses[var] for var in g_2]
                            self.clauses.append(g_2_clause)

                            # At most one neighbor from g_1 is true when current_cell is true.
                            for n1 in g_1:
                                for n2 in g_1:
                                    if n1 != n2:
                                        self.clauses.append(
                                            # if current_cell is true, than only one of the neighbors from g_1 can be true
                                            # current_cell => -n1 or -n2 <=> -current_cell or -n1 or -n2
                                            [-current_cell, -self.all_clauses[n1], -self.all_clauses[n2]])

                            # At most one neighbor from g_2 is true when current_cell is true.
                            for n1 in g_2:
                                for n2 in g_2:
                                    if n1 != n2:
                                        self.clauses.append(
                                            # if current_cell is true, than only one of the neighbors from g_2 can be true
                                            # current_cell => -var1 or -var2 <=> -current_cell or -var1 or -var2
                                            [-current_cell, -self.all_clauses[n1], -self.all_clauses[n2]])

        if echo:
            print(f"Clauses generated. [{len(self.clauses)}]")

    def generate_all_clauses_3D(self, echo=False):
        """
        Generates all combinations of clauses for 3D theory.
        :param echo:
        :return:
        """

        counter = 1
        for i in range(self.height):
            for j in range(self.width):
                for p in range(1, self.number_of_paths + 1):
                    if (i, j, p, 0) not in self.all_clauses:
                        self.all_clauses[(i, j, p, 0)] = counter
                        counter += 1
        if echo:
            print(f"All clauses generated. [{len(self.all_clauses)}]")

    def generate_clausess_3D(self, echo=False, _extra_clauses = []):
        """
        Generates clauses for 3D theory.
        :param echo:
        :return:
        """

        # 0. Add clauses to eliminate cycles
        if len(_extra_clauses) != 0:
            for cycle in _extra_clauses:
                cycle = set(cycle)
                for p in range(1, self.number_of_paths + 1):
                    clause = []
                    for extra_clause in cycle:
                        i1, j1, p1, d1 = extra_clause
                        clause.append(-self.all_clauses[(i1, j1, p, 0)])
                    self.clauses.append(clause)


        # Iterate over all cells in the number link board.
        for i in range(self.height):
            for j in range(self.width):

                # 1. All starting and ending points are fixed.
                if self.board[i][j] != ".":
                    path = int(self.board[i][j])
                    self.clauses.append([self.all_clauses[(i, j, path, 0)]])
                    for _clause in self.all_clauses.items():
                        if _clause[0][0] == i and _clause[0][1] == j and _clause[0][2] != path:
                            self.clauses.append([-_clause[1]])

                # 2. Every cell which is not start or end point has exactly one path.
                if (i, j) not in self.start_end_points_locs:
                    # At least one path is in the cell
                    _clause = []
                    for p in range(1, self.number_of_paths + 1):
                        _clause.append(self.all_clauses[(i, j, p, 0)])
                    self.clauses.append(_clause)

                    # At most one path is in the cell
                    for p1 in range(1, self.number_of_paths + 1):
                        for p2 in range(1, self.number_of_paths + 1):
                            if p1 != p2:
                                _clause = [-self.all_clauses[(i, j, p1, 0)], -self.all_clauses[(i, j, p2, 0)]]
                                self.clauses.append(_clause)

                # 3. Points which are not start or end points have exactly two neighbors with same path.
                if (i, j) not in self.start_end_points_locs:
                    for p in range(1, self.number_of_paths + 1):
                        neighbors = self.get_neighbors(i, j)
                        # At least 2 neighbors are true.
                        # How this works?
                        # for 2 neighbors: [(5, 6), (6, 5)] we get these combinations:
                        # ((5, 6),)
                        # ((6, 5),) ... we say that if (i, j, p, 0) is true, then (5, 6) is true and if (i, j, p, 0) is true then (6, 5) is true
                        # ---------
                        # for 3 neighbors: [(5, 5), (6, 4), (6, 6)] we get these combinations:
                        # ((5, 5), (6, 4))
                        # ((5, 5), (6, 6))
                        # ((6, 4), (6, 6))
                        # ---------
                        # for 4 neighbors: [(4, 5), (6, 5), (5, 4), (5, 6)] we get these combinations:
                        # ((4, 5), (6, 5), (5, 4))
                        # ((4, 5), (6, 5), (5, 6))
                        # ((4, 5), (5, 4), (5, 6))
                        # ((6, 5), (5, 4), (5, 6))
                        # every time we say that if (i, j, p, 0) is true, then at least one from each combination must be true and since every 2 combinations
                        # have len(combination) - 1 common neighbors, we can say that at least 2 neighbors must be true
                        # if only one neighbor is true, despite that if we iterate over all combinations we will get that at least 2 neighbors must be true
                        for _neighbors in itertools.combinations(neighbors, len(neighbors) - 1):
                            _clause = [-self.all_clauses[(i, j, p, 0)]]
                            for _n in _neighbors:
                                _clause.append(self.all_clauses[(_n[0], _n[1], p, 0)])
                            self.clauses.append(_clause)

                        # Adding path and direction to neighbor tuple.
                        _ = []
                        for index in range(len(neighbors)):
                            i1, j1 = neighbors[index]
                            _.append((i1, j1, p, 0))
                        neighbors = _

                        # At most 2 neighbors are true.
                        for n1 in neighbors:
                            for n2 in neighbors:
                                for n3 in neighbors:
                                    if n1 != n2 and n1 != n3 and n2 != n3:
                                        self.clauses.append([-self.all_clauses[(i, j, p, 0)], -self.all_clauses[n1], -self.all_clauses[n2], -self.all_clauses[n3]])

                        if len(neighbors) == 4:
                            self.clauses.append([-self.all_clauses[(i, j, p, 0)], -self.all_clauses[neighbors[0]], -self.all_clauses[neighbors[1]], -self.all_clauses[neighbors[2]], -self.all_clauses[neighbors[3]]])

                # 4. Every starting and ending point has one neighbor with the same path.
                # - this ensures that path will not connect back to itself
                # - this constraint eliminates some possible solution, especially zigzag ines
                for p in range(1, self.number_of_paths + 1):
                    if (i, j) in self.start_end_points[p]:
                        neighbors = self.get_neighbors(i, j)

                        # At least one neighbor is in the same path
                        _clause = [self.all_clauses[(n[0], n[1], p, 0)] for n in neighbors]
                        self.clauses.append(_clause)

                        # At most one neighbor is in the same path
                        for n1 in neighbors:
                            for n2 in neighbors:
                                if n1 != n2:
                                    self.clauses.append([
                                        -self.all_clauses[(n1[0], n1[1], p, 0)],
                                        -self.all_clauses[(n2[0], n2[1], p, 0)]])

        if echo:
            print(f"Clauses generated. [{len(self.clauses)}]")

    def print_clauses_variables(self, clause):
        """
        Helper method for printing clauses.
        :param clause:
        :return:
        """

        result = ""
        for c in clause:
            # find key by value
            index = abs(c)
            for key, value in self.all_clauses.items():
                if value == index:
                    if c < 0:
                        result += "-" + str(key) + " "
                    else:
                        result += str(key) + " "

        print(result)

    def get_neighbors(self, i, j):
        """
        Returns all neighbors of cell i, j.
        :param i:
        :param j:
        :return:
        """
        neighbors = []
        if i > 0:
            neighbors.append((i - 1, j))
        if i < self.height - 1:
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < self.width - 1:
            neighbors.append((i, j + 1))
        return neighbors

    def save_to_dimacs(self, filename):
        """
        Saves clauses to DIMACS format.
        """

        filename = filename.split("/")[-1].split(".")[0]
        num_variables = len(self.all_clauses)
        num_clauses = len(self.clauses)
        with open(f"CNFS/{self.theory}-{filename}.cnf", "w") as file:
            file.write(f"p cnf {num_variables} {num_clauses}\n")
            for clause in self.clauses:
                file.write(" ".join(map(str, clause)) + " 0\n")

    def retrieve_paths_from_models(self, models):
        """
        Retrieves paths from models.
        :param models:
        :return:
        """

        # construct empty paths
        for i in range(1, self.number_of_paths + 1):
            self.paths[i] = []

        for true_clause in self.true_clauses:
            i, j, p, d = true_clause
            self.paths[p].append((i, j))

    def get_true_variables(self, models, _print=False):
        """
        Retrieves true clauses from models.
        :param models:
        :param _print:
        :return:
        """

        models = map(int, models.split(" ")[1:-1])

        if _print:
            print("-" * 50)

        for model in models:
            abs_model = abs(model)  # Compute absolute value once
            if model > 0:  # Only consider positive models
                true_vars = [
                    (i, j, p, d)
                    for (i, j, p, d), var in self.all_clauses.items()
                    if var == abs_model
                ]
                self.true_clauses.extend(true_vars)  # Add all matching variables

                if _print:
                    for (i, j, p, d) in true_vars:
                        print(f"Variable {abs_model} is True: {i, j, p, d}")

        if _print:
            print("-" * 50)

    def print_paths(self):
        """
        Prints paths.
        :return:
        """
        for path, cells in self.paths.items():
            print(f"Path {path}: {cells}")

    def print_modified_board(self, _true_claues: [], print_numbered_board=True, print_direction_board_list=True,
                             print_direction_board_string=True, print_heatmap=True):
        """
        Method responsible for visualization of solutions.
        :param print_numbered_board:
        :param print_direction_board_list:
        :param print_direction_board_string:
        :param print_heatmap:
        :return:
        """

        # deep copy of board
        modified_board = [row[:] for row in self.board]
        modified_board2 = [row[:] for row in self.board]

        for path, cells in self.paths.items():
            for cell in cells:
                modified_board[cell[0]][cell[1]] = path
                modified_board2[cell[0]][cell[1]] = str(path)

        board_string = ""

        if self.theory == "3D":
            modified_board2 = self.get_direction_board(modified_board)
        else:
            for true_var in _true_claues:
                i, j, p, d = true_var
                if d != 0:
                    modified_board2[i][j] = self.direction_signs[d - 1]

        def correct_formatting(_board):
            """
            This function takes a board and corrects the formatting of the board so that all the cells have the same length.
            :param _board: list of lists of strings
            :return: list of lists of strings
            """
            modified_board = [row[:] for row in _board]

            for width in range(len(_board[0])):
                max_len_in_column = 0
                for height in range(len(_board)):
                    max_len_in_column = max(max_len_in_column, len(_board[height][width]))

                for height in range(len(_board)):
                    if len(_board[height][width]) < max_len_in_column:
                        modified_board[height][width] = " " * (max_len_in_column - len(_board[height][width])) + \
                                                        _board[height][width]

            return modified_board

        formated_modified_board = correct_formatting(modified_board2)

        for i in range(self.height):
            for j in range(self.width):
                board_string += str(formated_modified_board[i][j])
            board_string += "\n"

        self.result_board1 = modified_board
        self.direction_board_string = board_string
        self.direction_board_list = modified_board2
        self.numbered_board = modified_board

        if print_numbered_board:
            self.print_board(modified_board)
            print()
        if print_direction_board_list:
            self.print_board(modified_board2)
            print()
        if print_direction_board_string:
            print(board_string)

        if print_heatmap:
            self.get_heatmap(modified_board)

    def get_heatmap(self, modified_board: []):
        """
        Generates heatmap graph.
        :param modified_board:
        :return:
        """

        matrix = np.array(modified_board)

        # Extract unique numbers from the matrix
        unique_numbers = np.unique(matrix)

        """cmap = plt.colormaps['Accent']  # Use colormaps[name] for the colormap
        norm = mcolors.BoundaryNorm(boundaries=np.arange(len(unique_numbers) + 1) - 0.5, ncolors=len(unique_numbers))
        """

        # Dynamically create a colormap and normalization
        colors = plt.get_cmap('tab20').colors + plt.get_cmap('tab20b').colors + plt.get_cmap('tab20c').colors
        cmap = mcolors.ListedColormap(colors[:len(unique_numbers)])
        norm = mcolors.BoundaryNorm(boundaries=np.arange(len(unique_numbers) + 1) - 0.5, ncolors=len(unique_numbers))

        # Create a mapping for annotations
        number_to_color_idx = {num: i for i, num in enumerate(unique_numbers)}

        # Plot the matrix
        fig, ax = plt.subplots(figsize=(self.height, self.width))
        im = ax.imshow([[number_to_color_idx[val] for val in row] for row in matrix], cmap=cmap, norm=norm)

        # Add text annotations
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                ax.text(j, i, str(matrix[i, j]), ha='center', va='center', color='black')

        # Set labels and title
        ax.set_xticks(range(matrix.shape[1]))
        ax.set_yticks(range(matrix.shape[0]))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title("Solution")

        plt.show()

    def get_direction_board(self, _board):
        """
        Generates direction board for 3D theory.
        :param _board:
        :return:
        """

        modified_board = [row[:] for row in self.board]

        signs = ["│", "─", "┘", "└", "┐", "┌"]
        solved = set()

        # set corners
        if self.board[0][0] == ".":
            modified_board[0][0] = "┌"
            solved.add((0, 0))
        if self.board[0][self.width - 1] == ".":
            modified_board[0][self.width - 1] = "┐"
            solved.add((0, self.width - 1))
        if self.board[self.height - 1][0] == ".":
            modified_board[self.height - 1][0] = "└"
            solved.add((self.height - 1, 0))
        if self.board[self.height - 1][self.width - 1] == ".":
            modified_board[self.height - 1][self.width - 1] = "┘"
            solved.add((self.height - 1, self.width - 1))

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.start_end_points_locs and (i, j) not in solved:
                    for p in range(1, self.number_of_paths + 1):
                        if (i, j) in solved:
                            break
                        else:

                            try:
                                if _board[i][j] == _board[i + 1][j] and _board[i][j] == _board[i][j + 1]:
                                    # print(_board[4][1], _board[3][1], _board[3][2])
                                    modified_board[i][j] = "┌"
                                    solved.add((i, j))
                                    continue
                            except:
                                pass
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.start_end_points_locs and (i, j) not in solved:
                    for p in range(1, self.number_of_paths + 1):
                        if (i, j) in solved:
                            break
                        else:
                            try:

                                if j - 1 < 0:
                                    continue

                                if _board[i][j] == _board[i + 1][j] and _board[i][j] == _board[i][j - 1]:
                                    modified_board[i][j] = "┐"
                                    solved.add((i, j))
                                    continue
                            except:
                                pass
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.start_end_points_locs and (i, j) not in solved:
                    for p in range(1, self.number_of_paths + 1):
                        if (i, j) in solved:
                            break
                        else:
                            try:

                                if i - 1 < 0:
                                    continue
                                if _board[i][j] == _board[i - 1][j] and _board[i][j] == _board[i][j + 1]:


                                    modified_board[i][j] = "└"
                                    solved.add((i, j))
                                    continue

                            except:
                                pass

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.start_end_points_locs and (i, j) not in solved:
                    for p in range(1, self.number_of_paths + 1):
                        if (i, j) in solved:
                            break
                        else:

                            try:
                                if i - 1 < 0 or j - 1 < 0:
                                    continue

                                if _board[i][j] == _board[i - 1][j] and _board[i][j] == _board[i][j - 1]:
                                    modified_board[i][j] = "┘"
                                    solved.add((i, j))
                                    continue
                            except:
                                pass

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.start_end_points_locs and (i, j) not in solved:
                    for p in range(1, self.number_of_paths + 1):
                        if (i, j) in solved:
                            break
                        else:
                            try:
                                if _board[i][j] == _board[i + 1][j]:
                                    modified_board[i][j] = "│"
                                    solved.add((i, j))
                                    continue
                            except:
                                pass

                            try:
                                if _board[i][j] == _board[i][j + 1]:
                                    modified_board[i][j] = "─"
                                    solved.add((i, j))
                                    continue
                            except:
                                pass
        return modified_board

    def get_cnf_path(self, instance_path: str):
        """
        Returns path to CNF file.
        :param instance_path:
        :return:
        """
        return str(os.getcwd()) + "/" + "CNFS/" + f"{self.theory}-{instance_path.split("/")[-1].split(".")[0]}.cnf"

    def exit(self):
        print("Error: Invalid input.")
        sys.exit(-1)
