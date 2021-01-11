import itertools
from functools import reduce
from math import gcd
from pathlib import Path
from typing import Union, List, Tuple

from numba import njit
from numba.typed import List as nlist

import dill as pickle


def read_input(filepath: Union[str, Path]) -> Tuple[int, List[int]]:
    data = Path(filepath).resolve().read_text().split('\n')
    return 0, [2, 0, 11, 7]  # [17, 0, 13, 19]#[2,7,12]#1789,37,47,1889]
    # return int(data[0]), [int(bus) if bus != 'x' else 0 for bus in data[1].split(',')]


def iter_buses(buses, time) -> int:
    for bus in buses:
        if time % bus == 0:
            return bus
    return 0


def part1(data: Tuple[int, List[int]]) -> int:
    stamp, buses = data
    buses = [x for x in buses if x != 0]
    time = stamp
    while True:
        bus = iter_buses(buses, time)
        if bus:
            return bus * (time - stamp)
        time += 1


@njit(parallel=True)
def part2(data: Tuple[int, List[int]]) -> int:
    buses = nlist()
    startbuses = nlist()
    timedeltas = nlist()
    # for startbus in data[-1]:
    for startbus in data:
        startbuses.append(startbus)
    for i, startbus in enumerate(startbuses):
        if startbus != 0:
            timedeltas.append(i)
            buses.append(startbus)
    # print("Buses", buses)
    # print("Timedeltas", timedeltas)
    limit = 300_000_000
    time = buses[0]
    # while True:
    for t in range(1, limit + 1):
        # if time % 30_000_000 == 0:
        # print("search step", time)

        for dt, bus in zip(timedeltas, buses):
            if (time + dt) % bus != 0:
                break
        else:
            return time
        time += 1
    return -10


def part2_python(data: Tuple[int, List[int]]) -> int:
    buses = data  # [-1]
    dts = [t for t, bus in enumerate(buses) if bus != 0]
    buses = [bus for bus in buses if bus != 0]
    # print(f"Time deltas: {', '.join(str(t) for t  in dts)}")
    # print(f"Buses: {', '.join(str(b) for b in buses)}")

    time = min(buses)
    while True:
        # if time % 1_000_000 == 0:
        # print("search step", time)

        for dt, bus in zip(dts, buses):
            # print(gcd())
            if (time + dt) % bus != 0:
                break
            else:
                pass  # print(bus, dt, gcd(bus, dt))
        else:
            # print(f"Time deltas: {', '.join(str(t) for t in dts)}")
            # print(f"Buses: {', '.join(str(b) for b in buses)}")
            # print(f"First occuring time: {time}")
            return time
        time += 1

        if time > 30_000_000:
            return -10


class Attempt:

    def __init__(self, data: List[int], answer: int):
        self.data = data
        self.n_odd = len([x for x in data if x % 2 != 0])
        self.n_even = len([x for x in data if x % 2 == 0])
        self.solved = True if answer >= 0 else False
        self.grcd = reduce(lambda x, y: gcd(x, y), data)


if __name__ == '__main__':
    # data = read_input('input_day13.txt')

    # print(f"Part 1: bus * (time-stamp) = {part1(data)}")
    attempts = []
    a = nlist()
    for x in itertools.combinations_with_replacement([0, 2, 3, 4, 12], 5):
        if x.count(0) <= 2:
            a.append(nlist(x))
    tot = len(a)

    for i, data in enumerate(a):
        print(f'{(i / tot) * 100:.2f} %...', end='\r')

        attempts.append(Attempt(data=data, answer=part2_python(data)))

        # print(f"Temporary breakpoint in {__name__}")
        # print(f"Part 2: earliest timestep at which bus conditions apply = {part2_python(data)}")
        # print(f"Part 2: earliest timestep at which bus conditions apply = {part2(data)}")
    # print(f"Temporary breakpoint in {__name__}")

    with open("attempts.pkl", 'wb') as f:
        pickle.dump(f)

    print(f"Temporary breakpoint in {__name__}")
