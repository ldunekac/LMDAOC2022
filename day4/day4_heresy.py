import re


def is_slacker(elf1, elf2):
    return  (elf1[0] >= elf2[0] and elf1[1] <= elf2[1]) or \
            (elf2[0] >= elf1[0] and elf2[1] <= elf1[1])


def is_some_what_of_a_slacker(elf1, elf2):
    return  (elf1[0] <= elf2[0] <= elf1[1]) or \
            (elf2[0] <= elf1[0] <= elf2[1])


def parse_line(line):
    vals = tuple(int(x) for x in re.split(',|-', line.strip()))
    return (vals[0], vals[1]), (vals[2], vals[3])


def read_input(file_name):
    with open(file_name, "r") as f:
        for line in f:
            yield parse_line(line) 


def solution1(file):
    return sum(is_slacker(elf1, elf2) for elf1, elf2 in read_input(file))


def solution2(file):
    return sum(is_some_what_of_a_slacker(elf1, elf2) for elf1, elf2 in read_input(file))


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
