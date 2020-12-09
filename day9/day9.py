from pathlib import Path
from typing import List, Tuple, Iterator
from itertools import combinations_with_replacement, tee


def read_input(inpath: Path) -> List[int]:
    with open(inpath, 'r') as infile:
        return [int(x) for x in infile.read().split('\n') if x]


def min_max_val_in_single_iteration(values: List[int]) -> Tuple[int, int, Iterator[int]]:
    min_, max_, val = tee(values, 3)
    return min(min_), max(max_), val


def part1(data: List[int], preamble_size: int) -> int:
    for curidx, num in enumerate(data[preamble_size:], start=preamble_size):
        assert num > 0
        preamble = data[curidx - preamble_size:curidx]
        if not any(num_a + num_b == num for num_a, num_b in combinations_with_replacement(preamble, 2)):
            return num
    print("Part 1 failed: No number found which cannot be constructed by any number pair in the preamble...")
    return -1


def part2(data: List[int], target_sum) -> int:
    for idx1 in range(len(data)-1):
        for idx2 in range(idx1+1, len(data)-1):
            min_, max_, vals = min_max_val_in_single_iteration(data[idx1:idx2])
            cur_sum = sum(vals)
            if cur_sum > target_sum:
                break
            if cur_sum == target_sum:
                return min_ + max_
    print("Part 2 failed: no contiguous set of size > 2 was found for which its sum was the target sum...")
    return -1


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day9.txt')

    data = read_input(datapath)

    invalid_num = part1(data, preamble_size=25)

    print(f"\nPart 1:\n\tFirst wrong number: {invalid_num}")
    print(f"\nPart 2:\n\t{part2(data, invalid_num)}")
