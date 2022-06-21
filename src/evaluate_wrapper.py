import pathlib
from typing import List
from level import TileMap
from pacman import Pacman
from ghosts import BaseGhost
from ctypes import *

file_dir = pathlib.Path(__file__).parent.resolve()
module = CDLL(f"{file_dir}/evaluate.so")
retTestFunc = module.retTest
retTestFunc.restype = c_int
retTestFunc.argtypes = [POINTER(c_int), c_int]

find_paths_func = module.retTest
find_paths_func.restype = None
find_paths_func.argtypes = [
    c_int, # level_w
    c_int, # level_h
    POINTER(c_int), # level map
    POINTER(c_int), # pacman pos
    c_int, # pacman dir
    c_int, # ghost num
    POINTER(c_int), # ghosts pos
    POINTER(c_int), # ghosts directions
    POINTER(POINTER(c_int)) # return paths
]


# values = list(range(10))
# (c_int * len) creates an array type, then create an instance with unpacked values
# arr = (ctypes.c_int * len(values))(*values)
# ret = retTestFunc(arr, len(values))
def pick_paths(level_map: TileMap, pacman: Pacman, ghosts: List[BaseGhost]):
    max_path_len = 50
    paths = ()
    find_paths_func()
