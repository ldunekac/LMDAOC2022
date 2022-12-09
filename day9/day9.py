from typing import Generator
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    x: int = 0
    y: int = 0

    @staticmethod
    def add(coordinate1, coordinate2):
        return Coordinate(
            coordinate1.x + coordinate2.x,
            coordinate1.y + coordinate2.y
        )

    @staticmethod
    def subtract(coordinate1, coordinate2):
        return Coordinate(
            coordinate1.x - coordinate2.x,
            coordinate1.y - coordinate2.y
        )

class Rope:

    def __init__(self, rope_length: int):
        self.rope:list = [Coordinate() for _ in range(rope_length)]
        self.coordinates_that_the_tail_has_touched: set = {self.rope[-1]} # Fist position of the tail

    def move(self, direction: Coordinate):
        """
        :param direction:   One-step Coordinate: (1,0), (-1,0), (0,1), or (0,-1).
                            This is not checked because AoC (not production code)
        :return:
        """
        self.rope[0] = Coordinate.add(self.rope[0], direction)
        for i in range(1, len(self.rope)):
            self.rope[i] = Rope.update_tail(self.rope[i-1], self.rope[i])
        self.add_tail_coordinate_to_coordinates_seen()

    def add_tail_coordinate_to_coordinates_seen(self):
        self.coordinates_that_the_tail_has_touched.add(self.rope[-1])

    def count_num_coordinates_that_the_tail_has_touched(self) -> int:
        return len(self.coordinates_that_the_tail_has_touched)

    @staticmethod
    def change_distance_by(amount: int) -> int:
        if amount == 0:
            return 0
        elif amount > 0:
            return 1
        else: # amount < 0
            return -1

    @staticmethod
    def update_tail(head: Coordinate, tail: Coordinate) -> Coordinate:
        difference = Coordinate.subtract(head, tail)
        if abs(difference.x) > 1 or abs(difference.y) > 1:
            return Coordinate.add(
                tail,
                Coordinate(
                    Rope.change_distance_by(difference.x),
                    Rope.change_distance_by(difference.y)
                )
            )
        else:
            return tail


def parse_line(text: str) -> Generator:
    direction_map = {
        "R": Coordinate(1, 0), # X, Y
        "L": Coordinate(-1, 0),
        "U": Coordinate(0, 1),
        "D": Coordinate(0, -1),
    }
    direction, count = text.strip().split(" ")
    for i in range(int(count)):
        yield direction_map[direction]


def read_input(file: str) -> Generator:
    with open(file, "r") as f:
        for line in f:
            yield line


def solution(file: str, tail_length: int) -> int:
    rope = Rope(tail_length)
    for line in read_input(file):
        for command in parse_line(line):
            rope.move(command)
    return rope.count_num_coordinates_that_the_tail_has_touched()


def solution1(file:str) -> int:
    return solution(file, 2)


def solution2(file: str) -> int:
    return solution(file, 10)


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
