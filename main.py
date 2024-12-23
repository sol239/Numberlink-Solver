from sat import *

if __name__ == '__main__':
    # not parallel version
    # put your path to the glucose executable
    # glucose_path = "/root/glucose2/glucose/simp/glucose_release"

    # parallel version
    # USE THIS with if the cycle_breaker=True
    # put your path to the glucose-syrup file
    glucose_path = "/root/glucose2/glucose/parallel/glucose-syrup"

    instance_path = "instances/instance_1.txt"

    # 3D = [FAST] the version without taking direction into account - 3 variables per cell
    # 4D = [SLOW] the version taking direction into account - 4 variables per cell, allows zigzag paths
    # 3D+4D = [DEFAULT] the version tries 3D first, if it fails (= solving without zizag paths
    # is not possible or not possible at all), it tries 4D. It is the best choice for most cases.
    # thanks to the cycle_breaker, the theory does not have to solve cycles itself - which is in my opinion impossible
    theory_name = "3D+4D"   # possible values: "3D" ... Encoding 1, "4D" .. Encoding 2, "3D+4D" .. Encoding 1 first then Encoding 2

    # WITHOUT PARALLEL VERSION USE cycle_breaker=False !!!
    board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name, cycle_breaker=True, _echo=False)
    print_sat_result(board, instance_result,instance_path,
                     original_board=True,               # prints the original unsolved board
                     board_info=True,                   # prints the board info
                     numbered_board=False,               # prints the board with numbers belonging to the paths
                     direction_board_list=False,         # prints the board with directions signs as list
                     direction_board_string=True,       # prints the board with directions signs as string
                     _model=False,                      # prints the model returned by the SAT solver
                     _sat_output=False,                 # prints the output of the SAT solver
                     heatmap=False,                      # plots the colored heatmap of the solved board
                     _dimacs=False
                     )