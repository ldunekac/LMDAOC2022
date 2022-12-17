
import numpy as np
from dataclasses import dataclass

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
        self.tower_height = (num_of_falling_blocks + 5) * max_block_height
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
        # bottom left needs to be:
        #   2 spots right of the left wall
        #   the bottom need to be 3 squares above the current tower height
        piece_offset = Coord(piece_start_x - next_piece.bottom_most_pos,
                             piece_start_y - next_piece.left_most_pos)
        wind_direction = next(self.wind_stream)
        self.move_piece_let_or_right(next_piece, piece_offset, wind_direction)
        while True:

            if not self.move_piece_down(next_piece, piece_offset):
                break
            wind_direction = next(self.wind_stream)
            self.move_piece_let_or_right(next_piece, piece_offset, wind_direction)



        piece_loc_in_tower = [Coord(piece_coord.x + piece_offset.x, piece_coord.y + piece_offset.y) for piece_coord in next_piece.coordinates]
        for coord in piece_loc_in_tower:
            self.tower[coord.x][coord.y] = 1

        self.current_tower_height = max(self.current_tower_height, piece_offset.x + next_piece.top_most_pos + 1)

    def run(self):
        for i in range(self.number_of_blocks_to_drop):
            self.drop_piece()


    def print(self):
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

        for row in range(len(rows)-1, 0-1, -1):
            print(rows[row])


def read_input(file):
    with open(file, "r") as f:
        return f.readline().strip()



def solution1(file: str) -> int:
    sim = TowerSimulation(2022, read_input(file))
    sim.run()
    return sim.current_tower_height

def solution2(file: str) -> int:
    pass


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")
    #
    # ans = solution2("example.txt")
    # print(f"Solution 2 for Example is: {ans}")
    # ans = solution2("input.txt")
    # print(f"Solution 2 for Input is: {ans}")


if __name__ == "__main__":
    main()
