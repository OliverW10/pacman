import random
import time
import pygame
import math
from ai.ghosts.ai3 import AStarGhostSystem
from ai.level_mapper import to_pacman_relative_inputs
from ai.pacman.pacman_ai1 import GreedyPacman
from game.game import Game
from game.ghosts import BaseGhostSystem, ClassicGhostSystem
from game.level import Tile, classic_map, classic_map_pacman, classic_map_ghost
from ai.level_mapper import view_size
import numpy as np
pygame.init()


inputs = []
outputs = []
pacmans = [
    GreedyPacman(*classic_map_pacman, 8),
    GreedyPacman(*classic_map_pacman, 20),
    GreedyPacman(*classic_map_pacman, 8),
]
ghost_systems = [
    AStarGhostSystem(classic_map_ghost),
    BaseGhostSystem(classic_map_ghost),
    ClassicGhostSystem(classic_map_ghost),
]
for g in ghost_systems:
    g.set_debug(False)

games = [
    # Game(classic_map, pacmans[0], ghost_systems[0]),
    Game(classic_map, pacmans[1], ghost_systems[1]),
    # Game(classic_map, pacmans[2], ghost_systems[2]),
]

running = True
last_frame_time = time.time()

# setup pygame
pygame.display.set_caption("Test caption")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
screen = pygame.display.set_mode((800, 600))
fps_ticker = 0
map_w = len(games[0].tilemap[0])
map_h = len(games[0].tilemap)
padding = 0.1
grid_size = math.floor(
    (1 - padding) / max(map_w / screen.get_width(), map_h / screen.get_height())
)
game_rect = (
    400 - map_w / 2 * grid_size,
    300 - map_h / 2 * grid_size,
    map_w * grid_size,
    map_h * grid_size,
)
game_idx = 0
game = games[game_idx]

# draw every draw_interval
step_counter = 1
# if pacman hasnt moved in some time kill him
still_cutoff = 1  # seconds
still_counter = 0
last_pos = (0, 0)
# if pacman hasnt gained any score in some time kill him
score_cutoff = 4  # seconds
score_counter = 0
last_score = 0
# if game goes too long (5 minutes) kill it
game_cutoff = 60 * 5 / (1/30)

while running:
    # get delta time
    real_dt = time.time() - last_frame_time
    dt = 1/30
    last_frame_time = time.time()
    # print out fps every hundred frames
    fps_ticker += 1
    if fps_ticker > 100:
        print(f"fps: {1/real_dt}")
        fps_ticker = 0

    # quit on quit event
    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    died, score = game.step(dt, False)
    if died:
        new_pos = (0, 0)
        game_idx = (game_idx+1)%len(games)
        game = games[game_idx]
        while not game.tilemap[new_pos[1]][new_pos[0]] is Tile.PELLET:
            print("generateed new pos", new_pos)
            new_pos = (
                random.randint(0, map_w-1),
                random.randint(0, map_h-1),
            )
        game.pacman.x = new_pos[0]
        game.pacman.y = new_pos[1]

    # incriment timers
    step_counter += 1
    score_counter += dt
    still_counter += dt
    # check if position and score have changed
    if game.score != last_score:
        last_score = game.score
        score_counter = 0
    if (game.pacman.x, game.pacman.y) != last_pos:
        last_pos = (game.pacman.x, game.pacman.y)
        still_counter = 0
    if still_counter > still_cutoff or score_counter > score_cutoff or step_counter > game_cutoff:
        step_counter = 0
        inputs = inputs[:-90]
        outputs = outputs[:-90]
        game.ate_pacman(0)

    if fps_ticker % 30 == 0:
        game.draw(
            screen,
            400 - map_w/2 * grid_size,
            300 - map_h/2 * grid_size,
            map_w * grid_size,
            map_h * grid_size,
        )
    inputs.append(to_pacman_relative_inputs(game.tilemap, game.ghosts_system, game.pacman, view_size))
    outputs.append(game.pacman.get_direction_weights(game.tilemap, game.ghosts_system))
    print(len(outputs))
    # time.sleep(20)
    if len(outputs) > 10000:
        np.save("inputs.npy", inputs)
        np.save("outputs.npy", outputs)
        quit()