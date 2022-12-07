import re 

class Directory():

    def __init__(self, name):
        self.name = name
        self.sub_dirs = []
        self.files = []
        self.file_size = []

    def cd(self, dir_name):
        for sd in self.sub_dirs:
            if sd.name == dir_name:
                return sd
        raise Exception("No such sub directory")

    def add_sub_directory(self, name):
        self.sub_dirs.append(Directory(name))

    def add_file(self, name, size):
        self.files.append(name)
        self.file_size.append(size)

    def print(self, tab:int =0):
        tabs = "\t" * tab
        print(f"{tabs}-{self.name}")
        for sd in self.sub_dirs:
            sd.print(tab+1)
        for i in range(len(self.files)):
            print(f"{tabs}{self.file_size[i]} : {self.files[i]}")

    def get_size(self):
        return sum(self.file_size) + sum([sd.get_size() for sd in self.sub_dirs])


def read_input(file):
    dirs = Directory("/")
    current_working_dir = dirs
    path = []
    with open(file) as f:
        for line in f:
            if line[0] == "$":
                command_str = re.split(" ", line)
                if command_str[1] == "cd":
                    name = command_str[2].strip()
                    if name == "..":
                        current_working_dir = path.pop()
                    elif not name == "/":
                        path.append(current_working_dir)
                        current_working_dir = current_working_dir.cd(name)
            else: # Listing dir
                left, right = line.split(" ")
                left = left.strip()
                right = right.strip()
                if left == "dir":
                    current_working_dir.add_sub_directory(right)
                else:
                    current_working_dir.add_file(right, int(left))
    return dirs


def solution1(file):
    dirs = read_input(file)
    stack = [dirs]
    dirs_at_most_100000 = []
    while len(stack) > 0:
        current_dir = stack.pop()
        dir_size = current_dir.get_size()
        if dir_size < 100000:
            # print(f"Dir {current_dir.name} of size {dir_size} is added")
            dirs_at_most_100000.append(dir_size)
        for sd in current_dir.sub_dirs:
            stack.append(sd)
    return sum(dirs_at_most_100000)


def solution2(file):
    dirs = read_input(file)
    total_disk_space = 70000000
    free_space_needed_for_update = 30000000
    total_disk_usage = dirs.get_size()
    free_space_left = total_disk_space - total_disk_usage
    amount_of_clean_up_needed = free_space_needed_for_update - free_space_left
    
    stack = [dirs]
    file_sizes = []
    while len(stack) > 0:
        current_dir = stack.pop()
        dir_size = current_dir.get_size()
        if dir_size > amount_of_clean_up_needed:
            file_sizes.append(dir_size)
        for sd in current_dir.sub_dirs:
            stack.append(sd)
    return min(file_sizes)


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
