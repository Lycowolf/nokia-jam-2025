import pyxel
from typing import Self, Callable
from input import Map
from ui import invert_text_blink, draw_text_row, draw_smart_text
from constants import *
from input import btnp
from .base import Screen

# TODO: scrolling markers
class WordMenu(Screen):
    selected: int
    on_confirmed: Callable[[str], None]
    previous_screen: Screen
    words: list[str]

    # NOTE: maybe add selection change callback for weird effects?
    def __init__(self, word_list, selected, on_confirmed: Callable[[str], None], previous_screen):
        """
        Displays a list of word for user to choose from. When choice is confirmed, calls confirmed_callback
        and returns (update()s to) a previous_state.
        """
        self.on_confirmed = on_confirmed
        self.previous_screen = previous_screen
        sorted_words = sorted(list(word_list))
        try:
            self.selected = sorted_words.index(selected)
        except ValueError:
            print(f"can't find index {selected} in {sorted_words}")
            self.selected = 0
        self.words = sorted_words

    def update(self) -> Screen:
        if btnp(Map.down):
            self.selected = min(len(self.words) - 1, self.selected + 1)
        if btnp(Map.up):
            self.selected = max(0, self.selected - 1)
        if btnp(Map.action):
            self.on_confirmed(self.words[self.selected])
            return self.previous_screen
        return self

    def draw(self):
        start_idx = self.selected - MIDDLE_ROW

        pyxel.cls(BACKGROUND)
        for i in range(TEXT_ROWS):
            word_idx = start_idx + i
            if not (0 <= word_idx < len(self.words)):
                continue
            if word_idx == self.selected:
                word = invert_text_blink(self.words[word_idx], False)
            else:
                word = self.words[word_idx]
            draw_text_row(i, word)