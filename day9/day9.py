from typing import Tuple, List
from operator import add, sub

class Rope:

    def __init__(self, rope_length):
        self.rope_length: int = rope_length
        self.rope:List = [tuple([0,0]) for _ in range(rope_length)]
        self.tail_locations: set = set()
        self.tail_locations.add(self.rope[-1])

    def move(self, direction: Tuple[int, int]):
        self.rope[0] = tuple(map(add, self.rope[0], direction))
        for i in range(1, self.rope_length):
            self.rope[i] = Rope._update_tail(self.rope[i-1], self.rope[i])
        self._store_path(self.rope[-1])

    def _store_path(self, new_tail_location):
        self.tail_locations.add(new_tail_location)

    def count_num_spaces_that_the_tail_touched(self):
        return len(self.tail_locations)

    @staticmethod
    def _change_distance_by(amount):
        if amount == 0:
            return 0
        elif amount > 0:
            return 1
        else: # amount < 0
            return -1

    @staticmethod
    def _update_tail(head, tail):
        difference = tuple(map(sub, head, tail))
        if abs(difference[0]) > 1 or abs(difference[1]) > 1:
            return tuple(map(add, tail, (
                Rope._change_distance_by(difference[0]),
                Rope._change_distance_by(difference[1]),
            )))
        return tail


def parse_line(text):
    direction_map = {
        "R": (1, 0), # X, Y
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    direction, count = text.strip().split(" ")
    for i in range(int(count)):
        yield direction_map[direction]


def read_input(file):
    with open(file, "r") as f:
        for line in f:
            yield line


def solution1(file):
    rope = Rope(2)
    for line in read_input(file):
        for command in parse_line(line):
            rope.move(command)
    return rope.count_num_spaces_that_the_tail_touched()


def solution2(file):
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
