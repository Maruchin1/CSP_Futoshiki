import numpy as np
import copy
import time
import Main


class BackTracking:

    def __init__(self, data):
        self.data = data
        self.back_count = 0
        self.nodes_count = 0
        self.board_matrix = np.copy(data.board_matrix)
        self.vars_dict = copy.deepcopy(data.variables_dict)
        self.vars_list = list(self.vars_dict)
        self.curr_var_idx = 0

    def search_solutions(self):
        start_time = time.time()
        print("\nSTART BACKTRACKING LOOP")
        while self.curr_var_idx < len(self.vars_list):
            if self.curr_var_idx == -1:
                Main.notify_end_loop(start_time, self.back_count, self.nodes_count)
                return

            curr_var = self.vars_list[self.curr_var_idx]
            next_val = self.get_next_val(curr_var)
            self.nodes_count += 1

            if next_val is None:
                self.go_back(curr_var)
                continue

            is_val_correct = self.check_cons(curr_var, next_val)
            if is_val_correct:
                self.go_deeper(curr_var, next_val, start_time)
            else:
                self.back_count += 1

    def go_back(self, curr_var):
        self.vars_dict[curr_var] = self.data.variables_dict[curr_var].copy()
        self.board_matrix[curr_var] = self.data.board_matrix[curr_var].copy()
        self.curr_var_idx -= 1

    def go_deeper(self, curr_var, corr_value, start_time):
        self.board_matrix[curr_var] = corr_value
        if curr_var != (self.data.dimension - 1, self.data.dimension - 1):
            self.curr_var_idx += 1
        else:
            Main.notify_solution_found(start_time, self.board_matrix, self.back_count, self.nodes_count)

    def get_next_val(self, curr_var):
        field = self.vars_dict[curr_var]
        if len(field) <= 0:
            return None
        return field.pop(0)

    def check_cons(self, var_to_check, value):
        rows_and_cols_correct = self.check_rows_and_cols(var_to_check, value)
        global_cons_correct = self.check_global_cons(var_to_check, value)
        return rows_and_cols_correct and global_cons_correct

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

    def check_global_cons(self, var_to_check, value):
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
