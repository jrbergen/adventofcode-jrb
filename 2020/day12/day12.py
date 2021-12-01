from pathlib import Path
from typing import Tuple

import numpy as np
from numpy import pi, ndarray


def read_input(inpath: Path) -> Tuple[Tuple[str, int]]:
    return tuple((x[0], int(x[1:]),) for x in inpath.read_text().split('\n') if x)


def rot2d(vec: ndarray, rad: float) -> ndarray:
    return np.dot(vec,
                  np.array([[np.cos(rad), -np.sin(rad)],
                            [np.sin(rad), np.cos(rad)]]))


def navigate(instructions: Tuple[Tuple[str, int]], mode: str, initheading: Tuple[int, int],
             initpos: Tuple[int, int] = (0, 0)) -> int:
    """
    Runs navigation instructions and returns Manhattan's distance of traversed distance relative to starting position.

    :param instructions: list, mandatory: list of 2-tuples containing instructions ([ESWNLRF]{1}, int,)
    :param mode: str, mandatory, options: 'waypoint','pos'.
    :param initheading: 2-tuple, mandatory: initial heading.
    :param initpos: 2-tuple, default = (0,0,): ship's starting position.
    """
    if mode not in ('waypoint', 'pos'):
        raise ValueError(f"Unrecognized mode {mode}. Valid: 'waypoint' or 'pos'")

    vectors = {'waypoint': np.array(initheading, dtype=np.float64),
               'pos': np.array(initpos, dtype=np.float64)}

    for inst in instructions:
        inst, magnitude = inst
        if inst == 'E':
            vectors[mode][0] += magnitude
        elif inst == 'S':
            vectors[mode][1] -= magnitude
        elif inst == 'W':
            vectors[mode][0] -= magnitude
        elif inst == 'N':
            vectors[mode][1] += magnitude
        elif inst == 'L':
            vectors['waypoint'] = rot2d(vectors['waypoint'], -magnitude * (pi / 180))
        elif inst == 'R':
            vectors['waypoint'] = rot2d(vectors['waypoint'], magnitude * (pi / 180))
        elif inst == 'F':
            vectors['pos'] += vectors['waypoint'] * magnitude

    return sum(abs(np.round(vectors['pos'] - initpos).astype(np.int64)))


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day12.txt')
    instructions_ = read_input(datapath)

    p1 = navigate(instructions_, mode='pos', initpos=(0, 0,), initheading=(1, 0,))
    print(f"\n\nPart 1: Manhattan distance between starting position and final position = {p1}\n")
    p2 = navigate(instructions_, mode='waypoint', initpos=(0, 0,), initheading=(10, 1,))
    print(f"\n\nPart 2: Manhattan distance between starting position and final position = {p2}\n")
