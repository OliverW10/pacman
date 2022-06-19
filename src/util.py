from enum import Enum
import math
from typing import Tuple


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    NONE = (0, 0)

    def inverse(self):
        return Direction((-self.value[0], -self.value[1]))

    def __getitem__(self, item):
        return self.value[item]

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


ALL_DIRECTIONS = [x for x in Direction]


def rate_limit(n, goal, speed):
    error = goal - n
    return n + math.copysign(min(abs(error), speed), error)

def clamp(n, low, high):
    return min(high, max(low, n))

Grid2d = Tuple[int, int]

# converts grid to screen coordinates
def to_screen(pos: Grid2d, offset: Grid2d, grid_size: int) -> Grid2d:
    return (offset[0] + pos[0] * grid_size, offset[1] + pos[1] * grid_size)


def center(pos: Grid2d) -> Grid2d:
    x = math.floor(pos[0]) + 0.5
    y = math.floor(pos[1]) + 0.5
    return (x, y)

def floor_pos(pos: Grid2d) -> Grid2d:
    return math.floor(pos[0]), math.floor(pos[1])
