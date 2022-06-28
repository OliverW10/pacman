import numpy as np
from game.level import TileMap, Tile
from game.ghosts import BaseGhostSystem
from game.pacman import BasePacman
from math import floor

view_size = 20
# converts objects to a nparray representing the world for input to a neural network
def to_pacman_relative_inputs(
    tile_map: TileMap, ghost_system: BaseGhostSystem, pacman: BasePacman, view_size
) -> np.ndarray:
    map_w = len(tile_map[0])
    map_h = len(tile_map)
    # walls, pellets, energisers, ghosts, ghost_prev
    inputs = np.zeros((5, map_h, map_w))
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            # postion relative to pacman
            rel_x = x-floor(pacman.x)
            rel_y = y-floor(pacman.y)
            if (
                abs(rel_x) < view_size / 2
                and abs(rel_y) < view_size / 2
            ):
                if tile is Tile.WALL:
                    inputs[0][rel_y+view_size//2][rel_x+view_size//2] = 1
                elif tile is Tile.PELLET:
                    inputs[1][rel_y+view_size//2][rel_x+view_size//2] = 1
                elif tile is Tile.SUPER_PELLET:
                    inputs[2][rel_y+view_size//2][rel_x+view_size//2] = 1

    for ghost in ghost_system.ghosts:
        if not ghost.dead:
            # current pos
            rel_x = floor(ghost.x)-floor(pacman.x)+view_size//2
            rel_y = floor(ghost.y)-floor(pacman.y)+view_size//2
            if rel_x >= 0 and rel_x < map_w and rel_y >= 0 and rel_y < map_h:
                inputs[3][rel_y][rel_x] = 1
            # last pos
            last_rel_x = floor(ghost.last_x)-floor(pacman.x)+view_size//2
            last_rel_y = floor(ghost.last_y)-floor(pacman.y)+view_size//2
            if last_rel_x >= 0 and last_rel_x < map_w and last_rel_y >= 0 and last_rel_y < map_h:
                inputs[4][last_rel_y][last_rel_x] = 1
    return inputs
