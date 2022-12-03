
# A = Rock
# B = Paper
# C = Scissors

# X = Rock
# Y = Paper
# Z = Scissors

# W = 6
# D = 3
# L = 0

# Rock = 1
# Paper = 2
# Scissors = 3

extensible = {
    "A X": 4, # 3 + 1
    "A Y": 8, # 6 + 2
    "A Z": 3, # 0 + 3
    "B X": 1, # 0 + 1
    "B Y": 5, # 3 + 2
    "B Z": 9, # 6 + 3
    "C X": 7, # 6 + 1
    "C Y": 2, # 0 + 2
    "C Z": 6, # 3 + 3
}

# A = Rock
# B = Paper
# C = Scissors

# X Lose
# Y Draw
# Z Win

# Rock = 1
# Paper = 2
# Scissors = 3

extensible2 = {
    "A X": 3, # 0 + 3
    "A Y": 4, # 3 + 1
    "A Z": 8, # 6 + 2
    "B X": 1, # 0 + 1
    "B Y": 5, # 3 + 2
    "B Z": 9, # 6 + 3
    "C X": 2, # 0 + 2
    "C Y": 6, # 3 + 3
    "C Z": 7, # 6 + 1
}


def solution1(file_name):
    with open(file_name)as f:
        return sum(
            extensible[l.strip()] for l in f
        )

def solution2(file_name):
    with open(file_name)as f:
        return sum(
            extensible2[l.strip()] for l in f
        )

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


