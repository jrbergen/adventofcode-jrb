import re
from pathlib import Path
from typing import List, Union


def read_input(pth: Path, rexpat: re.Pattern) -> List[List[Union[int, str]]]:
    with open(pth, 'r') as inputhandle:
        return [[int(y) if y.isdigit() else y for y in x]
                for x in [list(rexpat.search(line.strip()).groups()) for line in inputhandle]]


def get_n_valid_pt1(invals) -> int:
    n_valid = 0
    for passw in invals:
        occur = passw[-1].count(passw[-2])
        if passw[0] <= occur <= passw[1]:
            n_valid += 1
    return n_valid


def get_n_valid_pt2(invals) -> int:
    n_valid = 0
    for passw in invals:
        pw = {passw[-1][passw[0] - 1], passw[-1][passw[1] - 1]}
        if passw[-2] in pw and len(pw) == 2:
            n_valid += 1
    return n_valid


if __name__ == '__main__':
    ROOT = Path(__file__).parent
    inpath = Path(ROOT / 'input_day2.txt').resolve()
    repat = re.compile(r'(\d+)-(\d+) ([A-Za-z]{1}): (.+)')
    inputvals = read_input(inpath, repat)

    # Part 1
    print(f"There are {get_n_valid_pt1(inputvals)} valid passwords in the input (day 2 part 1)")

    # Part 2
    print(f"There are {get_n_valid_pt2(inputvals)} valid passwords in the input (day 2 part 2)")
