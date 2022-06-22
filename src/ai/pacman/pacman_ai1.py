# pick path some distance in future that maximises score

import math
import random
from mover import Mover
from util import ALL_DIRECTIONS, Direction
from level import Tile
from typing import Tuple, List
import pygame
from pathfinder import pathfind
