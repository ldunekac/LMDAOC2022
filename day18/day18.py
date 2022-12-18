adj_indexes = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]

def find_trapped_cubes(cubes):
    nodes = set(cubes)

    xs = [x for x, _, _ in cubes]
    minx = min(xs)
    maxx = max(xs)

    ys = [y for _, y, _ in cubes]
    miny = min(ys)
    maxy = max(ys)

    zs = [z for _, _, z in cubes]
    minz = min(zs)
    maxz = max(zs)

    possible_inner_cubes = set()
    outer_cubes = []
    for i in range(minx, maxx + 1):
        for j in range(miny, maxy + 1):
            for k in range(minz, maxz + 1):
                if not (i, j, k) in nodes:
                    if i == minx or i == maxx or \
                        j == miny or j == maxy or \
                        k == minz or k == maxz:
                        outer_cubes.append((i,j,k))
                    else:
                        possible_inner_cubes.add((i, j, k))

    while len(outer_cubes) > 0:
        current_node = outer_cubes.pop()
        (x, y, z) = current_node
        adj_nodes = [(x + x1, y + y1, z + z1) for x1, y1, z1 in adj_indexes]
        for adj_node in adj_nodes:
            if adj_node in possible_inner_cubes:
                outer_cubes.append(adj_node)
                possible_inner_cubes.remove(adj_node)

    return list(possible_inner_cubes)


def get_total_edges(cubes):
    nodes = set(cubes)

    total_edges = 0
    for (x, y, z) in nodes:
        adj_nodes = [(x + x1, y + y1, z + z1) for x1, y1, z1 in adj_indexes]
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
    cubes = read_input(file)
    cubes += find_trapped_cubes(cubes)
    total_edges = get_total_edges(cubes)
    number_of_outer_faces = (len(cubes) * 6) - total_edges
    return number_of_outer_faces


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

