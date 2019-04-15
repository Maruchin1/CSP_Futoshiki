import numpy as np
import copy
import time
from FutoData import load_data

back_count = 0
nodes_count = 0

curr_var_idx = 0


def search_solutions():
    start_time = time.time()

    ref_board_matrix = board_matrix
    ref_vars_dict = vars_dict

    print("\nSTART LOOP")
    while curr_var_idx < vars_count:
        if curr_var_idx == -1:
            notify_end_loop(start_time)
            return

        curr_var = vars_list[curr_var_idx]
        next_value = get_next_val(curr_var)

        if next_value is None:
            go_back(curr_var)
            incr_back_count()
            continue

        is_val_correct = check_constrains(curr_var, next_value)
        if is_val_correct:
            go_deeper(curr_var, next_value, start_time)
        else:
            incr_back_count()


def incr_nodes_count():
    global nodes_count
    nodes_count += 1


def incr_back_count():
    global back_count
    back_count += 1


def go_back(curr_var):
    vars_dict[curr_var] = orig_vars_dict[curr_var].copy()
    board_matrix[curr_var] = orig_board_matrix[curr_var]
    global curr_var_idx
    curr_var_idx -= 1


def go_deeper(curr_var, corr_value, start_time):
    board_matrix[curr_var] = corr_value
    if curr_var != (orig_dimension - 1, orig_dimension - 1):
        global curr_var_idx
        curr_var_idx += 1
    else:
        notify_solution_found(start_time)


def get_next_val(var):
    field = vars_dict[var]
    if len(field) <= 0:
        return None
    return field.pop(0)


def check_constrains(var_to_check, value):
    rows_and_columns_correct = check_rows_and_columns(var_to_check, value)
    global_cons_correct = check_global_cons(var_to_check, value)
    # global_cons_correct = True

    return rows_and_columns_correct and global_cons_correct


def check_rows_and_columns(var_to_check, value):
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


def check_global_cons(var_to_check, value):
    cons_with_var = [(x, y) for (x, y) in orig_cons_list if x == var_to_check or y == var_to_check]
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


def notify_solution_found(start_time):
    search_time = time.time() - start_time
    global back_count
    print("\nFOUND SOLUTION")
    print(board_matrix)
    print(f'search time = {search_time}')
    print(f'back count = {back_count}')


def notify_end_loop(start_time):
    end_time = time.time() - start_time
    global back_count
    print("\nEND OF LOOP")
    print(f'end time = {end_time}')
    print(f'back count = {back_count}')


def print_data():
    print("LOADED DADA")
    print("data matrix")
    print(data.board_matrix)
    print("constraints_list")
    print(data.constraints_list)
    print("variables_dict")
    print(data.variables_dict)


def heuristic():
    vars_list.sort(key=number_of_cons, reverse=True)


def number_of_cons(var):
    count = 0
    for (x, y) in orig_cons_list:
        if x == var or y == var:
            count += 1
    return count


if __name__ == '__main__':
    data = load_data("test_futo_6_0.txt")
    print_data()

    orig_dimension = int(data.dimension)
    orig_board_matrix = np.copy(data.board_matrix)
    orig_vars_dict = copy.deepcopy(data.variables_dict)
    orig_cons_list = list(data.constraints_list)
    orig_def_field = list(data.def_field)

    board_matrix = np.copy(data.board_matrix)
    vars_dict = copy.deepcopy(data.variables_dict)
    vars_list = list(vars_dict.keys())
    vars_count = len(vars_list)

    # heuristic()

    search_solutions()
