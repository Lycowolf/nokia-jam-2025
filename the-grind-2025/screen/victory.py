import pyxel
import ui
from constants import MIDDLE_ROW
from .base import Screen

class Victory(Screen):
    def update(self):
        return self

    def draw(self):
        pyxel.cls(0)
        ui.draw_text_row(MIDDLE_ROW, "    You win!", 1)