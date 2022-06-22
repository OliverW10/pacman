# uses machine learning

import math
from typing import List, Tuple
from ghosts import BaseGhostSystem
from simple_ghost import SimpleGhost
from level import Tile
from pacman import Pacman
from util import Grid2d
import pygame

class MachineLearningGhostSystem(BaseGhostSystem):
    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        colours = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 160, 0)]
        ghost_num = 4
        self.ghosts: List[SimpleGhost] = [
            SimpleGhost(ghost_start[0], ghost_start[1], col)
            for col in colours[:ghost_num]
        ]
        self.level_size = (0, 0)
        self.pacman_tree: List[List[TreeNode]] = []

    def step(self, dt: float, level_map: List[List[Tile]], pacman: Pacman):
        self.level_size = (len(level_map[0]), len(level_map))
        super().step(dt, level_map, pacman)

    def draw(self, screen: pygame.Surface, offset: Grid2d, grid_size: int):
        super().draw(screen, offset, grid_size)
