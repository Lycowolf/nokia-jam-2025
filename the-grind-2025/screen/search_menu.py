from typing import Self
import pyxel
from ui import draw_wrapped_text, draw_text_row
from input import btnp as pressed, Map

from .base import Screen
from .item import ItemScreen


class SearchMenuScreen(Screen):
    def __init__(self, previous_screen, objects):
        self.prev = previous_screen

        self.current = 0
        self.objects = objects

    def draw(self):
        pyxel.cls(0)
        for i, (text, _) in enumerate(self.objects):
            # if i == self.current:
            #     text = invert_text(text)
            draw_text_row(i, text, x_off=5)

        draw_text_row(self.current, ">", x_off=1)



    def update(self) -> Self:
        if pressed(Map.action):
            return ItemScreen(self, self.objects[self.current][1])

        if pressed(Map.back):
            return self.prev

        if pressed(Map.up):
            self.current = (self.current - 1) % len(self.objects)

        if pressed(Map.down):
            self.current = (self.current + 1) % len(self.objects)

        return self