from pathlib import Path
from typing import Tuple, List


def read_input(inpath: Path):
    with open(inpath, 'r') as infile:
        return tuple(line for line in (line.rstrip() for line in infile) if line)


def bin_instruction_to_int(instruction: str, zero_char: str, one_char: str) -> int:
    """Converts binary instruction to integer position"""
    instruction = ''.join(char for char in instruction if char in (one_char, zero_char,))
    return int(instruction.replace(one_char, '1').replace(zero_char, '0'), 2)


def get_seat_location(instruction: str) -> Tuple[int, int]:
    return bin_instruction_to_int(instruction, 'F', 'B'), bin_instruction_to_int(instruction, 'L', 'R')


def get_seat_id(seat_row: int, seat_col: int, seat_mult: int = 8) -> int:
    return seat_row * seat_mult + seat_col


def get_seat_locations(instructions: Tuple[str, ...]):
    for instruction in instructions:
        yield get_seat_location(instruction)


def find_seat_id(seat_ids: List[int]) -> int:
    """
    Finds missing seat ID in a list of seat ids assuming that seatID - 1 and seatID + 1 are on the list
    Also assumes that there is only one missing value in the list in concordance the constraint above.

    :param seat_ids: list of seat id integers
    :returns: seat id if found, -1 if seat id was not found
    """
    seat_ids = sorted(seat_ids)
    for cur_id, next_id in zip(seat_ids[:-2], seat_ids[2:]):
        if next_id != cur_id + 2:
            return cur_id + 2
    print("Seat not found!")
    return -1


if __name__ == '__main__':
    inputpath = Path(__file__).parent / 'input_day5.txt'

    data = read_input(inputpath)

    # Note: for large input (e.g. boarding pass list for planetary-scale interstellar ant transportation vehicles),
    #  list() could be avoided as to not put everything into RAM, and itertools.tee could be used here to require only
    #  one iteration over the dataset for value and maximum.

    seat_id_lst = list(get_seat_id(seatrow, seatcol) for seatrow, seatcol in get_seat_locations(instructions=data))

    # Answer part 1
    max_seat_id = max(seat_id_lst)

    # Answer part 2
    your_seat_id = find_seat_id(seat_id_lst)

    print(f"Max seat id = {max_seat_id}")
    print(f"Your seat id = {your_seat_id if your_seat_id >= 0 else 'NOT FOUND'}")
