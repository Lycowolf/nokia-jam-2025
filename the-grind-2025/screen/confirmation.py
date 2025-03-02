from typing import Self

import pyxel

from input import Map, btnp as pressed
from .base import Screen
from constants import *
from ui import draw_text_row, font

class ConfirmationScreen(Screen):
    def __init__(self, prev_screen, next_screen, question):
        self.prev = prev_screen
        self.next = next_screen
        self.text = question

        assert len(question) <= 21, "This won't work with long text. If necessary, implement line break"

        self.current = 1

    def update(self) -> Self:
        if pressed(Map.up) or pressed(Map.down):
            self.current = 1-self.current

        if pressed(Map.action):
            if self.current == 0:
                return self.next
            else:
                return self.prev

        if pressed(Map.back):
            return self.prev

        return self

    def draw(self):
        self.prev.draw()

        text_w = font.text_width(self.text)

        x = (SCREEN_W - text_w) // 2 - 2
        y = 2 * FONT_HEIGHT + TEXT_OFFSET_Y - 2
        w = text_w + 4
        h = 3 * FONT_HEIGHT + TEXT_OFFSET_Y

        pyxel.rect(x, y, w, h, col=BACKGROUND)
        pyxel.line(x+1, y, x+w-1, y, col=FOREGROUND)
        pyxel.line(x + 1, y+h, x + w - 1, y+h, col=FOREGROUND)
        pyxel.line(x, y+1, x, y+h-1, col=FOREGROUND)
        pyxel.line(x+w, y + 1, x+w, y + h - 1, col=FOREGROUND)

        draw_text_row(2, self.text, x_off=x + 2)
        draw_text_row(3, "Yes", x_off=30)
        draw_text_row(4, "No", x_off=30)
        draw_text_row(3 + self.current, ">", x_off=25)