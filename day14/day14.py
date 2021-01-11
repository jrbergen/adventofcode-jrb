from pathlib import Path
from typing import List, Dict, Tuple, Union
import re


def read_input(fname: str) -> List[Dict[str, Union[str, List[List[int]]]]]:
    maskno, entries = -1, []
    maskpat = re.compile(r'mask = (?P<mask>[10X]+)')
    mempat = re.compile(r'mem\[(\d+)] = (\d+)')
    for i, line in enumerate(Path(fname).read_text().split('\n')):
        maskmatch = maskpat.search(line)
        memmatch = mempat.search(line)
        if maskmatch:
            maskno += 1
            entries.append({'mask': maskmatch['mask']})
        elif memmatch:
            try:
                entries[-1]['mems'].append(memmatch.groups())
            except KeyError:
                entries[-1]['mems'] = [memmatch.groups()]
    return entries


def apply_mask(mask: str, value: str, nbits: int = 36) -> str:
    intval = int(value, 2)
    for (i, maskchar), valchar in zip(enumerate(mask, start=1), value):
        if maskchar == '1' and valchar == '0':
            intval += 2 ** (nbits - i)
        elif maskchar == '0' and valchar == '1':
            intval -= 2 ** (nbits - i)
    return intstr_to_binstr(str(intval))


def intstr_to_binstr(intstr: str) -> str:
    return f'{int(intstr):036b}'


def apply_masks(instructions) -> dict:
    progdict = {}
    for maskdict in instructions:
        mask = maskdict['mask']
        for mementry in maskdict['mems']:
            address, val = (intstr_to_binstr(x) for x in mementry)
            progdict[int(address, 2)] = apply_mask(mask, val)
    return progdict


def sum_dict(dict_: dict, base_numeral: int = 2):
    return sum((int(x, base_numeral) for x in dict_.values()))


def part1(mems):
    print(sum_dict(apply_masks(mems)))


if __name__ == '__main__':
    mems = read_input('day14_input.txt')

    part1(mems)
