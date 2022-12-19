import re
from dataclasses import dataclass

@dataclass
class BluePrint:
    ore: int
    clay: int
    obsidian: tuple
    geod: tuple

def read_file(file: str):
    blue_prints = []
    with open(file, "r") as f:
        for line in f:
            data = re.split("costs | ore| and | clay| obs", line)
            ore_robot_cost = int(data[2])
            clay_robot_cost = int(data[5])
            obsidian_robot_cost = int(data[8]), int(data[10])
            geod_robot_cost = int(data[12]), int(data[14])
            print(f"{ore_robot_cost=}, {clay_robot_cost=}, {obsidian_robot_cost=}, {geod_robot_cost=}")
            blue_prints.append(
                BluePrint(
                    ore_robot_cost,
                    clay_robot_cost,
                    obsidian_robot_cost,
                    geod_robot_cost
                )
            )
        return blue_prints
def solution1(file: str) -> int:
    return read_file(file)


def solution2(file: str) -> int:
    pass

def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    # ans = solution1("input.txt")
    # print(f"Solution 1 for Input is: {ans}")
    # #
    # ans = solution2("example.txt")
    # print(f"Solution 2 for Example is: {ans}")
    # ans = solution2("input.txt")
    # print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()

