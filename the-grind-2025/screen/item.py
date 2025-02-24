import pyxel
from ui import draw_wrapped_text, draw_text_row
from input import btnp as pressed, Map
from .base import Screen

class ItemScreen(Screen):
    def __init__(self, prev_screen, text):
        self.prev = prev_screen
        self.text = text

    def draw(self):
        pyxel.cls(0)
        draw_wrapped_text(self.text, 0)
        draw_text_row(6, "...", x_off=-3)

    def update(self):
        if pressed(Map.action) or pressed(Map.back):
            return self.prev
        else:
            return self
