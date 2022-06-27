from typing import Tuple
from enum import Enum
import pygame


class AnchorPoint(Enum):
    CENTER = (0.5, 0.5)
    BOTTOM_LEFT = (0, 1)


def calc_pos(
    screen: pygame.Surface, anchor: AnchorPoint, pos: Tuple[int, int]
) -> Tuple[int, int]:
    x = screen.get_width() * anchor.value[0] + pos[0]
    y = screen.get_height() * anchor.value[1] + pos[1]
    return (x, y)


class Button:
    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        screen_anchor: AnchorPoint,
        button_anchor: AnchorPoint,
        text: str,
    ):
        self.x, self.y, self.w, self.h = rect
        self.text = text
        self.hovered = False
        self.held = False
        self.hover_shrink = 5
        self.screen_anchor = screen_anchor
        self.button_anchor = button_anchor

    def step(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        l_mouse, m_mouse, r_mouse = pygame.mouse.get_pressed()
        if (
            mouse_x > self.x
            and mouse_x < self.x + self.w
            and mouse_y > self.y
            and mouse_y < self.y + self.h
        ):
            self.hovered = True
            if not l_mouse and self.held:
                return True
            if l_mouse:
                self.held = True
        elif not l_mouse:
            self.hovered = False

        return False

    def draw(self, screen):
        hover_offset = (self.hovered + self.held) * self.hover_shrink
        pos = calc_pos(screen, self.screen_anchor, (self.x, self.y))
        pos = (
            pos[0] - self.w * self.button_anchor.value[0],
            pos[1] - self.h * self.button_anchor.value[1],
        )
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (
                pos[0] - hover_offset,
                pos[1] - hover_offset,
                self.w + hover_offset * 2,
                self.h + hover_offset * 2,
            ),
            10,
        )
