from dataclasses import dataclass
import random
from re import T
from typing import List, Tuple, Optional
from ghosts import ClassicGhost, GhostSystem, BaseGhost
from level import Tile, TileMap, get_available_directions, is_wall, nearest_free
from pacman import Pacman
from pathfinder import pathfind
from util import Direction, Grid2d, center, to_screen
import math
import pygame
from astar import find_path



@dataclass
class TreeNode:
    parent: Optional[int]  # index of parent in list previous list
    pos: Grid2d
    direction: Direction  # direction came from


# explore all possible paths from a position
def create_tree(
    level_map: TileMap, start_pos: Grid2d, length: int, start_direction=Direction.NONE
) -> List[List[TreeNode]]:
    possible_tree = [
        [
            TreeNode(
                None,
                (math.floor(start_pos[0]), math.floor(start_pos[1])),
                start_direction,
            )
        ],
    ]
    for i in range(length):
        possible_tree.append([])
        for idx, current_node in enumerate(possible_tree[i]):
            available_directions = get_available_directions(
                level_map, (current_node.pos[0], current_node.pos[1])
            )
            try:
                available_directions.remove(current_node.direction.inverse())
            except ValueError:
                pass
            for direction in available_directions:
                pos = (
                    current_node.pos[0] + direction[0],
                    current_node.pos[1] + direction[1],
                )
                wrapped_pos = (pos[0] % len(level_map[0]), pos[1] % len(level_map))
                possible_tree[i + 1].append(TreeNode(idx, wrapped_pos, direction))
    return possible_tree


class LookaheadGhost(BaseGhost):
    def __init__(self, x, y, colour):
        super().__init__(x, y)
        self.colour = colour
        self.cur_colour = colour
        self.path: List[Grid2d] = []
        self.goal: Grid2d = [0, 0]

    def set_goal(self, goal: Grid2d, level: TileMap):
        self.goal = goal
    
    # called whenever there are more than one possible directions to go
    def get_new_direction(self, available: List[Direction], level_map: TileMap) -> Direction:
        x = math.floor(self.x)
        y = math.floor(self.y)
        last_x = x-self.last_direction.value[0]
        last_y = y-self.last_direction.value[1]
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
        diff = (self.path[1][0]-x, self.path[1][1]-y)
        wanted_dir = Direction(diff)
        if wanted_dir in available:
            return wanted_dir
        else:
            print("couldnt go in wanted direction")
            return random.choice(available)
    
    def draw(self, screen, offset, grid_size):
        super().draw(screen, offset, grid_size)

        for g1, g2 in zip(self.path, self.path[1:]):
            p1 = to_screen(center(g1), offset, grid_size)
            p2 = to_screen(center(g2), offset, grid_size)
            pygame.draw.line(screen, self.colour, p1, p2, 3)

    
class LookaheadGhostSystem(GhostSystem):
    def __init__(self, ghost_start: Grid2d):
        super().__init__(ghost_start)
        colours = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 160, 0)]
        self.ghosts: List[LookaheadGhost] = [
            LookaheadGhost(ghost_start[0], ghost_start[1], col) for col in colours
        ]
        self.pacman_trees: List[List[TreeNode]] = []
        self.look_ahead = 5
        # ghosts wont set goals within this dist of each other
        self.wipeout_dist = 4
        self.level_size = (0, 0)

    def step(self, dt: float, level_map: List[List[Tile]], pacman: Pacman):
        self.level_size = (len(level_map[0]), len(level_map))
        # create pacman possible path tree
        closest_dist = min(
            [
                math.hypot(ghost.x - pacman.x, ghost.y - pacman.y)
                for ghost in self.ghosts
            ]
        )
        # clamp to 10
        closest_dist = min(10, closest_dist)
        pacman_tree_ahead = create_tree(
            level_map,
            (math.floor(pacman.x), math.floor(pacman.y)),
            math.floor(closest_dist * 1.3),
            pacman.direction,
        )
        pacman_tree_all = create_tree(
            level_map,
            (math.floor(pacman.x), math.floor(pacman.y)),
            math.floor(closest_dist * 0.5),
        )
        self.pacman_trees = [pacman_tree_ahead, pacman_tree_all]
        # pick goals for ghosts
        used_paths = []
        used_ghosts = []
        # all tails of possible paths pacman can take
        _all_ends = [x[-1] for x in self.pacman_trees]
        all_ends: List[TreeNode] = []
        for x in _all_ends:
            all_ends.extend(x)
        # print(all_ends)
        for route_idx in range(len(self.ghosts)):
            avalible_ends = [
                x for i, x in enumerate(all_ends) if not i in used_paths
            ]
            avalible_ghosts = [
                x for i, x in enumerate(self.ghosts) if not i in used_ghosts
            ]
            # more ghosts than pacman paths
            if len(avalible_ends) == 0:
                print("more ghosts than goals")
                for ghost in avalible_ghosts:
                    ghost.set_goal((pacman.x, pacman.y), level_map)
                break
            # find ghost closest to a pacman path
            best_dist = 99999
            # path idx, ghost idx
            best = (-1, -1)
            for gh_idx, ghost in enumerate(avalible_ghosts):
                for path_idx, end in enumerate(avalible_ends):
                    dist = math.hypot(end.pos[0] - ghost.x, end.pos[1] - ghost.y)
                    if dist < best_dist:
                        best_dist = dist
                        best = (path_idx, gh_idx)
            used_paths.append(best[0])
            for idx, p in enumerate(avalible_ends):
                if math.hypot(avalible_ends[best[0]].pos[0]-p.pos[0], avalible_ends[best[0]].pos[1]-p.pos[1]) < 3:
                    used_paths.append(idx)
            used_ghosts.append(best[1])
            avalible_ghosts[best[1]].set_goal(avalible_ends[best[0]].pos, level_map)

        super().step(dt, level_map, pacman)

    def draw_tree(
        self,
        screen: pygame.Surface,
        offset: Grid2d,
        grid_size: int,
        tree: List[List[TreeNode]],
        colour: Tuple[int, int, int],
    ):
        def draw_grid_line(g1: Grid2d, g2: Grid2d):
            p1 = to_screen(center(g1), offset, grid_size)
            p2 = to_screen(center(g2), offset, grid_size)
            pygame.draw.line(screen, colour, p1, p2, 3)

        for step in range(1, len(tree)):
            for node in tree[step]:
                g1 = node.pos
                g2 = tree[step - 1][node.parent].pos
                # check if its wrapped
                if abs(g1[0] - g2[0]) > 5:
                    if g1[0] > g2[0]:
                        draw_grid_line(g1, (self.level_size[0], g1[1]))
                        draw_grid_line(g2, (0, g2[1]))
                    else:
                        draw_grid_line(g2, (self.level_size[0], g2[1]))
                        draw_grid_line(g1, (0, g1[1]))
                else:
                    draw_grid_line(g1, g2)

        for node in tree[-1]:
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                to_screen(center(node.pos), offset, grid_size),
                grid_size * 0.3,
            )

    def draw(self, screen: pygame.Surface, offset: Grid2d, grid_size: int):
        super().draw(screen, offset, grid_size)
        # for tree in self.pacman_trees:
        #     self.draw_tree(screen, offset, grid_size, tree, (255, 200, 100))
        # if random.random() > 0.9:
        #     print(len(self.pacman_tree[-1]))
