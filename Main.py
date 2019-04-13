import numpy as np
import copy
from Data import load_data

FILE_NAME = "futoshiki_4_0.txt"


def search_solutions():
    solutions_list = []

    board_matrix = np.copy(data.board_matrix)
    variables_dict = copy.deepcopy(data.variables_dict)

    variables_count = len(variables_dict)

    print("main loop")
    curr_var_idx = 0

    while curr_var_idx <= variables_count:
        if curr_var_idx == variables_count:
            solutions_list.append(np.copy(board_matrix))
            curr_var_idx -= 1

        if curr_var_idx == -1:
            print("EXIT TREE !!!!!!!!!!!")
            return solutions_list

        curr_var = list(variables_dict.keys())[curr_var_idx]
        print(curr_var)

        corr_value = look_for_correct_value(curr_var, board_matrix, variables_dict)

        if corr_value is None:
            orig_field = orig_variables_dict[curr_var].copy()
            variables_dict[curr_var] = orig_field

            orig_value = orig_board_matrix[curr_var]
            board_matrix[curr_var] = orig_value

            curr_var_idx -= 1
        else:
            board_matrix[curr_var[0]][curr_var[1]] = corr_value
            curr_var_idx += 1

    return solutions_list


def look_for_correct_value(var_to_check, board_matrix, variables_dict):
    field = variables_dict[var_to_check]

    while len(field) > 0:
        next_value = field.pop(0)
        cons_correct = check_constrains(var_to_check, next_value, board_matrix)
        if cons_correct:
            return next_value

    return None


def check_constrains(var_to_check, value, board_matrix):
    rows_and_columns_correct = check_rows_and_columns(var_to_check, value, board_matrix)
    global_cons_correct = check_global_cons(var_to_check, value, board_matrix)

    return rows_and_columns_correct and global_cons_correct


def check_rows_and_columns(var_to_check, value, board_matrix):
    row_num = var_to_check[0]
    col_num = var_to_check[1]

    row = list(board_matrix[row_num, :])
    del row[col_num]
    col = list(board_matrix[:, col_num])
    del col[row_num]

    if value in row:
        return False

    if value in col:
        return False

    return True


def check_global_cons(var_to_check, value, board_matrix):
    cons_with_var = [(x, y) for (x, y) in orig_constrains_list if x == var_to_check or y == var_to_check]
    if len(cons_with_var) <= 0:
        return True

    for (firs_cell, second_cell) in cons_with_var:
        firs_cell_value = value if firs_cell == var_to_check else board_matrix[firs_cell]
        second_cell_value = value if second_cell == var_to_check else board_matrix[second_cell]

        if firs_cell_value == 0 or second_cell_value == 0:
            return True

        if firs_cell_value >= second_cell_value:
            return False

    return True


if __name__ == '__main__':
    print("start")
    data = load_data(FILE_NAME)
    print("data matrix")
    print(data.board_matrix)
    print("constraints_list")
    print(data.constraints_list)
    print("variables_dict")
    print(data.variables_dict)

    orig_board_matrix = np.copy(data.board_matrix)
    orig_variables_dict = copy.deepcopy(data.variables_dict)
    orig_constrains_list = list(data.constraints_list)
    orig_def_field = list(data.def_field)

    solutions = search_solutions()
    print(solutions)
