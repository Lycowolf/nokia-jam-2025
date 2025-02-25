import pyxel
import ui
from input import Map
from ui import invert_text_blink, draw_text_row, draw_smart_text, layout_smart_text, words_on_screen
from constants import *
from input import btnp
import sound

from .base import Screen
from .word_menu import WordMenu

class SmartText(Screen):
    text: str
    words: list[str]
    known_words: set[str]
    frame = 0
    scroll = 0
    selected_word_idx = 0
    menu_enabled = True

    def __init__(self, text: str, words: list[str], known_words: set[str]):
        self.text = text
        self.words = words
        self.known_words = known_words
        ui.switch_palette(self.words[0]) # TODO

    def update(self) -> Screen:
        self.frame = (self.frame + 1) % FPS
        def on_word_selected(word):
            self.words[self.selected_word_idx] = word
            sound.play("c3e3", 8)

        if btnp(Map.up):
            prev_row, on_screen, _, _ = words_on_screen(self.text, self.words, self.scroll)
            if self.selected_word_idx - 1 in on_screen:
                self.selected_word_idx -= 1
            elif self.selected_word_idx - 1 in prev_row:
                self.scroll -= 1
                self.selected_word_idx -= 1
            else:
                self.scroll = max(0, self.scroll - 1)

        if btnp(Map.down):
            _, on_screen, next_row, max_row = words_on_screen(self.text, self.words, self.scroll)
            if self.selected_word_idx + 1 in on_screen:
                self.selected_word_idx += 1
            elif self.selected_word_idx + 1 in next_row:
                self.scroll += 1
                self.selected_word_idx += 1
            else:
                self.scroll = max(0, min(self.scroll + 1, max_row - TEXT_ROWS + 1))

        if btnp(Map.action) and self.menu_enabled:
            return WordMenu(self.known_words, self.words[0], on_word_selected, self)

        return self

    def draw(self) -> None:
        pyxel.cls(0)
        smart_word_rows = draw_smart_text(
            self.text,
            self.words,
            self.known_words,
            self.selected_word_idx,
            (self.frame > FPS // 2),
            self.scroll)