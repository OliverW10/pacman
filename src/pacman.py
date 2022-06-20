import random
from mover import Mover
from util import ALL_DIRECTIONS, Direction
from level import Tile
from typing import Tuple, List
import pygame


class Pacman(Mover):
    def __init__(self, x, y):
        # 60fps, 1 pixel/frame, 8 pixels per tile
        # TODO: pacman slows down when eating pellets
        pacman_speed = 1 / (8 / 60)
        super().__init__(x, y, pacman_speed)
        self.last_pressed = Direction.NONE
        self.last_move = Direction.RIGHT  # last direction that wasnt none, for pinky

    @property
    def cornercut(self) -> float:
        return 0.5

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

        for event in pygame.event.get([pygame.KEYDOWN]):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.last_pressed = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.last_pressed = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.last_pressed = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.last_pressed = Direction.DOWN

        if not self.direction is Direction.NONE:
            self.last_move = self.direction

    def check_new_direction(self, _) -> Direction:
        if self.last_pressed is Direction.NONE:
            return self.direction
        else:
            return self.last_pressed

# pacman that moves randomly
class RandomPacman(Pacman):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_move = Direction.RIGHT
    
    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1/15

    def step(self, dt: float, level_map: List[List[Tile]]):
        super().step(dt, level_map)
        if not self.direction is Direction.NONE:
            self.last_move = self.direction

    def check_new_direction(self, _) -> Direction:
        x = random.choice(ALL_DIRECTIONS)
        while x in [self.direction.inverse(), self.last_move.inverse()]:
            x = random.choice(ALL_DIRECTIONS)
        return x
