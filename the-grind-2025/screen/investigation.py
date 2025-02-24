from enum import Enum, auto
from typing import Self
import pyxel
from ui import draw_wrapped_text, draw_text_row
from input import btnp as pressed, Map
from .search_menu import SearchMenuScreen
from .item import ItemScreen
import game_state

from .base import Screen

class Way(Enum):
    up = auto(),
    down = auto(),
    left = auto(),
    right = auto(),

    @staticmethod
    def all():
        return [Way.up, Way.down, Way.left, Way.right]

keys = {
    Way.up: Map.up,
    Way.down: Map.down,
    Way.left: Map.left,
    Way.right: Map.right,
}


class InvestigationScreen(Screen):
    last = None

    def __init__(self, name, text, left=None, right=None, up=None, down=None, objects={}):
        self.name = name
        self.text = text
        self.exits = {
            Way.up: up,
            Way.down: down,
            Way.left: left,
            Way.right: right,
        }
        self.objects = objects

    def draw(self):
        pyxel.cls(0)
        draw_wrapped_text(self.text, 0)

        exit_indicator = ''.join(
            (arrow if self.exits[way] is not None else '' for arrow, way in
             zip('<^v>', [Way.left, Way.up, Way.down, Way.right])
            )
        )
        draw_text_row(6, exit_indicator, x_off=70)

    def update(self) -> Self:
        game_state.last_investigation = self

        for way in Way.all():
            if self.exits[way] and pressed(keys[way]):
                return self.exits[way]

        if pressed(Map.action):
            if len(self.objects) == 0:
                return ItemScreen(self, "Nothing to search here")
            else:
                return SearchMenuScreen(self, self.objects)

        if pressed(Map.switch):
            return game_state.last_deduction

        return self

