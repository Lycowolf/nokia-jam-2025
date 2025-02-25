from typing import Self
import pyxel
from ui import draw_wrapped_text, draw_text_row, draw_smart_text
from input import btnp as pressed, Map
from constants import SMART_TEXT_MARKER, SCREEN_H
from .base import Screen
from .word_menu import WordMenu
from .victory import Victory
import game_state

class DeductionScreen(Screen):
    last = None

    def __init__(self, smart_text, word_set, solutions):
        self.text = smart_text
        self.word_set = word_set
        self.word_count = self.text.count(SMART_TEXT_MARKER)
        self.words = [self.word_set[0] for _ in range(self.word_count)]
        self.solutions = solutions
        self.selected = 0
        self.prev = self
        self.next = self

    def draw(self):
        pyxel.cls(0)

        draw_smart_text(self.text, self.words, self.word_set, self.selected, False, 0)

        draw_progress(game_state.deduction_progress(self))

        if self.correct():
            draw_text_row(6, "ok", x_off=-3)

    def correct(self):
        return self.words == self.solutions

    def on_word_selected(self, word):
        self.words[self.selected] = word

    def update(self) -> Self:
        game_state.last_deduction = self

        if game_state.is_everything_solved():
            return Victory()

        if pressed(Map.left):
            return self.prev

        if pressed(Map.right):
            return self.next

        if pressed(Map.up):
            self.selected = (self.selected - 1) % self.word_count

        if pressed(Map.down):
            self.selected = (self.selected + 1) % self.word_count

        if pressed(Map.action) and not self.correct():
            return WordMenu(self.word_set, self.words[self.selected], self.on_word_selected, self)

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