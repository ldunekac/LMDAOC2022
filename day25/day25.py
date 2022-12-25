

def snfu_to_dec(snfu):
    total = 0
    base = 1
    for i, char in enumerate(reversed(snfu)):
        if char == "-":
            char = -1
        elif char == "=":
            char = -2
        else:
            char = int(char)
        total += char * base
        base *= 5
    return total


def propgrate_snfu(snfu_number):
    
    for i in range(len(snfu_number)-1, -1, -1):
        if snfu_number[i] == 3:
            snfu_number[i-1] += 1
            snfu_number[i] = -2
        elif snfu_number[i] == 4:
            print("WWWWWWWWWW")
            snfu_number[i-1] += 1
            snfu_number[i] = -1


def dec_to_snfu(dec):
    base = 1
    snff_spots = 1
    while base < dec:
        base *= 5
        snff_spots +=1
    snfu_number = [0]

    for _ in range(snff_spots):
        times = dec // base
        dec -= (base * times)
        if base == 0:
            print("WATH")
            raise
        if times == 3:
            snfu_number[-1] += 1
            propgrate_snfu(snfu_number)
            snfu_number.append(-2)
        elif times == 4:
            snfu_number[-1] += 1
            propgrate_snfu(snfu_number)
            snfu_number.append(-1)
        elif times <= 2:
            snfu_number.append(times)
        base /= 5

    snfu_string = ""
    leading_zeros = True
    for num in snfu_number:
        if leading_zeros and num == 0:
            continue
        else:
            leading_zeros = False
        if num >= 0:
            snfu_string += str(int(num))
        elif num == -1:
            snfu_string += "-"
        elif num == -2:
            snfu_string += "="
    return snfu_string



def read_input(file):
    lines = []
    with open(file, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines

def solution1(file: str):
    snfu =read_input(file)
    base10nums = [snfu_to_dec(s) for s in snfu]
    total = sum(base10nums)
    snfu_num = dec_to_snfu(total)
    return snfu_num

def solution2(file: str) -> int:
    pass

def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")

    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    # NO part 2
    # ans = solution2("example.txt")
    # print(f"Solution 2 for Example is: {ans}")

    # ans = solution2("input.txt")
    # print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()
