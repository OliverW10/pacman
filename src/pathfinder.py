from astar import AStar
from level import is_wall, Tile
from util import Grid2d, floor_pos
from typing import List
import math

# https://github.com/jrialland/python-astar/blob/master/tests/maze/test_maze.py
class MazeSolver(AStar):

    """sample use of the astar algorithm. In this exemple we work on a maze made of ascii characters,
    and a 'node' is just a (x,y) tuple that represents a reachable position"""

    def __init__(self, maze: List[List[Tile]]):
        self.maze = maze
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    def heuristic_cost_estimate(self, node1, node2):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = node1
        (x2, y2) = node2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 1

    def neighbors(self, node):
        """for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
        nodes that can be reached (=any adjacent coordinate that is not a wall)
        """
        x, y = node
        possible_neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [n for n in possible_neighbors if not is_wall(self.maze, n[0], n[1])]


def pathfind(maze: List[List[Tile]], start: Grid2d, end: Grid2d) -> List[Grid2d]:
    return list(MazeSolver(maze).astar(floor_pos(start), floor_pos(end)))
