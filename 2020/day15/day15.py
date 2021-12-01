from pathlib import Path
from typing import List

from utils import ProgBar


def read_input(filename: Path) -> List[int]:
    with open(filename, 'r') as fhandle:
        return [int(x) for x in ','.join(fhandle.read().split('\n')).split(',')]


def part1and2(starting_nums: List[int], maxiter: int = 2020):
    occ_num_dict = {x: i for i, x in enumerate(starting_nums, start=1)}
    curnum = starting_nums[-1]
    pbar = ProgBar(maxiter)
    for turn in range(len(starting_nums), maxiter):
        if curnum in occ_num_dict:
            lastnum = curnum
            curnum = turn - occ_num_dict[curnum]
            occ_num_dict[lastnum] = turn
        else:
            occ_num_dict[curnum] = turn
            curnum = 0
        if turn % 1000 == 0:
            pbar.update(turn)
    return curnum


if __name__ == '__main__':
    infile = Path('input_day15.txt')
    numbers = read_input(infile)
    [print(f"Answer to part {part} = {part1and2(numbers, maxiter=partiter)}.")
     for part, partiter in enumerate((2012, 30_000_000), start=1)]

