import random
from typing import List
from game.level import Tile
from game.pacman import BasePacman
from game.util import ALL_DIRECTIONS, Direction
from game.ghosts import BaseGhostSystem

# pacman that moves randomly
class RandomPacman(BasePacman):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1/15
    
    def step(self, a, b, c):
        super().step(a, b)

    def check_new_direction(self, _) -> Direction:
        x = random.choice(ALL_DIRECTIONS)
        while x in [self.direction.inverse(), self.last_direction.inverse()]:
            x = random.choice(ALL_DIRECTIONS)
        return x