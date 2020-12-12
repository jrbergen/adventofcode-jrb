from pathlib import Path
from numba import jit
import numpy as np
from numpy import pi, ndarray


def read_instr(inpath: Path) -> ndarray:
    instrs = [str(x[0]) for x in inpath.read_text().split('\n') if x]
    return np.array(instrs)


def read_magn(inpath: Path) -> ndarray:
    magns = [x[1:] for x in inpath.read_text().split('\n') if x]
    return np.array(magns, dtype=np.float64)


@jit(nopython=True)
def rot2d(vec: ndarray, rad: float) -> ndarray:
    return np.dot(vec,
                  np.array([[np.cos(rad), -np.sin(rad)],
                            [np.sin(rad), np.cos(rad)]]))


@jit(nopython=True)
def navigate(instructions: ndarray, magnitudes: ndarray,
             mode: int, initheading: ndarray, initpos: ndarray) -> np.float64:
    waypoint = initheading
    pos = initpos.copy()
    update = np.array([0, 0], dtype=np.float64)
    for inst, magnitude in zip(instructions, magnitudes):
        uflag = False
        if inst == 'E':
            update = np.array((magnitude, 0), dtype=np.float64)
            uflag = True
        elif inst == 'S':
            update = np.array((0, -1*magnitude), dtype=np.float64)
            uflag = True
        elif inst == 'W':
            update = np.array((-1*magnitude, 0), dtype=np.float64)
            uflag = True
        elif inst == 'N':
            update = np.array((0, magnitude), dtype=np.float64)
            uflag = True
        elif inst == 'L':
            waypoint = rot2d(waypoint, -1*magnitude * (pi / 180))
        elif inst == 'R':
            waypoint = rot2d(waypoint, magnitude * (pi / 180))
        elif inst == 'F':
            waypoint += waypoint * magnitude
        if uflag:
            if mode == 1:
                waypoint += update
            elif mode == 0:
                pos += update

    abs_ = np.abs(pos-initpos)
    return abs_[0] + abs_[1]


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day12a.txt')
    instructions_ = read_instr(datapath)
    magnitudes = read_magn(datapath)

    initheading_ = np.array([1, 0], dtype=np.float64)
    initpos_ = np.array([0, 0], dtype=np.float64)
    p1 = navigate(instructions_, magnitudes, 0, initpos_, initheading_)
    print(f"\n\nPart 1: Manhattan distance between starting position and final position = {p1}\n")
    initheading_ = np.array([10, 1], dtype=np.float64)
    p2 = navigate(instructions_, magnitudes, 1, initpos_, initheading_)
    print(f"\n\nPart 2: Manhattan distance between starting position and final position = {p2}\n")
