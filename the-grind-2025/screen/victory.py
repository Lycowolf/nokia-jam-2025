import pyxel
import ui
from constants import *
from .base import Screen

class Victory(Screen):
    def update(self):
        return self

    def draw(self):
        pyxel.cls(BACKGROUND)
        ui.draw_centered_text_row(MIDDLE_ROW, "CASE SOLVED", FOREGROUND)