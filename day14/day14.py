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


def generate_floating_masks(mask: str, floating_char: str = 'X'):

    float_positions = [chr.start() for chr in re.finditer(floating_char, mask)]

    n_masks = 2 ** len(float_positions)
    masks = [mask[:float_positions[0]] for _ in range(n_masks)]

    print(f"Temporary breakpoint in {__name__}")






    float_subsets = {''.join(x)
                     for x in itertools.combinations_with_replacement(
            ['1', '0'] * (len(float_positions) // 2 + 1),
            len(float_positions))}

    assert len(float_subsets) == 2 ** len(float_positions)

    newmasks = [list(mask).copy() for _ in float_subsets]
    for (i, newmask), floatset in zip(enumerate(newmasks), float_subsets):
        for floatpos, floatset_char in zip(float_positions, floatset):
            newmasks[i][floatpos] = floatset_char

    newmasks = [''.join(newmask) for newmask in newmasks]

    return newmasks


def apply_mask_to_address(mask: str,
                          starting_address: str,
                          nbits: int = 36) -> Set[int]:

    masks = generate_floating_masks(mask)
    start_addr_int = starting_address
    addresses = set()
    for newmask in masks:
        cur_addr = start_addr_int
        for (i, maskchar), addr_char in zip(enumerate(newmask, start=1), starting_address):
            if maskchar == '1' and addr_char == '0':
                cur_addr += 2 ** (nbits - i)
        addresses.add(cur_addr)
    print(addresses)
    return addresses





def apply_masks_to_addresses(instructions) -> dict:

    progdict = {}
    for maskdict in instructions:
        mask = maskdict['mask']
        new_addresses = set()
        for mementry in maskdict['mems']:#val in zip(*((intstr_to_binstr(x) for x in mementry) for mementry in maskdict['mems'])):
            val = mementry[-1]
            new_addresses.add(apply_mask_to_address(mask=mask, starting_address=intstr_to_binstr(mementry[0])))
            for new_addr in new_addresses:
                progdict[int(new_addr, 2)] = val
    return progdict


def sum_dict(dict_: dict, base_numeral: int = 2):
    return sum((int(x, base_numeral) for x in dict_.values()))


def part1(mems):
    print("Answer day 14 part 1:", sum_dict(apply_masks_to_values(mems)))


def part2(mems):
    print("Answer day 14 part 2:", sum_dict(apply_masks_to_addresses(mems)))


if __name__ == '__main__':
    mems = read_input('input_day14.txt')

    part1(mems)
    part2(mems)
