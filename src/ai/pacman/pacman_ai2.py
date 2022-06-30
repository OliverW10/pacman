import math
import random
import pygame
from typing import List, Tuple
from ai.tree import create_tree, draw_tree, get_path_from_tree
from game.ghosts import BaseGhostSystem
from game.level import Tile
from game.pacman import BasePacman
from game.util import ALL_DIRECTIONS, Direction, center, to_screen

# avoid ghosts
class ScaredPacman(BasePacman):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.wanted_dir = Direction.NONE
        self.path = []
        self.ghost_poss = []
    
    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1/15

    def step(self, dt: float, level_map: List[List[Tile]], ghost_system: BaseGhostSystem):
        super().step(dt, level_map, ghost_system)
        self.ghost_poss = [(gh.x, gh.y) for gh in ghost_system.ghosts]
        # helper function, returns distance to closest ghost
        def closest_ghost(pos):
            return min([math.dist(pos, (ghost.x, ghost.y)) for ghost in ghost_system.ghosts])

        tree = create_tree(level_map, (self.x, self.y), 10)
        if len(ghost_system.ghosts):
            # pick path that is furthest away from any ghost at end,
            # TODO: dosent check if it goes through a ghost on the way there
            self.path = get_path_from_tree(tree, max(tree[-1], key=lambda x:closest_ghost(x.pos)))
            self.wanted_dir = self.path[1].direction
        else:
            # if there are no ghosts theres no one to run away from
            # so just turn randomly
            self.wanted_dir = random.choice(ALL_DIRECTIONS)
            while self.wanted_dir in [Direction.NONE, self.last_direction]:
                self.wanted_dir = random.choice(ALL_DIRECTIONS)

    def check_new_direction(self, tile_map) -> Direction:
        return self.wanted_dir

    def draw(self, screen, offset: Tuple[int, int], grid_size: int):
        super().draw(screen, offset, grid_size)
        if self.debug:
            for g1, g2 in zip(self.path, self.path[1:]):
                p1 = to_screen(center(g1.pos), offset, grid_size)
                p2 = to_screen(center(g2.pos), offset, grid_size)
                pygame.draw.line(screen, self.colour, p1, p2, 3)
            
            for pos in self.ghost_poss:
                pygame.draw.line(screen, (255, 0, 0), to_screen(pos, offset, grid_size), to_screen(self.path[-1].pos, offset, grid_size))