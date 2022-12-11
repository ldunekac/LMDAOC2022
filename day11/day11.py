from collections.abc import Callable
from functools import reduce

class Monkey:

    def __init__(self, number: int, items: list, operation: Callable, test:int):
        self.number = number
        self.items = items
        self.operation = operation
        self.test = test
        self.true_monkey = None
        self.false_monkey = None
        self.total_inspected_items = 0

    def inspect_item(self):
        self.total_inspected_items += 1

    def add_item(self, item: int):
        self.items.append(item)

    def add_true_monkey(self, monkey):
        self.true_monkey = monkey

    def add_false_monkey(self, monkey):
        self.false_monkey = monkey

    def print(self):
        print(f"Monkey: {self.number}")
        print(self.items)
        print(self.operation)
        print(self.test)
        print(f"True Monkey: {self.true_monkey.number}")
        print(f"True Monkey: {self.false_monkey.number}")
        print(f"Inspected: {self.total_inspected_items}")


def pase_starting_items_string(line: str):
    item_string = line.split("items:")[1]
    return [int(item.strip()) for item in item_string.split(",")]


def pase_operation_string(line: str):
    op_map = {
        "*": lambda value: lambda x: x * value,
        "+": lambda value: lambda x: x + value,
        "*old": lambda x: x*x,
        "+old": lambda x: x+x
    }
    op_str = line.split("= old ")[-1].strip()
    op, val = op_str.split(" ")
    if val.strip() == "old":
        return op_map[op+val.strip()]
    else:
        return op_map[op](int(val))


def parse_test_condition(line: str):
    return int(line.split("by ")[-1].strip())


def get_monkey_to_throw_to(line: str):
    return int(line.split("monkey ")[-1].strip())


def create_monkey(monkey_number, monkey_lines):
    starting_items = pase_starting_items_string(monkey_lines[1])
    operation = pase_operation_string(monkey_lines[2])
    test = parse_test_condition(monkey_lines[3])
    true_monkey_index = get_monkey_to_throw_to(monkey_lines[4])
    false_monkey_index = get_monkey_to_throw_to(monkey_lines[5])
    return Monkey(monkey_number, starting_items, operation, test), true_monkey_index, false_monkey_index


def parse_input(file):
    monkey_list = []
    with open(file, "r") as f:
        lines = [line for line in f.read().split("\n") if line]

    for i in range(len(lines)//6):
        monkey_list.append(create_monkey(i, lines[i*6:i*6+6]))

    for monkey, true_index, false_index in monkey_list:
        monkey.add_true_monkey(monkey_list[true_index][0])
        monkey.add_false_monkey(monkey_list[false_index][0])

    return [monkey[0] for monkey in monkey_list]


def perform_round(monkey_list, sanity):
    common_denominator = reduce(lambda x,y: x*y, [monkey.test for monkey in monkey_list])
    for monkey in monkey_list:
        for item in monkey.items:
            monkey.inspect_item()
            new_worry_value = (monkey.operation(item) // sanity) % common_denominator
            if new_worry_value % monkey.test == 0:
                monkey.true_monkey.add_item(new_worry_value)
            else:
                monkey.false_monkey.add_item(new_worry_value)
            monkey.items = []


def solution1(file:str) -> int:
    monkeys = parse_input(file)
    for _ in range(20):
        perform_round(monkeys, sanity=3)
    return reduce(lambda x,y: x*y,
           sorted([monkey.total_inspected_items for monkey in monkeys], reverse=True)[:2])


def solution2(file: str) -> int:
    monkeys = parse_input(file)
    for _ in range(10000):
        perform_round(monkeys, sanity=1)
    return reduce(lambda x,y: x*y,
           sorted([monkey.total_inspected_items for monkey in monkeys], reverse=True)[:2])


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
