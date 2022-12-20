from copy import deepcopy


def unencrypt_file(encrypted_list):
    list_len = len(encrypted_list)
    unencrypted_list = deepcopy(encrypted_list)
    # The index of mapping aligns with the index of encrypted_list
    # The value of mapping, is the index in the unencrypted list 
    # E.g. If encrypted_list[4] = -3
    # and if unencrypeted_list[7] = -3
    # Then the mapping[4] = 7. 
    # We can say that encrypted_list[4] = unencrypeted_list[mapping[4]]
    mapping = [x for x in range(len(unencrypted_list))]

    for ind, num in enumerate(encrypted_list):
        print("Current array status")
        print(encrypted_list)
        print(mapping)
        print(unencrypted_list)
        
        num_idx_in_unencrypted_list = mapping[ind]
        assert num == unencrypted_list[num_idx_in_unencrypted_list]

        new_index = (num_idx_in_unencrypted_list + num) % list_len
        
        if new_index > num_idx_in_unencrypted_list:
            # update the unencrypted map
            for i in range(num_idx_in_unencrypted_list, new_index):
                print(i)
                unencrypted_list[i] = unencrypted_list[i + 1]
            unencrypted_list[new_index] = num
            # move the number in the unencryped list to the right
            # all values in between get shifted one index down ( -1)
            for i in range(list_len):
                if num_idx_in_unencrypted_list <= mapping[i] <= new_index:
                    mapping[i] -= 1
            
            mapping[ind] = new_index 
            for idx2, num2 in enumerate(encrypted_list):
                assert num2 == unencrypted_list[mapping[idx2]]
        else:
            print("not yet")
            raise
        


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

