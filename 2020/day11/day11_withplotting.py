import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from numpy import ndarray


def read_input(inpath: Path, ignore_val: str = '-2') -> List[List[int]]:
    return [[int(x.replace('.', ignore_val).replace('L', '0').replace('#', '1')) for x in y]
            for y in [list(x) for x in inpath.read_text().split('\n') if x]]


def part1_purepython(seatmat: List[List[int]], ignoreval: int = -2) -> Tuple[int, int]:
    row_offset = len(seatmat[0])
    seatlist = [x for y in seatmat for x in y]
    positions = (-row_offset - 1, -row_offset, -row_offset + 1, -1, 1, row_offset - 1, row_offset, row_offset + 1,)

    iteration = 0
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
        print(f"Iteration no: {iteration}")
        if newseats == seatlist:
            return sum((x for x in seatlist if x > 0)), iteration
        seatlist = newseats
        iteration += 1


def part2_purepython(seatmat: List[List[int]], ignoreval: int = -2,
                     gtfo_thresh: int = 5) -> Tuple[int, int]:
    # row_offset = len(seatmat[0])
    # seatlist = [x for y in seatmat for x in y]
    niterations = 0
    savedir = Path(Path(__file__).parent / 'figs').resolve()
    if not savedir.exists:
        savedir.mkdir()

    lastseats = seatmat

    # make a color map of fixed colors
    c = Cols

    state_iter = 0
    plotit = False
    if plotit:
        statepic = np.zeros(shape=(len(seatmat), len(seatmat[0])))

    while True:
        newseats = [[None for _ in y] for y in lastseats]

        for row, col, seat in iterate_2dlist(lastseats):

            direction_results = {k: None for k in itertools.combinations_with_replacement([0, 1, -1, 1], 2) if
                                 k != (0, 0)}

            for dkey in direction_results:
                dr, dc = dkey
                dist = 1
                if plotit:
                    statepic[col, row] = c.curseat

                while direction_results[dkey] is None:

                    tgtrow, tgtcol = row + dr * dist, col + dc * dist
                    # print(tgtrow, tgtcol)
                    if tgtrow > len(seatmat) - 1 or tgtcol > len(seatmat[tgtrow]) - 1:
                        direction_results[dkey] = -2
                        tgtrow, tgtcol = row + dr * dist - 1, col + dc * dist - 1
                        if plotit:
                            statepic[col, row] = c.floor
                            plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, c)
                            state_iter += 1
                        continue

                    curtgt = lastseats[tgtrow][tgtcol]

                    if curtgt == ignoreval:
                        direction_results[dkey] = -2
                        if plotit:
                            statepic[tgtrow, tgtcol] = c.empty
                    elif curtgt == 1:
                        direction_results[dkey] = curtgt
                        if plotit:
                            statepic[tgtrow, tgtcol] = c.occupied
                    elif curtgt == 0:
                        direction_results[dkey] = curtgt
                        if plotit:
                            statepic[tgtrow, tgtcol] = c.floor
                    if plotit:
                        plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, c)
                        state_iter += 1
                    if plotit:
                        if statepic[row, col] == 0:
                            statepic[row, col] = c.lastvisited
                            plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, c)
                            state_iter += 1
                    dist += 1

            sum_ = sum((res for res in direction_results.values() if res > 0))
            if sum_ >= gtfo_thresh and seat:
                newseats[row][col] = 0
                if plotit:
                    statepic[row, col] = c.empty
            elif sum_ == 0 and not seat:
                newseats[row][col] = 1
                if plotit:
                    statepic[row, col] = c.occupied
            else:
                newseats[row][col] = seat
        if plotit:
            try:
                statepic[row, col] = c.visited
            except IndexError:
                pass
        if newseats == lastseats:
            return sum((x for y in newseats for x in y if x > 0)), niterations
        lastseats = newseats.copy()
        print(f"Iterations: {niterations}")
        niterations += 1


@dataclass
class Cols:
    unvisited: int = 0
    curseat: int = 1
    lastvisited: int = 2
    floor: int = 3
    occupied: int = 4
    empty: int = 5
    cmap = colors.ListedColormap(['whitesmoke', 'tab:blue', 'tab:olive', 'lightsteelblue', 'crimson', 'springgreen'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = colors.BoundaryNorm(bounds, cmap.N)


def plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, colscls):
    # coords = np.array([[col, row],[tgtrow, tgtcol]])
    # coords = coords.dot([[-1,0],[0,1]])
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=200)
    ax.set_title(f"Direction painted seats")  # . Direction = {dkey}")
    ax.imshow(statepic + 0.5, cmap=colscls.cmap, norm=colscls.norm, origin='lower', interpolation='nearest')  # ,
    ax.set_xlim((len(seatmat) - 0.5, -0.5,))
    ax.set_ylim((len(seatmat[0]) - 0.5, -0.5))
    plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False,
                    right=False, left=False,
                    labelleft=False)
    # ax.grid(Fal, which='major')

    # ax.arrow(coords[0,0], coords[0,1], coords[1,0], coords[1,1], head_width=0.4, zorder=100, clip_on=False,
    # color='black', edgecolor='black')
    storepath = Path(f'figs/state{state_iter}.jpg')
    if storepath.exists():
        storepath.unlink()
    print(f"Plotting for state iteration {state_iter}")
    plt.savefig(storepath)
    plt.autoscale(False)
    plt.close()


def part2_purepython(seatmat: List[List[int]], ignoreval: int = -2,
                     gtfo_thresh: int = 5) -> Tuple[int, int]:
    # row_offset = len(seatmat[0])
    # seatlist = [x for y in seatmat for x in y]
    niterations = 0
    savedir = Path(Path(__file__).parent / 'figs').resolve()
    if not savedir.exists:
        savedir.mkdir()

    lastseats = seatmat

    # make a color map of fixed colors
    c = Cols

    state_iter = 0
    plotit = False
    if plotit:
        statepic = np.zeros(shape=(len(seatmat), len(seatmat[0])))

    while True:
        newseats = [[None for _ in y] for y in lastseats]

        for row, col, seat in iterate_2dlist(lastseats):

            direction_results = {k: None for k in itertools.combinations_with_replacement([0, 1, -1, 1], 2) if
                                 k != (0, 0)}

            for dkey in direction_results:
                dr, dc = dkey
                dist = 1
                if plotit:
                    statepic[col, row] = c.curseat

                while direction_results[dkey] is None:

                    tgtrow, tgtcol = row + dr * dist, col + dc * dist
                    # print(tgtrow, tgtcol)
                    if tgtrow > len(seatmat) - 1 or tgtcol > len(seatmat[tgtrow]) - 1:
                        direction_results[dkey] = -2
                        tgtrow, tgtcol = row + dr * dist - 1, col + dc * dist - 1
                        if plotit:
                            statepic[col, row] = c.floor
                            plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, c)
                            state_iter += 1
                        continue

                    curtgt = lastseats[tgtrow][tgtcol]

                    if curtgt == ignoreval:
                        direction_results[dkey] = -2
                        if plotit:
                            statepic[tgtrow, tgtcol] = c.empty
                    elif curtgt == 1:
                        direction_results[dkey] = curtgt
                        if plotit:
                            statepic[tgtrow, tgtcol] = c.occupied
                    elif curtgt == 0:
                        direction_results[dkey] = curtgt
                        if plotit:
                            statepic[tgtrow, tgtcol] = c.floor
                    if plotit:
                        plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, c)
                        state_iter += 1
                    if plotit:
                        if statepic[row, col] == 0:
                            statepic[row, col] = c.lastvisited
                            plotstate(statepic, seatmat, col, row, tgtcol, tgtrow, state_iter, c)
                            state_iter += 1
                    dist += 1

            sum_ = sum((res for res in direction_results.values() if res > 0))
            if sum_ >= gtfo_thresh and seat:
                newseats[row][col] = 0
                if plotit:
                    statepic[row, col] = c.empty
            elif sum_ == 0 and not seat:
                newseats[row][col] = 1
                if plotit:
                    statepic[row, col] = c.occupied
            else:
                newseats[row][col] = seat
        if plotit:
            try:
                statepic[row, col] = c.visited
            except IndexError:
                pass
        if newseats == lastseats:
            return sum((x for y in newseats for x in y if x > 0)), niterations
        lastseats = newseats.copy()
        print(f"Iterations: {niterations}")
        niterations += 1


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


def part2(data: List[int], target_sum) -> int:
    ...


if __name__ == '__main__':
    datapath = Path(Path(__file__).parent / 'input_day11a.txt')

    seatimg = read_input_as_padded_array(datapath)
    # p1 = part1_purepython(seatimg)
    # print(f"\nPart1: Stable seat occupation state occured with {p1[0]} seats occupied after {p1[1]} iterations")
    p2 = part2_purepython(read_input(datapath))
    print(f"\nPart2: Stable seat occupation state occured with {p2[0]} seats occupied after {p2[1]} iterations")
    print(f"Temporary breakpoint in {__name__}")
