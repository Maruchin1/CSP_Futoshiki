import numpy as np
import copy
import time
from Main import Output, Stats, notify_solution_found, notify_end_loop


class Backtracking:
    def __init__(self, data):
        self.data = data
        self.start_time = 0
        self.back_count = 0
        self.nodes_count = 0
        self.output = Output(data.file_name, "Backtracking")
        self.board_matrix = np.copy(data.board_matrix)
        self.vars_dict = copy.deepcopy(data.vars_dict)
        self.vars_list = list(self.vars_dict)
        self.cons_matrix = np.copy(data.cons_matrix)
        self.curr_var_idx = 0

    def search_solutions(self):
        self.start_time = time.time()
        print("FILE NAME: ", self.data.file_name)
        print("START BACKTRACKING LOOP")
        while self.curr_var_idx < len(self.vars_list):
            if self.curr_var_idx == -1:
                self._loop_end()
                return self.output

            curr_var = self.vars_list[self.curr_var_idx]
            next_val = self.get_next_val(curr_var)

            if next_val is None:
                self.go_back(curr_var)
                continue

            self.nodes_count += 1
            is_val_correct = self.check_cons(curr_var, next_val)
            if is_val_correct:
                self.go_deeper(curr_var)
            else:
                self.back_count += 1
        return self.output

    def go_back(self, curr_var):
        self.vars_dict[curr_var] = list(self.data.def_field)
        self.board_matrix[curr_var] = 0
        self.curr_var_idx -= 1

    def go_deeper(self, curr_var):
        if curr_var != (self.data.dim - 1, self.data.dim - 1):
            self.curr_var_idx += 1
        else:
            self._solution_found()

    def get_next_val(self, curr_var):
        field = list(self.vars_dict[curr_var])
        if len(field) <= 0:
            return None
        next_val = field.pop(0)
        self.vars_dict[curr_var] = field
        return next_val

    def check_cons(self, var_to_check, value):
        self.board_matrix[var_to_check] = value
        if self.check_rows_and_cols(var_to_check, value):
            if self.check_global_cons(var_to_check):
                return True
        self.board_matrix[var_to_check] = 0
        return False

    def check_rows_and_cols(self, var_to_check, value):
        row_num = var_to_check[0]
        col_num = var_to_check[1]

        row = list(self.board_matrix[row_num, :])
        del row[col_num]
        if value in row:
            return False

        col = list(self.board_matrix[:, col_num])
        del col[row_num]
        if value in col:
            return False

        return True

    def check_global_cons(self, var_to_check):
        row_num = var_to_check[0]
        row = list(self.board_matrix[row_num, :])
        left_con = self.cons_matrix[2, row_num]
        if not self.check_single_con(row, left_con):
            return False

        row.reverse()
        right_con = self.cons_matrix[3, row_num]
        if not self.check_single_con(row, right_con):
            return False

        col_num = var_to_check[1]
        col = list(self.board_matrix[:, col_num])
        top_con = self.cons_matrix[0, col_num]
        if not self.check_single_con(col, top_con):
            return False

        col.reverse()
        bot_con = self.cons_matrix[1, col_num]
        if not self.check_single_con(col, bot_con):
            return False

        return True

    def check_single_con(self, vals_list, con):
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
