# Pacman
Pacman with various ghost ai's, made with python and pygame

ghost ai:
- classic: replica of the ghost ai from original pacman game (`src/ghost.py`)
- predict: tries to predict where pacman will go and target possible positions with A* (`src/ai1.py`)
- corner: considers all possible ghost paths and picks one the reduces available squares, pellets and super pellets to pacman (`src/ai2.py`)

## Install / run
install dependencies with
`pip install -r requirements.txt`
run with
`python src/game.py`