import time
import pygame
import math
from ai.ghosts.ai3 import AStarGhostSystem
from game.game import Game
from game.pacman import UserPacman, UserPacman
from game.level import classic_map

pacman = UserPacman(14, 23.5)
# pacman = UserPacman(35, 16.5, pacman_speed)
ghosts = AStarGhostSystem((14, 11.5))
game = Game(classic_map, pacman, ghosts)

running = True
last_frame_time = time.time()

# setup pygame
pygame.init()
pygame.display.set_caption("Test caption")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
screen = pygame.display.set_mode((800, 600))
fps_ticker = 0
map_w = len(game.tilemap[0])
map_h = len(game.tilemap)
padding = 0.1
grid_size = math.floor(
    (1 - padding) / max(map_w / screen.get_width(), map_h / screen.get_height())
)
print("grid size", grid_size)
game_rect = (
    400 - map_w / 2 * grid_size,
    300 - map_h / 2 * grid_size,
    map_w * grid_size,
    map_h * grid_size,
)
print("score:", game.run_full(1 / 30))
while running:
    # get delta time
    dt = time.time() - last_frame_time
    dt = min(dt, 1/30)
    last_frame_time = time.time()
    # print out fps every hundred frames
    fps_ticker += 1
    if fps_ticker > 100:
        print(f"fps: {1/dt}")
        fps_ticker = 0

    # quit on quit event
    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            running = False

    game.step(dt)
    screen.fill((0, 0, 0))
    game.draw(
        screen,
        400 - map_w/2 * grid_size,
        300 - map_h/2 * grid_size,
        map_w * grid_size,
        map_h * grid_size,
    )
