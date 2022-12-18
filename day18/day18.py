

def get_total_edges(cubes):
    outers = [
        ( 1,  0,  0),
        (-1,  0,  0),
        ( 0,  1,  0),
        ( 0, -1,  0),
        ( 0,  0,  1),
        ( 0,  0, -1),
    ]
    nodes = set(cubes)

    total_edges = 0
    for (x, y, z) in nodes:
        adj_nodes = [(x + x1, y + y1, z + z1) for x1, y1, z1 in outers]
        for adj_node in adj_nodes:
            if adj_node in nodes:
                total_edges += 1

    assert total_edges % 2 == 0
    return total_edges


def read_input(file):
    cubes = []
    with open(file, "r") as f:
        for line in f:
            x, y, z = line.strip().split(",")
            cubes.append((int(x), int(y), int(z)))
    return cubes

def solution1(file: str) -> int:
    cubes = read_input(file)
    total_edges =  get_total_edges(cubes)
    number_of_outer_faces = (len(cubes) * 6) - total_edges
    return number_of_outer_faces

def solution2(file: str) -> int:
    pass


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")
    #
    # ans = solution2("example.txt")
    # print(f"Solution 2 for Example is: {ans}")
    # start = time.perf_counter()
    # ans = solution2("input.txt")
    # end = time.perf_counter()
    # print(f"Solution 2 for Input is: {ans}")
    # print(f"Elapsed Time {end - start}")


if __name__ == "__main__":
    main()

