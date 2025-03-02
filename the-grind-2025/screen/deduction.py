from typing import Self
import pyxel
from constants import *
import sound
from ui import draw_wrapped_text, draw_text_row, draw_smart_text
from input import btnp as pressed, Map
from constants import SMART_TEXT_MARKER, SCREEN_H
from .endings import Victory
from .smart_text import SmartText
import game_state
from .transition import Transition
from misc_types import Way
from .lore import show_encyclopedia

class DeductionScreen(SmartText):
    last = None

    def __init__(self, smart_text: str, word_set: list[str], solutions: list[str]):
        super().__init__(smart_text,
                         [word_set[0] for _ in range(smart_text.count(SMART_TEXT_MARKER))],
                         set(word_set))

        self.solutions = solutions

        self.prev = self
        self.next = self
        self.solved = False

    def mark_solved(self):
        sound.deduction_success()
        self.solved = True

        # fix words, remove selection fields
        self.menu_enabled = False
        self.text = self.text.format(*self.words)

    def draw(self):
        super().draw()

        draw_progress(game_state.deduction_progress(self))

        if self.correct():
            draw_text_row(6, "ok", x_off=-3)

    def correct(self):
        return self.words == self.solutions

    def update(self) -> Self:
        if not self.solved and self.was_updated() and self.correct():
            self.mark_solved()

            if game_state.is_everything_solved():
                return Victory()

        new_state = super().update()
        if new_state != self:
            return new_state

        game_state.last_deduction = self



        if pressed(Map.left):
            return Transition(self, self.prev, shift_dir=Way.left)

        if pressed(Map.right):
            return Transition(self, self.next, shift_dir=Way.right)

        if pressed(Map.switch):
            return Transition(self, game_state.last_investigation, fade_label="Investigation")

        if pressed(Map.lore):
            return show_encyclopedia(self)

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
            pyxel.rect(x, y, size, size, col=FOREGROUND)
        else:
            pyxel.rectb(x, y, size, size, col=FOREGROUND)