import itertools
from pathlib import Path
from typing import List, Dict, Tuple, Union, Set
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


def intstr_to_binstr(intstr: str) -> str:
    return f'{int(intstr):036b}'


def apply_mask_to_value(mask: str, value: str, nbits: int = 36) -> str:
    intval = int(value, 2)
    for (i, maskchar), valchar in zip(enumerate(mask, start=1), value):
        if maskchar == '1' and valchar == '0':
            intval += 2 ** (nbits - i)
        elif maskchar == '0' and valchar == '1':
            intval -= 2 ** (nbits - i)
    return intstr_to_binstr(str(intval))


def apply_masks_to_values(instructions) -> dict:
    progdict = {}
    for maskdict in instructions:
        mask = maskdict['mask']
        for mementry in maskdict['mems']:
            address, val = (intstr_to_binstr(x) for x in mementry)
            progdict[int(address, 2)] = apply_mask_to_value(mask, val)
    return progdict


def apply_mask_to_address(mask: str,
                          starting_address: str,
                          nbits: int = 36) -> List[int]:
    addresses = [0]
    for (i, achr), mchr in zip(enumerate(starting_address), mask):
        if mchr == 'X':
            addresses += [address + 2 ** (nbits - i - 1) for address in addresses]
        elif achr == '1' or mchr == '1':
            addresses = [address + 2 ** (nbits - i - 1) for address in addresses]
    return addresses


def apply_masks_to_addresses(instructions) -> dict:
    progdict = {}
    for maskdict in instructions:
        mask = maskdict['mask']
        for mementry in maskdict['mems']:  # val in zip(*((intstr_to_binstr(x) for x in mementry) for mementry in maskdict['mems'])):
            val = mementry[-1]
            cur_addresses = apply_mask_to_address(mask=mask, starting_address=intstr_to_binstr(mementry[0]))
            for addr in cur_addresses:
                progdict[addr] = intstr_to_binstr(val)
    return progdict


def sum_dict(dict_: dict, base_numeral: int = 2):
    return sum((int(x, base_numeral) for x in list(dict_.values())))


def part1(mems):
    print("Answer day 14 part 1:", sum_dict(apply_masks_to_values(mems)))


def part2(mems):
    print("Answer day 14 part 2:", sum_dict(apply_masks_to_addresses(mems)))


if __name__ == '__main__':
    mems = read_input('input_day14.txt')

    part1(mems)
    part2(mems)
