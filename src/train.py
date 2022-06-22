import time
import math
from ai.ghosts.ai3 import AStarGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.game import Game
from game.level import classic_map

pacman = RandomPacman(14, 23.5)
ghosts = AStarGhostSystem((14, 11.5))
game = Game(classic_map, pacman, ghosts)

running = True
for i in range(3):
    score = game.run_full(1/30)
    print(f"{i} : score: {score}")
    game.reset()