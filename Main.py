from Data import load_data

if __name__ == '__main__':
    print("start main")

    data = load_data("futoshiki_4_1.txt")

    print("data matrix")
    print(data.board_matrix)
    print("constraints")
    print(data.constraints_arr)
