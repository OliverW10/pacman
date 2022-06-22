# each ghost pathfinds to pacman using A* which the ajencency value changed to make it
# more costly to go the same path as another ghost and less costly to cut off pacman

import math
from typing import List, Tuple
from game.ghosts import BaseGhostSystem
from ai.ghosts.simple_ghost import SimpleGhost
from game.level import Tile
from game.pacman import BasePacman
from ai.pathfinder import pathfind
from ai.tree import TreeNode, create_tree, draw_tree
from game.util import Grid2d
import pygame
import numpy as np


class AStarGhostSystem(BaseGhostSystem):
    USED_TILE_WEIGHT = 2
    AHEAD_TILE_WEIGHT = 0.33
    PELLET_WEIGHT = 0.95

    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        colours = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 160, 0)]
        ghost_num = 4
        self.ghosts: List[SimpleGhost] = [
            SimpleGhost(ghost_start[0], ghost_start[1], col)
            for col in colours[:ghost_num]
        ]
        self.level_size = (0, 0)
        self.pacman_tree: List[List[TreeNode]] = []

    def step(self, dt: float, level_map: List[List[Tile]], pacman: BasePacman):
        self.level_size = (len(level_map[0]), len(level_map))
        target_ahead = 1
        target_pos = (pacman.x+pacman.direction.x*target_ahead, pacman.y+pacman.direction.y*target_ahead)
        # a list of tile weight modifications
        # higher values makes the ghost want to avoid that tile
        tile_modifiers = np.ones((32, 32), dtype=np.single)

        # make tiles ahead of pacman favorable
        self.pacman_tree = create_tree(
            level_map,
            (pacman.x, pacman.y),
            5,
            pacman.direction,
        )
        for layer in self.pacman_tree:
            for node in layer:
                tile_modifiers[node.pos[1]][node.pos[0]] *= self.AHEAD_TILE_WEIGHT
        
        # ghost who is closest to pacman gets preference for pathing
        for ghost in sorted(self.ghosts, key=lambda x: x.euc_dist(x)):
            path = pathfind(level_map, (ghost.x, ghost.y), target_pos, ghost.direction, tile_modifiers)
            for node in path:
                tile_modifiers[node[1]][node[0]] *= self.USED_TILE_WEIGHT
            
            if len(path) > 1:
                ghost.set_path_plain(path)
        super().step(dt, level_map, pacman)

    def draw(self, screen: pygame.Surface, offset: Grid2d, grid_size: int):
        super().draw(screen, offset, grid_size)
