from Skyscrapper.SkyData import load_data
from Skyscrapper import Backtracking
from Skyscrapper import ForwardChecking
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


def start_backtracking(file_name, reduce_fields_enabled):
    data = load_data(file_name, reduce_fields_enabled)
    Backtracking.Backtracking(data).search_solutions()


def start_forward_checkin(file_name, reduce_fields_enabled):
    data = load_data(file_name, reduce_fields_enabled)
    ForwardChecking.ForwardChecking(data).search_solutions()


