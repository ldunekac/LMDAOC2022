import numpy as np

def iterate_through_rows(trees, views):
    tree_shape = trees.shape
    for i in range(tree_shape[0]):
        max_seen = -1
        for j in range(tree_shape[1]):
            tree_height = trees[i][j]
            if  tree_height > max_seen:
                views[i][j] = 1
                max_seen = tree_height


def find_visible_trees(trees, views):
    iterate_through_rows(trees, views)
    trees = np.flip(trees, axis=1)
    views = np.flip(views, axis=1)
    iterate_through_rows(trees, views)
    trees = np.flip(trees, axis=1)
    views = np.flip(views, axis=1)
    trees = np.transpose(trees)
    views = np.transpose(views)
    iterate_through_rows(trees, views)
    trees = np.flip(trees, axis=1)
    views = np.flip(views, axis=1)
    iterate_through_rows(trees, views)
    # Just getting the matricies back to the original spot for debugging
    trees = np.flip(trees, axis=1)
    views = np.flip(views, axis=1)
    trees = np.transpose(trees)
    views = np.transpose(views)

def read_input(file):
    with open(file) as f:
        input = f.readlines()
        num_rows = len(input)
        num_columns = len(input[0].strip())
        input = [[int(x) for x in i.strip()] for i in input]
        return np.array(input), np.zeros((num_rows, num_columns), dtype=int)


def solution1(file):
    tree_grid, view_grid = read_input(file)
    find_visible_trees(tree_grid, view_grid)
    return int(np.sum(view_grid))


def bruit_force_scenic_score(x, y, trees):
    score = 1
    tree_height = trees[x][y]
    # check left
    num_seen = 0
    for i in range(y-1,0-1,-1):
        num_seen += 1
        if trees[x,i] >= tree_height:
            break
    score *= num_seen

    # check right
    num_seen = 0
    for i in range(y+1,trees.shape[1]):
        num_seen += 1
        if trees[x,i] >= tree_height:
            break
    score *= num_seen

    # check up
    num_seen = 0
    for i in range(x-1,0-1,-1):
        num_seen += 1
        if trees[i,y] >= tree_height:
            break
    score *= num_seen

    # check down
    num_seen = 0
    for i in range(x+1,trees.shape[0]):
        num_seen += 1
        if trees[i,y] >= tree_height:
            break
    score *= num_seen
    
    return score


def solution2(file):
    trees, scenic_scores = read_input(file)
    for i in range(trees.shape[0]):
        for j in range(trees.shape[1]):
                scenic_scores[i][j] = bruit_force_scenic_score(i, j, trees)
    return np.max(scenic_scores)


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
