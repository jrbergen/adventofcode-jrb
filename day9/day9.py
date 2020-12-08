from pathlib import Path
from typing import List, Union, Dict, Tuple, NoReturn, Any


def read_input(textfile: Path) -> Any:
    with open(textfile, 'r') as tfile:
        return tfile.read().split('\n')


def part1():
    ...


def part2():
    ...


if __name__ == '__main__':
    data = read_input(Path(Path(__file__).parent / 'input_day9.txt'))

    part1()
    part2()
