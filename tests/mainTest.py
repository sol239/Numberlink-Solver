import shutil
import unittest
import warnings

from sat import *

# GLUCOSE PARALLEL EXECUTABLE PATH - parallel version is mandatory for cycle_breaker=True which is used in tests
glucose_path = "/root/glucose2/glucose/parallel/glucose-syrup"

# disable resource warnings - they are present in each test
warnings.simplefilter("ignore", ResourceWarning)


class TestNumberlinkClass(unittest.TestCase):
    """
    Test class for the Numberlink class.
    """

    def test_instance_1_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_1.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        expected = [['┌', '─', '┐', '4', '─', '─', '┐'],
                    ['│', '3', '└', '─', '2', '5', '│'],
                    ['│', '└', '─', '3', '1', '│', '│'],
                    ['│', '┌', '─', '5', '│', '│', '│'],
                    ['│', '│', '┌', '─', '┘', '│', '│'],
                    ['│', '│', '1', '┌', '─', '┘', '│'],
                    ['2', '└', '─', '┘', '4', '─', '┘']]
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_1_3D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_1.txt"
        theory_name = "3D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        expected = [['┌', '─', '┐', '4', '─', '─', '┐'],
                    ['│', '3', '└', '─', '2', '5', '│'],
                    ['│', '└', '─', '3', '1', '│', '│'],
                    ['│', '┌', '─', '5', '│', '│', '│'],
                    ['│', '│', '┌', '─', '┘', '│', '│'],
                    ['│', '│', '1', '┌', '─', '┘', '│'],
                    ['2', '└', '─', '┘', '4', '─', '┘']]
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_1_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_1.txt"
        theory_name = "4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        expected = [['┌', '─', '┐', '4', '─', '─', '┐'],
                    ['│', '3', '└', '─', '2', '5', '│'],
                    ['│', '└', '─', '3', '1', '│', '│'],
                    ['│', '┌', '─', '5', '│', '│', '│'],
                    ['│', '│', '┌', '─', '┘', '│', '│'],
                    ['│', '│', '1', '┌', '─', '┘', '│'],
                    ['2', '└', '─', '┘', '4', '─', '┘']]
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_2_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_2.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        possible_solution = [[['1', '─', '┐'],
                              ['┌', '┐', '1'],
                              ['2', '└', '2']],

                             [['1', '┌', '┐'],
                              ['└', '┘', '1'],
                              ['2', '─', '2']]

                             ]

        expected = 1

        actual = (board.direction_board_list in possible_solution)

        self.assertEqual(
            expected, actual
        )

    def test_instance_2_3D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_2.txt"
        theory_name = "3D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        expected = []

        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_2_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_2.txt"
        theory_name = "4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        possible_solution = [[['1', '─', '┐'],
                              ['┌', '┐', '1'],
                              ['2', '└', '2']],

                             [['1', '┌', '┐'],
                              ['└', '┘', '1'],
                              ['2', '─', '2']]

                             ]

        expected = 1

        actual = (board.direction_board_list in possible_solution)

        self.assertEqual(
            expected, actual
        )

    def test_instance_3_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_3.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        expected = [['1', '─', '─', '1'],
                    ['2', '─', '─', '2']]

        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_4_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_4.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        expected = []
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_5_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_5.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        expected = [['1', '─', '─', '─', '1'],
                    ['2', '─', '─', '─', '2'],
                    ['┌', '─', '─', '─', '3'],
                    ['3', '4', '─', '─', '4']]
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_6_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_6.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        expected = []
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    # @unittest.skip  # passed, but takes too long
    def test_instance_7_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_7.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        expected = [
            ['1', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐'],
            ['┌', '─', '─', '─', '─', '┐', '┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '6', '┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐', '│'],
            ['│', '┌', '─', '─', '2', '4', '│', '4', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '┘', '8', '─', '─', '─', '─', '┐', '┌', '─', '─', '─', '─', '─', '─', '┐', '│', '│'],
            ['│', '│', '┌', '─', '─', '─', '┘', '5', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '5', '│', '│', '9', '3', '─', '─', '─', '┐', '│', '│', '│'],
            ['│', '│', '│', '┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '─', '┘', '7', '└', '─', '─', '─', '9', '│', '│', '│', '│'],
            ['│', '│', '│', '│', '3', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '│', '│', '│'],
            ['│', '│', '│', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '8', '│', '│', '│'],
            ['│', '│', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '6', '2',
             '7', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '│', '│'],
            ['│', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘',
             '┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '│'],
            ['└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '┘', '1', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘']]
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_9_3D_4D_solution(self):

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_9.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)
        possible_solutions = [[['1', '┐', '┌', '┐'],
                               ['1', '┘', '│', '│'],
                               ['2', '─', '┘', '2'],
                               ['3', '─', '─', '3']]]

        expected = True
        actual = (board.direction_board_list in possible_solutions)

        self.assertEqual(
            expected, actual
        )

    # @unittest.skip  # passed, but takes too long
    def test_instance_10_3D_4D_solution(self):
        warnings.simplefilter("ignore", ResourceWarning)
        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_10.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        expected = [
            ['┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐', '┌', '─', '─', '─', '┐', '┌', '─', '─', '─', '┐', '1'],
            ['│', '┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '12', '┌', '─', '─', '┐', '┌', '─', '─',
             '─', '─', '─', '─', '┐', '┌', '─', '─', '┐', '│', '│', '25', '─', '┐', '│', '│', '┌', '─', '┐', '│', '│'],
            ['│', '│', '5', '─', '─', '─', '─', '┐', '┌', '─', '─', '─', '─', '10', '│', '17', '62', '│', '56', '61',
             '60', '18', '┌', '─', '┐', '│', '│', '┌', '50', '│', '│', '└', '─', '┐', '│', '│', '49', '│', '39', '│',
             '│', '│'],
            ['│', '└', '─', '─', '─', '─', '┐', '│', '│', '┌', '─', '─', '─', '─', '┘', '│', '│', '│', '61', '┘', '│',
             '│', '│', '34', '│', '│', '│', '│', '┌', '┘', '│', '59', '┐', '│', '│', '└', '─', '┘', '│', '24', '│',
             '│'],
            ['│', '┌', '─', '─', '─', '┐', '│', '│', '│', '│', '┌', '─', '─', '─', '─', '┘', '62', '15', '60', '─', '┘',
             '│', '│', '│', '│', '56', '│', '│', '│', '46', '│', '47', '│', '│', '└', '─', '─', '┐', '└', '┐', '49',
             '│'],
            ['│', '│', '┌', '─', '┐', '14', '│', '│', '│', '│', '│', '┌', '─', '─', '16', '19', '18', '─', '─', '─',
             '─', '┘', '│', '│', '└', '33', '│', '│', '│', '│', '│', '│', '59', '└', '─', '─', '┐', '└', '┐', '└', '┐',
             '│'],
            ['│', '│', '│', '4', '└', '13', '│', '│', '│', '│', '│', '│', '┌', '─', '17', '└', '─', '┐', '┌', '─', '55',
             '53', '│', '34', '┌', '35', '│', '│', '│', '│', '48', '└', '─', '─', '─', '┐', '└', '┐', '└', '┐', '│',
             '│'],
            ['│', '│', '│', '│', '┌', '7', '│', '│', '│', '│', '│', '│', '│', '┌', '─', '─', '13', '│', '│', '┌', '54',
             '│', '└', '33', '│', '57', '┘', '│', '│', '└', '─', '─', '─', '─', '┐', '└', '┐', '└', '┐', '│', '│', '│'],
            ['│', '│', '│', '│', '│', '12', '┘', '│', '│', '│', '│', '│', '│', '│', '3', '41', '42', '│', '│', '│',
             '53', '┘', '52', '32', '└', '─', '┐', '│', '└', '57', '┌', '─', '─', '┐', '└', '┐', '└', '47', '│', '│',
             '│', '│'],
            ['│', '│', '│', '│', '│', '11', '┐', '│', '│', '│', '│', '│', '│', '│', '│', '│', '│', '│', '│', '└', '┐',
             '┌', '┘', '└', '─', '┐', '35', '└', '─', '┐', '│', '┌', '45', '└', '┐', '│', '58', '┐', '│', '│', '│',
             '│'],
            ['│', '│', '│', '│', '│', '10', '│', '│', '│', '│', '│', '│', '│', '│', '│', '│', '│', '│', '└', '55', '│',
             '│', '┌', '─', '21', '│', '┌', '─', '51', '│', '│', '│', '┌', '26', '│', '└', '46', '│', '│', '│', '│',
             '│'],
            ['│', '│', '│', '│', '│', '│', '11', '5', '│', '│', '│', '│', '│', '│', '│', '│', '│', '└', '─', '19', '54',
             '│', '│', '┌', '─', '┘', '│', '┌', '─', '┘', '│', '│', '│', '┌', '┘', '58', '─', '┘', '│', '│', '│', '│'],
            ['│', '│', '│', '│', '│', '└', '─', '─', '┘', '│', '│', '│', '│', '│', '│', '│', '└', '─', '┐', '52', '─',
             '┘', '│', '│', '┌', '─', '┘', '│', '┌', '─', '┘', '│', '│', '│', '┌', '─', '─', '─', '┘', '│', '│', '│'],
            ['│', '│', '│', '│', '│', '┌', '─', '─', '┐', '│', '│', '│', '│', '│', '│', '└', '─', '┐', '└', '─', '─',
             '42', '│', '│', '│', '┌', '─', '┘', '│', '29', '45', '┘', '│', '│', '│', '┌', '─', '─', '─', '┘', '│',
             '│'],
            ['│', '│', '│', '│', '│', '9', '8', '6', '│', '│', '│', '16', '│', '│', '└', '─', '┐', '└', '┐', '┌', '─',
             '┐', '│', '32', '51', '│', '┌', '─', '┘', '└', '─', '┐', '│', '│', '│', '│', '28', '─', '─', '┐', '│',
             '│'],
            ['│', '│', '│', '│', '│', '8', '┘', '│', '│', '│', '└', '─', '┘', '└', '─', '┐', '│', '36', '│', '│', '38',
             '│', '│', '┌', '44', '50', '│', '30', '─', '─', '┐', '│', '│', '│', '│', '│', '27', '─', '┐', '│', '│',
             '│'],
            ['│', '│', '│', '│', '└', '─', '7', '│', '│', '│', '┌', '─', '─', '─', '┐', '│', '│', '│', '41', '22', '│',
             '22', '│', '│', '┌', '43', '23', '31', '─', '┐', '│', '│', '│', '│', '│', '│', '26', '┐', '│', '│', '│',
             '│'],
            ['│', '│', '│', '└', '┐', '6', '─', '┘', '│', '│', '│', '┌', '─', '┐', '│', '│', '│', '└', '36', '┌', '┘',
             '21', '┘', '│', '│', '27', '─', '─', '┐', '│', '│', '│', '│', '│', '│', '└', '25', '│', '│', '│', '│',
             '│'],
            ['│', '│', '└', '┐', '└', '─', '─', '┐', '9', '15', '│', '│', '14', '│', '│', '│', '└', '┐', '37', '│',
             '20', '44', '─', '┘', '└', '─', '─', '43', '│', '31', '│', '│', '│', '│', '└', '─', '24', '│', '│', '│',
             '│', '│'],
            ['│', '└', '┐', '└', '─', '─', '┐', '└', '─', '─', '┘', '│', '│', '│', '│', '└', '┐', '│', '│', '│', '│',
             '┌', '─', '─', '38', '39', '40', '28', '│', '30', '┘', '│', '│', '└', '─', '─', '23', '│', '│', '│', '│',
             '│'],
            ['│', '2', '└', '─', '─', '┐', '└', '─', '─', '─', '─', '┘', '│', '│', '└', '4', '│', '│', '│', '│', '20',
             '│', '37', '┌', '48', '│', '│', '│', '│', '29', '─', '┘', '└', '─', '─', '─', '─', '┘', '│', '│', '│',
             '│'],
            ['│', '│', '3', '─', '┐', '└', '─', '─', '─', '─', '─', '─', '┘', '└', '─', '─', '┘', '│', '│', '└', '─',
             '┘', '│', '│', '┌', '┘', '│', '│', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '│', '│', '│'],
            ['│', '└', '─', '2', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '└', '─', '─',
             '─', '┘', '│', '│', '40', '┘', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '│', '│'],
            ['└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '┘', '└', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘', '│'],
            ['1', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─',
             '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┘']]
        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_11_3D_4D_solution(self):
        warnings.simplefilter("ignore", ResourceWarning)

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_11.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)
        if instance_result == 0:
            board.direction_board_list = []

        expected = [['┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐'],
                    ['│', '1', '─', '─', '─', '1', '┌', '─', '─', '─', '─', '─', '┐', '│'],
                    ['│', '┌', '─', '─', '─', '─', '┘', '┌', '─', '─', '─', '12', '│', '│'],
                    ['│', '│', '┌', '─', '─', '─', '─', '┘', '4', '┌', '─', '─', '┘', '│'],
                    ['│', '2', '│', '┌', '─', '─', '─', '┐', '│', '│', '11', '─', '─', '┘'],
                    ['│', '┌', '┘', '13', '12', '┐', '15', '│', '│', '└', '─', '─', '─', '┐'],
                    ['│', '│', '14', '─', '14', '│', '│', '13', '└', '─', '─', '─', '┐', '│'],
                    ['11', '└', '─', '─', '─', '┘', '└', '15', '┌', '─', '─', '7', '│', '│'],
                    ['┌', '─', '─', '─', '7', '┌', '─', '9', '│', '5', '┐', '┌', '┘', '│'],
                    ['│', '┌', '─', '─', '8', '│', '┌', '8', '│', '6', '│', '│', '┌', '┘'],
                    ['│', '│', '10', '9', '─', '┘', '│', '┌', '┘', '│', '│', '│', '│', '3'],
                    ['│', '│', '└', '─', '10', '┌', '┘', '│', '┌', '┘', '5', '│', '│', '│'],
                    ['│', '└', '─', '─', '─', '┘', '┌', '┘', '│', '┌', '─', '┘', '2', '│'],
                    ['└', '─', '─', '─', '─', '─', '┘', '6', '┘', '4', '3', '─', '─', '┘']]

        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_11_3D_solution(self):
        warnings.simplefilter("ignore", ResourceWarning)

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_11.txt"
        theory_name = "3D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)
        if instance_result == 0:
            board.direction_board_list = []

        expected = [['┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐'],
                    ['│', '1', '─', '─', '─', '1', '┌', '─', '─', '─', '─', '─', '┐', '│'],
                    ['│', '┌', '─', '─', '─', '─', '┘', '┌', '─', '─', '─', '12', '│', '│'],
                    ['│', '│', '┌', '─', '─', '─', '─', '┘', '4', '┌', '─', '─', '┘', '│'],
                    ['│', '2', '│', '┌', '─', '─', '─', '┐', '│', '│', '11', '─', '─', '┘'],
                    ['│', '┌', '┘', '13', '12', '┐', '15', '│', '│', '└', '─', '─', '─', '┐'],
                    ['│', '│', '14', '─', '14', '│', '│', '13', '└', '─', '─', '─', '┐', '│'],
                    ['11', '└', '─', '─', '─', '┘', '└', '15', '┌', '─', '─', '7', '│', '│'],
                    ['┌', '─', '─', '─', '7', '┌', '─', '9', '│', '5', '┐', '┌', '┘', '│'],
                    ['│', '┌', '─', '─', '8', '│', '┌', '8', '│', '6', '│', '│', '┌', '┘'],
                    ['│', '│', '10', '9', '─', '┘', '│', '┌', '┘', '│', '│', '│', '│', '3'],
                    ['│', '│', '└', '─', '10', '┌', '┘', '│', '┌', '┘', '5', '│', '│', '│'],
                    ['│', '└', '─', '─', '─', '┘', '┌', '┘', '│', '┌', '─', '┘', '2', '│'],
                    ['└', '─', '─', '─', '─', '─', '┘', '6', '┘', '4', '3', '─', '─', '┘']]

        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_11_4D_solution(self):
        """
        All possible solutions are not contained - rerun the test multiple times or add not contained solutions.
        :return:
        """
        warnings.simplefilter("ignore", ResourceWarning)

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_11.txt"
        theory_name = "4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)
        if instance_result == 0:
            board.direction_board_list = []

        possible_solutions = [[['┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐'],
                               ['│', '1', '─', '─', '─', '1', '┌', '─', '─', '─', '─', '─', '┐', '│'],
                               ['│', '┌', '─', '─', '─', '─', '┘', '┌', '─', '─', '─', '12', '│', '│'],
                               ['│', '│', '┌', '┐', '┌', '─', '─', '┘', '4', '┌', '─', '─', '┘', '│'],
                               ['│', '2', '│', '│', '│', '┌', '─', '┐', '│', '│', '11', '─', '─', '┘'],
                               ['│', '┌', '┘', '13', '12', '│', '15', '│', '│', '└', '─', '─', '─', '┐'],
                               ['│', '│', '14', '─', '14', '│', '│', '13', '└', '─', '─', '─', '┐', '│'],
                               ['11', '└', '─', '─', '─', '┘', '└', '15', '┌', '─', '─', '7', '│', '│'],
                               ['┌', '─', '─', '─', '7', '┌', '─', '9', '│', '5', '┐', '┌', '┘', '│'],
                               ['│', '┌', '─', '─', '8', '│', '┌', '8', '│', '6', '│', '│', '┌', '┘'],
                               ['│', '│', '10', '9', '─', '┘', '│', '┌', '┘', '│', '│', '│', '│', '3'],
                               ['│', '│', '└', '─', '10', '┌', '┘', '│', '┌', '┘', '5', '│', '│', '│'],
                               ['│', '└', '─', '─', '─', '┘', '┌', '┘', '│', '┌', '─', '┘', '2', '│'],
                               ['└', '─', '─', '─', '─', '─', '┘', '6', '┘', '4', '3', '─', '─', '┘']],

                              [['┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐'],
                               ['│', '1', '─', '─', '─', '1', '┌', '─', '─', '─', '─', '─', '┐', '│'],
                               ['│', '┌', '─', '─', '─', '─', '┘', '┌', '─', '─', '─', '12', '│', '│'],
                               ['│', '│', '┌', '─', '─', '─', '─', '┘', '4', '┌', '─', '─', '┘', '│'],
                               ['│', '2', '│', '┌', '─', '─', '─', '┐', '│', '│', '11', '─', '─', '┘'],
                               ['│', '┌', '┘', '13', '12', '┐', '15', '│', '│', '└', '─', '─', '─', '┐'],
                               ['│', '│', '14', '─', '14', '│', '│', '13', '└', '─', '─', '─', '┐', '│'],
                               ['11', '└', '─', '─', '─', '┘', '└', '15', '┌', '─', '─', '7', '│', '│'],
                               ['┌', '─', '─', '─', '7', '┌', '─', '9', '│', '5', '┐', '┌', '┘', '│'],
                               ['│', '┌', '─', '─', '8', '│', '┌', '8', '│', '6', '│', '│', '┌', '┘'],
                               ['│', '│', '10', '9', '─', '┘', '│', '┌', '┘', '│', '│', '│', '│', '3'],
                               ['│', '│', '└', '─', '10', '┌', '┘', '│', '┌', '┘', '5', '│', '│', '│'],
                               ['│', '└', '─', '─', '─', '┘', '┌', '┘', '│', '┌', '─', '┘', '2', '│'],
                               ['└', '─', '─', '─', '─', '─', '┘', '6', '┘', '4', '3', '─', '─', '┘']],

                              [['┌', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '┐'],
                               ['│', '1', '┌', '─', '─', '1', '┌', '─', '─', '─', '─', '─', '┐', '│'],
                               ['│', '└', '┘', '┌', '─', '─', '┘', '┌', '─', '─', '─', '12', '│', '│'],
                               ['│', '┌', '─', '┘', '┌', '─', '─', '┘', '4', '┌', '─', '─', '┘', '│'],
                               ['│', '2', '┌', '┐', '│', '┌', '─', '┐', '│', '│', '11', '─', '─', '┘'],
                               ['│', '┌', '┘', '13', '12', '│', '15', '│', '│', '└', '─', '─', '─', '┐'],
                               ['│', '│', '14', '─', '14', '│', '│', '13', '└', '─', '─', '─', '┐', '│'],
                               ['11', '└', '─', '─', '─', '┘', '└', '15', '┌', '─', '─', '7', '│', '│'],
                               ['┌', '─', '─', '─', '7', '┌', '─', '9', '│', '5', '┐', '┌', '┘', '│'],
                               ['│', '┌', '─', '─', '8', '│', '┌', '8', '│', '6', '│', '│', '┌', '┘'],
                               ['│', '│', '10', '9', '─', '┘', '│', '┌', '┘', '│', '│', '│', '│', '3'],
                               ['│', '│', '└', '─', '10', '┌', '┘', '│', '┌', '┘', '5', '│', '│', '│'],
                               ['│', '└', '─', '─', '─', '┘', '┌', '┘', '│', '┌', '─', '┘', '2', '│'],
                               ['└', '─', '─', '─', '─', '─', '┘', '6', '┘', '4', '3', '─', '─', '┘']]
                              ]

        expected = True

        actual = (board.direction_board_list in possible_solutions)

        self.assertEqual(
            expected, actual
        )

    def test_instance_12_3D_4D_solution(self):
        warnings.simplefilter("ignore", ResourceWarning)

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_12.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        expected = [['1', '2', '3', '─', '┐'],
                    ['│', '└', '┐', '4', '│'],
                    ['│', '4', '2', '│', '│'],
                    ['│', '└', '─', '┘', '│'],
                    ['└', '─', '1', '3', '┘']]

        actual = board.direction_board_list

        self.assertEqual(
            expected, actual
        )

    def test_instance_13_3D_4D_solution(self):
        warnings.simplefilter("ignore", ResourceWarning)

        instance_path = "/root/glucose2/glucose/Numberlink/instances/instance_13.txt"
        theory_name = "3D+4D"

        board, instance_result, model, sat_output = run_sat(glucose_path, instance_path, theory_name,
                                                            cycle_breaker=True)

        if instance_result == 0:
            board.direction_board_list = []

        possible_solutions = [[['3', '┌', '─', '─', '3'],
                               ['└', '┘', '1', '─', '┐'],
                               ['2', '1', '─', '─', '┘'],
                               ['│', '2', '4', '┌', '┐'],
                               ['└', '┘', '└', '┘', '4']],

                              [['3', '┌', '─', '─', '3'],
                               ['└', '┘', '1', '─', '┐'],
                               ['2', '1', '─', '─', '┘'],
                               ['│', '2', '4', '┌', '┐'],
                               ['└', '┘', '└', '┘', '4']],

                              [['3', '┌', '─', '─', '3'],
                               ['└', '┘', '1', '─', '┐'],
                               ['2', '1', '─', '┐', '│'],
                               ['│', '2', '4', '└', '┘'],
                               ['└', '┘', '└', '─', '4']],

                              [['3', '┌', '─', '┐', '3'],
                               ['└', '┘', '1', '│', '│'],
                               ['2', '1', '┘', '│', '│'],
                               ['│', '2', '4', '└', '┘'],
                               ['└', '┘', '└', '─', '4']],

                              [['3', '┌', '─', '┐', '3'],
                               ['└', '┘', '1', '└', '┘'],
                               ['2', '1', '┘', '┌', '┐'],
                               ['│', '2', '4', '│', '│'],
                               ['└', '┘', '└', '┘', '4']]

                              ]

        solution = board.direction_board_list

        expected = True
        actual = (solution in possible_solutions)

        self.assertEqual(
            expected, actual
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
