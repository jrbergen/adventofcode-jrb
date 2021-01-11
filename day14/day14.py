from pathlib import Path
from typing import Union, List, Tuple
import re

REX = re.compile(r"(?:mask = (?P<mask>.+))|(?:mem\[(?P<memloc>\d+)?] = (?P<memval>\d+))")


def read_input(filepath: Union[str, Path]) -> List[Tuple[str, List[Tuple[int, int]]]]:
    data = [part for part in Path(filepath).resolve().read_text().splitlines()]
    instrs, curinstr = [], tuple()
    for i, line in enumerate(data):
        res = REX.search(line)

        if not res:
            raise IOError(f"Improper input file format; could not match line {i+1}.")
        if res['mask'] is None:
            curinstr[1].append((int(res['memloc']), int(res['memval'],)))
        else:
            if curinstr:
                instrs.append(curinstr)
            curinstr = (res['mask'], [],)
    return instrs

def part1(instructions: List[Tuple[str, List[Tuple[int, int]]]]) -> int:
    ...


def part2(instructions: List[Tuple[str, List[Tuple[int, int]]]]) -> int:
    ...


if __name__ == '__main__':
    instructions = read_input('input_day14a.txt')


    #print(f"Part 1: bus * (time-stamp) = {part1(datapt1)}")
    #print(f"Part 2: earliest timestep at which bus conditions apply = {part2(data)}")

    #(mask = (.+)\n(?:mem\[(\d+)?] = (\d+)?\n)+)

