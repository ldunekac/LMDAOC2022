from copy import deepcopy


def unencrypt_file(encrypted_list):
    unencrypted_list = deepcopy(encrypted_list)
    # The index of mapping aligns with the index of encrypted_list
    # The value of mapping, is the index in the unencrypted list 
    # E.g. If encrypted_list[4] = -3
    # and if unencrypeted_list[7] = -3
    # Then the mapping[4] = 7. 
    # We can say that encrypted_list[4] = unencrypeted_list[mapping[4]]
    mapping = [x for x in range(len(unencrypted_list))]

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

