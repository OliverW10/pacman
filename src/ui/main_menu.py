from typing import List, Dict, Optional
from game.game import Game
from game.ghosts import BaseGhostSystem
from game.pacman import BasePacman
from ui.button import Button, AnchorPoint
from game.level import classic_map


class MainMenu:
    def __init__(
        self, pacmans: Dict[str, BasePacman], ghost_systems: Dict[str, BaseGhostSystem]
    ):
        self.pacmans = pacmans
        self.ghost_systems = ghost_systems
        self.start_button = Button(
            (0, 100, 100, 30), AnchorPoint.CENTER, AnchorPoint.CENTER, "Start"
        )
        self.quit_button = Button(
            (10, -10, 65, 25), AnchorPoint.BOTTOM_LEFT, AnchorPoint.BOTTOM_LEFT, "Quit"
        )

        self.pacman_buttons: List[Button] = []
        for i, name in enumerate(pacmans):
            self.pacman_buttons.append(
                Button(
                    (-180, -100 + i * 60, 180, 45),
                    AnchorPoint.CENTER,
                    AnchorPoint.CENTER,
                    name,
                )
            )

        self.ghost_buttons: List[Button] = []
        for i, name in enumerate(ghost_systems):
            self.ghost_buttons.append(
                Button(
                    (180, -100 + i * 60, 180, 45),
                    AnchorPoint.CENTER,
                    AnchorPoint.CENTER,
                    name,
                )
            )

        self.selected_ghost = 0
        self.selected_pacman = 0

    def draw(self, screen) -> Optional[Game]:
        if self.start_button.draw(screen):
            return Game(
                classic_map,
                self.pacmans[list(self.pacmans.keys())[self.selected_pacman]],
                self.ghost_systems[list(self.ghost_systems.keys())[self.selected_ghost]],
            )
        if self.quit_button.draw(screen):
            quit()

        for idx, butt in enumerate(self.pacman_buttons):
            ret = butt.draw(screen, idx == self.selected_pacman)
            if ret:
                self.selected_pacman = idx
        for idx, butt in enumerate(self.ghost_buttons):
            ret = butt.draw(screen, idx == self.selected_ghost)
            if ret:
                self.selected_ghost = idx
