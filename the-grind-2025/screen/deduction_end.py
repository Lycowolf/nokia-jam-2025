from typing import Self, Callable
from constants import *
from input import btnp as pressed, Map
from constants import SMART_TEXT_MARKER, SCREEN_H
from .smart_text import SmartText
import game_state
from .transition import Transition
from misc_types import Way
from .lore import show_encyclopedia
from .deduction import draw_progress
from .confirmation import ConfirmationScreen
from .base import Screen

class DeductionEndScreen(SmartText):
    last = None

    def __init__(self, smart_text: str, word_set: list[str], ending_selector: Callable[[SmartText], Screen]):
        super().__init__(smart_text,
                         [word_set[0] for _ in range(smart_text.count(SMART_TEXT_MARKER))],
                         set(word_set))

        self.ending_selector = ending_selector

        self.prev = self
        self.next = self
        self.solved = False

    def correct(self):
        return False

    def draw(self):
        super().draw()

        draw_progress(game_state.deduction_progress(self))

    def update(self) -> Self:
        game_state.last_deduction = self

        if self.was_updated() and self.selected_word_idx == len(self.words) - 1:
            # last word updated
            next_screen = self.ending_selector(self)
            return ConfirmationScreen(self, next_screen, 'Are you sure?')

        new_state = super().update()
        if new_state != self:
            return new_state

        if pressed(Map.left):
            return Transition(self, self.prev, shift_dir=Way.left)

        if pressed(Map.right):
            return Transition(self, self.next, shift_dir=Way.right)

        if pressed(Map.switch):
            return Transition(self, game_state.last_investigation, fade_label="Investigation")

        if pressed(Map.lore):
            return show_encyclopedia(self)

        return self
