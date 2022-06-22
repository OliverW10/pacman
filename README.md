# Pacman
Pacman with various ghost and pacman ai's, made with python and pygame

ghost ai:
- classic: replica of the ghost ai from original pacman game (`src/ghosts.py`)
- random: all ghosts turn randomly (`src/ghosts.py`)
- predict: tries to predict where pacman will go and target possible positions with A* (`src/ai1.py`)
- corner: considers all possible ghost paths and picks one the reduces available squares, pellets and super pellets to pacman, function to evaluate ghost paths is written in c beacuse python was too slow (`src/ai2.py` and `src/evaluate.c`)
- pathfind: ghosts use a* to pathfind to pacman but the adjecency values are adjusted to make going the same path as another ghost more costly and cutting off pacman less costly (`src/ai3.py`)
- machine learning: trained model (`src/ai4.py`)

pacman ai:
- user: uses keyboard input (`src/pacman.py`)
- random: turns randomly (`src/pacman.py`)
- greedy: take path that will maximize score some moves in the future (`src/pacman_ai1.py`)
- machine learning: (`src/pacman_ai2.py`) 

## Install / run
install dependencies with
`pip install -r requirements.txt`
run with
`python src/game.py`

i'll setup a thing to build an exe later


as of 22/6
+--------+--------+--------+--------+---------+
|   vs   |  none  | random | AStar  | predict |
+--------+--------+--------+--------+---------+
| scared | 948.0  | 1034.0 | 1044.0 |  1233.0 |
| random | 2284.0 | 1001.0 | 1777.0 |  1490.0 |
| greedy | 2130.0 | 2766.0 | 3570.0 |  4930.0 |
+--------+--------+--------+--------+---------+