
def find_end_of_distinct(line, num_distinct):
    for i in range(0, len(line)-num_distinct):
        if len(set(line[i:i+num_distinct])) == num_distinct:
            return i + num_distinct
    return 0 # Did not find anything. Sad day :(


def find_start_of_packet(line):
    return find_end_of_distinct(line, 4)


def find_start_of_message(line):
    return find_end_of_distinct(line, 14)


def solution_to_each_line(file, start_of):
    with open(file) as f:
        return [start_of(line) for line in f]


def solution1(file):
    return solution_to_each_line(file, find_start_of_packet)


def solution2(file):
    return solution_to_each_line(file, find_start_of_message)


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Input is: {ans}")


if __name__ == "__main__":
    main()
