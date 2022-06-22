#include <stdlib.h>
#include <stdio.h>

typedef enum Directions
{
    RIGHT = 0,
    UP = 1,
    LEFT = 2,
    DOWN = 3
} Direction;

void dir_to_pos(Direction dir, int *ret)
{
    switch (dir)
    {
    case RIGHT:
        ret[0] = 1;
        ret[1] = 0;
        break;
    case UP:
        ret[0] = 0;
        ret[1] = -1;
        break;
    case LEFT:
        ret[0] = -1;
        ret[1] = 0;
        break;
    case DOWN:
        ret[0] = 0;
        ret[1] = 1;
        break;
    default:
        ret[0] = 0;
        ret[1] = 0;
    }
}

// coverts a array or turn directions to array of positions
void ints_to_path(int* turns, int turns_len, int* ret_path, int* ret_path_len){
    
}

// picks a path for each ghost to follow
void pick_paths(
    int level_w,
    int level_h,
    int *level_map,
    int *pacman_pos,
    Direction pacman_dir,
    int ghosts_num,
    int *ghosts,
    Direction *ghosts_dirs,
    int **paths,
    int search_depth)
{
    /*
    Parameters:
        level_w: width of the level in tiles
        level_h: height of the level in tiles
        level_map: array of tiles in row major order
        pacman_pos: pacman x and y position
        pacman_dir: initial pacman direction
        ghosts_num: how many ghosts there are
        ghosts: ghost positions [x1, y1, x2, y2 ...]
        paths: chosen paths to return
    */
    printf("lvl w: %d, lvl h: %d, ghts: %d, pacman x: %d, pacman y: %d\n",
           level_w, level_h, ghosts_num, pacman_pos[0], pacman_pos[1]);
}

// recursively explore all paths
void explore_paths(
    int *ghosts_poss, int depths, int max_depth, int *best_path_fittness, int *best_path
) {
    // paths are stored as array of direction ints for each turn made
}

// to test return arguments with python
int retTest(int *ret, int size)
{
    printf("start func. len: %d\n", size);
    for (int i = 0; i < size; i++)
    {
        ret[i] = -i * i + i * 10;
        printf("idx: %d, val: %d\n", i, ret[i]);
    }
    return size + 5;
}