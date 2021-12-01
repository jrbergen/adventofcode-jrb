from pathlib import Path
from typing import Union, List, Tuple


def read_input(filepath: Union[str, Path]) -> Tuple[int, List[int]]:
    data = Path(filepath).resolve().read_text().split('\n')
    return int(data[0]), [int(bus) if bus != 'x' else 0 for bus in data[1].split(',')]


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


def part2(buses: Tuple[int, List[int]]) -> int:
    dts = [t for t, bus in enumerate(buses) if bus != 0]
    buses = [bus for bus in buses if bus != 0]
    n_buses = len(buses)

    timestep = buses[0]
    t = timestep

    step = 0
    lockpos = 1
    print("TIMESTEP = ", timestep)
    while True:
        step += 1
        if (t + dts[lockpos]) % buses[lockpos] == 0:
            timestep *= buses[lockpos]
            lockpos += 1
            print("TIMESTEP = ", timestep)
        if lockpos == n_buses:
            print(f"TOTAL STEPS: {step}")
            return t
        t += timestep


if __name__ == '__main__':
    datapt1 = read_input('input_day13.txt')
    data = datapt1[-1]

    print(f"Part 1: bus * (time-stamp) = {part1(datapt1)}")
    print(f"Part 2: earliest timestep at which bus conditions apply = {part2(data)}")

    # bbuses = {(17, 0, 13, 19): 3417,
    #           (67, 0, 7, 59, 61): 754018,
    #           (67, 7, 0, 59, 61): 1261476,
    #           (1789, 37, 47, 1889): 1202161486}
    #
    # answers = list(bbuses.values())
    #
    # a1, a2, a3, a4 = answers
    # bb = list(bbuses.keys())
    # b1, b2, b3, b4 = bb
    #
    # bbo = tuple(tuple(i + b for i, b in enumerate(bus)) for bus in bb)
    # o1, o2, o3, o4 = bbo
    # c1, c2, c3, c4 = tuple(prime_factors_intersect(x, y, mode='max') for x, y in zip(bb, bbo))
    #
    # b5 = data
    # o5 = tuple(i + b for i, b in enumerate(b5))
    # for sub in bb:
    #     print(f"Part 2: earliest timestep at which bus conditions apply = {part2(sub)}")
    # for bb, aa in zip(bbuses, answers):
    #     print("\n\n###")
    #     print(f"prime factors of ans {aa}: {prime_factors(aa)}")
    #     # print(f"prime_factors for bbus: {prime_factors(bb)}")
    #     print(f"prime_factors for product of buses: {prime_factors(reduce_mul_zero_skip([b for b in bb if b]))}")
    #     print(
    #         f"prime_factos for product of buses + offset: {prime_factors(reduce_mul_zero_skip([b + i for i, b in enumerate(bb)]))}")
