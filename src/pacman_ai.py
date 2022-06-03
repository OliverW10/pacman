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

class AiPacman(Mover):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.last_move = Direction.RIGHT # last direction that wasnt none, for pinky
        self.cornercut = 0.5
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

    # called every frame
    def check_new_direction(self, _) -> Direction:
        x = math.floor(self.x)
        y = math.floor(self.y)
        last_x = x-self.last_direction.value[0]
        last_y = y-self.last_direction.value[1]
        # remember state of square behind us
        temp = level_map[last_y][last_x]
        # fill square behind us to stop turning around
        level_map[last_y][last_x] = Tile.WALL
        # move goal out of walls, TODO: can fail
        goal = nearest_free(level_map, *[math.floor(n) for n in self.goal])
        # find path to goal
        self.path = pathfind(level_map, (x, y), goal)
        # restore square behind us
        level_map[last_y][last_x] = temp
        # find direction from path
        if len(self.path) <= 1:
            print("no path")
            return random.choice(available)
        diff = (self.path[1][0]-x, self.path[1][1]-y)
        wanted_dir = Direction(diff)
        if wanted_dir in available:
            return wanted_dir
        else:
            print("couldnt go in wanted direction")
            return random.choice(available)