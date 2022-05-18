import math
from typing import List, Tuple
import pygame
import time
from copy import deepcopy
from ai import LookaheadGhostSystem
from level import Tile, TileMap, classic_map, draw_map
from util import Direction, Grid2d
from pacman import Pacman
from ghosts import ClassicGhostSystem, BaseGhost, GhostMode


class Game:
    def __init__(
        self,
        tilemap: TileMap,
        pacman_start: Grid2d,
        ghost_start: Grid2d,
    ):
        self.tilemap = deepcopy(tilemap)
        self.start_tilemap = tilemap
        self.pacman = Pacman(pacman_start[0], pacman_start[1], 6)
        self.pacman_start = pacman_start
        self.ghosts_system = ClassicGhostSystem((14, 11.5))
        self.ghost_start = ghost_start
        self.ghost_ate_time = 0
        self.dying = False
        self.ghost_streak = 0

        self.score = 0
        self.last_frame_time = time.time()

    def ate_ghost(self):
        self.ghost_streak += 1
        self.ghost_ate_time = 0.4
        self.score += 2**self.ghost_streak * 400

    def ate_pacman(self):
        self.dying = True
        self.ghost_ate_time = 1

    def reset(self):
        self.ghosts_system.reset()
        self.pacman.reset()
        self.tilemap = deepcopy(self.start_tilemap)
        self.dying = False

    def step(self, dt):
        self.ghost_ate_time -= dt
        if self.dying and self.ghost_ate_time < 0:
            self.reset()
        moving = self.ghost_ate_time < 0
        if moving:
            self.pacman.step(dt, self.tilemap)
            self.ghosts_system.step(dt, self.tilemap, self.pacman)

        # do tilemap collisions
        current_tile = self.tilemap[math.floor(self.pacman.y)][
            math.floor(self.pacman.x)
        ]
        if current_tile is Tile.PELLET:
            self.tilemap[math.floor(self.pacman.y)][
                math.floor(self.pacman.x)
            ] = Tile.EMPTY
            self.score += 10
        if current_tile is Tile.SUPER_PELLET:
            self.tilemap[math.floor(self.pacman.y)][
                math.floor(self.pacman.x)
            ] = Tile.EMPTY
            self.score += 50
            self.ghosts_system.set_mode(GhostMode.RUN)

        # do pacman - ghost collisions
        for ghost in self.ghosts_system.ghosts:
            if ghost.check_collisions(self.pacman):
                if self.ghosts_system.ghost_mode is GhostMode.RUN:
                    self.ate_ghost()
                else:
                    self.ate_pacman()

    def draw(self, screen, x, y, w, h):
        grid_size = max(h / len(self.tilemap), w / len(self.tilemap[0]))
        draw_map(screen, self.tilemap, (x, y), grid_size)
        # self.pacman.draw(self.screen, (400 - grid_size * 14, 25), grid_size)
        self.pacman.draw(screen, (x, y), grid_size)
        self.ghosts_system.draw(screen, (x, y), grid_size)


if __name__ == "__main__":
    game = Game(classic_map, (14, 23.5), (14, 11.5))
    running = True
    last_frame_time = time.time()
    # setup pygame
    pygame.init()
    pygame.display.set_caption("Test caption")
    screen = pygame.display.set_mode((800, 600))

    while running:
        dt = time.time() - last_frame_time
        last_frame_time = time.time()
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                running = False
        game.step(dt)
        grid_size = 16
        screen.fill((0, 0, 0))
        game.draw(
            screen,
            400 - 14 * grid_size,
            300 - 15 * grid_size,
            28 * grid_size,
            31 * grid_size,
        )
        pygame.display.flip()
