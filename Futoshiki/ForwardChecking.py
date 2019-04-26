import numpy as np
import copy
import time
from Main import Output, Stats, notify_solution_found, notify_end_loop


class ForwardChecking:
    def __init__(self, data):
        self.data = data
        self.start_time = 0
        self.back_count = 0
        self.nodes_count = 0
        self.output = Output(data.file_name, "Forward_Checking")
        self.board_matrix = np.copy(data.board_matrix)
        self.initial_vars_dict = copy.deepcopy(data.variables_dict)
        self.vars_dicts_stack = [self.initial_vars_dict]
        self.vars_list = list(self.initial_vars_dict)
        self.curr_var_idx = 0

    def search_solutions(self):
        self.start_time = time.time()
        print("FILE NAME: ", self.data.file_name)
        print("START FORWARD CHECKING LOOP")
        while self.curr_var_idx < len(self.vars_list):
            if self.curr_var_idx == -1:
                self._loop_end()
                return self.output

            curr_var = self.vars_list[self.curr_var_idx]
            next_value = self._get_next_val(curr_var)
            self.nodes_count += 1

            if next_value is None:
                self._go_back(curr_var)
                self.back_count += 1
                continue

            is_val_correct = self._check_forward(curr_var, next_value)
            if is_val_correct:
                self._go_deeper(curr_var, next_value)
            else:
                self.back_count += 1
        return self.output

    def _go_back(self, curr_var):
        self.vars_dicts_stack.pop()
        self.board_matrix[curr_var] = self.data.board_matrix[curr_var].copy()
        self.curr_var_idx -= 1

    def _go_deeper(self, curr_var, corr_value):
        self.board_matrix[curr_var] = corr_value
        if curr_var != (self.data.dimension - 1, self.data.dimension - 1):
            self.curr_var_idx += 1
        else:
            self._solution_found()
            self.vars_dicts_stack.pop()

    def _get_next_val(self, curr_var):
        curr_dict = self.vars_dicts_stack[len(self.vars_dicts_stack) - 1]
        field = list(curr_dict[curr_var])
        if len(field) <= 0:
            return None
        next_val = field.pop(0)
        curr_dict[curr_var] = field
        return next_val

    def _check_forward(self, var_to_check, value):
        curr_dict = self.vars_dicts_stack[len(self.vars_dicts_stack) - 1]
        new_dict = copy.copy(curr_dict)

        if self._clear_rows_and_cols(var_to_check, value, new_dict):
            if self._clear_global_cons(var_to_check, value, new_dict):
                self.vars_dicts_stack.append(new_dict)
                return True
        return False

    def _clear_rows_and_cols(self, var_to_check, value, new_dict):
        vars_to_clear = self._get_vars_in_same_row_or_col(var_to_check)
        for var in vars_to_clear:
            field = list(new_dict[var])
            if value in field:
                field.remove(value)
                new_dict[var] = field
            if len(field) <= 0:
                return False
        return True

    def _get_vars_in_same_row_or_col(self, var_to_check):
        linked_vars = []
        for i in range(self.curr_var_idx, len(self.vars_list)):
            var = self.vars_list[i]
            if var != var_to_check and (var[0] == var_to_check[0] or var[1] == var_to_check[1]):
                linked_vars.append(var)
        return linked_vars

    def _clear_global_cons(self, var_to_check, value, new_dict):
        smaller_vars, bigger_vars = self._get_smaller_and_bigger_vars(var_to_check)
        if self._remove_smaller_values(value, smaller_vars, new_dict):
            if self._remove_bigger_values(value, bigger_vars, new_dict):
                return True
        return False

    def _get_smaller_and_bigger_vars(self, var_to_check):
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

    def _remove_bigger_values(self, value, bigger_vars, new_dict):
        for var in bigger_vars:
            new_field = [val for val in new_dict[var] if val > value]
            new_dict[var] = new_field
            if len(new_field) <= 0:
                return False
        return True

    def _remove_smaller_values(self, value, smaller_vars, new_dict):
        for var in smaller_vars:
            new_field = [val for val in new_dict[var] if val < value]
            new_dict[var] = new_field
            if len(new_field) <= 0:
                return False
        return True

    def _solution_found(self):
        search_time = time.time() - self.start_time
        self.output.solution_matrix = np.copy(self.board_matrix)
        self.output.solution_stats = Stats(float(search_time), int(self.back_count), int(self.nodes_count))
        notify_solution_found(search_time, self.board_matrix, self.back_count, self.nodes_count)

    def _loop_end(self):
        end_time = time.time() - self.start_time
        self.output.end_stats = Stats(float(end_time), int(self.back_count), int(self.nodes_count))
        notify_end_loop(end_time, self.back_count, self.nodes_count)
