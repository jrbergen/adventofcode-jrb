import itertools
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

import numpy as np


class TileOrientation:
    def __init__(self, id: int, orig_mat: np.ndarray, flip: str, rot: int):
        self.id = id
        self.flip = flip
        self.rot = rot
        self.orig_mat: np.ndarray = orig_mat
        self.mat = self.constrmat()
        self.fits: List[TileOrientation] = []  # Other matrices which fit thisone

        self.top, self.bot, self.left, self.right = [], [], [], []
        self.edges = {attrname: getattr(self, attrname) for attrname in ('top', 'bot', 'left', 'right')}

        self.has_fit: bool = False
        self.n_fits: int = 0
        self.fits_with_ids: Set[int] = set()
        self.update_edges()

    def constrmat(self):
        return np.rot90(self._perform_flip(flip_str=self.flip, mat=self.orig_mat), k=self.rot)

    @staticmethod
    def _perform_flip(flip_str: str, mat: np.ndarray):
        """
        Flips matrix
        
        :param flipstr: str 'noflip', 'lr', 'ud', 'diag''
        """

        if flip_str == 'noflip':
            return mat
        elif flip_str == 'lr':
            return np.fliplr(mat)
        elif flip_str == 'ud':
            return np.flipud(mat)
        elif flip_str == 'diag':
            return np.flip(mat)

    def update_edges(self):
        self.top, self.bot, self.left, self.right \
            = (self.orig_mat[0, :], self.orig_mat[self.orig_mat.shape[0] - 1, :],
               self.orig_mat.T[0, :], self.orig_mat.T[self.orig_mat.shape[1] - 1, :],)
        self.edges = {attrname: getattr(self, attrname) for attrname in ('top', 'bot', 'left', 'right')}

    def fit(self, other: 'TileOrientation') -> Optional[Tuple[Tuple[int, str], Tuple[int,str]]]:
        if self.id == other.id:
            return False
        for edge_self_name, edge_self in self.edges.items():
            for edge_other_name, edge_other in other.edges.items():
                if all(edge_self == edge_other) or all(edge_self == edge_other[::-1]):
                    self.fits.append((other.id, edge_other_name, other.rot, other.flip))
                    other.fits.append((self.id, edge_self_name, self.rot, self.flip))
                    print(f"Found fit! for self={self.fits[-1]}, other={other.fits[-1]}")
                    self.n_fits += 1
                    self.fits_with_ids.add(other.id)
        self.has_fit = False if self.n_fits == 0 else True
        if self.fits and other.fits:
            return (self.fits[-1], other.fits[-1],)
        else:
            return None

    def __repr__(self):
        return ''.join([f"{self.__class__.__name__}(id={self.id}, rot={self.rot},",
                        f" flip={self.flip}, fits_with_ids={self.fits_with_ids})"])


def row_translate(row: List[str], transl_dict: Optional[Dict[str, int]] = None) -> List[int]:
    transl_dict = transl_dict or {'#': 1, '.': 0}
    return [transl_dict[el] for el in row]


def read_input(file: Path) -> Dict[int, np.ndarray]:
    with open(file, 'r') as filehandle:
        tiles = [tile.split('\n') for tile in filehandle.read().split('\n\n')]
    tile_dict = dict()
    for tile in tiles:
        tile_dict[int(re.search(pattern=r'\d+', string=tile[0]).group())] \
            = np.array([row_translate(list(row)) for row in tile[1:]])
    return tile_dict


def part1(tiles: Dict[int, np.ndarray], max_attempts: int = 5):
    found_tiles = set()
    remaining_tiles = set(tiles)
    orientations = range(4)
    flip_strs = ('lr', 'ud', 'diag', 'noflip')

    fits = set()
    fitmatrices: Set[TileOrientation] = set()
    for tile_id, tile in tiles.items():
        for (orientation, flip_str) in itertools.product(orientations, flip_strs):
            fitmatrices.add(TileOrientation(id=tile_id, orig_mat=tile, flip=flip_str, rot=orientation))

        for mat0 in fitmatrices:
            for mat1 in fitmatrices:
                fits.add(mat0.fit(mat1))

    [print(fit) for fit in fits]

    print(f"Temporary breakpoint in {__name__}")


def part2():
    ...


if __name__ == '__main__':
    input_filepath = Path('input_day20.txt')
    einput_filepath = Path('input_day20_example.txt')
    puzzle_input = read_input(file=einput_filepath)
    part1(tiles=puzzle_input)
    print(f"Temporary breakpoint in {__name__}")
