# each ghost pathfinds to pacman using A* which the ajencency value changed to make it
# more costly to go the same path as another ghost and less costly to cut off pacman

import time
from typing import List, Tuple, Optional
from ghosts import SimpleGhost, BaseGhostSystem
from level import Tile
from pacman import Pacman
from pathfinder import pathfind
from tree import create_tree, TreeNode, draw_tree
from util import Direction, Grid2d
import pygame


class AStarGhostSystem(BaseGhostSystem):
    USED_TILE_WEIGHT = 4
    AHEAD_TILE_WEIGHT = 0.25
    PELLET_WEIGHT = 0.95

    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        colours = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 160, 0)]
        ghost_num = 3
        self.ghosts: List[SimpleGhost] = [
            SimpleGhost(ghost_start[0], ghost_start[1], col)
            for col in colours[:ghost_num]
        ]
        self.level_size = (0, 0)

    def step(self, dt: float, level_map: List[List[Tile]], pacman: Pacman):
        self.level_size = (len(level_map[0]), len(level_map))
        # a list of tile weight modifications
        # higher values makes the ghost want to avoid that tile
        tile_modifiers: List[Tuple[Grid2d, float]] = []

        # make tiles ahead of pacman favorable
        start_time = time.perf_counter()
        pacman_tree = create_tree(
            level_map,
            (pacman.x, pacman.y),
            4,
            pacman.direction,
        )
        for layer in pacman_tree:
            for node in layer:
                tile_modifiers.append((node.pos, self.AHEAD_TILE_WEIGHT))
        
        # ghost who is closest to pacman gets preference for pathing
        for ghost in sorted(self.ghosts, key=lambda x: x.euc_dist(x)):
            path = pathfind(
                level_map, (ghost.x, ghost.y), (pacman.x, pacman.y), tile_modifiers
            )
            tile_modifiers.extend((x, self.USED_TILE_WEIGHT) for x in path)
            if len(path) > 1:
                ghost.set_path_plain(path)
        super().step(dt, level_map, pacman)

    def draw(self, screen: pygame.Surface, offset: Grid2d, grid_size: int):
        super().draw(screen, offset, grid_size)
        # if random.random() > 0.9:
        #     print(len(self.pacman_tree[-1]))
