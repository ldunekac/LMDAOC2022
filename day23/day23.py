

def calculate_total_area(elves):
    min_row = min(row for row, _ in elves)
    max_row = max(row for row, _ in elves)
    min_col = min(col for _, col in elves)
    max_col = max(col for _, col in elves)
    return (max_row - min_row + 1) * (max_col - min_col + 1) - len(elves)

def print_elves(elves):
    min_row = min(row for row, _ in elves)
    max_row = max(row for row, _ in elves)
    min_col = min(col for _, col in elves)
    max_col = max(col for _, col in elves)

    for col in range(min_col, max_col + 1):
        print(col, end='')
    print()
    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):
            if (row, col) in elves:
                print("#", end='')
            else:
                print('.', end='')
        print(row, flush=True)

def sim_count(elves):
    num_elves = len(elves)
    location_check = [
        ((-1, -1), (-1, 0), (-1, 1)), # north
        ((1, -1), (1, 0), (1, 1)), # south
        ((1, -1), (0, -1), (-1, -1)), # west
        ((1, 1), (0, 1), (-1, 1)), # east
    ]

    i = 0
    old_locs = elves[:]
    while True:
        i += 1
        new_loc = take_step(old_locs, location_check)
        location_check.append(location_check.pop(0))
        same = True
        for j in range(num_elves):
            if not new_loc[j] == old_locs[j]:
                same = False
                break
        if same:
            return i
        else:
            old_locs = new_loc

def sim(elves):
    location_check = [
        ((-1, -1), (-1, 0), (-1, 1)), # north
        ((1, -1), (1, 0), (1, 1)), # south
        ((1, -1), (0, -1), (-1, -1)), # west
        ((1, 1), (0, 1), (-1, 1)), # east
    ]

    for ind in range(10):
        elves = take_step(elves, location_check)
        location_check.append(location_check.pop(0))
        # print_elves(elves)
        # print("-------------------------")
    return elves

def take_step(elves, location_check):
    purpose_directions = []
    all_elves_location = set(elves)

    for elf in elves:
        total_elves_in_spot = 0
        new_direction = None
        for direction in location_check:
            check_locations = [(elf[0] + row, elf[1] + col) for row, col in direction]
            found = sum(1 for loc in check_locations if loc in all_elves_location)
            total_elves_in_spot += found
            if found == 0 and new_direction is None:
                new_direction = direction[1]
                elf_location = (elf[0] + direction[1][0], elf[1] + direction[1][1])
                purpose_directions.append(elf_location)
        if total_elves_in_spot == 0 and not new_direction is None: # found a position to move but no one is around so don't move
            purpose_directions[-1] = elf
        elif total_elves_in_spot > 0 and new_direction is None: # could not find a position to move
            purpose_directions.append(elf)

    # find duplicates
    new_positions = set()
    duplicate_moves = set()
    for elf in purpose_directions:
        if elf in new_positions:
            duplicate_moves.add(elf)
        else:
            new_positions.add(elf)

    new_elf_positions = []
    for i in range(len(elves)):
        if purpose_directions[i] not in duplicate_moves:
            new_elf_positions.append(purpose_directions[i])
        else:
            new_elf_positions.append(elves[i])

    return new_elf_positions

def read_input(file: str):
    elf_locations = []
    with open(file, "r") as f:
        for row, line in enumerate(f):
            for column, char in enumerate(line):
                if char == '#':
                    elf_locations.append((row, column))
    return elf_locations

def solution1(file: str) -> int:
    elves = read_input(file)
    elves = sim(elves)
    return calculate_total_area(elves)


def solution2(file: str) -> int:
    elves = read_input(file)
    return sim_count(elves)

def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("example2.txt")
    print(f"Solution 1 for Example 2 is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example2.txt")
    print(f"Solution 2 for Example 2 is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()

