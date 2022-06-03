from level import Tile, get_available_directions, is_wall
from util import rate_limit, ALL_DIRECTIONS, Direction
from typing import List
import math

# base class for object that moves around a maze
class Mover:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.direction = Direction.RIGHT
        self.speed = speed
        # should be overwritten by sub classes
        self.cornercut = 0.5

    def step(self, dt, level_map: List[List[Tile]]):
        self.x += self.direction.value[0] * dt * self.speed
        self.y += self.direction.value[1] * dt * self.speed

        # snap to grid
        if abs(self.direction.value[0]) == 0:
            self.x = rate_limit(self.x, math.floor(self.x) + 0.5, self.speed * dt)

        if abs(self.direction.value[1]) == 0:
            self.y = rate_limit(self.y, math.floor(self.y) + 0.5, self.speed * dt)

        avalible_directions = get_available_directions(level_map, (self.x, self.y))
        if self.direction not in avalible_directions:
            self.direction = Direction.NONE

        new_dir = self.check_new_direction(level_map)
        if (
            new_dir in avalible_directions
            and abs(self.x % 1 - 0.5) < self.cornercut
            and abs(self.y % 1 - 0.5) < self.cornercut
        ):
            self.direction = new_dir

        # looping
        self.x = self.x % len(level_map[0])
        self.y = self.y % len(level_map)

    def check_collisions(self, other: "Mover"):
        return (
            self.x + 0.75 > other.x + 0.25
            and self.x + 0.25 < other.x + 0.75
            and self.y + 0.75 > other.y + 0.25
            and self.y + 0.25 < other.y + 0.75
        )
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = Direction.NONE

    # to be implimented by sub classes
    def check_new_direction(self, _) -> Direction:
        raise NotImplementedError

    def draw(self, screen, offset, grid_size):
        raise NotImplementedError
