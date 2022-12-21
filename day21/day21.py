from operator import add, sub, mul, truediv, floordiv, eq


char_to_op = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": floordiv,
    "=": eq,
    None: None
}

class Monkey:

    def __init__(self, name, number, operation, left_monkey_name, right_monkey_name):
        self.name = name
        self.number = number
        self.left_monkey = None
        self.right_monkey = None
        self.left_monkey_name = left_monkey_name
        self.right_monkey_name = right_monkey_name
        self.operation = operation

    def add_left_monkey(self, monkey):
        self.left_monkey = monkey

    def add_right_monkey(self, monkey):
        self.right_monkey = monkey

    def get_number(self):
        if not self.number is None:
            return self.number
        else:
            return self.operation(self.left_monkey.get_number(), self.right_monkey.get_number())

    def get_left_number(self):
        return self.left_monkey.get_number()

    def get_right_number(self):
        return self.right_monkey.get_number()

def read_input(file):
    monkey_dict = {}
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            parts = line.split(" ")
            name = parts[0][:-1]

            number = None
            operation = None
            left_monkey_name = None
            right_monkey_name = None
            if len(parts) <= 2:
                number = int(parts[1])
            else:
                left_monkey_name = parts[1]
                operation = parts[2]
                right_monkey_name = parts[3]
                
            monkey_dict[name] = Monkey(name, number, char_to_op[operation], left_monkey_name, right_monkey_name)

    for key, monkey in monkey_dict.items():
        if not monkey.number:
            monkey.add_left_monkey(monkey_dict[monkey.left_monkey_name])
            monkey.add_right_monkey(monkey_dict[monkey.right_monkey_name])
            
    return monkey_dict["root"], monkey_dict["humn"]


def solution1(file: str) -> int:
    root, _ = read_input(file)
    return root.get_number()



def solution2(file: str) -> int:
    root, humn = read_input(file)
    root.operation = eq
    current_num = 1
    min_num = current_num
    max_num = current_num
    humn.number = current_num

    # right number does not depend on your input
    # find max
    # while True:
    #     current_num = 1
    #     min_num = current_num
    #     max_num = current_num
    #     humn.number = current_num
    #     left_num = root.get_left_number()
    #     right_num = root.get_right_number()
    #     if left_num > right_num
        

    # prev = 0
    # for i in range(100, 103):
    #     humn.number = i
    #     if root.get_number():
    #         return i
    #     else:
    #         left_num = root.get_left_number()
    #         print(prev - left_num)
    #         print(left_num, root.get_right_number())
    #         prev = left_num
    # return None


def main():
    # ans = solution1("example.txt")
    # print(f"Solution 1 for Example is: {ans}")
    # ans = solution1("input.txt")
    # print(f"Solution 1 for Input is: {ans}")
    # #
    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    # ans = solution2("input.txt")
    # print(f"Solution 2 for Example is: {ans}")

262412007595970
46779208742730
if __name__ == "__main__":
    main()

