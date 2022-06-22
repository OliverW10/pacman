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
        self.last_move = Direction.RIGHT
    
    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1/15

    def step(self, dt: float, level_map: List[List[Tile]], ghost_system: BaseGhostSystem):
        super().step(dt, level_map, ghost_system)
        if not self.direction is Direction.NONE:
            self.last_move = self.direction

    def check_new_direction(self, _) -> Direction:
        x = random.choice(ALL_DIRECTIONS)
        while x in [self.direction.inverse(), self.last_move.inverse()]:
            x = random.choice(ALL_DIRECTIONS)
        return x