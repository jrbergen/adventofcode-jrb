# Author: Joost Dorscheidt
from pathlib import Path
from typing import List, Tuple


def parse_input(tfile: Path) -> List[List[str]]:
    with open(tfile, 'r') as f:
        return [line.split(" contain ") for line in f.read()[:-1].split('\n')]


def format_to_dict_with_count(bags: str) -> dict:
    return {format_to_single_with_count(b)[0]: format_to_single_with_count(b)[1] for b in bags[:-1].split(", ")}


def format_to_single_with_count(bag: str) -> Tuple[str, int]:
    if bag[:2] == "no":
        return bag, 0
    if bag[-1] == "g":
        return f"{bag[2:]}s", 1
    if bag[-1] == "s":
        return bag[2:], int(bag[0])


def part1(bags_list: List[List[str]], target_bag_str: str = "shiny gold bags"):
    bags_dict = {bag[0]: list(format_to_dict_with_count(bag[1]).keys()) for bag in bags_list}

    def get_parents(key):
        parents = {parent for parent in bags_dict.keys() if key in bags_dict[parent]}
        if not parents:
            return {key}
        return {el for key in parents for el in get_parents(key)} | parents

    return len(get_parents(target_bag_str))


def part2(bags_list: List[List[str]]):
    bags_dict = {bag[0]: format_to_dict_with_count(bag[1]) for bag in bags_list}

    def get_counts(key: str):
        if "no other bags" in bags_dict[key]:
            return 0
        return sum(count * get_counts(bag) + count for bag, count in bags_dict[key].items())

    return get_counts("shiny gold bags")


if __name__ == '__main__':
    infile = Path(Path(__file__).parent / 'input_day7.txt').resolve()
    print(part1(parse_input(infile)))
    print(part2(parse_input(infile)))
