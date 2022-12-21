from operator import add, sub, mul, truediv, floordiv, eq


char_to_op = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "=": eq,
    None: None
}

char_to_opposit_op = {
    "+": sub,
    "-": add,
    "*": truediv,
    "/": mul,
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
            return char_to_op[self.operation](self.left_monkey.get_number(), self.right_monkey.get_number())

    def get_left_number(self):
        return self.left_monkey.get_number()

    def get_right_number(self):
        return self.right_monkey.get_number()

    def is_humn_under_me(self):
        if self.name == "humn":
            return True
        elif not self.number is None:
            return False
        else:
            return self.left_monkey.is_humn_under_me() or self.right_monkey.is_humn_under_me()

    def is_humn_in_right(self):
        if self.name == "humn":
            return True
        elif not self.number is None:
            return False
        else:
            return self.right_monkey.is_humn_under_me()

    def calc_humn_val(self, current_val=None):
        if self.name == "humn":
            return current_val

        if current_val is None:
            if self.is_humn_in_right():
                target_val = self.left_monkey.get_left_number()
                return self.right_monkey.calc_humn_val(target_val)
            else:
                target_val = self.right_monkey.get_number()
                return self.left_monkey.calc_humn_val(target_val)
        else:
            if self.is_humn_in_right():
                # left = left_monkey
                # target = left op human
                if "+" == self.operation:
                    # target = left + humn
                    # humn = target - left
                    humn = current_val - self.left_monkey.get_number()
                    return self.right_monkey.calc_humn_val(humn)
                elif "-" == self.operation:
                    # target = left - humn
                    # humn = -(target - left)
                    humn = -1 * (current_val - self.left_monkey.get_number())
                    return self.right_monkey.calc_humn_val(humn)
                elif "*" == self.operation:
                    # target = left * humn
                    # humn = target/left
                    humn = current_val / self.left_monkey.get_number()
                    return self.right_monkey.calc_humn_val(humn)
                elif "/" == self.operation:
                    # target = left / humn
                    # humn = left / target
                    humn = self.left_monkey.get_number() / current_val
                    return self.right_monkey.calc_humn_val(humn)
                else:
                    print(self.name)
                    print(self.operation)
                    raise
            else: # humn in left
                # target = humn op right
                if "+" == self.operation:
                    # target = humn + right
                    # humn = target - right
                    humn = current_val - self.right_monkey.get_number()
                    return self.left_monkey.calc_humn_val(humn)
                elif "-" == self.operation:
                    # target = humn - right
                    # humn = target + right
                    humn = current_val + self.right_monkey.get_number()
                    return self.left_monkey.calc_humn_val(humn)
                elif "*" == self.operation:
                    # target = humn * right
                    # humn = target / right
                    humn = current_val / self.right_monkey.get_number()
                    return self.left_monkey.calc_humn_val(humn)
                elif "/" == self.operation:
                    # target = humn / right
                    # humn = target * right
                    humn = current_val * self.right_monkey.get_number()
                    return self.left_monkey.calc_humn_val(humn)
                else:
                    print(self.name)
                    print(self.operation)
                    raise

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
                
            monkey_dict[name] = Monkey(name, number, operation, left_monkey_name, right_monkey_name)

    for key, monkey in monkey_dict.items():
        if not monkey.number:
            monkey.add_left_monkey(monkey_dict[monkey.left_monkey_name])
            monkey.add_right_monkey(monkey_dict[monkey.right_monkey_name])
            
    return monkey_dict["root"], monkey_dict["humn"]


def solution1(file: str) -> int:
    root, _ = read_input(file)
    return int(root.get_number())



def solution2(file: str) -> int:
    # humn only shows up one in the operations
    root, humn = read_input(file)
    return int(root.calc_humn_val())


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")
    
    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")
    ans = solution2("input.txt")
    print(f"Solution 2 for Example is: {ans}")


if __name__ == "__main__":
    main()

