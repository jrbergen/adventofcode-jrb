from __future__ import annotations

from pathlib import Path

import numba
import numpy as np

INPUT_PATH_7A: Path = Path(__file__).parent.joinpath('input7a.txt')
INPUT_PATH_7B: Path = INPUT_PATH_7A  # Same inputs for A and B


def parse_input_to_horizontal_crab_positions(filepath: Path) -> list[int]:
    return [int(num) for num in filepath.read_text(encoding='utf-8').replace('\n', ',').split(',') if num]


def exercise_a() -> None:
    positions = sorted(parse_input_to_horizontal_crab_positions(filepath=INPUT_PATH_7A))
    potential_hor_tgt_coords = range(min(positions), max(positions))
    best_error = np.inf
    optimal_hpos = None
    for horizontal_reference_position in potential_hor_tgt_coords:

        error = sum(abs(pos - horizontal_reference_position) for pos in positions)

        if error < best_error:
            best_error = error
            optimal_hpos = horizontal_reference_position
            print(f"Found new best position: {optimal_hpos} with error: {best_error}.", end='\r')

    if optimal_hpos is None:
        raise ValueError("Could not find otimal horizontal position somehow.")

    print(' '.join([f"Day 7 exercise A: fuel usage at optimal horizontal target position {optimal_hpos}:",
                    f"{best_error}."]))


@numba.njit()
def get_fuel_consumption_at_optimal_position(positions: tuple[int, ...]) -> tuple[int, int]:
    potential_hor_tgt_coords = range(min(positions), max(positions))  # = set(positions)
    best_error = np.inf
    optimal_hpos = -1
    for horizontal_reference_position in potential_hor_tgt_coords:
        error = 0
        for pos in positions:
            error += sum(range(1, abs(pos - horizontal_reference_position) + 1))

        if error < best_error:
            best_error = int(error)
            optimal_hpos = horizontal_reference_position
    return best_error, optimal_hpos


def exercise_b() -> None:
    print("Starting dumb bruteforce whilst still feasible...")
    positions = sorted(parse_input_to_horizontal_crab_positions(filepath=INPUT_PATH_7B), reverse=True)
    best_error, optimal_hpos = get_fuel_consumption_at_optimal_position(positions=tuple(positions))
    print(' '.join([f"Day 7 exercise B: fuel usage at optimal horizontal target position {optimal_hpos}:",
                    f"{int(best_error)}."]))


if __name__ == '__main__':
    exercise_a()
    exercise_b()
