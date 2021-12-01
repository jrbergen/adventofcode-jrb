from pathlib import Path
from typing import List


def read_passports(pth: Path) -> List[str]:
    with open(pth, 'r') as inputhandle:
        return inputhandle.read().split('\n\n')


if __name__ == '__main__':
    passports = read_passports(Path(Path(__file__).parent / 'input_day4.txt').resolve())

    validbase = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid',)
    n_valid = sum(1 if all(x in pp for x in validbase) else 0 for pp in passports)
    print(f"Found {n_valid} valid passports")
