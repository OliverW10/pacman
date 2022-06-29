import math
from ai.ghosts.ai1 import PredictGhostSystem
from ai.ghosts.ai3 import AStarGhostSystem
from game.ghosts import BaseGhostSystem, RandomGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.game import Game
from game.level import classic_map, classic_map_ghost_start, classic_map_pacman_start
import keras.layers as layers
import keras.losses as losses
import keras.activations
import keras.models as models
import tensorflow as tf
from ai.level_mapper import to_pacman_relative_inputs, view_size
import numpy as np
import time

start_time = time.perf_counter()
outputs_train = np.load("traindata/outputs-train.npy")
inputs_train = np.load("traindata/inputs-train.npy")
outputs_test = np.load("traindata/outputs-test.npy")
inputs_test = np.load("traindata/inputs-test.npy")
print("file load time:", time.perf_counter()-start_time)

# just guessing at structure, should experiment later
model = models.Sequential([
    layers.Flatten(input_shape=(5, view_size, view_size)),
    layers.Dense(32, activation=keras.activations.sigmoid),
    layers.Dense(4, activation=keras.activations.softmax),
])

if __name__ == "__main__":
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.1,
            epsilon=1.0
        ),
        loss=losses.CategoricalCrossentropy(),
        metrics=['accuracy']
    )
    model.fit(inputs_train, outputs_train, epochs=20)
    model.evaluate(inputs_test, outputs_test)
    model.save("models/1")