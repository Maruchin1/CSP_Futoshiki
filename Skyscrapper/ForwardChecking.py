import numpy as np
import copy
import time
from Main import Output, Stats, notify_solution_found, notify_end_loop
import random


class ForwardChecking:
    def __init__(self, data):
        self.data = data
        self.start_time = 0
        self.back_count = 0
        self.nodes_count = 0
        self.output = Output(data.file_name, "ForwardChecking")
        self.board_matrix = np.copy(data.board_matrix)
        self.cons_matrix = np.copy(data.cons_matrix)
        self.initial_vars_dict = copy.deepcopy(data.vars_dict)
        self.vars_dicts_stack = [self.initial_vars_dict]
        self.vars_list = list(self.initial_vars_dict)
        # self.cons_list = data.cons_list
        self.curr_var_idx = 0

        # self._heuristic_most_cons()
        # self._heuristic_smallest_field()

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

            if next_value is None:
                self._go_back(curr_var)
                continue

            self.nodes_count += 1
            is_val_correct = self._check_forward(curr_var, next_value)
            if is_val_correct:
                self._go_deeper(curr_var)
            else:
                self.back_count += 1
        return self.output

    def _go_back(self, curr_var):
        self.vars_dicts_stack.pop()
        self.board_matrix[curr_var] = 0
        self.curr_var_idx -= 1

    def _go_deeper(self, curr_var):
        if curr_var != self.vars_list[len(self.vars_list) - 1]:
            self.curr_var_idx += 1
        else:
            self._solution_found()
            self.vars_dicts_stack.pop()

    def _get_next_val(self, curr_var):
        curr_dict = self.vars_dicts_stack[len(self.vars_dicts_stack) - 1]
        field = list(curr_dict[curr_var])
        if len(field) <= 0:
            return None
        # next_val = field.pop(0)
        next_val = field.pop(len(field) - 1)
        # next_val = field.pop(random.randint(0, len(field) - 1))
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

    def _solution_found(self):
        search_time = time.time() - self.start_time
        self.output.solution_matrix = np.copy(self.board_matrix)
        self.output.solution_stats = Stats(float(search_time), int(self.back_count), int(self.nodes_count))
        notify_solution_found(search_time, self.board_matrix, self.back_count, self.nodes_count)

    def _loop_end(self):
        end_time = time.time() - self.start_time
        self.output.end_stats = Stats(float(end_time), int(self.back_count), int(self.nodes_count))
        notify_end_loop(end_time, self.back_count, self.nodes_count)

    def _heuristic_most_cons(self):
        print("HEURISTIC MOST CONS")
        self.vars_list.sort(key=self._cons_num, reverse=True)

    def _cons_num(self, var):
        row_num, col_num = var
        cons_num = 0
        if self.board_matrix[0][col_num] > 0:
            cons_num += 1
        if self.board_matrix[1][col_num] > 0:
            cons_num += 1
        if self.board_matrix[2][row_num] > 0:
            cons_num += 1
        if self.board_matrix[3][row_num] > 0:
            cons_num += 1
        return cons_num

    def _heuristic_smallest_field(self):
        print("HEURISTIC SMALLEST FIELD")
        self.vars_list.sort(key=self._field_size)

    def _field_size(self, var):
        field = self.initial_vars_dict[var]
        return len(field)
