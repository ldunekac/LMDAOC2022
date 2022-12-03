


def getByThree (inputList):
    i = 0
    returnList = []
    for item in inputList:
        returnList.append(item.strip())
        if i == 2:
            yield tuple(returnList)
            returnList = list()
            i = 0
        else:
            i += 1

def solution1(file_name):
    theLIST = []
    with open(file_name)as f:
        for l in f:
            splitat = int(len(l.strip())/2)

            left = set(l.strip()[:splitat])
            right = set(l.strip()[splitat:])
            [theLIST.append(x) for x in left.intersection(right)]
    returnSum = 0
    for character in theLIST:
        ordVal = ord(character)
        if ordVal > 96:
            # lowercase
            ordVal -= 96
        else:
            # uppercase
            ordVal -= 38
        returnSum += ordVal

    return returnSum


def solution2(file_name):
    theLIST = []
    with open(file_name)as f:

        for a, b, c in getByThree(f.readlines()):
            theLIST.append(list(set(a).intersection(set(b)).intersection(set(c)))[0])

    returnSum = 0
    for character in theLIST:
        ordVal = ord(character)
        if ordVal > 96:
            # lowercase
            ordVal -= 96
        else:
            # uppercase
            ordVal -= 38
        returnSum += ordVal

    return returnSum


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


