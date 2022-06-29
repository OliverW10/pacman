import math
import random
import numpy as np
import pygame
from typing import List, Tuple
from ai.tree import create_tree, draw_tree, get_path_from_tree
from game.ghosts import BaseGhostSystem
from game.level import Tile
from game.pacman import BasePacman
from game.util import ALL_DIRECTIONS, Direction, center, int_to_dir, to_screen
import keras.models as models
from ai.level_mapper import to_pacman_relative_inputs, view_size
import tensorflow as tf

# machine learning
class MachineLearningPacman(BasePacman):
    def __init__(self, x, y, model_path):
        super().__init__(x, y)
        self.wanted_dir = Direction.NONE
        self.path = []
        self.model: models.Model = models.load_model(model_path)
        self.outputs = []
    
    @property
    def cornercut(self) -> float:
        # wont work below 15 fps
        return 1/15

    def step(self, dt: float, level_map: List[List[Tile]], ghost_system: BaseGhostSystem):
        super().step(dt, level_map, ghost_system)
        inputs = to_pacman_relative_inputs(level_map, ghost_system, self, view_size)
        inputs = tf.reshape(inputs, [1, 5, 20, 20])
        outputs: np.ndarray = self.model.predict(inputs)
        self.wanted_dir = int_to_dir(outputs.argmax())

    def check_new_direction(self, tile_map) -> Direction:
        return self.wanted_dir

    def draw(self, screen, offset: Tuple[int, int], grid_size: int):
        super().draw(screen, offset, grid_size)
        for g1, g2 in zip(self.path, self.path[1:]):
            p1 = to_screen(center(g1.pos), offset, grid_size)
            p2 = to_screen(center(g2.pos), offset, grid_size)
            pygame.draw.line(screen, self.colour, p1, p2, 3)