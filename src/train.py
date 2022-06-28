import math
from ai.ghosts.ai1 import PredictGhostSystem
from ai.ghosts.ai3 import AStarGhostSystem
from game.ghosts import BaseGhostSystem, RandomGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.game import Game
from game.level import classic_map, classic_map_ghost, classic_map_pacman
import tensorflow.keras as keras
import tensorflow as tf
from ai.level_mapper import to_pacman_relative_inputs, view_size

# just guessing what will work, should experiment later
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(5, view_size, view_size)),
    tf.keras.layers.Dense(math.floor(view_size*view_size), activation='relu'),
    tf.keras.layers.Dense(math.floor(view_size*view_size)*0.1, activation='relu'),
    tf.keras.layers.Dense(4)
])

if __name__ == "__main__":
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    ghosts = BaseGhostSystem(classic_map_ghost)
    pacman = RandomPacman(*classic_map_pacman)
    to_pacman_relative_inputs(classic_map, ghosts, pacman, view_size)
