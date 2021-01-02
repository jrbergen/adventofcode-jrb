from functools import reduce
from math import gcd
from pathlib import Path
from typing import Union, List, Tuple


def read_input(filepath: Union[str, Path]) -> Tuple[int, List[int]]:
    data = Path(filepath).resolve().read_text().split('\n')
    return 0, [17, 0, 13, 19]  # [2,7,12]#1789,37,47,1889]
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


def lpf(n):
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
    return n


def pf(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


from numba import njit


# @njit()
def part2(data: Tuple[int, List[int]], limit: int = 1_210_000_000) -> int:
    buses = data  # data[-1]
    dts = [t for t, bus in enumerate(buses) if bus != 0]
    buses = [bus for bus in buses if bus != 0]
    # for (i, dt), bus in zip(enumerate(dts), buses):
    #     if not is_prime(bus):
    #         raise ValueError(
    #             "This algo is only guaranteed to work for prime numbers! Not all input numbers were prime...")
    #     print(gcd(bus, buses[+1]))#print(bus**())
    for i in range(len(buses) - 1):
        print(gcd(buses[i], buses[i + 1]))
    # print(f"Time deltas: {', '.join(str(t) for t  in dts)}")
    # print(f"Buses: {', '.join(str(b) for b in buses)}")
    compa = set(pf(r(buses))) & set(pf(r([bus + dt for bus, dt in zip(buses, dts)])))
    #    for bb in bbus+offset
    t = 0  # min(buses)
    while True:
        # if time % 1_000_000 == 0:
        # print("search step", time)
        # okcnt = 0

        for dt, bus in zip(dts, buses):
            if (t + dt) % bus != 0:
                break
        else:
            return t
            # if t > 3416:
        # for
        #     a = True if gcd(t + dt, bus) == 1 else False
        # if a:
        #     print("EULER! A")
        #     print(f"\n### t = {t} ###")
        #     print("BUS: ", bus)
        #     print("t: ", t)
        #     print("dt: ", dt)

        # print("EULER", gcd(t+dt, bus)==1)
        # print("PRIME dT: ", pf(dt))
        # print("t+dt: ", t+dt)
        # print("PRIME t+dt: ", is_prime(t+dt))# pf(t+dt))
        # print("(t+dt) % bus: ", (t+dt)%bus)
        # print("IS PRIME t=dt?: ", "YES" if is_prime(t+dt) else "no...")

        # print()
        # print(bus, pf(bus), t+dt, dt, pf(t+dt))
        # print(gcd())
        # if bus+dt

        # if (t + dt) % bus == 0:
        #  okcnt += 1
        # else:
        # pass  # print(bus, dt, gcd(bus, dt))

        # pf =
        # print(f"ISPRIME MULTIPLIED??", is_prime(reduce(lambda x, y: x*y, [t+dt+b for b, dt in zip(buses, dts)])))
        # print(f"PRIME FACTORS MULTIPLIED bus * T: {pf(reduce(lambda x, y: x*y, [t+dt for b, dt in zip(buses, dts)]))}")
        # if okcnt == 3:
        # return t  # break#else:
        # print(f"Time deltas: {', '.join(str(t) for t in dts)}")
        # print(f"Buses: {', '.join(str(b) for b in buses)}")
        # print(f"First occuring time: {time}")
        # return t
        # print(f"\n\n@@@@@@@@@@@@@@TIMESTEP  {t}    TIMESTEP@@@@@@@@@@@@@@@@\n")
        t += 1

        if t > limit:
            return -1


class Attempt:

    def __init__(self, data: List[int], answer: int):
        self.data = data
        self.n_odd = len([x for x in data if x % 2 != 0])
        self.n_even = len([x for x in data if x % 2 == 0])
        self.solved = True if answer >= 0 else False
        self.grcd = reduce(lambda x, y: gcd(x, y), data)


def cset(a, b):
    r = set(pfa(a)).intersection(set(pfa(b)))
    if len(r) == 1:
        return list(r)[0]
    else:
        raise ValueError("Not a single prime remaining")


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def pfa(l):
    return tuple(a for b in [pf(x) for x in l] for a in b)


def r(l):
    l = tuple(l for l in l if l != 0)
    return reduce(lambda x, y: x * y, l)


def rg(l):
    l = tuple(l for l in l if l != 0)
    return reduce(lambda x, y: gcd(x, y), l)


def phi(primes: List[int]):
    return r(p - 1 for p in primes)


def euler(l):
    l = tuple(l for l in l if l != 0)
    return reduce(lambda x, y: pf(y))


if __name__ == '__main__':
    data = read_input('input_day13.txt')

    bbuses = {(17, 0, 13, 19): 3417,
              (67, 0, 7, 59, 61): 754018,
              (67, 7, 0, 59, 61): 1261476,
              (1789, 37, 47, 1889): 1202161486}

    answers = list(bbuses.values())

    a1, a2, a3, a4 = answers
    bb = list(bbuses.keys())
    b1, b2, b3, b4 = bb
    bbo = tuple(tuple(i + b for i, b in enumerate(bus)) for bus in bb)
    o1, o2, o3, o4 = bbo
    c1, c2, c3, c4 = tuple(cset(x, y) for x, y in zip(bb, bbo))

    print(f"Temporary breakpoint in {__name__}")

    for bb, aa in zip(bbuses, answers):
        print("\n\n###")
        print(f"prime factors of ans {aa}: {pf(aa)}")
        # print(f"pf for bbus: {pf(bb)}")
        print(f"pf for product of buses: {pf(r([b for b in bb if b]))}")
        print(f"pf for product of buses + offset: {pf(r([b + i for i, b in enumerate(bb)]))}")

    td = (17, 0, 13, 19)

    tdo = [x + i for i, x in enumerate(td) if x]
    print(cset(o1, b1))
    print(f"Part 2: earliest timestep at which bus conditions apply = {part2(b2)}")
    #    target =
    print(f"Temporary breakpoint in {__name__}")

    # print(f"Part 1: bus * (time-stamp) = {part1(data)}")

    # for i, data in enumerate(a):
    # print(f'{(i / tot) * 100:.2f} %...', end='\r')
    # ints = data[-1]
    # for i in ints:
    #     if i:
    #         if is_prime(i):
    #             print(f'{i} is prime!!')
    #         else:
    #             print("NOT A PRIME NOT A PRIME NOT A PRIME")
    #

    # attempts.append(Attempt(data=data, answer=part2_python(data)))

    # print(f"Temporary breakpoint in {__name__}")
    # print(f"Part 2: earliest timestep at which bus conditions apply = {part2_python(data)}")

    # print(f"Temporary breakpoint in {__name__}")

    print(f"Temporary breakpoint in {__name__}")
