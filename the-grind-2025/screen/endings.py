from typing import Self

import pyxel

import ui
from constants import BACKGROUND, MIDDLE_ROW, FOREGROUND
from screen import Screen
from ui import draw_centered_text_row


class Unsolved(Screen):
    text: str
    def __init__(self, text):
        self.text = text

    def update(self) -> Self:
        return self

    def draw(self):
        pyxel.cls(BACKGROUND)
        ui.draw_centered_text_row(MIDDLE_ROW - 1, "CASE UNSOLVED")
        ui.draw_centered_text_row(MIDDLE_ROW + 1, self.text)


class Victory(Screen):
    def update(self):
        return self

    def draw(self):
        pyxel.cls(BACKGROUND)
        ui.draw_centered_text_row(MIDDLE_ROW, "CASE SOLVED", FOREGROUND)


class GameOverScreen(Screen):
    text: str
    def __init__(self, text):
        self.text = text

    def update(self):
        return self

    def draw(self):
        pyxel.cls(FOREGROUND)
        lines = self.text.splitlines()
        i = 0
        for i in range(len(lines)):
            draw_centered_text_row(i, lines[i], BACKGROUND)
            i += 1
        draw_centered_text_row(i+2, "GAME OVER", BACKGROUND)
