from pathlib import Path
from typing import Tuple, List


def answer_part1(inpath: Path) -> int:
    with open(inpath, 'r') as filehandle:
        num_yes_ans = 0
        for group in filehandle.read().split('\n\n'):
            answerset = set(group.replace('\n', ''))
            num_yes_ans += len(answerset)
        return num_yes_ans


def answer_part2(inpath: Path) -> int:
    with open(inpath, 'r') as filehandle:
        all_answers = [line.split('\n') for line in filehandle.read().split('\n\n')]
        all_answered_yes_sum = 0
        for group in all_answers:
            combined_group_answers = ''.join(group)
            answerset = set(combined_group_answers)
            n_groupmembers = len(group)
            all_answered_yes_sum += \
                sum(1 for letter in answerset if combined_group_answers.count(letter) == n_groupmembers)
        return all_answered_yes_sum


if __name__ == '__main__':

    infile = Path(__file__).parent / 'input_day6.txt'

    print("The sum over the groups of questions from which any was answered with 'yes' is: ", answer_part1(infile))
    print("The sum of questions to which yes was answered by all group members summed over all groups: ",
          answer_part2(infile))
