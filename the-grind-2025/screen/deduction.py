from typing import Self
import pyxel
from ui import draw_wrapped_text, draw_text_row, draw_smart_text
from input import btnp as pressed, Map
from constants import SMART_TEXT_MARKER, SCREEN_H
from .smart_text import SmartText
from .victory import Victory
import game_state
from .transition import Transition
from misc_types import Way

class DeductionScreen(SmartText):
    last = None

    def __init__(self, smart_text, word_set, solutions):
        super().__init__(smart_text,
                         [word_set[0] for _ in range(smart_text.count(SMART_TEXT_MARKER))],
                         word_set)

        self.solutions = solutions

        self.prev = self
        self.next = self

    def draw(self):
        super().draw()

        draw_progress(game_state.deduction_progress(self))

        if self.correct():
            draw_text_row(6, "ok", x_off=-3)

    def correct(self):
        return self.words == self.solutions

    def update(self) -> Self:
        new_state = super().update()
        if new_state != self:
            return new_state

        game_state.last_deduction = self

        if self.menu_enabled and self.correct():
            self.menu_enabled = False
            # fix words, remove selection fields
            self.text = self.text.format(*self.words)

            if game_state.is_everything_solved():
                return Victory()

        if pressed(Map.left):
            return Transition(self, self.prev, shift_dir=Way.left)

        if pressed(Map.right):
            return Transition(self, self.next, shift_dir=Way.right)

        if pressed(Map.switch):
            return game_state.last_investigation

        return self

def draw_progress(progress):
    for idx, (correct, big) in enumerate(progress):
        size = 3
        x = 5 + idx * (size + 2)
        y = SCREEN_H - 5

        if big:
            x -= 1
            y -= 1
            size += 2

        if correct:
            pyxel.rect(x, y, size, size, col=1)
        else:
            pyxel.rectb(x, y, size, size, col=1)