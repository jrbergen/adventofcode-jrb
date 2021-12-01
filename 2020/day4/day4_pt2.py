import re
from pathlib import Path
from typing import List, Tuple, Union


def read_passports(pth: Path, short_and_badly_readable: bool = True) -> List[dict]:
    if short_and_badly_readable:
        with open(pth, 'r') as passportfile:
            return [{key: val for key, val in
                     [entry.split(':') for entry in pp.strip().replace('\n', ' ').split(' ')]}
                    for pp in passportfile.read().split('\n\n')]
    else:
        ppdicts = []
        with open(pth, 'r') as passportfile:
            for pp in passportfile.read().split('\n\n'):
                curppdict = {}
                for entry in pp.strip().replace('\n', ' ').split(' '):
                    key, val = entry.split(':')
                    curppdict[key] = val
                ppdicts.append(curppdict)
        return ppdicts


def validate_height(height: str,
                    heightbounds: Tuple[Tuple[str, int, int], ...] = (('cm', 150, 193,), ('in', 59, 76),)) -> bool:
    for height_unit_str, min_height, max_height in heightbounds:
        if height_unit_str not in height:
            continue
        return min_height <= int(height.replace(height_unit_str, '')) <= max_height
    return False


def validate_haircolor(hair_color: str, first_symbol: str = '#', colorrex: str = r'[0-9a-f]{6}') -> bool:
    if hair_color[0] != first_symbol:
        return False
    return bool(re.search(colorrex, hair_color[1:]))


def validate_eyecolor(eye_color: str,
                      accepted_eyecolors: Tuple[str, ...] = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',)) -> bool:
    return eye_color in accepted_eyecolors


def validate_date(date: Union[int, str], min_val: int, max_val: int) -> bool:
    try:
        date = int(date)
    except ValueError:
        if not type(date) == int:
            raise TypeError(f"Unexpected type {type(date)} for argument date")
    return min_val <= date <= max_val


def validate_passport_id(pid: str, n_digits: int = 9) -> bool:
    return pid.isdigit() and len(pid) == n_digits


if __name__ == '__main__':
    passports = read_passports(Path(Path(__file__).parent / 'input_day4.txt').resolve())

    valid_pps = []

    validations = {'byr': lambda x: validate_date(x, 1920, 2002),
                   'iyr': lambda x: validate_date(x, 2010, 2020),
                   'eyr': lambda x: validate_date(x, 2020, 2030),
                   'hgt': lambda x: validate_height(x),
                   'hcl': lambda x: validate_haircolor(x),
                   'ecl': lambda x: validate_eyecolor(x),
                   'pid': lambda x: validate_passport_id(x)}

    for pp in passports:
        if not all(valkey in pp.keys() for valkey in validations.keys()):
            continue

        if all(validations[pp_key](pp_val) if pp_key in validations else True for pp_key, pp_val in pp.items()):
            valid_pps.append(pp)
        else:
            print("---------------------------------")
            print("Validation failed for: \n")
            [print(key, val) for key, val in pp.items()]
            print(
                f"Invalid fields: {[pp_key for pp_key, pp_val in pp.items() if pp_key in validations and not validations[pp_key](pp_val)]}")
            print("#################################")

    print(f"Found {len(valid_pps)} valid passports")
