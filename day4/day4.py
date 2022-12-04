

def is_slacker(elf1, elf2):
    if elf1[0] >= elf2[0] and elf1[1] <= elf2[1]:
        return True
    elif elf2[0] >= elf1[0] and elf2[1] <= elf1[1]:
        return True
    else:
        return False

def is_some_what_of_a_slacker(elf1, elf2):
    if elf1[0] <= elf2[0] <= elf1[1]:
        return True
    elif elf2[0] <= elf1[0] <= elf2[1]:
        return True
    else:
        return False
            

def parse_line(line):
    left, right = tuple(line.strip().split(","))
    elf1 = tuple([int(x) for x in left.split("-")])
    elf2 = tuple([int(x) for x in right.split("-")])
    return (elf1, elf2)

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

