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

ALL_DIRECTIONS = [x for x in Direction]

def rate_limit(n, goal, speed):
    error = goal - n
    return n + math.copysign(min(abs(error), speed), error)

Grid2d = Tuple[int, int]