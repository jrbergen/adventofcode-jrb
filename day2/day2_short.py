import re
from pathlib import Path
from typing import List, Union


def read_input(pth: Path, rexpat: re.Pattern) -> List[List[Union[int, str]]]:
    with open(pth, 'r') as inputhandle:
        return [[int(y) if y.isdigit() else y for y in x]
                for x in [list(rexpat.search(line.strip()).groups()) for line in inputhandle]]


def get_n_valid(invals, part: int) -> int:
    if part:
        return len([pw for pw in invals if pw[0] <= pw[-1].count(pw[-2]) <= pw[1]])
    else:
        return len([pw for pw in invals if (pw[-2] in pw[-1][pw[0] - 1]) ^ (pw[-2] in pw[-1][pw[1] - 1])])


if __name__ == '__main__':
    inputvals = read_input(Path(Path(__file__).parent / 'input_day2.txt').resolve(),
                           re.compile(r'(\d+)-(\d+) ([A-Za-z]{1}): (.+)'))
    [print(f"There are {get_n_valid(inputvals, i)} valid passwords in the input (day 2 part {i + 1})")
     for i in range(2)]
