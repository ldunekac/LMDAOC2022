from typing import Generator
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    x: int = 0
    y: int = 0

    @staticmethod
    def add_positions(position1, position2):
        return Position(
            position1.x + position2.x,
            position1.y + position2.y
        )

    @staticmethod
    def difference(position1, position2):
        return Position(
            position1.x - position2.x,
            position1.y - position2.y
        )

class Rope:

    def __init__(self, rope_length: int):
        self.rope_length: int = rope_length
        self.rope:list = [Position() for _ in range(rope_length)]
        self.tail_locations: set = set()
        self.tail_locations.add(self.rope[-1])

    def move(self, direction: Position):
        self.rope[0] = Position.add_positions(self.rope[0], direction)
        for i in range(1, self.rope_length):
            self.rope[i] = Rope._update_tail(self.rope[i-1], self.rope[i])
        self._store_path(self.rope[-1])

    def _store_path(self, new_tail_location: Position):
        self.tail_locations.add(new_tail_location)

    def count_num_spaces_that_the_tail_touched(self) -> int:
        return len(self.tail_locations)

    @staticmethod
    def _change_distance_by(amount: int) -> int:
        if amount == 0:
            return 0
        elif amount > 0:
            return 1
        else: # amount < 0
            return -1

    @staticmethod
    def _update_tail(head: Position, tail: Position) -> Position:
        difference = Position.difference(head, tail)
        if abs(difference.x) > 1 or abs(difference.y) > 1:
            return Position.add_positions(
                tail,
                Position(
                    Rope._change_distance_by(difference.x),
                    Rope._change_distance_by(difference.y)
                )
            )
        else:
            return tail


def parse_line(text: str) -> Generator:
    direction_map = {
        "R": Position(1, 0), # X, Y
        "L": Position(-1, 0),
        "U": Position(0, 1),
        "D": Position(0, -1),
    }
    direction, count = text.strip().split(" ")
    for i in range(int(count)):
        yield direction_map[direction]


def read_input(file: str) -> Generator:
    with open(file, "r") as f:
        for line in f:
            yield line


def solution1(file:str) -> int:
    rope = Rope(2)
    for line in read_input(file):
        for command in parse_line(line):
            rope.move(command)
    return rope.count_num_spaces_that_the_tail_touched()


def solution2(file: str) -> int:
    rope = Rope(10)
    for line in read_input(file):
        for command in parse_line(line):
            rope.move(command)
    return rope.count_num_spaces_that_the_tail_touched()


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    ans = solution2("example2.txt")
    print(f"Solution 2 for Example2 is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Input is: {ans}")


if __name__ == "__main__":
    main()
