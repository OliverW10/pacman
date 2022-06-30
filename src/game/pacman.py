import random
from game.mover import Mover
from game.util import ALL_DIRECTIONS, Direction, to_screen
from game.level import Tile
from typing import Tuple, List
import pygame


class BasePacman(Mover):
    def __init__(self, x, y):
        # 60fps, 1 pixel/frame, 8 pixels per tile
        # TODO: pacman slows down when eating pellets
        pacman_speed = 1 / (8 / 60)
        super().__init__(x, y, pacman_speed)
        self.colour = (250, 218, 94)
        self.debug = False
    
    def step(self, dt: float, level_map: List[List[Tile]], ghost_system: 'BaseGhostSystem' = None):
        super().step(dt, level_map)

    @property
    def cornercut(self) -> float:
        return 0.5

    def draw(self, screen, offset: Tuple[int, int], grid_size: int):
        pygame.draw.circle(
            screen,
            self.colour,
            (
                round(offset[0] + grid_size * self.x),
                round(offset[1] + grid_size * self.y),
            ),
            grid_size * 0.7,
        )
    
    def set_debug(self, value: bool):
        self.debug = value

class UserPacman(BasePacman):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_pressed = Direction.NONE
        self.last_move = Direction.RIGHT  # last direction that wasnt none, for pinky

    def step(self, dt: float, level_map: List[List[Tile]], ghost_system: 'BaseGhostSystem'):
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

    def draw(self, screen, offset, grid_size):
        super().draw(screen, offset, grid_size)
        if self.debug:
            dir_indicator_pos = to_screen(
                (self.x + self.last_pressed.x, self.y + self.last_pressed.y),
                offset,
                grid_size,
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                dir_indicator_pos,
                5,
            )