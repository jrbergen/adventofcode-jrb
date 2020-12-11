from pathlib import Path
from typing import List


def read_voltages(inpath: Path) -> List[int]:
    return [int(x) for x in inpath.read_text().split('\n') if x]


def part1(adapters: List[int], vdelta_max: int = 3, starting_v: int = 0):

    adapters = sorted(adapters)
    difs = dict()
    cur_v = starting_v
    while adapters:

        min_v, choices = min(adapters[:vdelta_max]), adapters[:vdelta_max]
        choice_index = choices.index(min_v)+1
        delta_v = min_v - cur_v

        try:
            difs[delta_v] += 1
        except KeyError:
            difs[delta_v] = 1

        cur_v += delta_v
        adapters = adapters[choice_index:]
    try:
        difs[3] += 1  # Device always counts as 1 +3 voltage
    except KeyError:
        difs[3] = 1

    return difs[1]*difs[3]


def part2(vouts: List[int], vdelta_max: int = 3, starting_v: int = 0):

    vouts = sorted([vout + starting_v for vout in vouts])
    assert starting_v < vouts[0]
    vouts.insert(starting_v, 0)

    adapters = {}
    for idx, vout in zip(range(len(vouts)-1, -1, -1), reversed(vouts)):
        startidx = idx-vdelta_max if idx-vdelta_max >= 0 else 0
        adapters[vout] = tuple(v for v in vouts[startidx:idx] if vout - v <= vdelta_max)
    adapters = {key: adapters[key] for key in sorted(adapters.keys())}

    counts = {adap: 0 for adap in adapters}
    counts[starting_v] = 1
    for voltage, inputs in adapters.items():
        for input_ in inputs:
            counts[voltage] += counts[input_]

    return counts[max(vouts)]


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day10.txt')

    v_outs = read_voltages(datapath)

    print(f"\nPart 1:\n\tMultiple of 1 and 3 'jolt' differences: {part1(v_outs)}")
    print(f"\nPart 2:\n\t Number of possible arrangements = {part2(v_outs)}")
