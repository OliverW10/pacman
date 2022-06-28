import pygame
from typing import List, Tuple
from ai.tree import TreeNode, create_tree, draw_tree, get_path_from_tree
from game.level import Tile, TileMap
from game.pacman import BasePacman
from game.util import ALL_DIRECTIONS, Direction, center, to_screen
from game.ghosts import BaseGhostSystem, GhostMode

# pacman that picks the path that has the highest score
# has no concept of ghosts and if there are no pellets near it it has a panic attack
class GreedyPacman(BasePacman):
    def __init__(self, x, y, depth=8):
        super().__init__(x, y)
        self.wanted_dir = Direction.NONE
        self.path = []
        self.depth = depth

    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1 / 15

    def step(
        self, dt: float, level_map: List[List[Tile]], ghost_system: BaseGhostSystem
    ):
        super().step(dt, level_map, ghost_system)
        pacman_tree = create_tree(level_map, (self.x, self.y), self.depth)
        ghost_trees = [
            create_tree(level_map, (ghost.x, ghost.y), self.depth, ghost.direction)
            for ghost in ghost_system.ghosts
        ]
        self.path = get_path_from_tree(
            pacman_tree,
            max(
                pacman_tree[-1],
                key=lambda x: self.evaluate_path(
                    pacman_tree, x, level_map, ghost_trees, ghost_system
                ),
            ),
        )
        self.wanted_dir = self.path[1].direction

    def check_new_direction(self, tile_map) -> Direction:
        return self.wanted_dir

    def draw(self, screen, offset: Tuple[int, int], grid_size: int):
        super().draw(screen, offset, grid_size)
        for g1, g2 in zip(self.path, self.path[1:]):
            p1 = to_screen(center(g1.pos), offset, grid_size)
            p2 = to_screen(center(g2.pos), offset, grid_size)
            pygame.draw.line(screen, self.colour, p1, p2, 3)

    def evaluate_path(
        self,
        pacman_tree: List[List[TreeNode]],
        end_node: TreeNode,
        level_map: TileMap,
        ghost_trees: List[List[List[TreeNode]]],
        ghost_system: BaseGhostSystem,
    ):
        eatable_for = 0
        if ghost_system.ghost_mode is GhostMode.RUN:
            eatable_for = (GhostMode.RUN.value - ghost_system.mode_timer) * self.speed
        extra_score = 0
        cur_node = end_node
        last_node = end_node
        layer = len(pacman_tree)-1
        # step through each node in path
        while cur_node.parent:
            # check each ghost tree
            for ghost_idx, ghost_tree in enumerate(ghost_trees):
                if ghost_system.ghosts[ghost_idx].dead == False:
                    # check each possibility the ghost could be at
                    for node in ghost_tree[layer]:
                        # if its eaten us
                        if node.pos == cur_node.pos or node.pos == last_node.pos:
                            if eatable_for > 0:
                                extra_score += 100
                            else:
                                return cur_node.score - 1000

            if level_map[cur_node.pos[1]][cur_node.pos[0]] is Tile.SUPER_PELLET:
                eatable_for += 10

            last_node = cur_node
            layer -= 1
            cur_node = pacman_tree[layer][cur_node.parent]
        return end_node.score + extra_score
    
    # estimates how 'good' each direction to go in is
    def get_direction_weights(self, level_map, ghost_system) -> Tuple[float, float, float, float]:
        depth = 8
        pacman_tree = create_tree(level_map, (self.x, self.y), depth)
        ghost_trees = [
            create_tree(level_map, (ghost.x, ghost.y), depth, ghost.direction)
            for ghost in ghost_system.ghosts
        ]
        # get all paths
        pacman_tree[-1].sort(key=lambda x:self.evaluate_path(pacman_tree, x, level_map, ghost_trees, ghost_system))
        paths = [get_path_from_tree(pacman_tree, end_node) for end_node in pacman_tree[-1][:3]]
        direction_weights = [0, 0, 0, 0]
        for idx, path in enumerate(paths):
            d = path[1].direction
            if d is Direction.RIGHT:
                direction_weights[0] += 1/(idx+1)
            if d is Direction.LEFT:
                direction_weights[1] += 1/(idx+1)
            if d is Direction.UP:
                direction_weights[2] += 1/(idx+1)
            if d is Direction.DOWN:
                direction_weights[3] += 1/(idx+1)
        return direction_weights