from astar import AStar
from game.level import is_wall, Tile
from game.util import Direction, Grid2d, floor_pos
from typing import List, Tuple
import math
import numpy as np

# https://github.com/jrialland/python-astar/blob/master/tests/maze/test_maze.py
class MazeSolver(AStar):

    """sample use of the astar algorithm. In this exemple we work on a maze made of ascii characters,
    and a 'node' is just a (x,y) tuple that represents a reachable position"""

    def __init__(self, maze: List[List[Tile]], tile_modifiers: np.ndarray):
        self.maze = maze
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        self.tile_modifiers = tile_modifiers

    def heuristic_cost_estimate(self, node1, node2):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = node1
        (x2, y2) = node2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        return self.tile_modifiers[n1[1]][n1[0]] * self.tile_modifiers[n2[1]][n2[0]]

    def neighbors(self, node):
        """for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
        nodes that can be reached (=any adjacent coordinate that is not a wall)
        """
        x, y = node
        possible_neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [
            n for n in possible_neighbors if not is_wall(self.maze, n[0], n[1], True)
        ]

# creates an array of ones, 
ones_array = np.ones((100, 100), dtype=np.single)

def pathfind(
    maze: List[List[Tile]],
    start: Grid2d,
    end: Grid2d,
    start_dir=Direction.NONE,
    tile_weights: List[Tuple[Grid2d, float]] = None,
) -> List[Grid2d]:
    """Uses A* to pathfind from `start` to `end` through `maze`, uses `tile_weights` as distance between tiles
    if start_dir is set it wont go in start_dir.inverse() as the first move"""
    # if there was no tile weights given, use the ones array
    if tile_weights is None:
        tile_weights = ones_array
    # TODO: can still turn around on second move
    if not start_dir is Direction.NONE:
        last_x = math.floor(start[0]-start_dir.x)
        last_y = math.floor(start[1]-start_dir.y)
        # check if the guessed last postion is in the map
        if last_x < 0:
            last_x = len(maze[0])-1
        elif last_x >= len(maze[0]):
            last_x = 0
        # remember state of square behind us
        temp = maze[last_y][last_x]
        # fill square behind us to stop turning around
        maze[last_y][last_x] = Tile.WALL
        astar_ret = MazeSolver(maze, tile_weights).astar(floor_pos(start), floor_pos(end))
        # restore square behind us
        maze[last_y][last_x] = temp

        if astar_ret is None:
            return []
        try:
            ret = list(astar_ret)
        except TypeError:
            print("didnt get path or None from MazeSolver")
            return []

        return ret
    else:
        astar_ret = MazeSolver(maze, tile_weights).astar(floor_pos(start), floor_pos(end))
        if astar_ret is None:
            return []
        try:
            ret = list(astar_ret)
        except TypeError:
            print("didnt get path or None from MazeSolver")
            return []

        return ret
