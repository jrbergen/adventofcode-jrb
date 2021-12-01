from pathlib import Path


def answer_part1(inpath: Path) -> int:
    with open(inpath, 'r') as filehandle:
        return sum((len(set(line.replace('\n', ''))) for line in filehandle.read().split('\n\n')))


def answer_part2(inpath: Path) -> int:
    with open(inpath, 'r') as filehandle:
        all_answers = [line.split('\n') for line in filehandle.read().split('\n\n')]
        return sum(sum(1 for letter in set(''.join(group)) if ''.join(group).count(letter) == len(group))
                   for group in all_answers)


if __name__ == '__main__':
    infile = Path(__file__).parent / 'input_day6.txt'
    example = infile.parent / 'example_input_day6.txt'
    print("The sum over the groups of questions from which any was answered with 'yes' is: ", answer_part1(infile))

    print("The sum of questions to which yes was answered by all group members summed over all groups: ",
          answer_part2(infile))
