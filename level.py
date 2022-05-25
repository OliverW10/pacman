from enum import Enum
from itertools import permutations
import math
import pygame
from typing import Tuple, List
from util import ALL_DIRECTIONS, Direction, Grid2d

class Tile(Enum):
    EMPTY = 0
    PELLET = 2
    WALL = 1
    SUPER_PELLET = 3

TileMap = List[List[Tile]]

# fmt: off
classic_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,0,0,0,0,1,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,1,0,0,0,0,1,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,1],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
# fmt: on
print("w", len(classic_map[0]), ", h", len(classic_map))
classic_map = [list(map(Tile, row)) for row in classic_map]

# edge safe
def is_wall(tilemap, x, y):
    if x < 0 or x >= len(tilemap[0]) or y < 0 or y >= len(tilemap):
        return True
    else:
        return tilemap[y][x] in [Tile.WALL]

def nearest_free(tilemap, x, y):
    goal = [x, y]
    all_dirs = list(set(permutations((0, 1, 1, -1, -1), 2)))
    i = 0
    while is_wall(tilemap, goal[0], goal[1]):
        if i >= len(all_dirs):
            raise ValueError
        goal[0] = x + all_dirs[i][0] 
        goal[1] = y + all_dirs[i][1] 
        i += 1
    return tuple(goal)

def draw_map(
    screen, grid: List[List[int]], offset: Tuple[float, float], grid_size: int
):
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] is Tile.PELLET:
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        round(offset[0] + grid_size * (x + 0.5)),
                        round(offset[1] + grid_size * (y + 0.5)),
                    ),
                    round(grid_size * 0.1),
                )
            elif grid[y][x] is Tile.SUPER_PELLET:
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        round(offset[0] + grid_size * (x + 0.5)),
                        round(offset[1] + grid_size * (y + 0.5)),
                    ),
                    round(grid_size * 0.35),
                )
            elif grid[y][x] is Tile.WALL:
                # TODO: lines
                pygame.draw.rect(
                    screen,
                    (0, 0, 175),
                    (
                        round(offset[0] + grid_size * x),
                        round(offset[1] + grid_size * y),
                        grid_size + 1,
                        grid_size + 1,
                    ),
                )

def get_available_directions(level_map: List[List[Tile]], pos: Grid2d):
    tile_x = math.floor(pos[0])
    tile_y = math.floor(pos[1])
    return [
        d
        for d in ALL_DIRECTIONS
        if not is_wall(level_map, tile_x + d.value[0], tile_y + d.value[1]) and not d is Direction.NONE
    ]

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        # pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
        draw_map(screen, classic_map, (100, 25), 550 / 31)
        pygame.display.flip()

    pygame.quit()
