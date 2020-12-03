from pathlib import Path
from typing import List, Union
import re

ROOT = Path(__file__).parent

def read_input(pth: Path, repat) -> List[List[Union[int, str]]]:
    with open(pth, 'r') as inputhandle:
        retlist = [list(repat.search(line.strip()).groups()) for line in inputhandle]
    for i, ret in enumerate(retlist):
        retlist[i][0] = int(retlist[i][0])
        retlist[i][1] = int(retlist[i][1])
    return retlist


if __name__ == '__main__':
    inpath = Path(ROOT / 'input_day2.txt').resolve()
    repat = re.compile(r'(\d+)-(\d+) ([A-Za-z]{1}): (.+)')
    inputlst = read_input(inpath, repat)

    validpasswords = []
    for passw in inputlst:
        pw = {passw[-1][passw[0]-1], passw[-1][passw[1]-1]}
        if passw[-2] in pw and len(pw) == 2:
            validpasswords.append(passw[-1])

    print(f"There are {len(validpasswords)} valid passwords in the input")
