import pygame
from enum import Enum
from typing import Tuple

class TextAlign(Enum):
    LEFT = 0
    CENTER = 0.5
    RIGHT = 1

class Text:
    def __init__(self, text: str, size: int, colour: Tuple[int, int, int], align=TextAlign.CENTER):
        print("default: ", pygame.font.get_default_font())
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), size)
        self.align = align
        self.colour = colour
        self.text = ""
        self.set_text(text)

    def set_text(self, text: str):
        if text != self.text:
            self.text = text
            self._text = self.font.render(self.text, True, self.colour)
            self.size = self.font.size(self.text)
        print("size", self.size)

    def draw(self, screen: pygame.Surface, x, y):
        draw_x = x - self.size[0]*self.align.value
        draw_y = y - self.size[1]*self.align.value
        screen.blit(self._text, (draw_x, draw_y))
        pygame.display.update((draw_x, draw_y, self.size[0], self.size[1]))