import numpy as np
import copy
import time
from FutoData import load_data

back_count = 0

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

        if curr_var == (4, 2) and next_value == 3:
            x = 1

        if next_value is None:
            go_back(curr_var)
            incr_back_count()
            continue

        is_val_correct = check_forward(curr_var, next_value)
        if is_val_correct:
            go_deeper(curr_var, next_value, start_time)
        else:
            incr_back_count()


def incr_back_count():
    global back_count
    back_count += 1


def go_back(curr_var):
    dicts_stack.pop()
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
        dicts_stack.pop()


def get_next_val(var):
    curr_dict = dicts_stack[len(dicts_stack) - 1]
    field = curr_dict[var]
    if len(field) <= 0:
        return None
    return field.pop(0)


def check_forward(var_to_check, value):
    ref_matrix = board_matrix
    curr_dict = dicts_stack[len(dicts_stack) - 1]
    new_dict = copy.deepcopy(curr_dict)

    fields_not_empty_1 = clear_rows_and_cols_fields(var_to_check, value, new_dict)
    fields_not_empty_2 = clear_global_cons_fields(var_to_check, value, new_dict)

    if fields_not_empty_1 and fields_not_empty_2:
        dicts_stack.append(new_dict)
        return True
    return False


def clear_rows_and_cols_fields(var_to_check, value, new_dict):
    vars_to_clear = get_vars_in_same_row_or_col(var_to_check)

    for var in vars_to_clear:
        field = new_dict[var]
        if value in field:
            field.remove(value)
        if len(field) <= 0:
            return False
    return True


def clear_global_cons_fields(var_to_check, value, new_dict):
    ref_cons_list = orig_cons_list
    smaller_vars, bigger_vars = get_smaller_and_bigger_vars(var_to_check)

    if remove_smaller_values(value, smaller_vars, new_dict):
        if remove_bigger_values(value, bigger_vars, new_dict):
            return True
    return False


def remove_bigger_values(value, bigger_vars, new_dict):
    for var in bigger_vars:
        new_field = [val for val in new_dict[var] if val > value]
        new_dict[var] = new_field
        if len(new_field) <= 0:
            return False
    return True


def remove_smaller_values(value, smaller_vars, new_dict):
    for var in smaller_vars:
        new_field = [val for val in new_dict[var] if val < value]
        new_dict[var] = new_field
        if len(new_field) <= 0:
            return False
    return True


def get_smaller_and_bigger_vars(var_to_check):
    first_poss_linked_var = (var_to_check[0], var_to_check[1] + 1)
    second_poss_linked_var = (var_to_check[0] + 1, var_to_check[1])

    smaller_vars = []
    bigger_vars = []

    for (x, y) in orig_cons_list:
        if x == var_to_check:
            if y == first_poss_linked_var:
                bigger_vars.append(first_poss_linked_var)
            elif y == second_poss_linked_var:
                bigger_vars.append(second_poss_linked_var)
        elif y == var_to_check:
            if x == first_poss_linked_var:
                smaller_vars.append(first_poss_linked_var)
            elif x == second_poss_linked_var:
                smaller_vars.append(second_poss_linked_var)

    return smaller_vars, bigger_vars


def get_vars_in_same_row_or_col(var_to_check):
    linked_vars = []
    for i in range(curr_var_idx, vars_count):
        var = vars_list[i]
        if var != var_to_check and (var[0] == var_to_check[0] or var[1] == var_to_check[1]):
            linked_vars.append(var)
    return linked_vars


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
