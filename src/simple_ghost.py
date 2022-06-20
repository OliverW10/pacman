import random
import math
import pygame
from ghosts import BaseGhost
from util import Direction, Grid2d, to_screen, center
from level import TileMap
from typing import List, Tuple
from tree import TreeNode

class SimpleGhost(BaseGhost):
    def __init__(self, x, y, colour):
        super().__init__(x, y)
        self.colour = colour
        self.cur_colour = colour
        self.wanted_dirs = [Direction.NONE]
        self.path: List[Grid2d] = [] # just used for debug display
        self.show_path = True

    def set_path_tree(self, path: List[TreeNode]):
        """
        Takes the path as a list of TreeNode's which the ghost wants to traverse in order
        """
        self.wanted_dirs = [path[1].direction]
        self.path = [node.pos for node in path]
    
    def set_path_plain(self, path: List[Grid2d]):
        """
        Takes the path as a list of Grid2d's which the ghost wants to traverse in order
        """
        diff = (path[1][0]-math.floor(self.x), path[1][1]-math.floor(self.y))
        self.wanted_dirs = [Direction(diff)]
        self.path = path
    
    def set_directions(self, directions: List[Direction]):
        """Takes preference order for directions"""
        self.wanted_dirs = directions

    # called whenever there are more than one possible directions to go
    def get_new_direction(
        self, available: List[Direction], level_map: TileMap
    ) -> Direction:
        for dirc in self.wanted_dirs:
            if dirc in available:
                return dirc
        # print("cant go in wanted direction")
        return random.choice(available)

    def draw(self, screen, offset, grid_size):
        super().draw(screen, offset, grid_size)
        if self.show_path:
            for g1, g2 in zip(self.path, self.path[1:]):
                p1 = to_screen(center(g1), offset, grid_size)
                p2 = to_screen(center(g2), offset, grid_size)
                pygame.draw.line(screen, self.colour, p1, p2, 3)
