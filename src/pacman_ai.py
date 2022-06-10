import math
import random
from mover import Mover
from util import ALL_DIRECTIONS, Direction
from level import Tile
from typing import Tuple, List
import pygame
from pathfinder import pathfind


class RandomPacman(Mover):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.last_move = Direction.RIGHT
        self.cornercut = 0.1
        self.score = 0

    def draw(self, screen, offset: Tuple[int, int], grid_size: int):
        pygame.draw.circle(
            screen,
            (250, 218, 94),
            (
                round(offset[0] + grid_size * self.x),
                round(offset[1] + grid_size * self.y),
            ),
            grid_size * 0.7,
        )

    def step(self, dt: float, level_map: List[List[Tile]]):
        super().step(dt, level_map)
        if not self.direction is Direction.NONE:
            self.last_move = self.direction

    def check_new_direction(self, _) -> Direction:
        x = random.choice(ALL_DIRECTIONS)
        while x in [self.direction.inverse(), self.last_move.inverse()]:
            x = random.choice(ALL_DIRECTIONS)
        return x
