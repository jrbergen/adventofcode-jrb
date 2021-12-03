from __future__ import annotations

import os
from abc import ABCMeta
from dataclasses import dataclass
from pathlib import Path

INPUT_PATH_2A: Path = Path(__file__).parent.joinpath('input3a.txt')
INPUT_PATH_2B: Path = INPUT_PATH_2A  # Same inputs for A and B


@dataclass
class Point2D:
    x: int
    y: int


class AbstractMovingVehicle(metaclass=ABCMeta):

    def move(self, direction: str, magnitude: int) -> None:
        ...

    def read_instructions(self, instruction_path: os.PathLike) -> None:
        ...

    def execute_instructions(self) -> None:
        ...


class SubmarineBase(AbstractMovingVehicle):

    VALID_DIRECTIONS: tuple[str, ...] = ('forward', 'up', 'down')

    def __init__(self, verbose: bool = False):
        self.pos: Point2D = Point2D(0, 0)
        self.instructions: list[str] = []
        self.verbose: bool = verbose

    def move(self, direction: str, magnitude: int) -> None:
        raise NotImplementedError("Called basemethod")

    def read_instructions(self, instruction_path: os.PathLike):
        self.instructions: list[str] = [inst for inst in Path(instruction_path).read_text(encoding='utf-8').strip().split('\n')
                                        if inst]

    def execute_instructions(self) -> None:
        for inst in self.instructions:
            direction_, (magnitude_) = inst.split(' ')
            magnitude_ = int(magnitude_)
            self.move(direction=direction_, magnitude=magnitude_)
            if self.verbose:
                print(f"Moving {direction_} with magnitude {magnitude_}.")
        print(f"Ended up in position {self.pos}. Multiplied")

    @property
    def multiplied_position(self) -> int:
        mpos = self.pos.y * self.pos.x
        print(f"{type(self).__name__}: multiplied x*y pos = {self.pos.x * self.pos.y}.")
        return mpos


class SubmarineA(SubmarineBase):

    def move(self, direction: str, magnitude: int) -> None:
        match direction:
            case 'forward':
                self.pos.x += magnitude
            case 'up':
                self.pos.y -= magnitude
            case 'down':
                self.pos.y += magnitude
            case _:
                raise ValueError(f"Invalid direction: {direction!r}. Valid directions: {', '.join(SubmarineA.VALID_DIRECTIONS)}.")


class SubmarineB(SubmarineBase):

    def __init__(self):
        super().__init__()
        self.aim = 0

    def move(self, direction: str, magnitude: int) -> None:
        match direction:
            case 'forward':
                self.pos.x += magnitude
                self.pos.y += self.aim * magnitude
            case 'up':
                self.aim -= magnitude
            case 'down':
                self.aim += magnitude
            case _:
                raise ValueError(f"Invalid direction: {direction!r}. Valid directions: {', '.join(SubmarineB.VALID_DIRECTIONS)}.")


def exercise_a() -> int:
    subma = SubmarineA()
    subma.read_instructions(instruction_path=INPUT_PATH_2A)
    subma.execute_instructions()
    return subma.multiplied_position


def exercise_b() -> int:
    submb = SubmarineB()
    submb.read_instructions(instruction_path=INPUT_PATH_2B)
    submb.execute_instructions()
    return submb.multiplied_position


if __name__ == '__main__':
    exercise_a()
    exercise_b()
