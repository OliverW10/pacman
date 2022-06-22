import math
import pygame
import time
from copy import deepcopy
from ai.ghosts.ai1 import PredictGhostSystem
from ai.ghosts.ai2 import CornerGhostSystem
from ai.ghosts.ai3 import AStarGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.level import Tile, TileMap, classic_map, google_map, draw_map
from game.util import Direction, Grid2d
from game.pacman import BasePacman
from game.ghosts import (
    ClassicGhostSystem,
    GhostMode,
    BaseGhostSystem,
    RandomGhostSystem,
)


class Game:
    def __init__(
        self,
        tilemap: TileMap,
        pacman: BasePacman,
        ghosts: BaseGhostSystem,
    ):
        self.tilemap = deepcopy(tilemap)
        self.start_tilemap = tilemap
        self.pacman = pacman
        self.ghosts_system = ghosts
        # how long since pacman and a ghost collided
        self.ghost_ate_time = 0
        self.dying = False
        self.ghost_streak = 0

        self.score = 0

    def ate_ghost(self):
        self.ghost_streak += 1
        self.ghost_ate_time = 0.4
        self.score += 2**self.ghost_streak * 400

    def ate_pacman(self):
        self.dying = True
        self.ghost_ate_time = 1
        print(self.score)

    def reset(self):
        self.ghosts_system.reset()
        self.pacman.reset()
        self.tilemap = deepcopy(self.start_tilemap)
        self.dying = False
        self.score = 0
        self.ghost_ate_time = 0
        self.ghost_ate_streak = 0

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
        self.pacman.draw(screen, (x, y), grid_size)
        self.ghosts_system.draw(screen, (x, y), grid_size)
        pygame.display.update((x, y, w, h))

    def run_full(self, delta_t: float):
        """Simulates an entire game, dosent do any drawing"""
        # draw every draw_interval
        step_counter = 1
        # if pacman hasnt moved in some time kill him
        still_cutoff = 3  # seconds
        still_counter = 0
        last_pos = (0, 0)
        # if pacman hasnt gained any score in some time kill him
        score_cutoff = 25  # seconds
        score_counter = 0
        last_score = 0
        # if game goes too long (5 minutes) kill it
        game_cutoff = 60 * 5 / delta_t
        while True:
            self.step(delta_t)
            # incriment timers
            step_counter += 1
            if step_counter % 100 == 0:
                print(step_counter)
            score_counter += delta_t
            still_counter += delta_t
            # check if position and score have changed
            if self.score != last_score:
                last_score = self.score
                score_counter = 0
            if (self.pacman.x, self.pacman.y) != last_pos:
                last_pos = (self.pacman.x, self.pacman.y)
                still_counter = 0

            if (
                self.dying
                or still_counter > still_cutoff
                or score_counter > score_cutoff
                or step_counter > game_cutoff
            ):
                break
        return self.score
