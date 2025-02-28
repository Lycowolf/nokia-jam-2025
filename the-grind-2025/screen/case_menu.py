from typing import Self
import pyxel

from constants import BACKGROUND
from ui import draw_wrapped_text, draw_text_row, switch_palette
from input import btnp as pressed, Map
import scenario
from . import Screen, Transition

class CaseMenuScreen(Screen):
    def __init__(self):
        self.current = 0
        self.cases = [
            ('Tutorial', scenario.tutorial.setup_scenario),
            ('Haunted mansion', scenario.haunted_mansion.setup_scenario),
            ('Deadly theatrics', scenario.investigation_test.setup_test_scenario),
        ]

    def draw(self):
        pyxel.cls(BACKGROUND)
        draw_text_row(0, "Select case:", x_off=5)

        for i, (text, _) in enumerate(self.cases):
            # if i == self.current:
            #     text = invert_text(text)
            draw_text_row(i+1, text, x_off=10)

        draw_text_row(self.current+1, ">", x_off=6)



    def update(self) -> Self:
        if pressed(Map.action):
            case = self.cases[self.current][1]()
            return Transition(self, case, fade_noise="dark")

        if pressed(Map.up):
            self.current = (self.current - 1) % len(self.cases)

        if pressed(Map.down):
            self.current = (self.current + 1) % len(self.cases)

        return self