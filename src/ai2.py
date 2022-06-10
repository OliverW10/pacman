import random
from typing import List, Tuple, Optional
from ghosts import ClassicGhost, GhostSystem, BaseGhost
from level import Tile, TileMap, get_available_directions, is_wall, nearest_free
from pacman import Pacman
from pathfinder import pathfind
from util import Direction, Grid2d, TreeNode, center, clamp, create_tree, to_screen
from tree import create_tree, TreeNode
import math
import pygame


class PathGhost(BaseGhost):
    def __init__(self, x, y, colour):
        super().__init__(x, y)
        self.colour = colour
        self.cur_colour = colour
        self.path: List[Grid2d] = []
        self.goal: Grid2d = [0, 0]

    def set_goal(self, goal: Grid2d, level: TileMap):
        self.goal = goal

    # called whenever there are more than one possible directions to go
    def get_new_direction(
        self, available: List[Direction], level_map: TileMap
    ) -> Direction:
        x = math.floor(self.x)
        y = math.floor(self.y)
        last_x = x - self.last_direction.value[0]
        last_y = y - self.last_direction.value[1]
        # remember state of square behind us
        temp = level_map[last_y][last_x]
        # fill square behind us to stop turning around
        level_map[last_y][last_x] = Tile.WALL
        # move goal out of walls, TODO: can fail
        goal = nearest_free(level_map, *[math.floor(n) for n in self.goal])
        # find path to goal
        self.path = pathfind(level_map, (x, y), goal)
        # restore square behind us
        level_map[last_y][last_x] = temp
        # find direction from path
        if len(self.path) <= 1:
            print("no path")
            return random.choice(available)
        diff = (self.path[1][0] - x, self.path[1][1] - y)
        wanted_dir = Direction(diff)
        if wanted_dir in available:
            return wanted_dir
        else:
            print("couldnt go in wanted direction")
            return random.choice(available)

    def draw(self, screen, offset, grid_size):
        super().draw(screen, offset, grid_size)

        # for g1, g2 in zip(self.path, self.path[1:]):
        #     p1 = to_screen(center(g1), offset, grid_size)
        #     p2 = to_screen(center(g2), offset, grid_size)
        #     pygame.draw.line(screen, self.colour, p1, p2, 3)


# picks best routes for each ghost by looking at all possible ghost paths
# and taking the one which maximises an eval function (number of squares, pellets and energisers pacman can reach)
class LookaheadGhostSystem(GhostSystem):
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
            create_tree(level_map, (ghost.x, ghost.y), closest_dist, ghost.direction)
            for ghost in self.ghosts
        ]
        

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
