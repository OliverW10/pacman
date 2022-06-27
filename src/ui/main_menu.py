from typing import List, Dict, Optional
from game.game import Game
from game.ghosts import BaseGhostSystem
from game.pacman import BasePacman
from ui.button import Button, AnchorPoint


class MainMenu:
    def __init__(
        self, pacmans: Dict[str, BasePacman], ghost_systems: Dict[str, BaseGhostSystem]
    ):
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

    def draw(self, screen) -> Optional[Game]:
        self.start_button.draw(screen)
        self.quit_button.draw(screen)

        for b in self.pacman_buttons:
            b.draw(screen)
        
        for b in self.ghost_buttons:
            b.draw(screen)
