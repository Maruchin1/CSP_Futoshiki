import numpy as np
import copy
import time
from FutoData import load_data

dicts_stack = []
curr_var_idx = 0


def search_solutions():
    start_time = time.time()

    ref_matrix = board_matrix
    ref_dicts_stack = dicts_stack

    initial_dict = copy.deepcopy(orig_vars_dict)
    dicts_stack.append(initial_dict)

    print("\nSTART LOOP")
    while curr_var_idx < vars_count:
        if curr_var_idx == -1:
            notify_end_loop(start_time)
            return

        curr_var = vars_list[curr_var_idx]
        next_value = get_next_val(curr_var)

        if next_value is None:
            go_back(curr_var)
        else:
            is_val_correct = check_forward(curr_var, next_value)
            if is_val_correct:
                board_matrix[curr_var] = next_value
                go_deeper(curr_var, start_time)


def check_forward(var_to_check, value):
    ref_matrix = board_matrix
    ref_dict = vars_dict

    vars_same_row_or_col = get_vars_in_same_row_or_col(var_to_check)
    fields_not_empty = remove_value_from_fields(value, vars_same_row_or_col)
    return fields_not_empty


def get_vars_in_same_row_or_col(var_to_check):
    linked_vars = []
    for i in range(curr_var_idx, vars_count):
        var = vars_list[i]
        if var != var_to_check and (var[0] == var_to_check[0] or var[1] == var_to_check[1]):
            linked_vars.append(var)
    return linked_vars


def remove_value_from_fields(value, vars_to_clear):
    curr_dict = dicts_stack[len(dicts_stack) - 1]
    new_dict = copy.deepcopy(curr_dict)

    for var in vars_to_clear:
        field = new_dict[var]
        if value in field:
            field.remove(value)
        if len(field) <= 0:
            return False
    dicts_stack.append(new_dict)
    return True


def go_back(curr_var):
    dicts_stack.pop()
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


def get_next_val(var):
    curr_dict = dicts_stack[len(dicts_stack) - 1]
    field = curr_dict[var]
    if len(field) <= 0:
        return None
    return field.pop(0)


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
