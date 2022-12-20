from copy import deepcopy


def unencrypt_file(encrypted_list):
    unencrypted_list = deepcopy(encrypted_list)
    encrypted_num_to_unencrpyted_location = [x for x in range(len(unencrypted_list))]

def read_input(file):
    with open(file, "r") as f:
        return [int(line.strip()) for line in f.readlines()]

def solution1(file: str) -> int:
    unencrypted_file = unencrypt_file(read_input(file))



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

