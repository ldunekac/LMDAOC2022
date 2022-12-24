from dataclasses import dataclass, field
from queue import PriorityQueue


lizzard_states = {

}

@dataclass(frozen=True, order=True)
class State:
    norm: int # 1 norm
    num_steps: int
    position: tuple
    lizzard_state: int 


@dataclass(frozen=True)
class Liz:
    position: tuple
    direction: tuple

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.position == other
        else:
            return self.position == other.position and self.direction == other.direction


def read_input(file):
    with open(file, "r") as f:
        rows = f.readlines()
        rows = [row.strip() for row in rows]
        start = (0, rows[0].index("."))
        end = (len(rows)-1, rows[-1].index("."))

        bounds = (len(rows)-1, len(rows[0])-1)

        lizzards = []
        for rind, row in enumerate(rows):
            for cind, col in enumerate(row):
                if col == '>':
                    lizzards.append(Liz((rind, cind), (0, 1)))
                elif col == '<':
                    lizzards.append(Liz((rind, cind), (0, -1)))
                elif col == '^':
                    lizzards.append(Liz((rind, cind), (-1, 0)))
                elif col == 'v':
                    lizzards.append(Liz((rind, cind), (1, 0)))
        lizzard_states[-1] = tuple(lizzards)
        lizzard_states[1] = set([liz.position for liz in lizzard_states[-1]])
        return start, end, bounds

def walk_lizzard(liz, bounds):
    row, col = liz.position
    row_dir, col_dir = liz.direction
    row += row_dir
    col += col_dir
    max_row, max_col = bounds

    if row == 0:
        row = max_row - 1
    elif row == max_row:
        row = 1
    elif col == 0: 
        col = max_col - 1
    elif col == max_col:
        col = 1

    return Liz(
        (row, col),
        liz.direction
    )

def print_board(pos, bounds, lizzards):
    num_rows = bounds[0]
    num_cols = bounds[1]
    for i in range(num_rows + 1):
        for j in range(num_cols + 1):
            if i == 0 or j == 0 or i == num_rows or j == num_cols:
                print('#', end='')
            elif (i,j) == pos:
                print("E")
            elif (i,j) in lizzards:
                print('L', end='')
            else:
                print('.', end='')
        print("", flush=True)

def walk_the_lizzards(num_steps, bounds):
    num_steps %= ((bounds[0] - 1) * (bounds[1] -1))
    num_steps += 1
    global lizzard_states
    if num_steps in lizzard_states.keys():
        return lizzard_states[num_steps]
    lizzard_states[-1 * num_steps] = tuple(walk_lizzard(liz, bounds) for liz in lizzard_states[-1 * (num_steps-1)])
    lizzard_states[num_steps] = set([liz.position for liz in lizzard_states[-1 * num_steps]]) 
    return lizzard_states[num_steps]

def norm1(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def get_lizzard_state(step_num, bounds):
    return step_num % ((bounds[0] - 1) * (bounds[1] - 1))

def sim(start, end, bounds):
    pq = PriorityQueue()
    max_row = bounds[0]
    max_col = bounds[1]
    begin = State(
        end[0] - start[0] + end[1] - start[1],
        0,
        start,
        0
    )
    pq.put(begin)

    min_steps = None

    seen = {}

    movement = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
    i = 0
    while True:
        i += 1
        if i % 100000 == 0:
            print(pq.qsize())
        if pq.empty():
            break

        next_state = pq.get()
        lizzard_state = get_lizzard_state(next_state.num_steps, bounds)
        if (next_state.position, lizzard_state) in seen.keys():
            if next_state.num_steps < seen[(next_state.position, lizzard_state)]:
                 seen[(next_state.position, lizzard_state)] = next_state.num_steps
            else:
                continue
        else:
            seen[(next_state.position, lizzard_state)] = next_state.num_steps

        if next_state.norm == 0:
            if min_steps is None:
                print(f"First min {next_state.num_steps}")
                min_steps = next_state.num_steps
            else:
                if next_state.num_steps < min_steps:
                    min_steps = next_state.num_steps
                    print(f"New min {min_steps}")
        
        if min_steps is not None:
            best_remaining = next_state.num_steps + norm1(next_state.position, end)
            if best_remaining >= min_steps:
                continue

        new_lizzards_positions = walk_the_lizzards(next_state.num_steps + 1, bounds)
        crow, ccol = next_state.position
        next_possilbe_movements = [(crow + rowd, ccol + cold) for rowd, cold in movement ]
        for next_pos in next_possilbe_movements:
            if not next_pos in new_lizzards_positions:
                if 1 <= next_pos[0] < max_row and 1 <= next_pos[1] < max_col:
                    pq.put(
                        State(
                            end[0] - next_pos[0] + end[1] - next_pos[1],
                            next_state.num_steps + 1,
                            next_pos,
                            lizzard_state
                        )
                    )
                elif next_pos in [start, end]:
                    pq.put(
                        State(
                            end[0] - next_pos[0] + end[1] - next_pos[1],
                            next_state.num_steps + 1,
                            next_pos,
                            lizzard_state
                        )
                    )
    return min_steps

def solution1(file: str) -> int:
    start, end, bounds = read_input(file)

    # r = (bounds[0] - 1) * (bounds[1] - 1)
    # print(r)
    # for i in range(r):
    #     walk_the_lizzards(i, bounds)

    # print(walk_the_lizzards(0, bounds))
    # print(walk_the_lizzards(3000, bounds))
    # print_board(start, bounds, walk_the_lizzards(0, bounds))
    # print_board(start, bounds, walk_the_lizzards(1, bounds))
    # print_board(start, bounds, walk_the_lizzards(2, bounds))
    # print_board(start, bounds, walk_the_lizzards(3, bounds))
    # print_board(start, bounds, walk_the_lizzards(4, bounds))
    # return 
    # print(bounds)
    # return
    return sim(start, end, bounds)

def solution2(file: str) -> int:
    pass

def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    global lizzard_states
    lizzard_states = {}
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    # ans = solution2("example2.txt")
    # print(f"Solution 2 for Example 2 is: {ans}")
    # ans = solution2("input.txt")
    # print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()
