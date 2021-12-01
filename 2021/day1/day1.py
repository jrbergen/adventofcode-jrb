from __future__ import annotations

from typing import Iterable, Iterator, Sized
from pathlib import Path

INPUT_PATH_1A: Path = Path(__file__).parent.joinpath('input1a.txt')
INPUT_PATH_1B: Path = INPUT_PATH_1A  # Same inputs for A and B


def exercise_a() -> int:

    lines: list[int] = [int(line) for line in INPUT_PATH_1A.read_text(encoding='utf-8').split('\n') if line]

    n_increases: int = 0
    for num_a, num_b in zip(lines[:-1], lines[1:]):
        if num_b > num_a:
            n_increases += 1

    print(f"Exercise A; number of increases: {n_increases}")
    return n_increases


def moving_window(sized_iter: Sized, window_size: int = 3) -> Iterator[Iterable]:
    for curpos, _ in enumerate(sized_iter):
        yield sized_iter[curpos: curpos+window_size]


def exercise_b() -> int:
    lines: list[int] = [int(line) for line in INPUT_PATH_1B.read_text(encoding='utf-8').split('\n') if line]

    n_increases: int = 0
    for window_a, window_b in zip(moving_window(lines), moving_window(lines[1:])):
        if sum(window_b) > sum(window_a):
            n_increases += 1

    print(f"Exercise B; number of increases: {n_increases}")
    return n_increases


if __name__ == '__main__':
    exercise_a()
    exercise_b()
