import pathlib
import math
from typing import List
from ai.ghosts.ai2 import CornerGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.level import TileMap, classic_map, classic_map_c
from game.pacman import BasePacman
from game.ghosts import BaseGhost
from game.util import dir_to_int
from ctypes import *

file_dir = pathlib.Path(__file__).parent.resolve()
module = CDLL(f"{file_dir}/evaluate.so")
retTestFunc = module.retTest
retTestFunc.restype = c_int
retTestFunc.argtypes = [POINTER(c_int), c_int]

find_paths_func = module.pick_paths
find_paths_func.restype = None
find_paths_func.argtypes = [
    c_int,  # level_w
    c_int,  # level_h
    POINTER(c_int),  # level map
    POINTER(c_int),  # pacman pos
    c_int,  # pacman dir
    c_int,  # ghost num
    POINTER(c_int),  # ghosts pos
    POINTER(c_int),  # ghosts directions
    POINTER(POINTER(c_int)),  # return paths
]


# values = list(range(10))
# (c_int * len) creates an array type, then create an instance with unpacked values
# arr = (ctypes.c_int * len(values))(*values)
# ret = retTestFunc(arr, len(values))
def pick_paths(level_map: 'Array[c_int]', level_w, level_h, pacman: BasePacman, ghosts: List[BaseGhost]):
    max_path_len = 50
    # paths that result is put into
    paths = (POINTER(c_int) * len(ghosts))(
        *[(c_int * max_path_len)() for _ in range(len(ghosts))]
    )
    # create ghosts pos array
    ghost_poss = []
    for ghost in ghosts:
        ghost_poss.extend([math.floor(ghost.x), math.floor(ghost.y)])
    # pacman pos array
    pacman_pos = (c_int*2)(math.floor(pacman.x), math.floor(pacman.y))
    find_paths_func(
        c_int(level_w),
        c_int(level_h),
        level_map,
        pacman_pos,
        c_int(dir_to_int(pacman.direction)),
        c_int(len(ghosts)),
        (c_int * (len(ghosts) * 2))(*ghost_poss),
        (c_int * len(ghosts))(*[dir_to_int(x.direction) for x in ghosts]),
        paths,
        10,
    )

if __name__ == "__main__":
    pacman = RandomPacman(14, 23.5)
    ghost_system = CornerGhostSystem((14, 11.5))
    pick_paths(classic_map_c, len(classic_map[0]), len(classic_map), pacman, ghost_system.ghosts)
    