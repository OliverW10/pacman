# test every possible combination of ghost paths for next n moves
# pick one that maximies an eval function
# eval function either
#   countes total squares + pellets + super pellets availible to pacman in n moves
# or
#   countes maximum of same thing

import time
from typing import List, Tuple, Optional
from ghosts import BaseGhostSystem, TurnGhost
from level import Tile, TileMap, get_available_directions, is_wall, nearest_free
from pacman import Pacman
from util import Direction, Grid2d, center, clamp, to_screen
from tree import create_tree, TreeNode, get_path_from_tree
import math
import pygame
from itertools import product

# picks best routes for each ghost by looking at all possible ghost paths
# and taking the one which maximises an eval function (number of squares, pellets and energisers pacman can reach)
class CornerGhostSystem(BaseGhostSystem):
    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        colours = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 160, 0)]
        self.ghosts: List[TurnGhost] = [
            TurnGhost(ghost_start[0], ghost_start[1], col) for col in colours
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
        # remove pacman paths which are unlikey/bad
        for end in pacman_tree:
            pass

        ghost_trees = [
            create_tree(
                level_map, (ghost.x, ghost.y), closest_dist, ghost.direction, idx
            )
            for idx, ghost in enumerate(self.ghosts)
        ]
        len_before = sum(len(x[-1]) for x in ghost_trees)
        start_time = time.perf_counter()
        # remove paths which go in opposite direction of pacman
        for idx, ghost in enumerate(self.ghosts):
            initial_dist = math.hypot(pacman.x - ghost.x, pacman.y - ghost.y)
            ghost_trees[idx][-1] = list(filter(
                lambda node: math.hypot(node.pos[0]- pacman.x, node.pos[1] - pacman.y)
                < initial_dist+closest_dist*0.7,
                ghost_trees[idx][-1],
            ))


        # generate all possible combinations of paths ghosts could take
        # https://docs.python.org/3/library/itertools.html#itertools.product
        all_combs = list(product(*[x[-1] for x in ghost_trees]))
        len_after = sum(len(x[1]) for x in ghost_trees)
        combs_len = len(all_combs)
        # print("before:", len_before, "\tafter:", len_after, "\tcombs:", len(all_combs))
        all_combs = all_combs[:500]
        # find best
        # TODO: remove obviously bad ones to speed up
        best_eval = 99999
        best_idx = -1
        for comb_idx, comb in enumerate(all_combs):
            # to get better type info
            # comb is a list of final nodes for each ghost in this combination
            # each node stores the idx of its ghost
            comb: Tuple[TreeNode] = comb
            # create ghost path, list of positions in path, for each ghost
            ghost_paths: List[List[TreeNode]] = []
            for path_end in comb:
                node_path = get_path_from_tree(ghost_trees[path_end.ghost_idx], path_end)
                # print(node_path)
                ghost_paths.append([x.pos for x in node_path])

            fittness = CornerGhostSystem.evaluate(ghost_paths, pacman_tree, level_map)
            if fittness < best_eval:
                best_idx = comb_idx
                best_eval = fittness
        total_time = time.perf_counter()-start_time
        if total_time > 0.1:
            print(f"time: {round(total_time, 3)}\tcombs {combs_len}")
        best_paths = all_combs[best_idx]
        # get path for each ghost
        for path_end in best_paths:
            path = get_path_from_tree(ghost_trees[path_end.ghost_idx], path_end)
            # give path to ghost to follow
            self.ghosts[path_end.ghost_idx].set_path_tree(path)

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
        # pacman paths which have died
        dead_paths = [[]]
        for step in range(length):
            dead_paths.append([])
            for idx, pacman_possibility in enumerate(pacman_tree[step]):
                # if parent was dead, kill this one too
                if pacman_possibility.parent in dead_paths[-2]:
                    dead_paths[-1].append(idx)
                    continue

                square = level_map[pacman_possibility.pos[1]][pacman_possibility.pos[0]]
                if square is Tile.EMPTY:
                    total_points += 1
                elif square is Tile.PELLET:
                    total_points += 5
                elif square is Tile.SUPER_PELLET:
                    total_points += 100

                # check collisions with ghosts
                for path in ghost_paths:
                    if pacman_possibility.pos == path[step]:
                        dead_paths[-1].append(idx)
                # also check previous pacman step to stop ghost and pacman stepping past each other
                if pacman_possibility.parent != None and step > 0:
                    parent = pacman_tree[step - 1][pacman_possibility.parent]
                    for path in ghost_paths:
                        if parent.pos == path[step]:
                            dead_paths[-1].append(idx)

        return total_points
