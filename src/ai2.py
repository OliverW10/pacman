from dataclasses import dataclass
import random
from typing import List, Tuple, Optional
from ghosts import ClassicGhost, GhostSystem, BaseGhost
from level import Tile, TileMap, get_available_directions, is_wall, nearest_free
from pacman import Pacman
from pathfinder import pathfind
from util import Direction, Grid2d, center, clamp, to_screen
from tree import create_tree, TreeNode, get_path_from_tree
import math
import pygame
from itertools import product


class PathGhost(BaseGhost):
    def __init__(self, x, y, colour):
        super().__init__(x, y)
        self.colour = colour
        self.cur_colour = colour
        self.path: List[Grid2d] = []

    def set_path(self, path: Grid2d):
        self.path = path

    # called whenever there are more than one possible directions to go
    def get_new_direction(
        self, available: List[Direction], level_map: TileMap
    ) -> Direction:
        wanted_dir = self.path[1]
        return self.path[1]

    def draw(self, screen, offset, grid_size):
        super().draw(screen, offset, grid_size)

        # for g1, g2 in zip(self.path, self.path[1:]):
        #     p1 = to_screen(center(g1), offset, grid_size)
        #     p2 = to_screen(center(g2), offset, grid_size)
        #     pygame.draw.line(screen, self.colour, p1, p2, 3)


# picks best routes for each ghost by looking at all possible ghost paths
# and taking the one which maximises an eval function (number of squares, pellets and energisers pacman can reach)
class CornerGhostSystem(GhostSystem):
    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        colours = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 160, 0)]
        self.ghosts: List[PathGhost] = [
            PathGhost(ghost_start[0], ghost_start[1], col) for col in colours
        ]
        self.pacman_trees: List[List[TreeNode]] = []
        self.level_size = (0, 0)

    def step(self, dt: float, level_map: List[List[Tile]], pacman: Pacman):
        self.level_size = (len(level_map[0]), len(level_map))
        # use just over half the distance between pacman and nearest ghost as length to search
        closest_dist = 0.7 * min(
            math.hypot(ghost.x - pacman.x, ghost.y - pacman.y) for ghost in self.ghosts
        )
        closest_dist = clamp(closest_dist, 8, 15)
        pacman_tree = create_tree(
            level_map,
            (pacman.x, pacman.y),
            closest_dist,
            Direction.NONE,
        )
        ghost_trees = [
            create_tree(level_map, (ghost.x, ghost.y), closest_dist, ghost.direction, 1, idx)
            for idx, ghost in enumerate(self.ghosts)
        ]
        # generate all possible combinations of paths ghosts could take
        # https://docs.python.org/3/library/itertools.html#itertools.product
        all_combs = product(*[x[-1] for x in ghost_trees])
        # find best
        # TODO: remove obviously bad ones
        best_eval = 99999
        best_idx = -1
        for comb_idx, comb in enumerate(all_combs):
            print(comb_idx, comb)
            # to get better type info
            # comb has a [ghost_idx, final_node] for each ghost in this combination
            comb: Tuple[TreeNode] = comb
            # create 'ghost path', list of positions in path, for each ghost
            ghost_paths: List[List[Grid2d]] = []
            for path_end in comb:
                ghost_paths.append([x.pos for x in get_path_from_tree(ghost_trees[path_end.idx], path_end)])

            fittness = CornerGhostSystem.evaluate(ghost_paths, pacman_tree, level_map)
            print(fittness)
            if fittness > best_eval:
                best_idx = comb_idx
                best_eval = fittness
        
        best_paths = all_combs[best_idx]
        # get path for each ghost
        for path_end in best_paths:
            path = get_path_from_tree(ghost_trees[path_end.idx], path_end)
            # give path to ghost to follow
            self.ghosts[path_end.idx].set_path(path)

        super().step(dt, level_map, pacman)

    def draw(self, screen: pygame.Surface, offset: Grid2d, grid_size: int):
        super().draw(screen, offset, grid_size)

    def evaluate(
        ghost_paths: List[List[Grid2d]],
        pacman_tree: List[List[TreeNode]],
        level_map: TileMap,
    ) -> float:
        """
        Returns as estimate of how desirable these ghost positions are
        Parameters:
            ghost_paths: List for each ghost of the positions it will traverse
            pacman tree: Precomputed tree of every path pacman can take
            level_map: TileMap of level
        """
        assert len(ghost_paths[0]) == len(pacman_tree)
        # counts how many sqaures + pellets*5 + super pellets * 100 pacman can reach
        # steps to search, the higher the better (maybe) behavoir but the more computation
        length = len(pacman_tree)
        total_points = 0
        dead_paths = [[]]
        for step in range(length):
            dead_paths.append([])
            for idx, pacman_possibility in enumerate(pacman_tree[step]):
                # if parent was dead, kill child too
                if pacman_possibility.parent in dead_paths[-2]:
                    dead_paths[-1].append(idx)
                    continue

                square = level_map[pacman_possibility.pos[1]][pacman_possibility.pos[1]]
                if square is Tile.EMPTY:
                    total_points += 1
                elif square is Tile.PELLET:
                    total_points += 5
                elif square is Tile.SUPER_PELLET:
                    total_points += 100

                # check collisions with ghosts
                # also check previous pacman step to stop step past each other
                parent = pacman_tree[pacman_possibility.parent]
                for path in ghost_paths:
                    if pacman_possibility.pos == path[step] or parent.pos == path[step]:
                        dead_paths.append(idx)

        return total_points
