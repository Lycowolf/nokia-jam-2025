import pyxel
from ui import draw_wrapped_text, draw_text_row
from input import btnp as pressed, Map
from .base import Screen

class StoryScreen(Screen):
    def __init__(self, next_screen, script):
        self.next = next_screen
        self.more = script
        self.text = self.more.pop(0)

    def draw(self):
        pyxel.cls(0)
        draw_wrapped_text(self.text, 0)
        draw_text_row(6, "..." if self.more else ">>", x_off=-3)

    def update(self):
        if pressed(Map.action):
            if self.more:
                self.text = self.more.pop(0)
            else:
                return self.next

        if pressed(Map.back):
            return self.next

        return self
