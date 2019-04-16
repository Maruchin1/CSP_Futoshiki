from FutoData import load_data
import BackTracking
import ForwardChecking
import time


def notify_solution_found(start_time, board_matrix, back_count, nodes_count):
    search_time = time.time() - start_time
    print("\nFOUND SOLUTION")
    print(board_matrix)
    print(f'search time = {search_time}')
    print(f'back count = {back_count}')
    print(f'nodes count = {nodes_count}')


def notify_end_loop(start_time, back_count, nodes_count):
    end_time = time.time() - start_time
    print("\nEND OF LOOP")
    print(f'end time = {end_time}')
    print(f'back count = {back_count}')
    print(f'nodes count = {nodes_count}')


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

    # algorithm = ForwardChecking.ForwardChecking(data)
    algorithm = BackTracking.BackTracking(data)
    algorithm.search_solutions()
