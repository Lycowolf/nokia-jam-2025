import pyxel
from ui import draw_wrapped_text, draw_text_coords
from input import btnp as pressed, Map
from .base import Screen
from constants import *

class StoryScreen(Screen):
    def __init__(self, next_screen, script):
        self.next = next_screen
        self.more = script
        self.text = self.more.pop(0)

    def draw(self):
        pyxel.cls(BACKGROUND)
        draw_wrapped_text(self.text, 0)
        draw_text_coords(-1, -1, "..." if self.more else "→→")

    def update(self):
        if pressed(Map.action):
            if self.more:
                self.text = self.more.pop(0)
            else:
                return self.next

        if pressed(Map.back):
            return self.next

        return self
