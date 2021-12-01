from __future__ import annotations

from pathlib import Path
from typing import List, Union, Tuple, Set, Optional

# from itertools import reduce

ROOT = Path(__file__).parent


def read_input(pth: Path) -> Set[int]:
    with open(pth, 'r') as inputhandle:
        return {int(line.strip()) for line in inputhandle}


def multiple_of_two_sums(inputset: Set[int], lookfor: int) -> int:
    for i, innerval in enumerate(inputset):
        for j, outerval in enumerate(inputset):
            if innerval + outerval == lookfor and i != j:
                return innerval * outerval


def multiple_of_three_sums(inputset: Set[int], lookfor: int) -> int:
    for i, innerval in enumerate(inputset):
        for j, midval in enumerate(inputset):
            for k, outerval in enumerate(inputset):
                if innerval + midval + outerval == lookfor and i != j and j != k and i != k:
                    return innerval * midval * outerval


def sum_multiple_recursive(inputset: Set[int], numsums: int, lookfor: int, vals: Optional[List[int]] = None) -> int:
    vals = [] if not vals else vals
    assert numsums > 1

    for i, val in enumerate(inputset):
        if val + sum(vals) > lookfor:
            ...
        if len(vals) == numsums:
            valsum = sum(vals)
            if valsum == lookfor:
                return valsum
        else:
            vals.append(val)
            return sum_multiple_recursive(inputset, numsums, lookfor, vals)

    #
    #
    # #if not numsums:
    #  #   return reduce(lambda x,y: x*y, foundvals)
    # else:
    #     for i
    # foundvals = sum_multiple_recursive(inputset, lookfor, numsums-1)


if __name__ == '__main__':
    inpath = Path(ROOT / 'input_day1.txt').resolve()
    inputset = read_input(inpath)

    sum_mult_two = multiple_of_two_sums(inputset, lookfor=2020)
    sum_mult_three = multiple_of_three_sums(inputset, lookfor=2020)
    # res = sum_multiple_recursive(inputset, 2, 2020)
    print(f"Multiple of two sums: \t{res}")
    print(f"Multiple of three sums: \t{sum_mult_three}")
