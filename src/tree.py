# functions & classes to help with a 'tree' data structure
# has multiple levels of TreeNode's starting from a top level containg just the root
# each node holds a position, direction and the index of the parent in the above level
# Tree[Level[TreeNode], Level[TreeNode, ], Level[TreeNode, ]]

from typing import Optional, List, Tuple
from util import Grid2d, Direction, to_screen, center
from level import TileMap, get_available_directions
from dataclasses import dataclass
import pygame
import math


@dataclass
class TreeNode:
    parent: Optional[int]  # index of parent in previous list
    pos: Grid2d
    direction: Direction  # direction came from
    chance: Optional[float]
    ghost_idx: Optional[int]


def draw_tree(
    screen: pygame.Surface,
    offset: Grid2d,
    grid_size: int,
    tree: List[List[TreeNode]],
    colour: Tuple[int, int, int],
    ends=False
):
    def draw_grid_line(g1: Grid2d, g2: Grid2d, chance: float):
        p1 = to_screen(center(g1), offset, grid_size)
        p2 = to_screen(center(g2), offset, grid_size)
        pygame.draw.line(
            screen, tuple(round(x * chance**0.5) for x in colour), p1, p2, 3
        )

    for step in range(1, len(tree)):
        for node in tree[step]:
            g1 = node.pos
            g2 = tree[step - 1][node.parent].pos
            # check if its wrapped
            if abs(g1[0] - g2[0]) > 5:
                if g1[0] > g2[0]:
                    draw_grid_line(g1, (self.level_size[0], g1[1]), node.chance)
                    draw_grid_line(g2, (0, g2[1]), node.chance)
                else:
                    draw_grid_line(g2, (self.level_size[0], g2[1]), node.chance)
                    draw_grid_line(g1, (0, g1[1]), node.chance)
            else:
                draw_grid_line(g1, g2, node.chance)

    if ends:
        for node in tree[-1]:
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                to_screen(center(node.pos), offset, grid_size),
                grid_size * 0.3,
            )


# explore all possible paths from a position
def create_tree(
    level_map: TileMap,
    start_pos: Grid2d,
    length: int,
    start_direction=Direction.NONE,
    gh_idx=None,
) -> List[List[TreeNode]]:
    possible_tree = [
        [
            TreeNode(
                None,
                (math.floor(start_pos[0]), math.floor(start_pos[1])),
                start_direction,
                1,
                gh_idx,
            )
        ],
    ]
    for i in range(math.floor(length)):
        possible_tree.append([])
        for idx, current_node in enumerate(possible_tree[i]):
            available_directions = get_available_directions(
                level_map, (current_node.pos[0], current_node.pos[1])
            )
            # stop turnaround
            try:
                available_directions.remove(current_node.direction.inverse())
            except ValueError:
                pass

            new_chance = current_node.chance / len(available_directions)
            for direction in available_directions:
                pos = (
                    current_node.pos[0] + direction[0],
                    current_node.pos[1] + direction[1],
                )
                wrapped_pos = (pos[0] % len(level_map[0]), pos[1] % len(level_map))
                possible_tree[i + 1].append(
                    TreeNode(idx, wrapped_pos, direction, new_chance, gh_idx)
                )
    return possible_tree


def get_path_from_tree(
    tree: List[List[TreeNode]], end_node: TreeNode
) -> List[TreeNode]:
    """
    Returns a list of Grid2d's of the path from tree[0] to end_node
    Parameters:
        tree: tree structure like that returned from create_tree
        end_node: a node in tree
    """
    path = [end_node]
    # which level of the tree we are on
    level = len(tree) - 1
    node = end_node
    while (not node.parent is None) and level >= 0:
        level -= 1
        node = tree[level][node.parent]
        path.append(node)
    path.reverse()
    return path
