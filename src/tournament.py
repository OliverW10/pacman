from ai.ghosts.ai1 import PredictGhostSystem
from ai.ghosts.ai3 import AStarGhostSystem
from ai.pacman.pacman_ai1 import GreedyPacman
from ai.pacman.pacman_ai2 import ScaredPacman
from game.ghosts import BaseGhostSystem, RandomGhostSystem
from ai.pacman.pacman_random import RandomPacman
from game.game import Game
from game.level import classic_map
from game.pacman import BasePacman
from prettytable import PrettyTable
import pygame
# game uses text so gotta init pygame to get fonts
pygame.init()

pacmans = {
    "scared": ScaredPacman(*classic_map.pacman_start),
    "random": RandomPacman(*classic_map.pacman_start),
    "greedy": GreedyPacman(*classic_map.pacman_start),
}
ghosts = {
    "none": BaseGhostSystem((14, 11.5)),
    "random": RandomGhostSystem((14, 11.5)),
    "AStar": AStarGhostSystem((14, 11.5)),
    "predict": PredictGhostSystem((14, 11.5)),
}

def get_avg_score(ghost_system: BaseGhostSystem, pacman: BasePacman, runs=20) -> float:
    game = Game(classic_map.map, pacman, ghost_system)
    total = 0
    for i in range(runs):
        game.reset()
        score = game.run_full(1/30)
        print("score:", score)
        total += score
    return total/runs

myTable = PrettyTable(["vs", *ghosts])
for pacman_key in pacmans:
    scores = []
    for ghost_key in ghosts:
        scores.append(round(get_avg_score(ghosts[ghost_key], pacmans[pacman_key], 10), 1))
        print(f"{ghost_key} vs {pacman_key}")
    myTable.add_row([pacman_key, *scores])

print(myTable)