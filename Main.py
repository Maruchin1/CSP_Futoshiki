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
    print(data.variables_arr)
    search_solution(data)


def search_solution(data):
    dimension = int(data.dimension)
    variables_arr = np.copy(data.variables_arr)
    board_matrix = np.copy(data.board_matrix)
    constraints_arr = np.copy(data.constraints_arr)

    curr_var_idx = 0
    for idx in range(variables_arr.size):
        variable = np.copy(variables_arr[curr_var_idx])
        coords_arr = variable[dimension:]
        field_arr = variable[:dimension]


if __name__ == '__main__':
    start()
