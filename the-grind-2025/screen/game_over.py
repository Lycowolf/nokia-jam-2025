import pyxel

from constants import BACKGROUND
from screen import Screen
from ui import draw_wrapped_text, draw_centered_text_row


class GameOverScreen(Screen):
    text: str
    def __init__(self, text):
        self.text = text

    def update(self):
        return self

    def draw(self):
        pyxel.cls(BACKGROUND)
        lines = self.text.splitlines()
        i = 0
        for i in range(len(lines)):
            draw_centered_text_row(i, lines[i])
            i += 1
        draw_centered_text_row(i+2, "GAME OVER")