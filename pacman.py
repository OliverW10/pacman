from mover import Mover
from util import Direction
from level import Tile
from typing import Tuple, List
import pygame

class Pacman(Mover):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.last_pressed = Direction.NONE
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