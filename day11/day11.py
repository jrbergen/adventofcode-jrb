import itertools
from pathlib import Path
from typing import List, Tuple, Any

import numpy as np
from numpy import ndarray


def read_input(inpath: Path, ignore_val: str = '-2') -> List[List[int]]:
    return [[int(x.replace('.', ignore_val).replace('L', '0').replace('#', '1')) for x in y]
            for y in [list(x) for x in inpath.read_text().split('\n') if x]]


def part1_purepython(seatmat: List[List[int]], ignoreval: int = -2) -> Tuple[int, int]:
    row_offset = len(seatmat[0])
    seatlist = [x for y in seatmat for x in y]
    positions = (-row_offset - 1, -row_offset, -row_offset + 1, -1, 1, row_offset - 1, row_offset, row_offset + 1,)

    iteration = 0
    print("Calculating part 1:")
    while True:
        newseats = []
        for i, seat in enumerate(seatlist):
            sum_ = 0
            if seat == ignoreval:
                newseats.append(ignoreval)
                continue
            for position in positions:
                try:
                    curval = seatlist[i + position]
                except IndexError:
                    continue
                sum_ += curval if curval > 0 else 0
            if sum_ == 0 and not seat:
                newseats.append(1)
            elif sum_ > 3 and seat:
                newseats.append(0)
            else:
                newseats.append(seat)
        print(f"Iteration no: {iteration}", end='\r')
        if newseats == seatlist:
            return sum((x for x in seatlist if x > 0)), iteration
        seatlist = newseats
        iteration += 1


def explore(row:int, col: int, seat: int, newseats: List[List[int]], directions: Tuple[Tuple[int,int],...],
            num_directions: int, maxrow: int, maxcol: int, lastseats: List[List[int]], ignoreval: int, gtfo_thresh:int):

    if seat == -2:
        newseats[row][col] = -2
        return newseats

    occ, emp = 0, 0

    idx = -1
    curdirs = list(directions)
    dists = [1] * num_directions
    popped = 0

    while curdirs:
        idx = (idx + 1) % (num_directions - popped)

        dr, dc = curdirs[idx]
        dist = dists[idx]

        tgtrow, tgtcol = row + (dr * dist), col + (dc * dist)

        if tgtrow > maxrow or tgtcol > maxcol or tgtrow < 0 or tgtcol < 0:
            del curdirs[idx]
            del dists[idx]
            popped += 1
            continue

        curtgt = lastseats[tgtrow][tgtcol]

        if curtgt == ignoreval:
            dists[idx] += 1
            continue
        if curtgt == 0:
            emp += 1
        elif curtgt == 1:
            occ += 1

        popped += 1
        del curdirs[idx]
        del dists[idx]

        if occ >= gtfo_thresh:
            break

    if occ >= gtfo_thresh and seat:
        newseats[row][col] = 0
    elif occ == 0 and not seat:
        newseats[row][col] = 1
    else:
        newseats[row][col] = seat

    return newseats

def part2_purepython(seatmat: List[List[int]], ignoreval: int = -2,
                     gtfo_thresh: int = 5) -> Tuple[int, int]:

    niter = 0
    lastseats = seatmat
    directions = tuple({x for x in itertools.product([0, 1, -1, 1], [0, 1, -1, 1])} - {(0,0)})
    num_directions = len(directions)
    maxrow, maxcol = len(seatmat)-1, len(seatmat[0])-1

    while True:
        niter += 1
        print(f"Iteration: {niter}", end='\r')
        newseats = [[0 for _ in y] for y in lastseats]

        for row, col, seat in iterate_2dlist(lastseats):
            newseats = explore(row, col, seat, newseats, directions,
                               num_directions, maxrow, maxcol, lastseats,
                               ignoreval, gtfo_thresh)

        if newseats == lastseats:
            return sum((x for y in newseats for x in y if x > 0)), niter

        lastseats = newseats.copy()


def iterate_2dlist(nestedlist: List[List[Any]]):
    for row in range(len(nestedlist)):
        for col in range(len(nestedlist[row])):
            yield row, col, nestedlist[row][col]


def iterate_2darr(arr: ndarray, rowpad: int = 1, colpad: int = 1):
    for row in range(rowpad, arr.shape[0] - rowpad):
        for col in range(colpad, arr.shape[1] - colpad):
            yield row, col, arr[row, col]


def read_input_as_padded_array(inpath: Path, ignore_val: str = '-2') -> ndarray:
    """
    Returns seats as 2D np array with -1 for floor space, 0 for empty seats, and 1 for occupied seats.
    Increases hor. and ver. dimensions by 2 each, filled with nans to allow kernel iteration.
    """
    return np.pad(np.array(read_input(inpath, ignore_val), dtype=np.float32),
                  [(1, 1), (1, 1)], mode='constant', constant_values=ignore_val)


def part1_numpy(seatmat: ndarray) -> Tuple[int, int]:
    lastmat = seatmat.copy()
    rounditer = 0
    while True:
        newmat = lastmat.copy()
        for row, col, cell in iterate_2darr(lastmat):
            if cell < 0:
                continue
            window = lastmat[row - 1:row + 2, col - 1:col + 2]
            winsum = window[window > 0].sum() - cell
            if cell and winsum > 3:
                newmat[row, col] = 0
            elif not cell and winsum == 0:
                newmat[row, col] = 1
        rounditer += 1
        print(f"Iteration: {rounditer}")
        if np.array_equal(newmat, lastmat):
            return int(newmat[newmat > 0].sum()), rounditer
        lastmat = newmat
        del newmat


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day11.txt')
    seatimg = read_input_as_padded_array(datapath)

    p1 = part1_purepython(seatimg)
    print(f"\n\nPart 1: Stable seat occupation state occured with {p1[0]} seats occupied after {p1[1]} iterations\n")
    p2 = part2_purepython(read_input(datapath))
    print(f"\n\nPart 2: Stable seat occupation state occured with {p2[0]} seats occupied after {p2[1]} iterations\n")

