from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
from numpy import ndarray

INPUT_PATH_4A: Path = Path(__file__).parent.joinpath('input4a.txt')
INPUT_PATH_4B: Path = INPUT_PATH_4A  # Same inputs for A and B


class BingoMatrix:

    def __init__(self, matrix: ndarray | list[list[int]]):
        self.mat: ndarray = np.array(matrix, dtype=np.int32)
        self.mask: ndarray = np.ones(shape=self.mat.shape, dtype=np.int32)

    @property
    def bingo(self) -> bool:
        return not self.mask.sum(axis=1).all() or not self.mask.sum(axis=0).all()

    @property
    def score(self) -> int:
        return 0 if not self.bingo else (self.mask * self.mat).sum().sum()

    def fill_numbers(self, number: int | Iterable[int]) -> None:
        for num in number if isinstance(number, Iterable) else [number]:
            self.mask[np.where(self.mat == num)] = 0

    def __repr__(self):
        return f'{type(self).__name__}({self.mat})'

    def __str__(self):
        return f'{type(self).__name__}(bingo={self.bingo},\n{self.mat*self.mask})'


@functools.lru_cache(maxsize=1)
def parse_input(filepath: Path) -> tuple[list[int], list[BingoMatrix]]:
    texts = filepath.read_text(encoding='utf-8').split('\n')
    guesses_ = [int(num) for num in texts[0].split(',')]
    bingomatrices, curbingomat = [], []
    for line in texts[1:]:
        if line:
            curbingomat.append([int(num) for num in line.split(' ') if num])
        elif curbingomat:
            bingomatrices.append(BingoMatrix(matrix=curbingomat))
            curbingomat = []
    return guesses_, bingomatrices


def solve_bingo(filepath: Path, last_to_get_bingo_wins: bool = False) -> int:
    guesses, bingomats = parse_input(filepath)
    bingomats = set(bingomats)
    for guess in guesses:
        marked = []
        for bingomat in bingomats:
            bingomat.fill_numbers(guess)
            if (bingo := bingomat.bingo):
                marked.append(bingomat)
            if (marked and not last_to_get_bingo_wins) or (bingo and len(bingomats) == 1):
                matscore = bingomat.score
                final_score = matscore * guess
                print(f"Last guess: {guess}.")
                print(f"Sum of {'LAST' if last_to_get_bingo_wins else 'FIRST'} winning board: {bingomat.score}.")
                print(f"Final score of {'LAST' if last_to_get_bingo_wins else 'FIRST'} winning board: {final_score}.")
                return final_score
        bingomats -= set(marked)
    raise ValueError("solve_bingo couldn't find solution.")


def exercise_a() -> None:
    print(f"Exercise A, day 4: final score best board = {solve_bingo(filepath=INPUT_PATH_4A)}.")


def exercise_b() -> None:
    print(f"Exercise B, day 4: final score worst board = {solve_bingo(filepath=INPUT_PATH_4B, last_to_get_bingo_wins=True)}.")


if __name__ == '__main__':
    exercise_a()
    exercise_b()
