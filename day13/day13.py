from functools import cmp_to_key

def get_all_lists(file: str):
    full_list = []
    with open(file, "r") as f:
        for line in f:
            if line.strip():
                full_list.append(eval(line))
    return full_list


def get_pairs(file: str):
    with open(file, "r") as f:
        while True:
            packet1 = f.readline().strip()
            if not packet1:
                break
            packet2 = f.readline().strip()
            yield eval(packet1), eval(packet2)
            f.readline()
        

def are_packets_in_order(packet1, packet2):
    if isinstance(packet1, list) and isinstance(packet2, int):
        packet2 = [packet2]
    elif isinstance(packet1, int) and isinstance(packet2, list):
        packet1 = [packet1]
    if isinstance(packet1, list) and isinstance(packet2, list):
        for left, right in zip(packet1, packet2):
            ans = are_packets_in_order(left, right)
            if ans == 0:
                continue
            else:
                return ans
        return len(packet1) - len(packet2)
    elif isinstance(packet1, int) and isinstance(packet2, int):
        return packet1 - packet2
    else:
        print("EXPLODE")

def solution1(file: str) -> int:
    correct_ordered_packets = []
    for index, (packet1, packet2) in enumerate(get_pairs(file)):
        if are_packets_in_order(packet1, packet2) <= 0:
            correct_ordered_packets.append(index + 1)
    return sum(correct_ordered_packets)

def solution2(file: str) -> int:
    all_lists = get_all_lists(file)
    all_lists.append([[2]])
    all_lists.append([[6]])
    sorted_lists = sorted(all_lists, key=cmp_to_key(are_packets_in_order))
    start_key = 0
    end_key = 0
    for index, s in enumerate(sorted_lists):
        if s == [[2]]:
            start_key = index + 1
        if s == [[6]]:
            end_key = index + 1
    return start_key * end_key
            

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
