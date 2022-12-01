
class ElfCalorieCount():

    def __init__(self):
        self.calorie_list = []

    def add_snack(self, calories):
        self.calorie_list.append(calories)

    def total_calorie_count(self):
        return sum(self.calorie_list)


def read_input(file_name):
    elfs_cal_count = []
    with open(file_name, "r") as f:
        elf = ElfCalorieCount()
        for line in f:
            if line.strip() == "":
                elfs_cal_count.append(elf)
                elf = ElfCalorieCount()
            else:
                elf.add_snack(int(line))
        elfs_cal_count.append(elf)
    return elfs_cal_count


def solution1(input_file):
    elves_calories = read_input(input_file)
    print(max(elf.total_calorie_count() for elf in elves_calories))


def solution2(input_file):
    elves_calories = read_input(input_file)
    counts = [elf.total_calorie_count() for elf in elves_calories]
    print(sum(sorted(counts,reverse=True)[:3]))

def main():
    solution1("example.txt")
    solution1("input.txt")
    
    solution2("example.txt")
    solution2("input.txt")


if __name__ == "__main__":
    main()