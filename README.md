# Pacman
Pacman with various ghost and pacman ai's, made with python and pygame

ghost ai:
- classic: replica of the ghost ai from original pacman game (`src/game/ghosts.py`)
- random: all ghosts turn randomly (`src/game/ghosts.py`)
- predict: tries to predict where pacman will go and target possible positions with A* (`src/ai/ghosts/ai1.py`)
- corner: considers all possible ghost paths and picks one the reduces available squares, pellets and super pellets to pacman, function to evaluate ghost paths is written in c beacuse python was too slow (`src/ai/ghosts/ai2.py` and `src/ai/ghosts/evaluate.c`)
- pathfind: ghosts use a* to pathfind to pacman but the adjecency values are adjusted to make going the same path as another ghost more costly and cutting off pacman less costly (`src/ai/ghosts/ai3.py`)
- machine learning: trained model (`src/ai/ghosts/ai4.py`)

pacman ai:
- user: uses keyboard input (`src/game/pacman.py`)
- random: turns randomly (`src/ai/pacman/pacman_random.py`)
- greedy: take path that will maximize score some moves in the future (`src/ai/pacman/pacman_ai1.py`)
- scared: tries to get as far away from ghosts as possible (`src/ai/pacman/pacman_ai2.py`)
- machine learning: (`src/ai/pacman/pacman_ai3.py`)

## Install / run
install dependencies with
`pip install -r requirements.txt`
run with
`python src/game.py`

Builds to an executable with Pyinstaller