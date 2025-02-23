from symtable import Class

import pyxel
from typing import Self, Callable
from abc import ABC
import ui
from input import Map
from ui import invert_text_blink, draw_text_row, draw_smart_text
from constants import *
from input import btnp
import sound

class Screen(ABC):
    # Screens form a state machine. update() method updates self as necessary and returns a Screen to switch to
    # (can be self).
    def update(self) -> "Screen":
        return self

    def draw(self) -> None:
        pass

# TODO: scrolling
class Menu(Screen):
    intro_text = "The Player chose a(n) {} palette and {} the game."
    known_words = {"original", "harsh", "gray", "looked at", "started"}
    words = ["original", "looked at"]
    frame = 0
    selected_smart_word = 0

    def __init__(self):
        ui.switch_palette(self.words[0])

    def update(self) -> Screen:
        self.frame = (self.frame + 1) % FPS
        def on_word_selected(word):
            self.words[0] = word
            ui.switch_palette(word)
            sound.play("c3e3", 8)

        # TODO: scrolling

        if btnp(Map.action):
            return WordMenu(self.known_words, self.words[0], on_word_selected, self)

        return self

    def draw(self):
        pyxel.cls(0)
        smart_word_rows = draw_smart_text(
            self.intro_text,
            self.words,
            self.known_words,
            0,
            (self.frame > FPS // 2),
            0)


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

        pyxel.cls(0)
        for i in range(TEXT_ROWS):
            word_idx = start_idx + i
            if not (0 <= word_idx < len(self.words)):
                continue
            if word_idx == self.selected:
                word = invert_text_blink(self.words[word_idx], False)
            else:
                word = self.words[word_idx]
            draw_text_row(i, word)

class Victory(Screen):
    def update(self):
        return self

    def draw(self):
        pyxel.cls(0)
        ui.draw_text_row(MIDDLE_ROW, "You win!", 1)