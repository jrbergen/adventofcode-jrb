from pathlib import Path

import numpy as np
from numpy import ndarray

INPUT_PATH_13: Path = Path(__file__).parent.joinpath('input13.txt')


def parse_input(inputpath: Path) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[str, int], ...]]:
    coordinates, folds = inputpath.read_text(encoding='utf-8').split('\n\n')
    coordinates = tuple((int(coord.split(',')[0]), int(coord.split(',')[1])) for coord in coordinates.split('\n') if coord)
    return coordinates, tuple((str(fold.split('=')[0][-1]), int(fold.split('=')[1])) for fold in folds.split('\n') if fold)


def mat_from_coords(coords: tuple[tuple[int, int], ...]):
    mat = np.zeros(shape=(max(list(zip(*coords))[1]) + 1, max(list(zip(*coords))[0]) + 1), dtype=np.bool_)
    for col, row in coords:
        mat[row, col] = 1
    return mat


def render_dots(arr: ndarray, msg: str = '') -> None:
    print('\n'.join(['*' * 12, msg+'\n' if msg else '', '\n'.join(''.join('#' if col else '.' for col in row) for row in arr),
                     '*' * 12]))


def run_folds(mat: ndarray, folds: tuple[tuple[str, int], ...]) -> ndarray:
    for iifold, (axis, coord) in enumerate(folds):
        new = mat.copy()
        match axis:
            case 'x':
                new[:, :coord] += np.fliplr(mat[:, coord + 1:])
                new = new[:, :coord]
            case 'y':
                new[:coord, :] += np.flipud(mat[coord + 1:, :])
                new = new[:coord, :]
            case _:
                raise ValueError(f"Invalid axis {axis!r}")
        mat = new
    return mat


def exercise_a_and_b():
    coords_, folds_ = parse_input(INPUT_PATH_13)
    mat_ = mat_from_coords(coords=coords_)
    print(f"Day 13 exercise A: remaining dots = {run_folds(mat=mat_, folds=folds_[:1]).astype(np.uint32).sum()}")
    render_dots(arr=run_folds(mat=mat_, folds=folds_), msg=f"Day 13 exercise B: dotmat =")


if __name__ == '__main__':
    exercise_a_and_b()
