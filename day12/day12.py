

def find_shortest_path(grid, start, end):
    num_rows_in_grid = len(grid)
    num_columns_in_grid = len(grid[0])
    max_num_steps = num_rows_in_grid * num_columns_in_grid + 1
    start_path = start + (0,)
    paths = [start_path]
    paths_len = {
        start_path: 0
    }
    paths_seen = set()

    while len(paths) > 0:
        next_path = paths.pop(0)
        current_row = next_path[0]
        current_column = next_path[1]
        current_height = grid[current_row][current_column]
        number_of_steps_in_path = next_path[2]

        up = current_row - 1
        if  up >= 0: # moving up is in the grid
            if grid[up][current_column] <= current_height + 1:
                if paths_len.get((up, current_column), max_num_steps) > number_of_steps_in_path + 1:
                    paths_len[(up, current_column)] = number_of_steps_in_path + 1
                    paths.append((up, current_column, number_of_steps_in_path + 1))

        down = current_row + 1
        if  down < num_rows_in_grid: # moving down is in the grid
            if grid[down][current_column] <= current_height + 1:
                if paths_len.get((down, current_column), max_num_steps) > number_of_steps_in_path + 1:
                    paths_len[(down, current_column)] = number_of_steps_in_path + 1
                    paths.append((down, current_column, number_of_steps_in_path + 1))

        left = current_column - 1
        if  left >= 0: # moving left is in the grid
            if grid[current_row][left] <= current_height + 1:
                if paths_len.get((current_row, left), max_num_steps) > number_of_steps_in_path + 1:
                    paths_len[(current_row, left)] = number_of_steps_in_path + 1
                    paths.append((current_row, left, number_of_steps_in_path + 1))

        right = current_column + 1
        if  right < num_columns_in_grid: # moving right is in the grid
            if grid[current_row][right] <= current_height + 1:
                if paths_len.get((current_row, right), max_num_steps) > number_of_steps_in_path + 1:
                    paths_len[(current_row, right)] = number_of_steps_in_path + 1
                    paths.append((current_row, right, number_of_steps_in_path + 1))


    return paths_len.get(end, max_num_steps)

def make_graph(file: str):
    grid = []
    start_location = None
    end_location = None
    row_counter = 0
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            s_loc = line.find("S")
            if s_loc >= 0:
                start_location = (row_counter, s_loc)
                line = line.replace("S", "a")
            e_loc = line.find("E")
            if e_loc >= 0:
                end_location = (row_counter, e_loc)
                line = line.replace("E", "z")
            row = [ord(char) for char in line]
            grid.append(row)
            row_counter += 1
    return grid, start_location, end_location


def solution1(file: str) -> int:
    grid, start, end = make_graph(file)
    return find_shortest_path(grid, start, end)

def solution2(file: str) -> int:
    grid, _, end = make_graph(file)
    starts = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ord("a"):
                starts.append((i,j))

    return min([find_shortest_path(grid, start, end) for start in starts])


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Input is: {ans}")


if __name__ == "__main__":
    main()
