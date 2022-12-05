import re

class ContainerYard():

    def __init__(self, number_of_stacks: int) -> None:
        self.number_of_stacks = number_of_stacks
        self.yard = []
        for i in range(number_of_stacks):
            self.yard.append(list()) 

    def add_crate(self, crate_letter: str, stack_index: int)->None:
        self.yard[stack_index].append(crate_letter)

    def pop_top(self):
        for l in self.yard:
            l.pop()

    def reverse_crates(self) -> None:
        for i in range(self.number_of_stacks):
            self.yard[i] = self.yard[i][::-1]

    def move_crates_one_at_a_time(self, number_of_crates: int, from_stack: int, to_stack:int) -> None:
        for _ in range(number_of_crates):
            self.yard[to_stack].append(self.yard[from_stack].pop())

    def move_all_crates_at_once(self, number_of_crates: int, from_stack: int, to_stack:int) -> None:
        crates_being_moved = []
        for _ in range(number_of_crates):
            crates_being_moved.append(self.yard[from_stack].pop())
        self.yard[to_stack].extend(crates_being_moved[::-1])

    def get_top_crates(self) -> str:
        return "".join([stack[-1] for stack in self.yard])

    def print(self): # for sanity
        for i, stack in enumerate(self.yard):
            print(f"{i+1}: {stack}")

def unload_docker(open_file):
    yard = None
    first_line = True
    for line in open_file:
        if len(line.strip()) < 2: # The first blank line. Done creating stacks
            yard.pop_top() # Becuse the last line added where the row numbers and not letter crates
                           # I could of checked for the number row but lazy
            yard.reverse_crates() # Need to revers the order since we added top crates first
            break
        if first_line:
            first_line = False
            total_number_of_stacks = (len(line) + 1) // 4 # A defined 4 spaces per stack. Had to +1 since last stack is 3 spaces
            yard = ContainerYard(total_number_of_stacks)
        for stack_index in range(0, total_number_of_stacks):
            crate_letter = line[stack_index*4+1] 
            if not crate_letter == ' ':
                yard.add_crate(crate_letter, stack_index)
    return yard

def create_instruction_list(open_file):
    stack_commands = []
    for line in open_file:
        l = re.split("move|from|to", line)
        amount = int(l[1].strip())
        from_stack = int(l[2].strip()) - 1 # convert to zero based index
        to_stack = int(l[3].strip()) - 1
        stack_commands.append((amount, from_stack, to_stack))
    return stack_commands

def read_input(file_name: str):
    with open(file_name, "r") as f:
        yard = unload_docker(f)
        instruction_list = create_instruction_list(f)
        return (yard, instruction_list)

def solution1(file):
    yard, instruction_list = read_input(file)
    for num_stacks, from_stack, to_stack in instruction_list:
        yard.move_crates_one_at_a_time(num_stacks, from_stack, to_stack)
    return yard.get_top_crates()

def solution2(file):
    yard, instruction_list = read_input(file)
    for num_stacks, from_stack, to_stack in instruction_list:
        yard.move_all_crates_at_once(num_stacks, from_stack, to_stack)
    return yard.get_top_crates()

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

