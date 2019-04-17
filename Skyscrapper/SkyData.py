import numpy as np

TEST_DATA_DIR = "test_data/"
RES_DATA_DIR = "res_data/"


def load_data(file_name):
    with open(RES_DATA_DIR + file_name) as file:
        dim = int(file.readline())
        board_matrix = np.zeros(shape=(dim, dim), dtype=int)
        def_field = [number for number in range(1, dim + 1)]
        vars_dict = make_vars_dict(board_matrix, def_field)
        cons_matrix = load_cons_matrix(file, dim)
    return Data(dim, board_matrix, vars_dict, cons_matrix, def_field)


def make_vars_dict(board_matrix, def_field):
    all_positions = np.where(board_matrix != -1)
    vars_count = all_positions[0].size
    vars_dict = {}
    for i in range(vars_count):
        row_num = all_positions[0][i]
        col_num = all_positions[1][i]

        variable = (row_num, col_num)
        vars_dict[variable] = def_field
    return vars_dict


def load_cons_matrix(file, dim):
    cons_matrix = np.zeros(shape=(dim, dim), dtype=int)
    row_num = 0
    for line in file:
        line = line.replace("\n", "")
        line = line[2:]
        numbers_list = line.split(";")
        cons_matrix[row_num] = numbers_list
        row_num += 1
    return cons_matrix


class Data:
    def __init__(self, dim, board_matrix, vars_dict, cons_matrix, def_field):
        self.dim = dim
        self.board_matrix = board_matrix
        self.vars_dict = vars_dict
        self.cons_matrix = cons_matrix
        self.def_field = def_field
