import random
from game.mover import Mover
from game.util import Direction, Grid2d, center, to_screen
from game.pacman import BasePacman
from game.level import Tile, TileMap, get_available_directions
from typing import Tuple, List
from enum import Enum
import pygame
import math


class GhostMode(Enum):
    CHASE = 20
    SCATTER = 10
    RUN = 7

# base ghost for others to inherit from, randomly turns at all intersections
class BaseGhost(Mover):
    def __init__(self, x, y):
        super().__init__(x, y, 0.95*7.5)
        self.colour = (255, 0, 0)
        self.cur_colour = self.colour
        self.start_x = x
        self.start_y = y
        self.dead = True
        self.pen_timer = 5
        self.last_direction = self.direction
        self.debug = False

    @property
    def cornercut(self) -> float:
        return 1/30

    def step(self, dt: float, level_map: List[List[Tile]]):
        if not self.dead:
            super().step(dt, level_map)
        else:
            self.pen_timer -= dt
            if self.pen_timer < 0:
                self.dead = False
                self.pen_timer = 5

    # called by mover class every frame
    def check_new_direction(self, tile_map: TileMap) -> Direction:
        available = get_available_directions(tile_map, [self.x, self.y])
        # stop turning around
        for direction in [self.direction, self.last_direction]:
            try:
                available.remove(direction.inverse())
            except ValueError:
                pass
        if self.direction != Direction.NONE:
            self.last_direction = self.direction

        if len(available) == 0:
            return self.direction
        elif len(available) == 1:
            return available[0]
        else:
            return self.get_new_direction(available, tile_map)

    # is overwritten by child
    def get_new_direction(self, available: List[Direction], *args) -> Direction:
        return random.choice(available)

    def check_collisions(self, other: "Mover"):
        if not self.dead and super().check_collisions(other):
            self.x = self.start_x
            self.y = self.start_y
            self.dead = True
            return True
        return False

    def draw(self, screen: pygame.Surface, offset: Tuple[int, int], grid_size: int):
        pygame.draw.circle(
            screen,
            self.cur_colour,
            (
                round(offset[0] + grid_size * self.x),
                round(offset[1] + grid_size * self.y),
            ),
            grid_size * 0.7,
        )


class ClassicGhost(BaseGhost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.goal = (0, 0)

    # called whenever there are more than one possible directions to go
    def get_new_direction(self, available: List[Direction], level_map) -> Direction:
        # pick closest
        best = Direction.NONE
        best_dist = 999999
        for i in available:
            dist = (self.goal[0] - (self.x + i.value[0])) ** 2 + (
                self.goal[1] - (self.y + i.value[1])
            ) ** 2
            if dist < best_dist:
                best = i
                best_dist = dist
        return best

    def set_goal(self, goal: Tuple[int, int]):
        self.goal = goal

    def draw(self, screen: pygame.Surface, offset: Tuple[int, int], grid_size: int):
        super().draw(screen, offset, grid_size)
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (
                round(offset[0] + grid_size * self.goal[0]),
                round(offset[1] + grid_size * self.goal[1]),
            ),
            grid_size * 0.3,
        )

        for g1, g2 in zip(self.path, self.path[1:]):
            p1 = to_screen(center(g1), offset, grid_size)
            p2 = to_screen(center(g2), offset, grid_size)
            # pygame.draw.line(screen, self.colour, p1, p2, 3)

    def step(self, dt, level_map):
        super().step(dt, level_map)

        # create path[], not actually used for pathfinding
        self.path = []
        pos = (math.floor(self.x), math.floor(self.y))
        direction = self.direction
        last_direction = self.last_direction
        iters = 0
        while not pos == self.goal and iters < 100:
            available = get_available_directions(level_map, pos)
            for dirc in [direction, last_direction]:
                try:
                    available.remove(dirc.inverse())
                except ValueError:
                    pass
            # pick best direction
            if len(available) == 0:
                print(get_available_directions(level_map, pos))
            else:
                direction = min(
                    available,
                    key=lambda x: math.hypot(
                        pos[0] + x.value[0] - self.goal[0],
                        pos[1] + x.value[1] - self.goal[1],
                    ),
                )
            pos = (pos[0] + direction.value[0], pos[1] + direction.value[1])
            self.path.append(pos)
            if not direction is Direction.NONE:
                last_direction = direction
            iters += 1


class Blinky(ClassicGhost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.colour = (255, 0, 0)
        self.pen_timer = 1


class Inky(ClassicGhost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.colour = (0, 255, 255)
        self.pen_timer = 5


class Pinky(ClassicGhost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.colour = (255, 0, 255)
        self.pen_timer = 9


class Clyde(ClassicGhost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.colour = (255, 160, 0)
        self.pen_timer = 13


class BaseGhostSystem:
    def __init__(self, ghost_start: Tuple[int, int]):
        self.ghosts: List[BaseGhost] = []
        self.ghost_mode = GhostMode.CHASE
        self.speed_mult = 1
        self.ghost_start = ghost_start
        self.mode_timer = 0

    def set_mode(self, mode: GhostMode):
        self.ghost_mode = mode
        self.mode_timer = 0

    def draw(self, screen, offset, grid_size):
        for ghost in self.ghosts:
            ghost.draw(screen, offset, grid_size)

    def step(self, dt: float, level_map: List[List[Tile]], pacman: BasePacman):
        self.mode_timer += dt
        if self.mode_timer > self.ghost_mode.value:
            if self.ghost_mode is GhostMode.RUN:
                self.set_mode(GhostMode.CHASE)
            if self.ghost_mode is GhostMode.CHASE:
                self.set_mode(GhostMode.SCATTER)
            if self.ghost_mode is GhostMode.SCATTER:
                self.set_mode(GhostMode.CHASE)

        if self.ghost_mode is GhostMode.RUN:
            self.speed_mult = 0.5
        else:
            self.speed_mult = 1

        for ghost in self.ghosts:
            if self.ghost_mode is GhostMode.RUN:
                ghost.cur_colour = (0, 0, 255)
            else:
                ghost.cur_colour = ghost.colour
            ghost.step(dt * self.speed_mult, level_map)

    def reset(self):
        self = self.__init__(self.ghost_start)

class RandomGhostSystem(BaseGhostSystem):
    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        self.ghosts = [BaseGhost(ghost_start[0], ghost_start[1]) for _ in range(4)]


class ClassicGhostSystem(BaseGhostSystem):
    def __init__(self, ghost_start: Tuple[int, int]):
        super().__init__(ghost_start)
        self.ghosts: List[ClassicGhost] = [
            Blinky(*ghost_start),
            Inky(*ghost_start),
            Pinky(*ghost_start),
            Clyde(*ghost_start),
        ]
        self.blinky = self.ghosts[0]
        self.inky = self.ghosts[1]
        self.pinky = self.ghosts[2]
        self.clyde = self.ghosts[3]

    def step(self, dt: float, level_map: List[List[Tile]], pacman: BasePacman):
        super().step(dt, level_map, pacman)
        if self.ghost_mode is GhostMode.CHASE:
            self.blinky.set_goal((pacman.x, pacman.y))
            self.pinky.set_goal(
                (
                    pacman.x + pacman.last_move.value[0] * 4,
                    pacman.y + pacman.last_move.value[1] * 4,
                )
            )
            inky_pacman_goal = (
                pacman.x + pacman.direction.value[0] * 2,
                pacman.y + pacman.direction.value[1] * 2,
            )
            blinky_offset = (
                inky_pacman_goal[0] - self.blinky.x,
                inky_pacman_goal[1] - self.blinky.y,
            )
            self.inky.set_goal(
                (
                    inky_pacman_goal[0] + blinky_offset[0],
                    inky_pacman_goal[1] + blinky_offset[1],
                )
            )
            if math.hypot(self.clyde.x - pacman.x, self.clyde.y - pacman.y) > 8:
                self.clyde.set_goal((pacman.x, pacman.y))
            else:
                self.clyde.set_goal((1, 32))
        else:
            self.blinky.set_goal((26, -3))
            self.pinky.set_goal((1, -3))
            self.inky.set_goal((28, 32))
            self.clyde.set_goal((1, 32))
