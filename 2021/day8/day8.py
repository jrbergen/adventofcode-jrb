from __future__ import annotations

import functools
import itertools
from collections import Counter
from pathlib import Path
from frozendict import frozendict

import numpy as np

INPUT_PATH: Path = Path(__file__).parent.joinpath('input8.txt')

N_DIGITS_PER_SYMBOL: dict[int, set[int]] = {2: {1},
                                            3: {7},
                                            4: {4},
                                            5: {2, 3, 5},
                                            6: {0, 6, 9},
                                            7: {8}}

N_SYMBOLS_PER_DIGIT: dict[int, int] = {0: 6,
                                       1: 2,
                                       2: 5,
                                       3: 5,
                                       4: 4,
                                       5: 5,
                                       6: 6,
                                       7: 3,
                                       8: 7,
                                       9: 6}
REFERENCE_POSITIONS: dict[int, str] = {0: 'ABCEFG', 1: 'CF', 2: 'ACDEG', 3: 'ACDFG', 4: 'BCDF',
                                       5: 'ABDFG', 6: 'ABDEFG', 7: 'ACF', 8: 'ABCDEFG', 9: 'ABCDFG'}

REFERENCE_DIGITS: dict[str, set[int]] = {'A': {0, 2, 3, 5, 6, 7, 8, 9},
                                         'B': {0, 4, 5, 6, 8, 9},
                                         'C': {0, 1, 2, 3, 4, 7, 8, 9},
                                         'D': {0, 2, 3, 5, 6, 7, 8, 9},
                                         'E': {0, 2, 3, 5, 6, 7, 8, 9},
                                         'F': {0, 2, 3, 5, 6, 7, 8, 9},
                                         'G': {0, 2, 3, 5, 6, 7, 8, 9},
                                         }

def parse_input(filepath: Path) -> tuple[tuple[list[str], list[str]]]:
    processed: list[list[list[str]]] = [
        [linepart.split(' ') for linepart in line.split('|') if linepart]
        for line in filepath.read_text(encoding='utf-8').split('\n') if line
    ]

    for iientry, entry in enumerate(processed):
        processed[iientry] = (tuple(experiment for experiment in entry[0] if experiment),
                              tuple(digitoutput for digitoutput in entry[1] if digitoutput))
    return tuple(processed)


@functools.lru_cache(maxsize=1)
def get_all_hypotheses(valid_symbols: str) -> set[frozendict[str, str]]:
    hypotheses = set()
    for permutation in itertools.permutations(valid_symbols, r=len(valid_symbols)):
        hypotheses.add(frozendict({ref: candidate for ref, candidate in zip(valid_symbols, permutation)}))
    return hypotheses




def proces_candidate_evidence(experiments: list[str], valid_symbols: str = 'abcdefg'):

    hypotheses = set()
    for permutation in itertools.permutations(valid_symbols, r=len(valid_symbols)):
        hypotheses.add(frozendict({ref: candidate for ref, candidate in zip(valid_symbols.upper(), permutation)}))

    refpositions_sorted = sorted(REFERENCE_POSITIONS.items(), key=lambda kv: len(kv[1]))
    for experiment_symbols in experiments:
        #for refernce_position in REFERENCE_POSITIONS.sort:
        #match len(experiment_symbols):
        for refposition in refpositions_sorted:
            for hypothesis in hypotheses:

                if any(hypothesis[refposition] not in experiment_symbols.upper()):
                    hypotheses.remove(hypothesis)
                #hypotheses.remove(hypothesis)
        # for
        #     case 2:
        #
        #     case _:
        #         ...
        # #if len(experiment_symbols) == 2:



    possibilities_per_symbol: dict[str, dict[int, int]] = {sym: {num: 0 for num in range(10)} for sym in valid_symbols}
    #possibilities_per_symbol: dict[str, dict[int, int]] = {sym: {num: 0 for num in range(10)} for sym in valid_symbols}

    candidates: dict[str, set[int]] = {sym.upper(): set(valid_symbols) for sym in valid_symbols}
    # set(range(10)) for sym in valid_symbols}

    # First truncate problem set by removing impossible candidates
    # for experiment_symbols in experiments:
    #     n_symbols = len(experiment_symbols)
    #     possible_digits = N_DIGITS_PER_SYMBOL[n_symbols]
    #     impossible_digits = set(range(10)) - set(possible_digits)
    #
    #     for impossible_digit in impossible_digits:
    #         REFERENCE_POSITIONS[impossible_digit]


            #for reference_num, reference_symbols in REFERENCE_POSITIONS:


#        for digit, refsymbols in REFERENCE_POSITIONS.items():

    print(f"Temporary breakpoint in {__name__}")

        #for symbol in experiment_symbols:
         #   for possible_digit in possible_digits:
          #      possibilities_per_symbol[symbol][possible_digit] += 1

    print(f"Temporary breakpoint in {__name__}")

def get_valid_symbols_from_parsed_input(parsed_input: tuple[tuple[list[str], list[str]]]) -> str:
    symbols = set()
    for experimentsymbols, outputsymbols in parsed_input:
        for experimentchars in experimentsymbols:
            symbols.update(set(experimentchars))
        for outputchars in outputsymbols:
            symbols.update(set(outputchars))
    return ''.join(sorted(list(symbols)))


def check_hypothesis(hypothesis: dict[str, str], data: list[str], outcomes: list[str]) -> bool:
    refpos: dict[int, str] = {0: 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf',
                              5: 'abdfg', 6: 'abdefg', 7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
    refnums = {v: k for k, v in refpos.items()}

    hypothesized_translation_num_to_str = {num: ''.join([hypothesis[x] for x in reference])
                                           for num, reference in refpos.items()}
    hypothesized_translation_str_to_num = {v: k for k, v in hypothesized_translation_num_to_str.items()}

    output_num = ''
    for segmentnumberstring in outcomes:
        try:
            output_num += str(hypothesized_translation_str_to_num[segmentnumberstring])
        except KeyError:
            return False

    print(f"Temporary breakpoint in {__name__}")

   # if hypothesis[]


def exercise_a():
    outtuples = parse_input(INPUT_PATH)
    n_unique_digits = 0
    for _, digitoutput in outtuples:
        n_unique_digits += sum(len(suboutput) in (2, 3, 4, 7) for suboutput in digitoutput)
    print(f"Day 8, exercise A: digits 1, 4, 7, or 8 appear {n_unique_digits} times.")


def exercise_b():
    outtuples = parse_input(INPUT_PATH)
    valid_symbols = get_valid_symbols_from_parsed_input(parsed_input=outtuples)



    for data, outcome in outtuples:
        for hypothesis in (hypotheses := get_all_hypotheses(valid_symbols=valid_symbols)):
            valid = check_hypothesis(hypothesis=hypothesis, data=data, outcomes=outcome)


    #
    # REF_POSITIONS: dict[int, str] = {0: 'ABCEFG', 1: 'CF', 2: 'ACDEG', 3: 'ACDFG', 4: 'BCDF',
    #                                  5: 'ABDFG', 6: 'ABDEFG', 7: 'ACF', 8: 'ABCDEFG', 9: 'ABCDFG'}
    # #REF_LENS: dict[int, int] = {k: len(v) for k, v in REF_POSITIONS.items()}
    # REFERENCE_DIGITS: dict[str, set[int]] = {'A': {0, 2, 3, 5, 6, 7, 8, 9},
    #                                          'B': {0, 4, 5, 6, 8, 9},
    #                                          'C': {0, 1, 2, 3, 4, 7, 8, 9},
    #                                          'D': {0, 2, 3, 5, 6, 7, 8, 9},
    #                                          'E': {0, 2, 3, 5, 6, 7, 8, 9},
    #                                          'F': {0, 2, 3, 5, 6, 7, 8, 9},
    #                                          'G': {0, 2, 3, 5, 6, 7, 8, 9},
    #                                          }
    # REF_LENS: dict[str, set[int]] = {sym: {len(v) for k, v in REF_POSITIONS.items() if sym.upper() in v} for sym in valid_symbols}
    #
    # countref: dict[int, str] = {
    #     2: 'cf',
    #     3: 'acf',
    #     4: 'bcdf',
    #     7: 'abcdefg',
    # }
    # refpositions_sorted = sorted(REF_LENS.items(), key=lambda kv: len(kv[1]))
    #
    # for experiments, output in outtuples:
    #     possibilities: dict[str, set(str)] = {k: set(valid_symbols) for k in valid_symbols}
    #     for experiment in experiments:
    #         n_segments_lit = len(experiment)
    #         for count, syms in countref.items():
    #             if n_segments_lit == count:
    #                 for expsym in experiment:
    #                     possibilities[expsym] = set(countref[count])
    #                     for key in possibilities:
    #                         if key != expsym:
    #                             possibilities[key] -= set(countref[count])
    #


            #         for pkey, pval in possibilities.items():
            #             if pkey not in 'cf':
            #                 possibilities[pkey] -= set(experiment)
            #
            #
            #     possibilities['f'] = set(experiment)
            # cur_possibilities = set(k for k, v in REF_LENS.items() if n_segments_lit in v)


        print(f"Temporary breakpoint in {__name__}")
            #for ref_digit in ref_digitsif len(experiment) == 1:

          #      print(f"Temporary breakpoint in {__name__}")
         #  3 ...



        print(f"Temporary breakpoint in {__name__}")
    print(f"Temporary breakpoint in {__name__}")

    #output_value_sum: int = -1
    print(f"Day 8, exercise B: sum of decoded output values: {output_value_sum}.")


if __name__ == '__main__':
    #exercise_a()
    exercise_b()
    # valid_symbols = get_valid_symbols_from_parsed_input(parsed_input=outtuples)
    # hypotheses = get_all_hypotheses(valid_symbols=valid_symbols)
    #
    #
    #
    # for experiments_entry, digitoutput in outtuples:
    #     proces_candidate_evidence(experiments=experiments_entry, valid_symbols=valid_symbols)
    #     #hypothesis={symbol.upper(): None for symbol in valid_symbols}

        #if data





        #proces_candidate_evidence(experiments=experiments_entry)

      #  print(f"Temporary breakpoint in {__name__}")
    #proces_candidate_evidence(experiments=)

    print(f"Temporary breakpoint in {__name__}")
