from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy import ndarray

INPUT_PATH_5A: Path = Path(__file__).parent.joinpath('input5a.txt')
INPUT_PATH_5B: Path = INPUT_PATH_5A  # Same inputs for A and B


def parse_input_to_fourtuples(filepath: Path, include_diagonal: bool = False) -> tuple[tuple[int, int, int, int], ...]:
    tups = []
    for line_ in filepath.read_text(encoding='utf-8').split('\n'):
        if (tup := tuple(int(num) for num in line_.replace(' -> ', ',').split(',') if num)):
            x1, y1, x2, y2 = tup
            dy, dx = y2-y1, x2-x1
            if (x1 == x2 or y1 == y2) or (include_diagonal and (abs(dy) == abs(dx))):
                tups.append(tup)
    return tuple(tups)


def add_linecoords_to_2darr(arr: ndarray, x1: int, y1: int, x2: int, y2: int) -> ndarray:
    dy, dx = y2 - y1, x2 - x1
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    if abs(dx) == abs(dy):
        xstep = 1 if x2 > x1 else -1
        ystep = 1 if y2 > y1 else -1
        for x, y in zip(range(x1, x2+xstep, xstep), range(y1, y2+ystep, ystep)):
            arr[y, x] += 1
    elif x1 == x2:
        arr[ymin:ymax+1, x1] += 1
    elif y1 == y2:
        arr[y1, xmin:xmax+1] += 1
    return arr


def count_intersecting_vent_lines(linecoords: tuple[tuple[int, int, int, int], ...],
                                  min_intersections: int) -> int:
    max_ = max([max(tup) for tup in linecoords]) + 1
    ncoords = len(linecoords)
    arr = np.zeros(shape=(max_, max_), dtype=np.int32)
    print("Starting retarded bruteforce method by enumerating over all possible coordinates "
          "instead of extracting line equations and solving for their intersections or something.")

    for ii, (x1, y1, x2, y2) in enumerate(linecoords):
        print(f"Processing line " + str(ii + 1) + '/' + str(ncoords), end='\r')
        arr = add_linecoords_to_2darr(arr, x1, y1, x2, y2)

    return arr[arr >= min_intersections].size


def exercise_a() -> None:
    coords_as_4tups = parse_input_to_fourtuples(filepath=INPUT_PATH_5A)
    n_intersecting = count_intersecting_vent_lines(linecoords=coords_as_4tups, min_intersections=2)
    print(f"Day 5 exercise A: number of intersecting vent lines: {n_intersecting}.")


def exercise_b() -> None:
    coords_as_4tups = parse_input_to_fourtuples(filepath=INPUT_PATH_5B, include_diagonal=True)
    n_intersecting = count_intersecting_vent_lines(linecoords=coords_as_4tups, min_intersections=2)
    print(f"Day 5 exercise B: number of intersecting vent lines: {n_intersecting}.")


if __name__ == '__main__':
    exercise_a()
    exercise_b()
