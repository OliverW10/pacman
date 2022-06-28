from typing import List, Dict, Optional

import pygame
from game.game import Game
from game.ghosts import BaseGhostSystem
from game.pacman import BasePacman
from ui.button import Button, AnchorPoint
from ui.text import Text
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
            (10, -10, 65, 25), AnchorPoint.BOTTOM_LEFT, AnchorPoint.BOTTOM_LEFT, "Quit", 28
        )

        self.pacman_buttons: List[Button] = []
        for i, name in enumerate(pacmans):
            self.pacman_buttons.append(
                Button(
                    (-180, -80 + i * 60, 180, 45),
                    AnchorPoint.CENTER,
                    AnchorPoint.CENTER,
                    name,
                )
            )

        self.ghost_buttons: List[Button] = []
        for i, name in enumerate(ghost_systems):
            self.ghost_buttons.append(
                Button(
                    (180, -80 + i * 60, 180, 45),
                    AnchorPoint.CENTER,
                    AnchorPoint.CENTER,
                    name,
                )
            )

        self.selected_ghost = 0
        self.selected_pacman = 0

        self.title_text = Text("PorkMan", 86, (235, 219, 52))
        self.pacman_text = Text("Pacman controller", 32, (255, 255, 255))
        self.ghost_text = Text("Ghosts controller", 32, (255, 255, 255))

    def draw(self, screen: pygame.Surface) -> Optional[Game]:
        self.title_text.draw(screen, screen.get_width()/2, screen.get_height()*0.17)
        _, top_butt_y = self.pacman_buttons[0].calc_pos(screen)
        self.pacman_text.draw(screen, screen.get_width()/2-180, top_butt_y-20)
        self.ghost_text.draw(screen, screen.get_width()/2+180, top_butt_y-20)

        if self.start_button.draw(screen):
            self.pacmans[list(self.pacmans.keys())[self.selected_pacman]].reset()
            self.ghost_systems[list(self.ghost_systems.keys())[self.selected_ghost]].reset()
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
