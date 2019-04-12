import numpy as np
from Data import load_data

FILE_NAME = "futoshiki_4_0.txt"


def start():
    print("start")
    data = load_data(FILE_NAME)
    print("data matrix")
    print(data.board_matrix)
    print("constraints")
    print(data.constraints_arr)
    print("variables")
    print(data.variables_dict)
    search_solution(data)


def search_solution(data):
    dimension = int(data.dimension)
    variables_dict = data.variables_dict.copy()
    board_matrix = np.copy(data.board_matrix)
    constraints_arr = np.copy(data.constraints_arr)

    for i in variables_dict:
        print(i)

    curr_var_idx = 0
    # for idx in range(variables_dict.size):
    #     print(variables_dict[idx])
        # variable = np.copy(variables_arr[curr_var_idx])
        # coords_arr = np.array(variable[dimension:])
        # field_arr = np.array(variable[:dimension])
        #
        # not_checked_idx_arr = np.where(field_arr != -1)[0]
        # if not_checked_idx_arr.size > 0:
        #     next_value = field_arr[not_checked_idx_arr[0]]


if __name__ == '__main__':
    start()
