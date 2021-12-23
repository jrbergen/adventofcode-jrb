import functools
import math
from pathlib import Path
from typing import Optional

import numpy as np
from numpy import ndarray

INPUT_PATH_16: Path = Path(__file__).parent.joinpath('input16.txt')
INPUT_PATH_16_EXAMPLE: Path = Path(__file__).parent.joinpath('input16-example.txt')

def hex_to_bin(hexstr: str):
    return f'{int(hexstr, 16):#04b}'

def parse_input(inputpath: Path):
    return [hex_to_bin(s.strip()) for s in inputpath.read_text(encoding='utf-8').split('\n') if s]


class Packet:

    def __init__(self, s: str):
        self.s = s
        self.header = s[:6]

        self.payload = s[6:]
        self.version: int = int(self.header[:3], 2)
        self.type_id: int = int(self.header[3:], 2)
        self.length_type_id = None
        self.n_subpackets: Optional[int] = None
        self.bits_subpackets: Optional[int] = None

        self.children = set()

    def payload_as_chunks(self) -> list[str]:
        return [self.payload[i * 5 + 1:i * 5 + 5] for i in range(math.floor(len(self.payload) / 5))]

    def decode(self):
        match self.type_id, self.version:
            case 4, _:
                return int(''.join(self.payload_as_chunks()), 2)
            case _, _:
                if (length_type_id := int(self.payload[0][0])):
                    self.n_subpackets = int(''.join(self.payload)[1:12], 2)
                else:
                    self.bits_subpackets = int(''.join(self.payload)[1:15], 2)
                self.length_type_id = length_type_id


    def __hash__(self):
        return hash(self.header + ''.join(self.payload))

    def __str__(self):
        return f"{type(self).__name__}(" \
               + ', '.join(f'{name}={val}' for name, val in vars(self).items()) + ')'

if __name__ == '__main__':
    #bincodes = parse_input(INPUT_PATH_16)
    #'D2FE28'
    bincodes = [hex_to_bin('D2FE28'), hex_to_bin('38006F45291200')]
    packets = []
    for bincode in bincodes:
        p = Packet(bincode)
        p.decode()
        packets.append(p)


    print(f"Temporary breakpoint in {__name__}")
