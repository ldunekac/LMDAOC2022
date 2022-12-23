from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Row:
    start: int
    end: int
    length: int
    walls: tuple


right_rotation = {
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1),
    (0, 1): (1, 0)
}

left_rotation = {
    (0, -1): (1, 0),
    (-1, 0): (0, -1),
    (0, 1): (-1, 0),
    (1, 0): (0, 1),
}

rotation_score = {
    (0, 1): 0, # facing right
    (1, 0): 1, # facing down
    (0, -1): 2, # facing left
    (-1, 0): 3 # facing up
}

def move_up(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_row = current_row - 1

    wrap = False
    # check if we are off the grid
    if new_row < 0: # off the start
        wrap = True
    elif not(board[new_row].start <= current_column <= board[new_row].end):
        # not in a valid grid cell
        wrap = True

    while wrap:
        # move down until we no loner reach a valid position
        new_row += 1
        if new_row >= len(board) or not(board[new_row].start <= current_column <= board[new_row].end):
            # now we have iterated one too many
            wrap = False
            new_row -= 1

    return new_row, current_column


def move_down(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_row = current_row + 1

    wrap = False
    # check if we are off the grid
    if new_row >= len(board): # off the end
        wrap = True
    elif not(board[new_row].start <= current_column <= board[new_row].end):
        # not in a valid grid cell
        wrap = True

    while wrap:
        # move down until we no loner reach a valid position
        new_row -= 1
        if new_row < 0 or not(board[new_row].start <= current_column <= board[new_row].end):
            # now we have iterated one too many
            wrap = False
            new_row += 1

    return new_row, current_column

def move_left(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_column = current_column - 1

    if new_column < board[current_row].start:
        new_column = board[current_row].end
    elif new_column >  board[current_row].end:
        new_column = board[current_row].start

    return  current_row, new_column


def move_right(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_column = current_column + 1

    if new_column < board[current_row].start:
        new_column = board[current_row].end
    elif new_column >  board[current_row].end:
        new_column = board[current_row].start

    return  current_row, new_column

def move_step(board, current_position, current_direction):
    if current_direction[0] == 1:
        return move_down(board, current_position)
    elif current_direction[0] == -1:
        return  move_up(board, current_position)
    elif current_direction[1] == 1:
        return move_right(board, current_position)
    elif current_direction[1] == -1:
        return move_left(board, current_position)
    else:
        print("Can not determine where to step")
        raise

def move_forward(board, current_position, current_direction, num_steps):
    row_step = current_direction[0]
    column_step = current_direction[1]
    prev_row, prev_column = current_position
    new_row, new_column = current_position
    for step in range(num_steps):
        new_row, new_column = move_step(board, (prev_row, prev_column), current_direction)
        # Check collision
        if new_column in board[new_row].walls:
            new_row, new_column = prev_row, prev_column
            break
        else:
            prev_row = new_row
            prev_column = new_column

    return new_row, new_column

def sim(board, instructions):
    current_position = (0, board[0].start)
    current_direction = (0, 1)

    for steps, turn in instructions:
        current_position = move_forward(board, current_position, current_direction, steps)
        current_direction = turn_left_or_right(turn, current_direction)

    row_points = 1000 * (current_position[0] + 1)
    column_points = 4 * (current_position[1] + 1)
    rotation_points = rotation_score[current_direction]
    return rotation_points + row_points + column_points


def turn_left_or_right(turn, current_rotation):
    if turn: # make sure turn is not none
        if turn == 'R':
            return right_rotation[current_rotation]
        elif turn == 'L':
            return left_rotation[current_rotation]
        else:
            raise
    else:
        return current_rotation


def move_right2(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_column = current_column + 1

    if new_column >  board[current_row].end:
        if 0 <= current_row <= 49: # going right off of top cube
            new_row = 149 - current_row
            new_column = 99
            return (new_row, new_column), (0, -1)
        elif 50 <= current_row <= 99:
            new_row = 49
            new_column = current_row + 50
            return (new_row, new_column), (-1, 0)
        elif 100 <= current_row <= 149:
            new_row = 49 - (current_row % 50)
            new_column = 149
            return (new_row, new_column), (0, -1)
        elif 150 <= current_row <= 199:
            new_row = 149
            new_column = current_row - 100
            return (new_row, new_column), (-1, 0)
        else:
            print("Moving Right dies")
            raise

    return  (current_row, new_column), (0, 1)


def move_left2(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_column = current_column - 1

    if new_column < board[current_row].start:
        if 0 <= current_row <= 49: # going right off of top cube
            new_row = 149 - current_row
            new_column = 0
            return (new_row, new_column), (0, 1)
        elif 50 <= current_row <= 99:
            new_row = 100
            new_column = -50 + current_row
            return (new_row, new_column), (1, 0)
        elif 100 <= current_row <= 149:
            new_row = 149 - current_row
            new_column = 50
            return (new_row, new_column), (0, 1)
        elif 150 <= current_row <= 199:
            new_row = 0
            new_column = current_row - 100
            return (new_row, new_column), (1, 0)
        else:
            print("Moving Left dies")
            print(current_row, current_column)
            raise

    return (current_row, new_column), (0, -1)


def move_down2(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_row = current_row + 1

    if new_row == 50 and 100 <= current_column <= 149:
        new_row = current_column - 50
        new_column = 99
        return (new_row, new_column), (0, -1)
    elif new_row == 150 and 50 <= current_column <= 99:
        new_row = current_column + 100
        new_column = 49
        return (new_row, new_column), (0, -1)
    elif new_row == 200 and 0 <= current_column <= 49:
        new_row = 0
        new_column = current_column + 100
        return (new_row, new_column), (1, 0)

    return (new_row, current_column), (1, 0)


def move_up2(board, current_position):
    current_row = current_position[0]
    current_column = current_position[1]

    new_row = current_row - 1

    if new_row == -1 and 100 <= current_column <= 149:
        new_row = 199
        new_column = current_column - 100
        return (new_row, new_column), (-1, 0)
    elif new_row == -1 and 50 <= current_column <= 99:
        new_row = 100 + current_column
        new_column = 0
        return (new_row, new_column), (0, 1)
    elif new_row == 99 and 0 <= current_column <= 49:
        new_row = current_column + 50
        new_column = 50
        return (new_row, new_column), (0, 1)

    return (new_row, current_column), (-1, 0)



def move_step2(board, current_position, current_direction):
    if current_direction[0] == 1:
        return move_down2(board, current_position)
    elif current_direction[0] == -1:
        return  move_up2(board, current_position)
    elif current_direction[1] == 1:
        return move_right2(board, current_position)
    elif current_direction[1] == -1:
        return move_left2(board, current_position)
    else:
        print("Can not determine where to step")
        raise

def move_forward2(board, current_position, current_direction, num_steps):
    prev_row, prev_column = current_position
    new_row, new_column = current_position
    new_direction = current_direction
    prev_direction = current_direction
    for step in range(num_steps):
        (new_row, new_column), new_direction = move_step2(board, (prev_row, prev_column), prev_direction)
        # Check collision
        assert board[new_row].start <= new_column <= board[new_row].end
        if new_column in board[new_row].walls:
            new_row, new_column = prev_row, prev_column
            new_direction = prev_direction
            break
        else:
            prev_row = new_row
            prev_column = new_column
            prev_direction = new_direction

    return (new_row, new_column), new_direction


def sim2(board, instructions):

    # rights
    current_position = (0, 149)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 149
    assert pos[1] == 99
    assert dir == (0, -1)

    current_position = (49, 149)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 100
    assert pos[1] == 99
    assert dir == (0, -1)

    current_position = (50, 99)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 49
    assert pos[1] == 100
    assert  dir == (-1, 0)


    current_position = (99, 99)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 49
    assert pos[1] == 149
    assert dir == (-1, 0)

    current_position = (100, 99)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 49
    assert pos[1] == 149
    assert dir == (0, -1)

    current_position = (149, 99)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 0
    assert pos[1] == 149
    assert dir == (0, -1)

    current_position = (150, 49)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 149
    assert pos[1] == 50
    assert dir == (-1, 0)

    current_position = (199, 49)
    pos, dir = move_right2(board, current_position)
    assert pos[0] == 149
    assert pos[1] == 99
    assert dir == (-1, 0)

    ## lefts

    current_position = (0, 50)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 149
    assert pos[1] == 0
    assert dir == (0, 1)

    current_position = (49, 50)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 100
    assert pos[1] == 0
    assert dir == (0, 1)

    current_position = (50, 50)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 100
    assert pos[1] == 0
    assert dir == (1, 0)

    current_position = (99, 50)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 100
    assert pos[1] == 49
    assert dir == (1, 0)

    current_position = (100, 0)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 49
    assert pos[1] == 50
    assert dir == (0, 1)

    current_position = (149, 0)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 0
    assert pos[1] == 50
    assert dir == (0, 1)

    current_position = (150, 0)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 0
    assert pos[1] == 50
    assert dir == (1, 0)

    current_position = (199, 0)
    pos, dir = move_left2(board, current_position)
    assert pos[0] == 0
    assert pos[1] == 99
    assert dir == (1, 0)


    ## going down
    current_position = (49, 99) # happy path
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 50
    assert pos[1] == 99
    assert dir == (1, 0)

    current_position = (49, 100)
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 50
    assert pos[1] == 99
    assert dir == (0, -1)

    current_position = (49, 149)
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 99
    assert pos[1] == 99
    assert dir == (0, -1)

    current_position = (149, 49) # happy path
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 150
    assert pos[1] == 49
    assert dir == (1, 0)

    current_position = (149, 50)
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 150
    assert pos[1] == 49
    assert dir == (0, -1)

    current_position = (149, 99)
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 199
    assert pos[1] == 49
    assert dir == (0, -1)

    current_position = (199, 0)
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 0
    assert pos[1] == 100
    assert dir == (1, 0)

    current_position = (199, 49)
    pos, dir = move_down2(board, current_position)
    assert pos[0] == 0
    assert pos[1] == 149
    assert dir == (1, 0)


    ## UPs
    current_position = (100, 0)
    pos, dir = move_up2(board, current_position)
    assert pos[0] == 50
    assert pos[1] == 50
    assert dir == (0, 1)


    current_position = (100, 49)
    pos, dir = move_up2(board, current_position)
    assert pos[0] == 99
    assert pos[1] == 50
    assert dir == (0, 1)


    current_position = (0, 50)
    pos, dir = move_up2(board, current_position)
    assert pos[0] == 150
    assert pos[1] == 0
    assert dir == (0, 1)

    current_position = (0, 99)
    pos, dir = move_up2(board, current_position)
    assert pos[0] == 199
    assert pos[1] == 0
    assert dir == (0, 1)

    current_position = (0, 100)
    pos, dir = move_up2(board, current_position)
    assert pos[0] == 199
    assert pos[1] == 0
    assert dir == (-1, 0)

    current_position = (0, 149)
    pos, dir = move_up2(board, current_position)
    assert pos[0] == 199
    assert pos[1] == 49
    assert dir == (-1, 0)


    current_position = (0, board[0].start)
    current_direction = (0, 1)

    for steps, turn in instructions:
        current_position, current_direction = move_forward2(board, current_position, current_direction, steps)
        assert board[current_position[0]].start <= current_position[1] <= board[current_position[0]].end
        current_direction = turn_left_or_right(turn, current_direction)

    row_points = 1000 * (current_position[0] + 1)
    column_points = 4 * (current_position[1] + 1)
    rotation_points = rotation_score[current_direction]
    return rotation_points + row_points + column_points

def create_board(rows):
    grid = []
    start = None
    for row in rows:
        blockers = []
        first = True
        for i, char in enumerate(row):
            if not char == ' ' and first:
                first = False
                start = i
            if char == '#':
                blockers.append(i)

        end = len(row) - 1
        row_len = (end - start + 1)
        grid.append(Row(start, end, row_len, tuple(blockers)))
    return grid

def read_input(file: str):

    with open(file, "r") as f:
        rows = f.readlines()
        return [re.sub("\n", '', line) for line in rows]



def solution1(file: str) -> int:
    lines = read_input(file)
    directions = lines[-1]
    board = lines[0:-2]
    board = create_board(board)

    instruction_list = re.split("(R|L)", directions)
    steps = [int(x) for x in instruction_list if not x == 'R' and not x == 'L']
    turns = [x for x in instruction_list if x == 'R' or x == 'L'] + [None]
    directions = list(zip(steps, turns))

    return sim(board, directions)





def solution2(file: str) -> int:
    lines = read_input(file)
    directions = lines[-1]
    board = lines[0:-2]
    board = create_board(board)

    instruction_list = re.split("(R|L)", directions)
    steps = [int(x) for x in instruction_list if not x == 'R' and not x == 'L']
    turns = [x for x in instruction_list if x == 'R' or x == 'L'] + [None]
    directions = list(zip(steps, turns))

    return sim2(board, directions)


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    # ans = solution2("example.txt")
    # print(f"Solution 2 for Example is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()

