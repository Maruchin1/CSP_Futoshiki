import numpy as np
import copy
import time
from FutoData import load_data

back_count = 0

curr_var_idx = 0


def search_solutions_forward_checking():
    start_time = time.time()

    ref_matrxi = board_matrix
    ref_vars_list = vars_list
    ref_vars_dict = vars_dict

    print("\nSTART LOOP")
    while curr_var_idx < vars_count:
        if curr_var_idx == -1:
            notify_end_loop(start_time)
            return

        curr_var = vars_list[curr_var_idx]
        next_value = get_next_val_from_field(curr_var)

        if next_value is None:
            reset_var_and_back(curr_var)
        else:
            is_val_correct = check_forward(curr_var, next_value)
            if is_val_correct:
                board_matrix[curr_var] = next_value
                go_deeper(curr_var, start_time)


def get_next_val_from_field(var):
    field = vars_dict[var]
    if len(field) <= 0:
        return None
    return field.pop(0)


def check_forward(var_to_check, value):
    ref_matrix = board_matrix
    ref_dict = vars_dict

    linked_vars = get_linked_vars(var_to_check)
    fields_not_empty = remove_value_from_fields(value, linked_vars)
    if not fields_not_empty:
        restore_value_in_fields(value, linked_vars)
        return False
    return True


def get_linked_vars(var_to_check):
    linked_vars = []
    for i in range(curr_var_idx, vars_count):
        var = vars_list[i]
        if var != var_to_check and (var[0] == var_to_check[0] or var[1] == var_to_check[1]):
            linked_vars.append(var)
    return linked_vars


def remove_value_from_fields(value, vars_to_clear):
    for var in vars_to_clear:
        field = vars_dict[var]
        if value in field:
            field.remove(value)
        if len(field) <= 0:
            return False
    return True


def restore_value_in_fields(value, vars_to_restore):
    for var in vars_to_restore:
        field = vars_dict[var]
        field.append(value)


# BACKTRACKING ---------------------------------------------------------------------------------------------------------


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
        corr_value = look_for_correct_value(curr_var)

        if corr_value is None:
            reset_var_and_back(curr_var)
        else:
            board_matrix[curr_var] = corr_value
            go_deeper(curr_var, start_time)


def reset_var_and_back(curr_var):
    vars_dict[curr_var] = orig_vars_dict[curr_var].copy()
    board_matrix[curr_var] = orig_board_matrix[curr_var]
    global curr_var_idx
    curr_var_idx -= 1


def go_deeper(curr_var, start_time):
    # board_matrix[curr_var] = corr_value
    if curr_var != (orig_dimension - 1, orig_dimension - 1):
        global curr_var_idx
        curr_var_idx += 1
    else:
        notify_solution_found(start_time)


def look_for_correct_value(var_to_check):
    field = vars_dict[var_to_check]

    while len(field) > 0:
        next_value = field.pop(0)
        cons_correct = check_constrains(var_to_check, next_value)
        if cons_correct:
            return next_value

    return None


def check_constrains(var_to_check, value):
    rows_and_columns_correct = check_rows_and_columns(var_to_check, value)
    global_cons_correct = check_global_cons(var_to_check, value)

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
    print("\nFOUND SOLUTION")
    print(board_matrix)
    search_time = time.time() - start_time
    print(f'search time = {search_time}')


def notify_end_loop(start_time):
    print("\nEND OF LOOP")
    end_time = time.time() - start_time
    print(f'end time = {end_time}')


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
    data = load_data("test_futo_4_0.txt")
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
