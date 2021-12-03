from __future__ import annotations

import functools
from pathlib import Path
from typing import Callable

import numpy as np
from numpy import ndarray

INPUT_PATH_3A: Path = Path(__file__).parent.joinpath('input3a.txt')
INPUT_PATH_3B: Path = INPUT_PATH_3A  # Same inputs for A and B


@functools.lru_cache(maxsize=1)
def parse_input(filepath: Path ) -> np.ndarray:
    return np.array([[int(char) for char in list(row)] for row in filepath.read_text(encoding='utf-8').split('\n') if row])


def get_power_consumption(filepath: Path) -> int:
    binarr = parse_input(filepath)
    gammastr: str = ''
    for icol, col in enumerate(binarr.T):
        if col.sum() > round(col.size / 2):
            gammastr += '1'
        elif col.sum() < round(col.size / 2):
            gammastr += '0'
        else:
            raise ValueError(f"Bits equally common in col {icol}.")

    epsilon: int = int(''.join([str(int(not int(binnum))) for binnum in gammastr]), 2)
    gamma: int = int(gammastr, 2)
    return epsilon * gamma


def get_rating(filepath: Path,
               selection_rule: Callable[[ndarray, int, int], ndarray],
               equally_common_rule: Callable[[ndarray, int], ndarray]
               ) -> int:
    binarr = parse_input(filepath)
    for cur_bitpos, col in enumerate(binarr.T):
        vals, counts = np.unique(binarr[:, cur_bitpos], return_counts=True)
        if binarr.shape[0] < 2:
            break
        if len(set(counts)) == counts.size:
            try:
                most_common = vals[np.argmax(counts)]
            except ValueError as err:
                print(err)
                print(f"Temporary breakpoint in {__name__}")
                raise

            binarr = binarr[selection_rule(binarr, cur_bitpos, most_common)]
        else:
            binarr = binarr[equally_common_rule(binarr, cur_bitpos)]

    return int(''.join(str(x) for x in binarr.flatten().tolist()), 2)


def get_life_support_rating(filepath: Path) -> int:
    selection_rule_o2 = lambda arr, bitpos, mostcommon: arr[:, bitpos] == mostcommon
    selection_rule_co2 = lambda arr, bitpos, mostcommon: arr[:, bitpos] != mostcommon
    equally_common_rule_o2 = lambda arr, bitpos: arr[:, bitpos] == 1
    equally_common_rule_co2 = lambda arr, bitpos: arr[:, bitpos] == 0
    oxrating = get_rating(filepath=filepath,
                          selection_rule=selection_rule_o2,
                          equally_common_rule=equally_common_rule_o2)
    co2rating = get_rating(filepath=filepath,
                           selection_rule=selection_rule_co2,
                           equally_common_rule=equally_common_rule_co2)
    return oxrating * co2rating


def exercise_a() -> None:
    print(f"Exercise A, day 3: power consumption = {get_power_consumption(INPUT_PATH_3A)}.")


def exercise_b() -> None:
    print(f"Exercise B, day 3: life support rating = {get_life_support_rating(filepath=INPUT_PATH_3B)}.")


if __name__ == '__main__':
    exercise_a()
    exercise_b()
