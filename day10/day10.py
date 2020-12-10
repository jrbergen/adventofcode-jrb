from pathlib import Path
from typing import List, Tuple, Iterator
from itertools import combinations_with_replacement, tee


def read_input(inpath: Path) -> List[int]:
    with open(inpath, 'r') as infile:
        return [int(x) for x in infile.read().split('\n') if x]

def part1(data: List[int], preamble_size: int) -> int:
    ...


def part2(data: List[int], target_sum) -> int:
    ...


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day9.txt')

    data = read_input(datapath)

    invalid_num = part1(data, preamble_size=25)

    print(f"\nPart 1:\n\tFirst wrong number: {invalid_num}")
    print(f"\nPart 2:\n\t{part2(data, invalid_num)}")
