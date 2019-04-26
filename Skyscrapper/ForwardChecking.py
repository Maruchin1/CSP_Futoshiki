import numpy as np
import copy
import time
from Skyscrapper import SkyMain


class ForwardChecking:
    def __init__(self, data):
        self.data = data
        self.back_count = 0
        self.nodes_count = 0
        self.board_matrix = np.copy(data.board_matrix)
        self.cons_matrix = np.copy(data.cons_matrix)
        self.initial_vars_dict = copy.deepcopy(data.vars_dict)
        self.vars_dicts_stack = [self.initial_vars_dict]
        self.vars_list = list(self.initial_vars_dict)
        self.curr_var_idx = 0

    def search_solutions(self):
        start_time = time.time()
        print("\nSTART FORWARD CHECKING LOOP")
        while self.curr_var_idx < len(self.vars_list):
            if self.curr_var_idx == -1:
                SkyMain.notify_end_loop(start_time, self.back_count, self.nodes_count)
                return

            curr_var = self.vars_list[self.curr_var_idx]
            next_value = self._get_next_val(curr_var)

            # if curr_var == (0, 2) and next_value == 4:
            #     x = 1

            if next_value is None:
                self._go_back(curr_var)
                self.back_count += 1
                continue

            is_val_correct = self._check_forward(curr_var, next_value)
            if is_val_correct:
                self._go_deeper(curr_var, next_value, start_time)
            else:
                self.back_count += 1

    def _go_back(self, curr_var):
        self.vars_dicts_stack.pop()
        self.board_matrix[curr_var] = self.data.board_matrix[curr_var].copy()
        self.curr_var_idx -= 1

    def _go_deeper(self, curr_var, corr_value, start_time):
        # self.board_matrix[curr_var] = corr_value
        if curr_var != (self.data.dim - 1, self.data.dim - 1):
            self.curr_var_idx += 1
        else:
            SkyMain.notify_solution_found(start_time, self.board_matrix, self.back_count, self.nodes_count)
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
        self.board_matrix[var_to_check] = value
        curr_dict = self.vars_dicts_stack[len(self.vars_dicts_stack) - 1]
        new_dict = copy.copy(curr_dict)

        if self._clear_rows_and_cols(var_to_check, value, new_dict):
            if self._check_global_cons(var_to_check):
                self.vars_dicts_stack.append(new_dict)
                return True
        self.board_matrix[var_to_check] = 0
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

    def _check_global_cons(self, var_to_check):
        (row_num, col_num) = var_to_check
        row = list(self.board_matrix[row_num, :])
        left_con = self.cons_matrix[2, row_num]
        if not self._check_single_con(row, left_con):
            return False

        row.reverse()
        right_con = self.cons_matrix[3, row_num]
        if not self._check_single_con(row, right_con):
            return False

        col_num = var_to_check[1]
        col = list(self.board_matrix[:, col_num])
        top_con = self.cons_matrix[0, col_num]
        if not self._check_single_con(col, top_con):
            return False

        col.reverse()
        bot_con = self.cons_matrix[1, col_num]
        if not self._check_single_con(col, bot_con):
            return False

        return True

    def _check_single_con(self, vals_list, con):
        if con == 0 or 0 in vals_list:
            return True
        visible_count = self._visible_count(vals_list)
        return visible_count == con

    def _visible_count(self, vals_list):
        visible_count = 1
        biggest_val = vals_list[0]
        for i in range(1, len(vals_list)):
            curr_val = vals_list[i]
            if curr_val > biggest_val:
                visible_count += 1
                biggest_val = curr_val
        return visible_count