
import numpy as np

def simulate(grid, start_sand_pos):
    grid_len = grid.shape[1]
    grid_height = grid.shape[0]
    sand_counter = -1
    while True:
        sand_counter += 1
        current_row = start_sand_pos[0]
        current_col = start_sand_pos[1]
        # if sand is off earth
        sand_moving = True
        if not grid[current_row][current_col] == 0:
            return sand_counter
        while sand_moving:
            if current_row + 1 == grid_height:
                return sand_counter
            if grid[current_row+1][current_col] == 0: # move down
                current_row += 1
            elif current_col - 1 < 0: #off the grid
                return sand_counter
            elif grid[current_row+1][current_col-1] == 0: # move left
                current_row += 1
                current_col -= 1
            elif current_col + 1 == grid_len: # off the grid
                return sand_counter
            elif grid[current_row+1][current_col+1] == 0: # move right
                current_row += 1
                current_col += 1
            else:
                grid[current_row][current_col] = 2
                sand_moving = False

def print_grid(grid, file):
    with open(file, "w+") as f:
        nrow, ncol = grid.shape
        for i in range(nrow):
            for j in range(ncol):
                if grid[i][j] == 0:
                    f.write(".")
                elif grid[i][j] == 1:
                    f.write("#")
                elif grid[i][j] == 2:
                    f.write("+")
                else:
                    f.write("W")
            f.write("\n")

def fill_grid(grid, paths, offset=0):
    for path in paths:
        prow, pcol = -1, -1
        for col, row in path:
            grid[row][col+offset] = 1
            if not prow == -1:
                if prow == row: # fill in the ys
                    horizontal_direction = -1 if pcol - col < 0 else 1
                    for ind in range(col, pcol, horizontal_direction):
                        grid[row][ind+offset] = 1
                elif pcol == col:
                    vertical_direction = 1 if row - prow < 0 else -1
                    for ind in range(row, prow, vertical_direction):
                        grid[ind][col+offset] = 1
                else:
                    print("CANT BE HERE")
                    raise
            prow = row
            pcol = col
        pcol = -1
        prow = -1
    last_row = grid.shape[0] - 1
    num_col = grid.shape[1]
    if not offset == 0: # fill bottom
        for i in range(num_col):
            grid[last_row][i] = 1

    return grid


def subtract_mins(minx, miny, paths):
    new_paths = []
    for path in paths:
        new_paths.append([(x-minx, y-miny) for x, y in path])
    return new_paths

def get_mins_and_maxes(paths):
    minx = 1_000_000_000
    maxx = 0
    miny = 1_000_000_000
    maxy = 0
    for path in paths:
        xs = [x for x, _ in path]
        ys = [y for _, y in path]
        minx = min(minx, min(xs))
        maxx = max(maxx, max(xs))
        miny = min(miny, min(ys))
        maxy = max(maxy, max(ys))

    return maxx, minx, maxy, miny

def read_input(file: str):
    paths = []
    with open(file, "r") as f:
        for line in f:
            sections = line.strip().split(" -> ")
            to_int = lambda x, y: (int(x), int(y))
            paths.append([to_int(*tuple(x.split(","))) for x in sections])
    return paths


def solution1(file: str) -> int:
    paths = read_input(file)
    maxx, minx, maxy, miny = get_mins_and_maxes(paths)
    paths = subtract_mins(minx, 0, paths)
    grid = np.ndarray(shape=(maxy + 1, maxx - minx + 1), dtype=int)
    grid.fill(0)
    grid = fill_grid(grid, paths)
    sand_count = simulate(grid, (0, 500-minx))

    print_grid(grid, "solution1"+file)
    return  sand_count

def solution2(file: str) -> int:
    paths = read_input(file)
    maxx, minx, maxy, miny = get_mins_and_maxes(paths)
    paths = subtract_mins(minx, 0, paths)
    max_height = maxy + 1 + 2
    grid = np.ndarray(shape=(maxy + 1 + 2, maxx - minx + 1 + max_height*2), dtype=int)
    grid.fill(0)
    grid = fill_grid(grid, paths, max_height + 1)
    sand_count = simulate(grid, (0, 500-minx+max_height+1))
    print_grid(grid, "solution2"+file)
    return  sand_count


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
