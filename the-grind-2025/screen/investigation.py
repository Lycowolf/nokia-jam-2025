from typing import Self
import pyxel
from ui import draw_wrapped_text, draw_text_row
from input import btnp as pressed, Map
from .search_menu import SearchMenuScreen
from .item import ItemScreen
import game_state
from misc_types import Way

from .base import Screen
from .transition import Transition

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
        draw_text_row(6, exit_indicator, x_off=-3)

    def update(self) -> Self:
        game_state.last_investigation = self

        for way in Way.all():
            if self.exits[way] and pressed(Map.way_keys[way]):
                return Transition(self, self.exits[way], shift_dir=way)

        if pressed(Map.action):
            if len(self.objects) == 0:
                return ItemScreen(self, "Nothing to search here")
            else:
                return SearchMenuScreen(self, self.objects)

        if pressed(Map.switch):
            return game_state.last_deduction

        return self

