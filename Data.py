import numpy as np


def load_data(file_name):
    with open(file_name) as file:
        dimension = int(file.readline())
        board_matrix = load_board_matrix(file, dimension)
        variables_dict = make_variables(board_matrix)
        constraint_arr = load_constraints_array(file)

    return Data(dimension, board_matrix, constraint_arr, variables_dict)


def load_board_matrix(file, dimension):
    board_matrix = np.zeros(shape=(dimension, dimension), dtype=int)

    file.readline()
    line = file.readline().replace("\n", "")
    line_number = 0
    while line != "REL:":
        numbers_list = line.split(";")
        board_matrix[line_number] = numbers_list
        line = file.readline().replace("\n", "")
        line_number += 1

    return board_matrix


def make_variables(board_matrix):
    zeros_positions_arr = np.where(board_matrix == 0)
    print(zeros_positions_arr)
    variables_count = zeros_positions_arr[0].size
    dimension = board_matrix[0].size

    # variables_arr = np.empty(shape=(variables_count, dimension + 2), dtype=int)

    variables_dict = {}
    for i in range(variables_count):
        field_arr = np.arange(1, dimension+1)
        coord_tuple = (zeros_positions_arr[0][i], zeros_positions_arr[1][i])
        # coord_arr = np.array((zeros_positions_arr[0][i], zeros_positions_arr[1][i]))
        # variable = np.concatenate((field_arr, coord_arr))
        # variables_arr[i] = variable
        variables_dict[coord_tuple] = field_arr

    return variables_dict


def load_constraints_array(file):
    constraints_list = []
    line = file.readline().replace("\n", "")
    while line != "":
        constraint = make_constraint(line)
        constraints_list.append(constraint)
        line = file.readline().replace("\n", "")

    constraints_arr = np.array(constraints_list, dtype=((int, int), (int, int)))
    return constraints_arr


def make_constraint(constraint_string):
    string_tuple = tuple(fix_constraint(constraint_string).split(";"))
    constraint = (tuple(int(char) for char in string_tuple[0]), tuple(int(char) for char in string_tuple[1]))
    return constraint


def fix_constraint(constraint_string):
    return constraint_string.replace("1", "0").replace("2", "1").replace("3", "2").replace("4", "3") \
        .replace("A", "0").replace("B", "1").replace("C", "2").replace("D", "3")


class Data:

    def __init__(self, dimension, board_matrix, constraints_arr, variables_dict):
        self.dimension = dimension
        self.board_matrix = board_matrix
        self.constraints_arr = constraints_arr
        self.variables_dict = variables_dict
