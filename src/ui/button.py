import math
import random
from typing import Tuple
from enum import Enum
import pygame
from game.util import Grid2d
from ui.text import TextAlign, Text


class AnchorPoint(Enum):
    CENTER = (0.5, 0.5)
    BOTTOM_LEFT = (0, 1)
    BOTTOM_RIGHT = (1, 1)
    TOP_LEFT = (0, 0)


def calc_pos(
    screen: pygame.Surface, anchor: AnchorPoint, pos: Tuple[int, int]
) -> Tuple[int, int]:
    
    return (x, y)


class Button:
    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        screen_anchor: AnchorPoint,
        button_anchor: AnchorPoint,
        text: str,
        text_size: int = 32,
    ):
        self.x, self.y, self.w, self.h = rect
        self.str_text = text
        self.hovered = False
        self.held = False
        self.hover_expand = 0.05
        self.screen_anchor = screen_anchor
        self.button_anchor = button_anchor
        self.texts = [
            Text(text, text_size, (255, 255, 255), TextAlign.CENTER),
            Text(text, round(text_size*(1+self.hover_expand)), (255, 255, 255), TextAlign.CENTER),
            Text(text, round(text_size*(1+self.hover_expand*2)), (255, 255, 255), TextAlign.CENTER),
        ]

    def calc_pos(self, screen) -> Grid2d:
        # calculate position of button anchor on screen
        x = screen.get_width() * self.screen_anchor.value[0] + self.x
        y = screen.get_height() * self.screen_anchor.value[1] + self.y
        # calculate position of button top left on screen
        pos = (
            x - self.w * self.button_anchor.value[0],
            y - self.h * self.button_anchor.value[1],
        )
        return pos

    def draw(self, screen: pygame.Surface, selected: bool = False) -> bool:
        pos = self.calc_pos(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        l_mouse, m_mouse, r_mouse = pygame.mouse.get_pressed()
        if (
            mouse_x > pos[0]
            and mouse_x < pos[0] + self.w
            and mouse_y > pos[1]
            and mouse_y < pos[1] + self.h
        ):
            self.hovered = True
            # if just released
            if (not l_mouse) and self.held:
                self.held = False
                return True
            if l_mouse:
                self.held = True
        else:
            self.hovered = False
            self.held = False
        if not l_mouse:
            self.held = False

        offset_percent = (self.hovered + self.held) * self.hover_expand
        offset_pixels = (offset_percent * self.w, offset_percent * self.h)
        pygame.draw.rect(
            screen,
            (0, 100, 255) if selected else (0, 0, 255),
            (
                math.floor(pos[0] - offset_pixels[0]),
                math.floor(pos[1] - offset_pixels[1]),
                math.floor(self.w + offset_pixels[0] * 2),
                math.floor(self.h + offset_pixels[1] * 2),
            ),
            5,
            5,
        )
        self.texts[int(self.hovered+self.held)].draw(screen, math.floor(pos[0]+self.w/2), math.floor(pos[1]+self.h/2))
        pygame.display.update(
            (
                math.floor(pos[0] - self.hover_expand * self.w * 2),
                math.floor(pos[1] - self.hover_expand * self.h * 2),
                math.floor(self.w * (1 + self.hover_expand * 4)),
                math.floor(self.h * (1 + self.hover_expand * 4)),
            )
        )

        return False
