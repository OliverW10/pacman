import time
import pygame
import math
from ai.ghosts.ai1 import PredictGhostSystem
from ai.ghosts.ai3 import AStarGhostSystem
from ai.pacman.pacman_ai2 import ScaredPacman
from ai.pacman.pacman_random import RandomPacman
from ai.pacman.pacman_ai1 import GreedyPacman
from game.game import Game
from game.ghosts import ClassicGhostSystem
from game.pacman import UserPacman, UserPacman
from game.level import classic_map, classic_map_pacman, classic_map_ghost
from enum import Enum, auto
from ui.button import AnchorPoint, Button
from ui.main_menu import MainMenu
pygame.init()

class GameState(Enum):
    MENU = auto()
    GAME = auto()

pacmans = {
    "User": UserPacman(*classic_map_pacman),
    "Random": RandomPacman(*classic_map_pacman),
    "Scared": ScaredPacman(*classic_map_pacman),
    "Greedy": GreedyPacman(*classic_map_pacman),
}

ghost_systems = {
    "Classic": ClassicGhostSystem(classic_map_ghost),
    "Predict": PredictGhostSystem(classic_map_ghost),
    "A*": AStarGhostSystem(classic_map_ghost),
}

game = Game(classic_map, pacmans["User"], ghost_systems["A*"])
auto_respawn_button = Button(
    (10, 10, 140, 35), AnchorPoint.TOP_LEFT, AnchorPoint.TOP_LEFT, "Auto respawn", 24
)
# wether to restart the game or go to the main menu
auto_respawn = False
back_button = Button(
    (10, -10, 65, 25), AnchorPoint.BOTTOM_LEFT, AnchorPoint.BOTTOM_LEFT, "Back", 28
)
main_menu = MainMenu(pacmans, ghost_systems)

running = True
game_state = GameState.MENU
last_frame_time = time.time()

# setup pygame
pygame.display.set_caption("Test caption")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
screen = pygame.display.set_mode((800, 600))
fps_ticker = 0
map_w = len(game.tilemap[0])
map_h = len(game.tilemap)
padding = 0.15
grid_size = math.floor(
    (1 - padding) / max(map_w / screen.get_width(), map_h / screen.get_height())
)
game_rect = (
    400 - map_w / 2 * grid_size,
    300 - map_h / 2 * grid_size,
    map_w * grid_size,
    map_h * grid_size,
)
while running:
    # get delta time
    dt = time.time() - last_frame_time
    # cap the dt to prevent weird behavior
    dt = min(dt, 1/30)
    last_frame_time = time.time()
    # print out fps every hundred frames
    fps_ticker += 1
    if fps_ticker > 100 and dt!=0:
        print(f"fps: {1/dt}")
        fps_ticker = 0

    # quit on quit event
    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    if game_state is GameState.MENU:
        game = main_menu.draw(screen)
        if game:
            game_state = GameState.GAME
            screen.fill((0, 0, 0))
            pygame.display.flip()

    if game_state is GameState.GAME:
        died, score = game.step(dt, True)
        if died and not auto_respawn:
            print(score)
            game_state = GameState.MENU
            screen.fill((0, 0, 0))
            pygame.display.flip()
            continue
        grid_size = math.floor(
            (1 - padding) / max(map_w / screen.get_width(), map_h / screen.get_height())
        )
        game.draw(
            screen,
            400 - map_w/2 * grid_size,
            300 - map_h/2 * grid_size,
            map_w * grid_size,
            map_h * grid_size,
        )
        if auto_respawn_button.draw(screen, auto_respawn):
            auto_respawn = not auto_respawn
        if back_button.draw(screen):
            game_state = GameState.MENU
            screen.fill((0, 0, 0))
            pygame.display.flip()

