from dataclasses import dataclass
from enum import Enum
from re import split as re_split
from typing import Generator, Optional


class InstructionType(Enum):
    ADDX = "addx"
    NOOP = "noop"


@dataclass(frozen=True)
class Instruction:
    instruction_type: InstructionType
    num_cycles_to_complete: int
    value: Optional[int]


class Computer:

    def __init__(self):
        self.current_cycle = 1
        self.registerX = 1
        self.signal_strengths = []
        self.computer_screen = []


    def add_row_to_screen(self, row: int):
        if len(self.computer_screen) - 1 < row:
            self.computer_screen.append("")


    def draw_pixel(self):
        row = (self.current_cycle - 1) // 40
        column = (self.current_cycle - 1) % 40
        self.add_row_to_screen(row)
        if self.registerX - 1 <= column <= self.registerX + 1:
            self.computer_screen[row] += "#"
        else:
            self.computer_screen[row] += "."


    def add_signal_strengths(self):
        if self.current_cycle % 40 == 20:
            self.signal_strengths.append(self.current_cycle * self.registerX)


    def process_instruction(self, instruction: Instruction):
        for _ in range(instruction.num_cycles_to_complete):
            self.draw_pixel()
            self.add_signal_strengths()
            self.current_cycle += 1

        if instruction.instruction_type == InstructionType.ADDX:
            self.registerX += instruction.value


    def print_signal_strengths(self):
        print(self.signal_strengths)


    def sum_of_signal_strengths(self) -> int:
        return sum(self.signal_strengths)


    def get_screen_display(self) -> str:
        return "\n".join(self.computer_screen)


def create_instruction(line: str) -> Instruction:
    instructions = re_split(' ', line)
    instruction_tye = instructions[0].strip()
    if instruction_tye == InstructionType.ADDX.value:
        return Instruction(InstructionType.ADDX, 2, int(instructions[1].strip()))
    else:
        return Instruction(InstructionType.NOOP, 1, None)


def read_input(file: str) -> Generator:
    with open(file, "r") as f:
        for line in f:
            yield create_instruction(line)


def solution1(file: str) -> int:
    computer = Computer()
    for instruction in read_input(file):
        computer.process_instruction(instruction)
    return computer.sum_of_signal_strengths()


def solution2(file: str) -> str:
    computer = Computer()
    for instruction in read_input(file):
        computer.process_instruction(instruction)
    return computer.get_screen_display()


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: \n{ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Input is: \n{ans}")


if __name__ == "__main__":
    main()
