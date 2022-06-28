import math
from ai.ghosts.ai1 import PredictGhostSystem
from ai.ghosts.ai3 import AStarGhostSystem
from game.ghosts import BaseGhostSystem, RandomGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.game import Game
from game.level import classic_map, classic_map_ghost, classic_map_pacman
import keras.layers as layers
import keras.losses as losses
import tensorflow as tf
from ai.level_mapper import to_pacman_relative_inputs, view_size
import numpy as np
import time

start_time = time.perf_counter()
outputs = np.load("outputs.npy")
inputs = np.load("inputs.npy")
print("file load time:", time.perf_counter()-start_time)
print("inputs shape:", inputs.shape)
print("outputs shape:", outputs.shape)
# just guessing at structure, should experiment later
model = tf.keras.models.Sequential([
    layers.Flatten(input_shape=(5, view_size, view_size)),
    layers.Dense(math.floor(view_size*view_size), activation='relu'),
    layers.Dense(math.floor(view_size*view_size)*0.1, activation='relu'),
    layers.Dense(4)
])

if __name__ == "__main__":
    model.compile(
        optimizer='adagrad',
        loss=losses.CategoricalCrossentropy(),
        metrics=['accuracy']
    )
    model.fit(inputs, outputs, epochs=200)
    ghosts = BaseGhostSystem(classic_map_ghost)
    pacman = RandomPacman(*classic_map_pacman)
    time.sleep(10)
    to_pacman_relative_inputs(classic_map, ghosts, pacman, view_size)