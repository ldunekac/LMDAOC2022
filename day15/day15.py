import re
import time

def in_combined_ranges(ranges, val):
    for x0, x1 in ranges:
        if x0 <= val <= x1:
            return True
    return False

def get_num_positions_where_beacons_caonnot_exist(sensors, beacons, test_y):
    ranges = []
    for s, b in zip(sensors, beacons):
        steps_to_x = abs(s[0] - b[0])
        steps_to_y = abs(s[1] - b[1]) 
        total_distance = steps_to_x + steps_to_y
        
        dist_from_sensor_to_test_y = abs(s[1] - test_y)
        numer_of_spaces_to_go = total_distance - dist_from_sensor_to_test_y
        if numer_of_spaces_to_go > 0:
            ranges.append((s[0] - numer_of_spaces_to_go, s[0] + numer_of_spaces_to_go))

    ranges = sorted(ranges, key=lambda x: x[0])
    combined_ranges = []
    start_range = None 
    end_range = None
    for ind, r in enumerate(ranges):
        if ind == 0:
            start_range = r[0]
            end_range = r[1]
            continue
        if r[0] <= end_range:
            end_range = max(r[1], end_range)
        else:
            combined_ranges.append((start_range, end_range))
            start_range = r[0]
            end_range = r[1]
    combined_ranges.append((start_range, end_range))
    total_len = sum([x1 - x0 + 1 for x0, x1 in combined_ranges])
    for b in set(beacons):
        if b[1] == test_y:
            if in_combined_ranges(combined_ranges, b[0]):
                total_len -= 1
    return total_len


def parse_input(file):
    sensors = []
    beacons = []
    with open(file, "r") as f:
        for line in f:
            parts = re.split(" |=|,|:|\n", line)
            sensors.append((int(parts[3]), int(parts[6])))
            beacons.append((int(parts[13]), int(parts[16])))
    return sensors, beacons


def solution1(file: str, y_test) -> int:
    sensors, beacons = parse_input(file)    
    return get_num_positions_where_beacons_caonnot_exist(sensors, beacons, y_test)


def get_pos_where_beacon_caonnot_exist(sensors, beacons, test_y):
    ranges = []
    for s, b in zip(sensors, beacons):
        steps_to_x = abs(s[0] - b[0])
        steps_to_y = abs(s[1] - b[1]) 
        total_distance = steps_to_x + steps_to_y
        
        dist_from_sensor_to_test_y = abs(s[1] - test_y)
        numer_of_spaces_to_go = total_distance - dist_from_sensor_to_test_y
        if numer_of_spaces_to_go > 0:
            ranges.append((s[0] - numer_of_spaces_to_go, s[0] + numer_of_spaces_to_go))

    ranges = sorted(ranges, key=lambda x: x[0])
    combined_ranges = []
    start_range = None 
    end_range = None
    for ind, r in enumerate(ranges):
        if ind == 0:
            start_range = r[0]
            end_range = r[1]
            continue
        if r[0] - 1 <= end_range:
            end_range = max(r[1], end_range)
        else:
            combined_ranges.append((start_range, end_range))
            start_range = r[0]
            end_range = r[1]
    combined_ranges.append((start_range, end_range))
    return combined_ranges

def solution2(file: str, max_x) -> int:
    sensors, beacons = parse_input(file) 
    start = time.perf_counter()
    x = 0
    for i in range(max_x):
        ans = get_pos_where_beacon_caonnot_exist(sensors, beacons, i)
        if len(ans) == 2:
            x = ans[0][1] + 1 # unused x val
            break
    end = time.perf_counter()
    print(f"Elapsed time seconds: {end-start}")
    return x*4000000 + i


def main():
    ans = solution1("example.txt", 10)
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt", 2000000)
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt", 20)
    print(f"Solution 2 for Example is: {ans}")
    ans = solution2("input.txt", 4000000)
    print(f"Solution 2 for Input is: {ans}")


if __name__ == "__main__":
    main()
