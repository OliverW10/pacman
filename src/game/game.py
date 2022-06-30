import math
from typing import Tuple
import pygame
from copy import deepcopy
from game.level import Tile, TileMap, draw_map
from game.pacman import BasePacman
from game.ghosts import (
    GhostMode,
    BaseGhostSystem,
)
from ui.button import AnchorPoint, Button


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
        # timer used to create pauses
        self.freeze_time = 0
        self.dying = False
        self.ghost_streak = 0

        self.score = 0
        self.ghost_debug_button = Button((-10, -10, 100, 35), AnchorPoint.BOTTOM_RIGHT, AnchorPoint.BOTTOM_RIGHT, "Ghost Debug", 18)
        self.ghost_debug = False
        self.pacman_debug_button = Button((-120, -10, 100, 35), AnchorPoint.BOTTOM_RIGHT, AnchorPoint.BOTTOM_RIGHT, "Pacman Debug", 18)
        self.pacman_debug = False

    def ate_ghost(self, pause_time: float):
        self.ghost_streak += 1
        self.freeze_time = pause_time
        self.score += 2**self.ghost_streak * 200

    def ate_pacman(self, pause_time: float):
        self.dying = True
        self.freeze_time = pause_time

    def reset(self):
        self.ghosts_system.reset()
        self.pacman.reset()
        self.tilemap = deepcopy(self.start_tilemap)
        self.dying = False
        self.score = 0
        self.freeze_time = 0
        self.ghost_streak = 0

    def step(self, dt, realtime=True) -> Tuple[bool, int]:
        """Paramters:
            dt: delta time in seconds
            realtime: weather to do pauses after pacman die or eats a ghost
        Returns: weather pacman has just died
        """
        self.freeze_time -= dt
        if self.dying and self.freeze_time <= 0:
            final_score = self.score
            self.reset()
            return (True, final_score)
        moving = self.freeze_time < 0
        if moving:
            # step returns true when it wants to stop
            moving = self.pacman.step(dt, self.tilemap, self.ghosts_system)
            moving = self.ghosts_system.step(dt, self.tilemap, self.pacman)

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
            self.ghost_streak = 0
            self.ghosts_system.set_mode(GhostMode.RUN)

        # do pacman - ghost collisions
        for ghost in self.ghosts_system.ghosts:
            if ghost.check_collisions(self.pacman):
                if self.ghosts_system.ghost_mode is GhostMode.RUN:
                    self.ate_ghost(0.4 if realtime else 0)
                else:
                    self.ate_pacman(1 if realtime else 0)
        return (False, self.score)

    def draw(self, screen, x, y, w, h):
        grid_size = max(h / len(self.tilemap), w / len(self.tilemap[0]))
        draw_map(screen, self.tilemap, (x, y), grid_size)
        self.pacman.draw(screen, (x, y), grid_size)
        self.ghosts_system.draw(screen, (x, y), grid_size)
        pygame.display.update((x, y, w, h))
        clicked = self.pacman_debug_button.draw(screen, self.pacman_debug)
        if clicked:
            self.pacman_debug = not self.pacman_debug
            self.pacman.set_debug(self.pacman_debug)
        clicked = self.ghost_debug_button.draw(screen, self.ghost_debug)
        if clicked:
            self.ghost_debug = not self.ghost_debug
            self.ghosts_system.set_debug(self.ghost_debug)

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
            score_counter += delta_t
            still_counter += delta_t
            # check if position and score have changed
            if self.score != last_score:
                last_score = self.score
                score_counter = 0
            if (self.pacman.x, self.pacman.y) != last_pos:
                last_pos = (self.pacman.x, self.pacman.y)
                still_counter = 0

            if self.dying:
                break
            if still_counter > still_cutoff:
                break
            if score_counter > score_cutoff:
                break
            if step_counter > game_cutoff:
                break
        return self.score
