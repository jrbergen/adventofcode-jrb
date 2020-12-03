
from pathlib import Path

import numpy as np
from numpy import ndarray


def read_input(pth: Path) -> ndarray:
    with open(pth, 'r') as inputhandle:
        return np.array([list(line.strip()) for line in inputhandle])


if __name__ == '__main__':
    forest = read_input(Path(Path(__file__).parent / 'input_day3.txt').resolve())
    starting_forest = forest
    forest_end = forest.shape[0]

    row, col = 0, 0
    drow, dcol = 1, 3

    tree, emptymark, foundmark = list('#OX')
    treepositions, emptypositions = [], []

    while row < forest_end:
        if col > forest.shape[1] - 1:
            forest = np.concatenate([forest, starting_forest], axis=1)

        if forest[row, col] == tree:
            treepositions.append((row, col))
        else:
            emptypositions.append((row, col))
        row += drow
        col += dcol

    ntrees = len(treepositions)

    # Not necessary but may ben ice for visualisation
    marked_forest = forest.copy()
    marked_forest[tuple(zip(*treepositions))] = foundmark
    marked_forest[tuple(zip(*emptypositions))] = emptymark

    print(f"I've encountered {ntrees} trees in our wander through the forest.")
