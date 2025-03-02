import pyxel

import ui
from constants import BACKGROUND, MIDDLE_ROW, FOREGROUND
from screen import Screen
from ui import draw_centered_text_row
from input import btnp, Map
from .confirmation import ConfirmationScreen
import game_state

class EndingScreen(Screen):
    def update(self):
        if btnp(Map.action) or btnp(Map.back) or btnp(Map.main_menu):
            return ConfirmationScreen(self, game_state.case_menu, 'Return to case menu?')

        return self


class Unsolved(EndingScreen):
    text: str
    def __init__(self, text):
        self.text = text

    def draw(self):
        pyxel.cls(BACKGROUND)
        ui.draw_centered_text_row(MIDDLE_ROW - 1, "CASE UNSOLVED")
        ui.draw_centered_text_row(MIDDLE_ROW + 1, self.text)


class Victory(EndingScreen):
    def draw(self):
        pyxel.cls(BACKGROUND)
        ui.draw_centered_text_row(MIDDLE_ROW, "CASE SOLVED", FOREGROUND)


class GameOverScreen(EndingScreen):
    text: str
    def __init__(self, text):
        self.text = text

    def draw(self):
        pyxel.cls(FOREGROUND)
        lines = self.text.splitlines()
        i = 0
        for i in range(len(lines)):
            draw_centered_text_row(i, lines[i], BACKGROUND)
            i += 1
        draw_centered_text_row(i+2, "GAME OVER", BACKGROUND)
