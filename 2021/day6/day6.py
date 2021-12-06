from __future__ import annotations

from pathlib import Path

INPUT_PATH_6A: Path = Path(__file__).parent.joinpath('input6a.txt')
INPUT_PATH_6A_EXAMPLE_STATES: Path = Path(__file__).parent.joinpath('input6a-example-states.txt')
INPUT_PATH_6B: Path = INPUT_PATH_6A  # Same inputs for A and B


def parse_input_to_fishcount(filepath: Path, max_spawntime: int = 8) -> dict[int, int]:
    nums = [int(num) for num in filepath.read_text(encoding='utf-8').replace('\n', ',').split(',') if num]
    counter = {daysleft: 0 for daysleft in range(max_spawntime + 1)}
    for num in nums:
        counter[num] += 1
    return counter


def advance_step(lfish_counter: dict[int, int], spawntime: int, days_before_reproducing: int = 2) -> dict[int, int]:
    n_zeros = lfish_counter[0]
    for leftnum, rightnum in zip(range(spawntime), range(1, spawntime + 1)):
        lfish_counter[leftnum] = lfish_counter[rightnum]
    lfish_counter[spawntime] = 0
    lfish_counter[spawntime - days_before_reproducing] += n_zeros
    lfish_counter[spawntime] += n_zeros
    return lfish_counter


def simulate_fishworld(ndays: int, filepath: Path, spawntime: int = 8) -> int:
    fishcounter = parse_input_to_fishcount(filepath=filepath, max_spawntime=spawntime)
    n_fish = 0
    for iiday in range(ndays):
        fishcounter = advance_step(lfish_counter=fishcounter, spawntime=spawntime)
        n_fish = sum(fishcounter.values())
        print(f"Step {iiday + 1}/{ndays}, num fish: {n_fish}.")
    return n_fish


def exercise_a() -> None:
    ndays = 80
    n_fish = simulate_fishworld(ndays=ndays, filepath=INPUT_PATH_6A)
    print(f"Day 6 exercise A: number lanternfish after {ndays} days: {n_fish}.")


def exercise_b() -> None:
    ndays = 256
    n_fish = simulate_fishworld(ndays=ndays, filepath=INPUT_PATH_6B)
    print(f"Day 6 exercise B: number lanternfish after {ndays} days: {n_fish}.")


if __name__ == '__main__':
    exercise_a()
    exercise_b()
