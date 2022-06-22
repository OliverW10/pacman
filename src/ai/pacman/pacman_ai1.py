import pygame
from typing import List, Tuple
from ai.tree import create_tree, draw_tree, get_path_from_tree
from game.level import Tile
from game.pacman import BasePacman
from game.util import ALL_DIRECTIONS, Direction, center, to_screen
from game.ghosts import BaseGhostSystem

# pacman that picks the path that has the highest score
# has no concept of ghosts and if there are no pellets near it it has a panic attack
class GreedyPacman(BasePacman):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_move = Direction.RIGHT
        self.wanted_dir = Direction.NONE
        self.path = []
    
    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1/15

    def step(self, dt: float, level_map: List[List[Tile]], ghost_system: BaseGhostSystem):
        super().step(dt, level_map, ghost_system)
        tree = create_tree(level_map, (self.x, self.y), 10)
        self.path = get_path_from_tree(tree, max(tree[-1], key=lambda x:x.score))
        self.wanted_dir = self.path[1].direction
        if not self.direction is Direction.NONE:
            self.last_move = self.direction

    def check_new_direction(self, tile_map) -> Direction:
        return self.wanted_dir

    def draw(self, screen, offset: Tuple[int, int], grid_size: int):
        super().draw(screen, offset, grid_size)
        for g1, g2 in zip(self.path, self.path[1:]):
            p1 = to_screen(center(g1.pos), offset, grid_size)
            p2 = to_screen(center(g2.pos), offset, grid_size)
            pygame.draw.line(screen, self.colour, p1, p2, 3)