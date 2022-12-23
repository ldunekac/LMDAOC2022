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












#### move right tests

    current_position = (0, 149)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].end == pos[1])

    current_position = (49, 149)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].end == pos[1])

    current_position = (49, 148)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].end == pos[1])

    current_position = (50, 99)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (99, 99)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (100, 99)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (149, 99)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (150, 49)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (199, 49)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)


    current_position = (190, 49)
    pos, dir = move_right2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)




##### move left test cases


    current_position = (0, 49)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])


    current_position = (49, 49)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])


    current_position = (50, 49)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (99, 49)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (100, 0)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (149, 0)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (150, 0)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (199, 0)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (199, 1)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

    current_position = (130, 55)
    pos, dir = move_left2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)
    print(board[pos[0]].start == pos[1])

##### move down test cases


    current_position = (49, 100)
    pos, dir = move_down2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (49, 149)
    pos, dir = move_down2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (49, 140)
    pos, dir = move_down2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (149, 50)
    pos, dir = move_down2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (149, 99)
    pos, dir = move_down2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (148, 98)
    pos, dir = move_down2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)



    #### move up test cases
    current_position = (0, 50)
    pos, dir = move_up2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (0, 99)
    pos, dir = move_up2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)


    current_position = (0, 100)
    pos, dir = move_up2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (0, 149)
    pos, dir = move_up2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (100, 49)
    pos, dir = move_up2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)

    current_position = (100, 0)
    pos, dir = move_up2(board, current_position)
    print(f"from={current_position}, to={pos}")
    print(dir)


