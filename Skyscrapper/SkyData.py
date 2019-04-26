import numpy as np

TEST_DATA_DIR = "test_data/"
RES_DATA_DIR = "res_data/"


def load_data(file_name, reduce_fields_enabled):
    with open(RES_DATA_DIR + file_name) as file:
        dim = int(file.readline())
        board_matrix = np.zeros(shape=(dim, dim), dtype=int)
        def_field = [number for number in range(1, dim + 1)]
        vars_dict = make_vars_dict(board_matrix, def_field)
        cons_matrix = load_cons_matrix(file, dim)

        if reduce_fields_enabled:
            reduce_edges_fields(vars_dict, dim, cons_matrix)

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


def reduce_edges_fields(vars_dict, dim, cons_matrix):
    top_edge = zip(row_vars(0, dim), cons_matrix[0])
    reduce_single_edge_fields(top_edge, vars_dict, dim)

    bot_edge = zip(row_vars(dim - 1, dim), cons_matrix[1])
    reduce_single_edge_fields(bot_edge, vars_dict, dim)

    left_edge = zip(col_vars(0, dim), cons_matrix[2])
    reduce_single_edge_fields(left_edge, vars_dict, dim)

    right_edge = zip(col_vars(dim - 1, dim), cons_matrix[3])
    reduce_single_edge_fields(right_edge, vars_dict, dim)


def reduce_single_edge_fields(edge, vars_dict, dim):
    for var, con in edge:
        if con != 0:
            vars_dict[var] = reduce_single_field(vars_dict[var], con, dim)


def reduce_single_field(field, con, dim):
    return [dim] if con == 1 else field[:dim - con + 1]


def row_vars(row_num, dim):
    return [(row_num, x) for x in range(dim)]


def col_vars(col_num, dim):
    return [(x, col_num) for x in range(dim)]


class Data:
    def __init__(self, dim, board_matrix, vars_dict, cons_matrix, def_field):
        self.dim = dim
        self.board_matrix = board_matrix
        self.vars_dict = vars_dict
        self.cons_matrix = cons_matrix
        self.def_field = def_field
