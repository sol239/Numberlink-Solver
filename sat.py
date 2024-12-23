from numberlink import *

def run_glucose(instance_cnf_path: str, glucose_executable_path: str, echo: bool = False) -> tuple:
    """
    Starts SAT solver.
    :param instance_cnf_path: path to the instance in DIMACS format (.cnf)
    :param glucose_executable_path: path to the executable of the SAT solver
    :return:
    """

    try:
        if echo: print(f"Running SAT solver on {instance_cnf_path} with {glucose_executable_path}")

        result = subprocess.run([rf"{glucose_executable_path}", '-model', f"{instance_cnf_path}"],
                                stdout=subprocess.PIPE)

        sat_output = result.stdout.decode('utf-8').strip()
        sat_output_lines = sat_output.split("\n")

        instace_result = 0
        model = "No model"

        if "s" in sat_output_lines[-1]:
            instace_result = 0  # 0 = unsatisfiable
            model = "No model"

        elif "v" in sat_output_lines[-1]:
            instace_result = 1  # 1 = satisfiable
            model = sat_output_lines[-1]

        if echo: print(f"Glucose finished with result {instace_result}")

        return instace_result, model, sat_output

    except FileNotFoundError:
        print("Executable not found at the specified path.")
    except Exception as e:
        print(f"An error occurred: {e}")

def select_theory(instance_path: str, theory_name: str, echo: bool = False, _extra_clauses = []):
    """Generates clauses for selected theory and saves to DIMACS format."""
    _board = NumberlinkBoard(f"{instance_path}")

    if theory_name == "4D":
        _board.theory = "4D"
        _board.generate_all_clauses_4D(echo)
        _board.generate_clauses_4D(echo, _extra_clauses)

    elif theory_name == "3D":
        _board.theory = "3D"
        _board.generate_all_clauses_3D(echo)
        _board.generate_clausess_3D(echo, _extra_clauses)

    elif theory_name == "3D+4D":
        _board.theory = "3D"
        _board.generate_all_clauses_3D(echo)
        _board.generate_clausess_3D(echo, _extra_clauses)

    _board.save_to_dimacs(f"{instance_path}.cnf")

    return _board

def cycle_detect(_board):
    """
    Detects cycles in the solved board and returns the clauses to break them = their negation is used for sat solver.
    :param _board:
    :return:
    """

    _paths = dict()

    for path in range(1, _board.number_of_paths + 1):

        _paths[path] = []
        signs = {"│": 1, "─": 2, "┘": 3, "└": 4, "┐": 5, "┌": 6}
        se_point = _board.start_end_points[path]
        start = se_point[0]
        end = se_point[1]
        j1 = j1 = 0

        _paths[path].append((start[0], start[1]))

        neigbors = _board.get_se_points_neigbors(start[0], start[1], path)
        n = neigbors[0]

        for neighbor in neigbors:
            # check if it is real one
            i1, j1, p1, d1 = neighbor

            if _board.numbered_board[i1][j1] == p1 and signs[_board.direction_board_list[i1][j1]] == d1:
                n = (i1, j1, p1, d1)
                break

        visited = set()
        visited.add(n)
        _paths[path].append((i1, j1))
        found_end = False

        _ = [1, 2, 3, 4, 5, 6, 7, 8]

        while not found_end:
            neigbors = _board.get_not_se_points_neighbours(n[0], n[1], n[3])
            _.append(n)

            if _[-1] == _[-2] and _[-2] == _[-3] and _[-3] == _[-4]:
                break
            for neighbor in neigbors:
                i1, j1, d1 = neighbor
                neighbor = (i1, j1, path, d1)

                if (i1, j1) == end and _board.numbered_board[i1][j1] == path:
                    found_end = True
                    _paths[path].append((i1, j1))

                try:
                    x = signs[_board.direction_board_list[i1][j1]]
                except:
                    continue

                if _board.numbered_board[i1][j1] == p1 and signs[
                    _board.direction_board_list[i1][j1]] == d1 and neighbor not in visited:
                    n = (i1, j1, p1, d1)
                    visited.add(n)
                    _paths[path].append((i1, j1))
                    break


    path_cells = []
    cycle_cells = []
    for path, cells in _paths.items():
        path_cells.extend(cells)

    for i in range(_board.height):
        for j in range(_board.width):
            if (i, j) not in path_cells:
                try:
                    cycle_cells.append((i, j, _board.numbered_board[i][j], signs[_board.direction_board_list[i][j]]))
                except:
                    continue
    cycles = []
    visited_cells = set()
    for cell in cycle_cells:
        if cell in visited_cells:
            continue
        neighbour = ()
        stack = [cell]
        cycle = [cell]
        visited = set()
        visited.add(cell)

        while neighbour != cell:
            try:
                i, j, p, d = stack[-1][0], stack[-1][1], stack[-1][2], stack[-1][3]
            except:
                break
            neigbors = _board.get_not_se_points_neighbours(i, j, d)

            _ = []
            for neighbor in neigbors:
                i1, j1, d1 = neighbor
                if (i1, j1, p, d1) in cycle_cells:
                    _.append((i1, j1, p, d1))
            neigbors = _

            for n in neigbors:
                if n not in visited:
                    visited.add(n)
                    visited_cells.add(n)
                    cycle.append(n)
                    stack.append(n)
            try:
                stack.pop()
            except:
                break
        cycles.append(cycle)

    return cycles

def retrieve_real_time(_sat_output: str):
    """
    Retrieves the CPU time from the SAT solver output.
    :param _sat_output: the output of the SAT solver
    :return: the CPU time
    """

    lines = _sat_output.split("\n")
    for line in lines:
        if "real time :" in line:
            return line.split(" : ")[1].split(" s")[0]

    return 0

def run_sat(glucose_executable_path:str, instance_path:str, theory_name:str, cycle_breaker:bool=True, _echo:bool=False):
    """
    Method for running SAT solver. It encapsulates the whole process of selecting
    the theory, running the solver and choosing whether to break the cycles in the solved board.
    :param glucose_executable_path: the path to the executable of the SAT solver
    :param instance_path: the path to the instance file
    :param theory_name: the name of the theory to be used
    :param cycle_breaker: whether to break the cycles in the solved board and find another solution
    :return: solved board, instance result, model, sat output
    """

    extra_clauses = []
    it = 1
    if cycle_breaker:
        while True:
            if _echo:
                print("Iteration", it)
                it += 1
            board = select_theory(instance_path, theory_name, _echo, _extra_clauses=extra_clauses)
            instance_result, model, sat_string = run_glucose(board.get_cnf_path(instance_path), glucose_executable_path, echo=_echo)
            if instance_result == 0 and theory_name == "3D+4D":
                board = select_theory(instance_path, "4D", _echo, _extra_clauses=extra_clauses)
                instance_result, model, sat_string = run_glucose(board.get_cnf_path(instance_path), glucose_executable_path, echo=_echo)
                if instance_result == 0:
                    break
            elif instance_result == 0:
                break

            if instance_result == 1:
                board.get_true_variables(model, _print=False)
                board.retrieve_paths_from_models(model)
                board.print_modified_board(board.true_clauses, False, _echo, _echo, False)
                # print("USING PYSAT")
                # board.use_pysat()

                # print possible direction of [0,0]
                if _echo: print("Cycle detection...")
                to_extend = cycle_detect(board)
                if _echo: print("Cycle detection finished.")
                if len(to_extend) == 0:
                    break
                extra_clauses.extend(to_extend)
                if len(extra_clauses) == 0:
                    break
    else:
        board = select_theory(instance_path, theory_name, _echo, _extra_clauses=extra_clauses)
        instance_result, model, sat_string = run_glucose(board.get_cnf_path(instance_path), glucose_executable_path, echo=_echo)
        if instance_result == 0 and theory_name == "3D+4D":
            print("3D - FAIL")
            board = select_theory(instance_path, "4D", _echo, _extra_clauses=extra_clauses)
            instance_result, model, sat_string = run_glucose(board.get_cnf_path(instance_path), glucose_executable_path, echo=_echo)
            if instance_result == 0:
                print("3D+4D - FAIL")

        if instance_result == 1:
            board.get_true_variables(model, _print=False)
            board.retrieve_paths_from_models(model)
            board.print_modified_board(board.true_clauses, False, False, False, False)

    board.sat_output = sat_string
    board.instance_result = instance_result
    board.model = model
    board.sat_real_time = retrieve_real_time(sat_string)
    return board, instance_result, model, sat_string

def print_dimacs(_board, _instance_path: str):
    """
    Prints the DIMACS format of the instance.
    :param _board:
    :return:
    """

    file = open(_board.get_cnf_path(_instance_path), "r")
    print(file.read())
    file.close()

def print_sat_result(_board, _instance_result, _instance_path:str, board_info:bool, original_board: bool, numbered_board:bool, direction_board_list:bool, direction_board_string:bool, _dimacs:bool,_model:bool, _sat_output:bool, heatmap:bool):
    """
    Prints the result of the SAT solver.
    :param _dimacs:
    :param _board:
    :param _instance_result:
    :param original_board:
    :param numbered_board:
    :param direction_board_list:
    :param direction_board_string:
    :param _model:
    :param _sat_output:
    :param heatmap:
    :return:
    """

    print("Numberlink")
    print("-" * 40)
    print(f"Solvable = {_instance_result == 1}")
    print("-" * 40)
    if (original_board):
        _board.print_board_info()
        print("-" * 40)

    _board.print_modified_board(_true_claues=_board.true_clauses, print_numbered_board=numbered_board, print_direction_board_list=direction_board_list, print_direction_board_string=direction_board_string, print_heatmap=heatmap)
    if _dimacs: print_dimacs(_board, _instance_path)
    if _model: print(_board.model)
    if _sat_output: print(_board.sat_output)

    # print(f"Proměnné [{len(board.variables)}] =", board.variables)
    # print("Počet cest =", board.number_of_paths)
    # Počet cest na desce
    # print(f"Klauzule [{len(board.clauses)}] =", board.clauses)
    # instance_result, model, sat_string = 1, open_model(instance_name), "SAT solver output"
