import numpy as np
import copy
import time
from Main import Output, Stats, notify_solution_found, notify_end_loop


class BackTracking:
    def __init__(self, data):
        self.data = data
        self.start_time = 0
        self.back_count = 0
        self.nodes_count = 0
        self.output = Output(data.file_name, "Backtracking")
        self.board_matrix = np.copy(data.board_matrix)
        self.vars_dict = copy.deepcopy(data.variables_dict)
        self.vars_list = list(self.vars_dict)
        self.vars_cons_num_dict = copy.copy(data.vars_cons_num_dict)
        self.curr_var_idx = 0

        self._heuristic_most_cons()

    def search_solutions(self):
        self.start_time = time.time()
        print("FILE NAME: ", self.data.file_name)
        print("START BACKTRACKING LOOP")
        while self.curr_var_idx < len(self.vars_list):
            if self.curr_var_idx == -1:
                self._loop_end()
                return self.output

            curr_var = self.vars_list[self.curr_var_idx]
            next_val = self._get_next_val(curr_var)

            if next_val is None:
                self._go_back(curr_var)
                continue

            self.nodes_count += 1
            is_val_correct = self._check_cons(curr_var, next_val)
            if is_val_correct:
                found = self._go_deeper(curr_var, next_val)
                if found:
                    return self.output
            else:
                self.back_count += 1
        return self.output

    def _go_back(self, curr_var):
        self.vars_dict[curr_var] = list(self.data.variables_dict[curr_var])
        self.board_matrix[curr_var] = self.data.board_matrix[curr_var].copy()
        self.curr_var_idx -= 1

    def _go_deeper(self, curr_var, corr_value):
        self.board_matrix[curr_var] = corr_value
        if curr_var != (self.data.dimension - 1, self.data.dimension - 1):
            self.curr_var_idx += 1
            return False
        else:
            self._solution_found()
            return True

    def _get_next_val(self, curr_var):
        field = list(self.vars_dict[curr_var])
        if len(field) <= 0:
            return None
        next_val = field.pop(0)
        self.vars_dict[curr_var] = field
        return next_val

    def _check_cons(self, var_to_check, value):
        if self._check_rows_and_cols(var_to_check, value):
            if self._check_global_cons(var_to_check, value):
                return True
        return False

    def _check_rows_and_cols(self, var_to_check, value):
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

    def _check_global_cons(self, var_to_check, value):
        cons_with_var = [(x, y) for (x, y) in self.data.constraints_list if x == var_to_check or y == var_to_check]
        if len(cons_with_var) <= 0:
            return True

        for (first_cell, second_cell) in cons_with_var:
            first_cell_val = value if first_cell == var_to_check else self.board_matrix[first_cell]
            second_cell_val = value if second_cell == var_to_check else self.board_matrix[second_cell]

            if first_cell_val == 0 or second_cell_val == 0:
                return True

            if first_cell_val >= second_cell_val:
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

    def _heuristic_most_cons(self):
        self.vars_list.sort(key=self._cons_num, reverse=True)

    def _cons_num(self, var):
        return self.vars_cons_num_dict[var]
