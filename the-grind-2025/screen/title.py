import pyxel
from typing import Self, Callable
from abc import ABC
import ui
from input import Map
from ui import invert_text_blink, draw_text_row, draw_smart_text, layout_smart_text, words_on_screen
from constants import *
from input import btnp
import sound
import game_state
import scenario.investigation_test as case1
from .transition import Transition
from misc_types import Way
from .base import Screen
from .smart_text import SmartText
from scenario import haunted_mansion


class TitleScreen(SmartText):
    def __init__(self):
        super().__init__(
            text="""The Player
                        chose a(n) {} palette.
                        
                        Player then {} the game.""",
            words=["original", "looked at"],
            known_words={"original", "harsh", "gray", "looked at", "started"}
        )

    def update(self) -> Screen:
        new_state = super().update()

        ui.switch_palette(self.words[0])
        if self.words[1] == "started":
            #scenario = case1.setup_test_scenario()
            # return Transition(self, game_state.last_investigation, fade_noise="dark")
            start = haunted_mansion.setup_scenario(skip_intro=False)
            return Transition(self, start, fade_noise="dark")
        else:
            return new_state

    def draw(self) -> None:
        super().draw()