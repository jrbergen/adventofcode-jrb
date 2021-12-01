import re
from pathlib import Path
from typing import List, Tuple, Union, Dict, Any, Optional


def read_passports(pth: Path, short_and_badly_readable: bool = True) -> List[dict]:
    if short_and_badly_readable:
        with open(pth, 'r') as passportfile:
            return [{key: int(val) if val.isdigit() else val for key, val in
                     [entry.split(':') for entry in pp.strip().replace('\n', ' ').split(' ')]}
                    for pp in passportfile.read().split('\n\n')]
    else:
        ppdicts = []
        with open(pth, 'r') as passportfile:
            for pp in passportfile.read().split('\n\n'):
                curppdict = {}
                for entry in pp.strip().replace('\n', ' ').split(' '):
                    key, val = entry.split(':')
                    val = int(val) if val.isdigit() else val
                    curppdict[key] = val
                ppdicts.append(curppdict)
        return ppdicts

# class Passport:
#     def __init__(self, passport_dict: Dict[str, Any],
#                  required_entries: Tuple[str] = ('byr','iyr','eyr','hgt','hcl','ecl','pid',)):
#         self._ppdict = passport_dict
#         self.required_entries = required_entries
#         self.valid = all(entryname in required_entries for entryname in self._ppdict.keys())
#
#         self.validate()
#
#     def validate(self):
#
#     @property
#     def byr(self):
#         return

class Validate:

    VALDICT = {'date': ['byr','iyr','eyr'],
               'height': ['hgt'],
               'haircolor': ['hcl'],
               'eyecolor': ['ecl'],
               'passport_id': ['pid']}

    DEFAULT_ACCEPTED_EYECOLORS = ('amb','blu','brn','gry','hzl','oth',)
    DEFAULT_HEIGHTBOUNDS = (('cm',150,193,),('in',59,76),)
    DEFAULT_COLOR_REX = r'[0-9a-f]{6}'

    def __init__(self, valdict: Dict[str, str]):
        """
        Validates passport entries
        :param valdict: dictionary containing entry keys as co
        """
        self.valdict = valdict or self.VALDICT

    def __call__(self):
        pass

    def height(self, height: str, heightbounds: Optional[Tuple[Tuple[str,int, int],...]] = None) -> bool:
        heightbounds = heightbounds or self.DEFAULT_HEIGHTBOUNDS
        for height_unit_str, min_height, max_height in heightbounds:
            try:
                return min_height <= int(height.replace(height_unit_str, '')) <= max_height
            except KeyError:
                print(f"Validation failed for height: {height}; proceeding...")

    def haircolor(self, hair_color: str, first_symbol: str = '#', colorrex: Optional[str] = None) -> bool:
        colorrex = colorrex or self.DEFAULT_COLOR_REX
        if hair_color[0] != first_symbol:
            return False
        return bool(re.search(colorrex, hair_color[1:]))

    def eyecolor(self, eye_color: str, accepted_eyecolors: Optional[Tuple[str, ...]] = None)  -> bool:
        accepted_eyecolors = accepted_eyecolors or self.DEFAULT_ACCEPTED_EYECOLORS
        return eye_color in accepted_eyecolors






def validate_date(date: Union[int, str], min_val: int, max_val: int):
    try:


def validate_eyecolor(eye_color: str, accepted_colors: Tuple[str, ...] = ):
    return eye_color in if eye_color not in


if __name__ == '__main__':
    passports = read_passports(Path(Path(__file__).parent / 'input_day4.txt').resolve())

    valid_pps = []
    validations = {'byr': lambda x: True if 1920 <= x <= 2002 else False,
                   'iyr': lambda x: True if 2010 <= x <= 2020 else False,
                   'eyr': lambda x: True if 2020 <= x <= 2030 else False,
                   'hgt': lambda x: validate_height(x),
                   'hcl': lambda x: validate_haircolor(x),
                   'ecl': lambda x: x in ('amb', 'blu','brn','gry','grn','hzl','oth',),
                   'pid': lambda x: validate_pid(x)}
    #'#, 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')

    for pp in passports:
        if not all(req_key in required_keys for req_key in pp.keys()):
            continue
        try:
            pp['byr']
        except KeyError:
            print("Passport {i} does not contain required key pp")

    # passports = [{key: val for key, val in kvpair.split(':')} for kvpair in
    # #pplist =[[y.split(':') for y in x] for x in
    # pplist=[pp.replace('\n',' ').split(' ') for pp in passports]
    #
    # for pp in pplist:
    #     for entry in pp:
    #         if len(entry) !=2:
    #             print(entry)
    # ppdict = [{key: val if len(pp) == 2 else print(f"Warning for entry no. {ppi}: {pp}") for key, val in pp} for ppi, pp in enumerate(pplist)]
    #
    # validbase = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid',)
    #
    # n_valid = sum(1 if all(x in pp for x in validbase) else 0 for pp in passports)
    # print(f"Found {n_valid} valid passports")
    print(f"Temporary breakpoint in {__name__}")
