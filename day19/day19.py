import re
from dataclasses import dataclass, field
import queue


@dataclass(frozen=True)
class BluePrint:
    ore_machine_cost: int
    clay_machine_cost: int
    obsidian_machine_cost: tuple
    geod_machine_cost: tuple

@dataclass(frozen=True, order=True)
class State:
    turns_to_go:int
    geod: int
    obsidian: int
    clay: int
    ore: int
    geodM: int
    obsidianM: int
    clayM: int
    oreM: int



def calculate_godes_produced(blue_print: BluePrint, total_time = 24) -> int:

    print(blue_print)
    first = State(total_time, 0, 0, 0, 0, 0, 0, 0, 1) # one ore machine to start
    best = first
    pq = queue.Queue()
    pq.put(first)

    max_geod_count = 0
    seen = set()
    iter = 0

    max_ore_cost = max([blue_print.ore_machine_cost,
                        blue_print.clay_machine_cost,
                        blue_print.obsidian_machine_cost[0],
                        blue_print.geod_machine_cost[0]])


    while True:
        if pq.empty():
            break

        nstate = pq.get()

        iter += 1
        if iter % 1000000 == 0:
            # print(nstate)
            print(pq.qsize())

        # Total resource_count
        num_ore_robots = min(nstate.oreM, max_ore_cost)
        num_clay_robots = min(nstate.clayM, blue_print.obsidian_machine_cost[1])
        num_obsidian_robots = min(nstate.obsidianM, blue_print.geod_machine_cost[1])

        max_ore = min(nstate.ore,  nstate.turns_to_go * max_ore_cost - nstate.oreM * (nstate.turns_to_go - 1))
        max_clay = min(nstate.clay, (nstate.turns_to_go * blue_print.obsidian_machine_cost[1]) - nstate.clayM * (nstate.turns_to_go -1))
        max_obsidian = min(nstate.obsidian, (nstate.turns_to_go * blue_print.geod_machine_cost[1]) - nstate.obsidianM * (nstate.turns_to_go -1))

        nstate = State(
            nstate.turns_to_go,
            nstate.geod,
            max_obsidian,
            max_clay,
            max_ore,
            nstate.geodM,
            num_obsidian_robots,
            num_clay_robots,
            num_ore_robots)

        if nstate in seen:
            continue
        seen.add(nstate)

        # print()
        # print()
        # print(nstate)
        if nstate.turns_to_go == 0:
            if nstate.geod > max_geod_count:
                best = nstate
                # print(best)
                print(f"Max so far {nstate.geod}")
                max_geod_count = max([max_geod_count, nstate.geod])
            continue



        next_state = State(
            nstate.turns_to_go - 1,
            nstate.geod + nstate.geodM,
            max_obsidian + num_obsidian_robots,
            max_clay + num_clay_robots,
            max_ore + num_ore_robots,
            nstate.geodM,
            num_obsidian_robots,
            num_clay_robots,
            num_ore_robots)
        pq.put(next_state)

        # print("New States:")
        # print(f"{next_state}")

        if max_ore >= blue_print.geod_machine_cost[0] and max_obsidian >= blue_print.geod_machine_cost[1]:
            # print("have geod")
            next_state = State(
                nstate.turns_to_go - 1,
                nstate.geod + nstate.geodM,
                max_obsidian + num_obsidian_robots - blue_print.geod_machine_cost[1],
                nstate.clay + num_clay_robots,
                max_ore + num_ore_robots - blue_print.geod_machine_cost[0],
                nstate.geodM + 1,
                num_obsidian_robots,
                num_clay_robots,
                num_ore_robots)
            # print(next_state)
            pq.put(next_state)

        if max_ore >= blue_print.obsidian_machine_cost[0] and max_clay >= blue_print.obsidian_machine_cost[1]:
            # print("Boughts obsidian")
            new_state = State(
                nstate.turns_to_go - 1,
                nstate.geod + nstate.geodM,
                max_obsidian + num_obsidian_robots,
                max_clay + num_clay_robots- blue_print.obsidian_machine_cost[1],
                max_ore + num_ore_robots- blue_print.obsidian_machine_cost[0],
                nstate.geodM,
                num_obsidian_robots + 1,
                num_clay_robots,
                num_ore_robots)
            # print(new_state)
            pq.put(new_state)

        if max_ore >= blue_print.clay_machine_cost:
            # print("buying clay")
            next_state = State(
                nstate.turns_to_go - 1,
                nstate.geod + nstate.geodM,
                max_obsidian + num_obsidian_robots,
                max_clay  + num_clay_robots,
                max_ore + num_ore_robots - blue_print.clay_machine_cost,
                nstate.geodM,
                num_obsidian_robots,
                num_clay_robots+ 1,
                num_ore_robots)
            # print(next_state)
            pq.put(next_state)

        if max_ore >= blue_print.ore_machine_cost:
            next_state = State(
                nstate.turns_to_go - 1,
                nstate.geod + nstate.geodM,
                max_obsidian + num_obsidian_robots,
                max_clay  + num_clay_robots,
                max_ore + num_ore_robots - blue_print.ore_machine_cost,
                nstate.geodM,
                num_obsidian_robots,
                num_clay_robots,
                num_ore_robots + 1)
            # print(next_state)
            pq.put(next_state)

    print(best)
    return max_geod_count

def read_file(file: str):
    blue_prints = []
    with open(file, "r") as f:
        for line in f:
            data = re.split("costs | ore| and | clay| obs", line)
            ore_robot_cost = int(data[2])
            clay_robot_cost = int(data[5])
            obsidian_robot_cost = int(data[8]), int(data[10])
            geod_robot_cost = int(data[12]), int(data[14])
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
    blue_prints = read_file(file)
    total = 0
    for i, blue_print in enumerate(blue_prints):
        geods_produce = calculate_godes_produced(blue_print, 24)
        quality = (i + 1) * geods_produce
        total += quality
        print(f"Index {i+1}, geods {geods_produce}, quality = {quality}")
    return total




def solution2(file: str) -> int:
    blue_prints = read_file(file)
    total = 1
    for i, blue_print in enumerate(blue_prints[:3]):
        geods_produce = calculate_godes_produced(blue_print, 32)
        print(geods_produce)
        total *= geods_produce
    return total

def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")
    #
    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()

