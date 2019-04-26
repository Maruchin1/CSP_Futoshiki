from datetime import datetime


class Output:
    def __init__(self, file_name, algorithm_name):
        self.file_name = file_name
        self.algorithm_name = algorithm_name
        self.solution_matrix = None
        self.solution_stats = None
        self.end_stats = None


class Stats:
    def __init__(self, time, back_count, nodes_count):
        self.time = time
        self.back_count = back_count
        self.nodes_count = nodes_count

    def __repr__(self):
        return "Time = " + str(self.time) + \
               "\nBack count = " + str(self.back_count) + \
               "\nNodes count = " + str(self.nodes_count) + "\n"


def notify_solution_found(search_time, board_matrix, back_count, nodes_count):
    print("\nFOUND SOLUTION")
    print(board_matrix)
    print(f'search time = {search_time}')
    print(f'back count = {back_count}')
    print(f'nodes count = {nodes_count}')


def notify_end_loop(end_time, back_count, nodes_count):
    print("\nEND OF LOOP")
    print(f'end time = {end_time}')
    print(f'back count = {back_count}')
    print(f'nodes count = {nodes_count}')


def futo_backtracking(file_name, iterations_count):
    from Futoshiki.BackTracking import BackTracking
    from Futoshiki.FutoData import load_data
    search_solution_loop(BackTracking, load_data(file_name), iterations_count)


def futo_forward_checking(file_name, iterations_count):
    from Futoshiki.ForwardChecking import ForwardChecking
    from Futoshiki.FutoData import load_data
    search_solution_loop(ForwardChecking, load_data(file_name), iterations_count)


def sky_backtracking(file_name, iterations_count, reduce_fields_enabled):
    from Skyscrapper.Backtracking import Backtracking
    from Skyscrapper.SkyData import load_data
    search_solution_loop(Backtracking, load_data(file_name, reduce_fields_enabled), iterations_count)


def sky_forward_checking(file_name, iterations_count, reduce_fields_enabled):
    from Skyscrapper.ForwardChecking import ForwardChecking
    from Skyscrapper.SkyData import load_data
    search_solution_loop(ForwardChecking, load_data(file_name, reduce_fields_enabled), iterations_count)


def search_solution_loop(algorithm, data, iterations_count):
    output_list = []
    for i in range(iterations_count):
        print("\nITERATION ", i + 1, " -------------------------------------------------------------------------------")
        output = algorithm(data).search_solutions()
        output_list.append(output)
    print("\nITERATIONS END")
    write_output_to_file(make_total_output(output_list))


def make_total_output(output_list):
    solution_stats_list = [o.solution_stats for o in output_list]
    end_stats_list = [o.end_stats for o in output_list]
    total_output = output_list[0]
    total_output.solution_stats = make_total_stats(solution_stats_list)
    total_output.end_stats = make_total_stats(end_stats_list)
    return total_output


def make_total_stats(stats_list):
    time_list = []
    back_count_list = []
    nodes_count_list = []
    for stats in stats_list:
        time_list.append(stats.time)
        back_count_list.append(stats.back_count)
        nodes_count_list.append(stats.nodes_count)
    stats = Stats(time_list, back_count_list, nodes_count_list)
    return stats


def write_output_to_file(output):
    dir_name = "output/"
    curr_datetime = "{date:%Y-%m-%d_%H-%M-%S}".format(date=datetime.now())
    file_name = output.file_name + "-" + output.algorithm_name + "-" + curr_datetime + ".txt"
    with open(dir_name + file_name, "w") as file:
        file.write("File name = " + output.file_name)
        file.write("\nAlgorithm = " + output.algorithm_name)
        file.write("\n\nSolution")
        file.write("\n" + str(output.solution_matrix))
        file.write("\n" + str(output.solution_stats))
        file.write("\nEnd")
        file.write("\n" + str(output.end_stats))
        file.close()


if __name__ == '__main__':
    FUTO_DATA = "test_futo_7_0.txt"
    # futo_backtracking(FUTO_DATA, 4)
    futo_forward_checking(FUTO_DATA, 4)

    SKY_DATA = "test_sky_6_2.txt"
    # sky_backtracking(SKY_DATA, 4, True)
    # sky_forward_checking(SKY_DATA, 4, True)
