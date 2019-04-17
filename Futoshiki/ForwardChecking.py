import numpy as np
import copy
import time
from Futoshiki import FutoMain


class ForwardChecking:
    def __init__(self, data):
        self.data = data
        self.back_count = 0
        self.nodes_count = 0
        self.board_matrix = np.copy(data.board_matrix)
        self.initial_vars_dict = copy.deepcopy(data.variables_dict)
        self.vars_dicts_stack = [self.initial_vars_dict]
        self.vars_list = list(self.initial_vars_dict)
        self.curr_var_idx = 0

    def search_solutions(self):
        start_time = time.time()
        print("\nSTART FORWARD CHECKING LOOP")
        while self.curr_var_idx < len(self.vars_list):
            if self.curr_var_idx == -1:
                FutoMain.notify_end_loop(start_time, self.back_count, self.nodes_count)
                return

            curr_var = self.vars_list[self.curr_var_idx]
            next_value = self.get_next_val(curr_var)
            self.nodes_count += 1

            if next_value is None:
                self.go_back(curr_var)
                self.back_count += 1
                continue

            is_val_correct = self.check_forward(curr_var, next_value)
            if is_val_correct:
                self.go_deeper(curr_var, next_value, start_time)
            else:
                self.back_count += 1

    def go_back(self, curr_var):
        self.vars_dicts_stack.pop()
        self.board_matrix[curr_var] = self.data.board_matrix[curr_var].copy()
        self.curr_var_idx -= 1

    def go_deeper(self, curr_var, corr_value, start_time):
        self.board_matrix[curr_var] = corr_value
        if curr_var != (self.data.dimension - 1, self.data.dimension - 1):
            self.curr_var_idx += 1
        else:
            FutoMain.notify_solution_found(start_time, self.board_matrix, self.back_count, self.nodes_count)
            self.vars_dicts_stack.pop()

    def get_next_val(self, curr_var):
        curr_dict = self.vars_dicts_stack[len(self.vars_dicts_stack) - 1]
        field = list(curr_dict[curr_var])
        if len(field) <= 0:
            return None
        next_val = field.pop(0)
        curr_dict[curr_var] = field
        return next_val

    def check_forward(self, var_to_check, value):
        curr_dict = self.vars_dicts_stack[len(self.vars_dicts_stack) - 1]
        new_dict = copy.copy(curr_dict)

        if self.clear_rows_and_cols(var_to_check, value, new_dict):
            if self.clear_global_cons(var_to_check, value, new_dict):
                self.vars_dicts_stack.append(new_dict)
                return True
        return False

    def clear_rows_and_cols(self, var_to_check, value, new_dict):
        vars_to_clear = self.get_vars_in_same_row_or_col(var_to_check)
        for var in vars_to_clear:
            field = list(new_dict[var])
            if value in field:
                field.remove(value)
                new_dict[var] = field
            if len(field) <= 0:
                return False
        return True

    def get_vars_in_same_row_or_col(self, var_to_check):
        linked_vars = []
        for i in range(self.curr_var_idx, len(self.vars_list)):
            var = self.vars_list[i]
            if var != var_to_check and (var[0] == var_to_check[0] or var[1] == var_to_check[1]):
                linked_vars.append(var)
        return linked_vars

    def clear_global_cons(self, var_to_check, value, new_dict):
        smaller_vars, bigger_vars = self.get_smaller_and_bigger_vars(var_to_check)
        if self.remove_smaller_values(value, smaller_vars, new_dict):
            if self.remove_bigger_values(value, bigger_vars, new_dict):
                return True
        return False

    def get_smaller_and_bigger_vars(self, var_to_check):
        first_poss_linked_var = (var_to_check[0], var_to_check[1] + 1)
        second_poss_linked_var = (var_to_check[0] + 1, var_to_check[1])
        smaller_vars = []
        bigger_vars = []
        for (x, y) in self.data.constraints_list:
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

    def remove_bigger_values(self, value, bigger_vars, new_dict):
        for var in bigger_vars:
            new_field = [val for val in new_dict[var] if val > value]
            new_dict[var] = new_field
            if len(new_field) <= 0:
                return False
        return True

    def remove_smaller_values(self, value, smaller_vars, new_dict):
        for var in smaller_vars:
            new_field = [val for val in new_dict[var] if val < value]
            new_dict[var] = new_field
            if len(new_field) <= 0:
                return False
        return True
