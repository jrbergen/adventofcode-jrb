from pathlib import Path
from typing import Union, List, NoReturn
from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' % \
          (f.__name__, te-ts))
        return result
    return wrap


def read_instructions(text_file: Union[str, Path]) -> List[List[Union[str, int]]]:
    text_file = text_file if isinstance(text_file, Path) else Path(text_file).resolve()
    return [[line.split(' ')[0], int(line.split(' ')[1])] for line in text_file.read_text().split('\n') if line]


@timing
def part1(program: List[List[Union[str, int]]]) -> NoReturn:
    acc, readhead = 0, 0
    ran_instructions = set()

    while True:
        if readhead in ran_instructions:
            print(f"Oh no! Program entered infinite loop... Breaking with accumulator value: {acc}.")
            break

        instruction, value = program[readhead]

        if readhead > len(program) + 1 or readhead < 0:
            break

        ran_instructions.add(readhead)

        if instruction == 'nop':
            readhead += 1
        elif instruction == 'acc':
            acc += value
            readhead += 1
        elif instruction == 'jmp':
            readhead += value
    print("Program ended!")


def bruteforce_instruction_replacement(repl_idx: List[int], replacement: str,
                                       program: List[List[str]], verbose: bool = False):
    bruteforce_attempts = 0
    program = tuple(program)
    for repl_index in repl_idx:

        oldval = program[repl_index][0]
        program[repl_index][0] = replacement

        acc, readhead = 0, 0

        ran_instructions = set()

        while True:

            if readhead > len(program) - 1 or readhead < 0:
                print('\n'.join([f"Found terminating state after {bruteforce_attempts} replacement attempts...",
                                 f"Value of 'acc' upon termination was: {acc}",
                                 f"Program terminates if '{oldval}' at line {repl_index} is ",
                                 f"replaced by '{replacement}'"]))
                return True

            if readhead in ran_instructions:
                if verbose:
                    print("Oh no! Program entered infinite loop... Breaking.")
                    print(f"Last acc = {acc}")
                bruteforce_attempts += 1
                program[repl_index][0] = oldval
                break

            instruction, value = program[readhead]

            ran_instructions.add(readhead)

            if instruction == 'nop':
                readhead += 1
            elif instruction == 'acc':
                acc += value
                readhead += 1
            elif instruction == 'jmp':
                readhead += value
    return False


@timing
def part2(program: List[List[Union[str, int]]]) -> NoReturn:
    nopidx = [lineno for lineno, instr in enumerate(program) if instr[0] == 'nop']
    jmpidx = [lineno for lineno, instr in enumerate(program) if instr[0] == 'jmp']

    for idxlist, repl in zip((nopidx, jmpidx,), ('jmp', 'nop',)):
        if bruteforce_instruction_replacement(idxlist, replacement=repl, program=program):
            break
    else:
        print("The attempted replacements did not lead to a terminating program :(")


if __name__ == '__main__':
    program = read_instructions(Path(Path(__file__).parent / 'input_day8.txt'))

    print("\nPart 1:\n")
    part1(program)

    print("\n\nPart 2:\n")
    part2(program)
