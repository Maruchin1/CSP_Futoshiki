import numpy as np

TEST_DATA_DIR = "test_data/"
RES_DATA_DIR = "res_data/"


def load_data(file_name):
    with open(RES_DATA_DIR + file_name) as file:
        dimension = int(file.readline())
        board_matrix = load_board_matrix(file, dimension)
        def_field = make_def_field(dimension)
        variables_dict = make_variables(board_matrix, def_field)
        constraints_list = load_constraints_list(file)

    return Data(dimension, board_matrix, constraints_list, variables_dict, def_field)


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


def make_def_field(dimension):
    return [number for number in range(1, dimension + 1)]


def make_variables(board_matrix, def_field):
    all_positions = np.where(board_matrix != -1)
    variables_count = all_positions[0].size

    variables_dict = {}
    for i in range(variables_count):
        row_num = all_positions[0][i]
        col_num = all_positions[1][i]

        val_in_pos = board_matrix[row_num, col_num]
        field_list = def_field.copy() if val_in_pos == 0 else [val_in_pos]
        pos_tuple = (row_num, col_num)

        variables_dict[pos_tuple] = field_list

    return variables_dict


def load_constraints_list(file):
    constraints_list = []
    line = file.readline().replace("\n", "")
    while line != "":
        constraint = make_constraint(line)
        constraints_list.append(constraint)
        line = file.readline().replace("\n", "")

    return constraints_list


def make_constraint(constraint_string):
    string_tuple = tuple(fix_constraint(constraint_string).split(";"))
    constraint = (tuple(int(char) for char in string_tuple[0]), tuple(int(char) for char in string_tuple[1]))
    return constraint


# todo rozszerzy to mapowanie dla większych planszy
def fix_constraint(constraint_string):
    return constraint_string.replace("1", "0").replace("2", "1").replace("3", "2").replace("4", "3").replace("5", "4")\
        .replace("6", "5").replace("7", "6").replace("8", "7").replace("9", "8") \
        .replace("A", "0").replace("B", "1").replace("C", "2").replace("D", "3").replace("E", "4").replace("F", "5")\
        .replace("G", "6").replace("H", "7").replace("I", "8")


class Data:

    def __init__(self, dimension, board_matrix, constraints_list, variables_dict, def_field):
        self.dimension = dimension
        self.board_matrix = board_matrix
        self.constraints_list = constraints_list
        self.variables_dict = variables_dict
        self.def_field = def_field
