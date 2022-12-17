import numpy as np
from dataclasses import dataclass
import time


@ dataclass
class Coord:
    x: int
    y: int


class Piece:

    def __init__(self, piece_coordinates, piece_type):
        self.piece_type = piece_type
        self.left_most_pos = min([coord.y for coord in piece_coordinates])
        self.right_most_pos = max([coord.y for coord in piece_coordinates])
        self.bottom_most_pos = min([coord.x for coord in piece_coordinates])
        self.top_most_pos = max([coord.x for coord in piece_coordinates])
        self.coordinates = piece_coordinates


class TowerSimulation:

    def __init__(self, num_of_falling_blocks, wind_currents):
        self.number_of_blocks_to_drop = num_of_falling_blocks
        max_block_height = 4
        self.tower_width = 7
        self.wind_currents = wind_currents
        self.tower_height = (num_of_falling_blocks + 1) * max_block_height
        self.current_tower_height = 0
        self.tower = np.zeros((self.tower_height, self.tower_width))
        self.pieces = [
            # (0,0) is on the left edge of the block
            Piece((Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3)), "horizontal line"),
            Piece((Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(-1, 1), Coord(0, 2)), "plus"),
            Piece((Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 2), Coord(2, 2)), "Left L"),
            Piece((Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)), "vertical line"),
            Piece((Coord(0, 0), Coord(0, 1), Coord(1, 0), Coord(1, 1)), "square")
        ]
        self.piece_stream = self.get_next_piece()
        self.wind_stream = self.get_next_wind()


    def get_next_wind(self):
        def wind_current_to_coord_offset(wind_direction):
            if wind_direction == "<":
                return -1
            elif wind_direction == ">":
                return  1
            else:
                print("DIES")
                print(wind_direction)
                raise
        wind_current_len = len(self.wind_currents)
        wind_index = 0
        while True:
            yield wind_current_to_coord_offset(self.wind_currents[wind_index])
            wind_index = (wind_index + 1) % wind_current_len


    def get_next_piece(self):
        piece_index = 0
        number_of_pieces = len(self.pieces)
        while True:
            yield self.pieces[piece_index]
            piece_index = (piece_index + 1) % number_of_pieces


    def move_piece_let_or_right(self, piece, piece_offset, wind_direction):
        piece_offset.y += wind_direction
        if 0 <= piece_offset.y + piece.left_most_pos and \
                piece_offset.y + piece.right_most_pos < self.tower_width and \
                not self.has_piece_collided_with_another(piece, piece_offset):
            return True
        else:
            # restore the piece offset
            piece_offset.y -= wind_direction
            return False


    def has_piece_collided_with_another(self, piece, piece_offset):
        piece_loc_in_tower = [Coord(piece_coord.x + piece_offset.x, piece_coord.y + piece_offset.y) for piece_coord
                              in piece.coordinates]
        for coord in piece_loc_in_tower:
            if not self.tower[coord.x][coord.y] == 0:
                return True
        return False


    def move_piece_down(self, piece, piece_offset):
        piece_offset.x -= 1 # move down
        piece_hit_ground = lambda x: x < 0
        if piece_hit_ground(piece_offset.x + piece.bottom_most_pos) or \
                self.has_piece_collided_with_another(piece, piece_offset):
            piece_offset.x += 1 # Could not move down so set offset back
            return False
        else:
            return True


    def drop_piece(self):
        next_piece = next(self.piece_stream)
        piece_start_y =  2
        piece_start_x = self.current_tower_height + 3
        num_times_the_wind_blows = 0
        # bottom left needs to be:
        #   2 spots right of the left wall
        #   the bottom need to be 3 squares above the current tower height
        piece_offset = Coord(piece_start_x - next_piece.bottom_most_pos,
                             piece_start_y - next_piece.left_most_pos)
        wind_direction = next(self.wind_stream)
        num_times_the_wind_blows += 1
        self.move_piece_let_or_right(next_piece, piece_offset, wind_direction)
        while True:
            if not self.move_piece_down(next_piece, piece_offset):
                break
            wind_direction = next(self.wind_stream)
            self.move_piece_let_or_right(next_piece, piece_offset, wind_direction)
            num_times_the_wind_blows += 1

        piece_loc_in_tower = [Coord(piece_coord.x + piece_offset.x, piece_coord.y + piece_offset.y) for piece_coord in next_piece.coordinates]
        for coord in piece_loc_in_tower:
            self.tower[coord.x][coord.y] = 1

        self.current_tower_height = max(self.current_tower_height, piece_offset.x + next_piece.top_most_pos + 1)
        return num_times_the_wind_blows, piece_offset.y

    def find_repeat(self):
        piece_dropping = -1
        num_peaces = len(self.pieces)
        len_of_wind_stream = len(self.wind_currents)
        current_wind_stream = -1
        loop_max =num_peaces * len_of_wind_stream

        wind_streams_seen = []
        offset_of_wind_stream = []
        tower_heights = []

        for i in range(self.number_of_blocks_to_drop): # max number of iterations
            wind, offset = self.drop_piece()
            current_wind_stream = (wind + current_wind_stream) % len_of_wind_stream
            piece_dropping = (piece_dropping + 1) % num_peaces

            if i % loop_max == 0:
                # Pattern is guaranteed to repeat every max loop
                # We just need to find a wind offset that we have seen before
                if current_wind_stream in wind_streams_seen:
                    ind = wind_streams_seen.index(current_wind_stream)
                    loop_amount = i - offset_of_wind_stream[ind]
                    tower_height_per_pattern = self.current_tower_height - tower_heights[ind]
                    iterations_completed = i + 1
                    return iterations_completed, loop_amount, tower_height_per_pattern
                else:
                    wind_streams_seen.append(current_wind_stream)
                    offset_of_wind_stream.append(i)
                    tower_heights.append(self.current_tower_height)


    def run(self, drop_n_blocks = None):
        num_to_drop = drop_n_blocks if drop_n_blocks else self.number_of_blocks_to_drop
        for i in range(num_to_drop):
            self.drop_piece()


    def print(self, file = None):
        rows = ["+-------+"]
        for i in range(self.current_tower_height + 1):
            row  = "|"
            for j in range(self.tower_width):
                if self.tower[i][j] == 0:
                    row += "."
                else:
                    row += "#"
            row += "|"
            rows.append(row)
        if file:
            with open(file, "w+") as f:
                for row in range(len(rows)-1, 0-1, -1):
                    f.write(rows[row])
                    f.write("\n")
        else:
            for row in range(len(rows) - 1, 0 - 1, -1):
                print(rows[row])


def read_input(file):
    with open(file, "r") as f:
        return f.readline().strip()


def solution1(file: str, out_file) -> int:
    sim = TowerSimulation(2022, read_input(file))
    sim.run()
    sim.print(out_file)
    return sim.current_tower_height


def solution2(file: str) -> int:
    total_sim_iterations = 1000000000000
    lets_hope_this_is_a_tall_enough_tower = 100_000_000 # Computer can't allocate anything much bigger :)
    sim = TowerSimulation(lets_hope_this_is_a_tall_enough_tower, read_input(file))
    iterations_completed, num_blocks_per_repeat, height_per_repeat = sim.find_repeat()

    iterations_to_go = total_sim_iterations - iterations_completed
    number_of_skips = (iterations_to_go // num_blocks_per_repeat)
    remaining_iterations_after_skip = iterations_to_go % num_blocks_per_repeat
    print(f"{sim.current_tower_height=}, {sim.tower_height}")
    print(f"{iterations_completed=}, {remaining_iterations_after_skip=}, {number_of_skips=}, {num_blocks_per_repeat=}")
    sim.run(remaining_iterations_after_skip) # subtract 1 to
    print(f"{sim.current_tower_height=}")
    return sim.current_tower_height + (number_of_skips * height_per_repeat)


def main():
    ans = solution1("example.txt", "day_1_example_out.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt", "day_1_input_out.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    start = time.perf_counter()
    ans = solution2("input.txt")
    end = time.perf_counter()
    print(f"Solution 2 for Input is: {ans}")
    print(f"Elapsed Time {end - start}")


if __name__ == "__main__":
    main()

