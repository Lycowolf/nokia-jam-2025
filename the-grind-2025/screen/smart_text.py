import pyxel
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
        if not known_words:
            self.menu_enabled = False

        self.updated_flag = False

    def is_top(self):
        return self.scroll == 0

    def is_bottom(self):
        _, max_row = layout_smart_text(self.text, self.words)
        return self.scroll >= max_row - TEXT_ROWS + 1

    def was_updated(self, clear=True):
        if self.updated_flag:
            if clear:
                self.updated_flag = False
            return True
        else:
            return False

    def update(self) -> Screen:
        self.frame = (self.frame + 1) % FPS
        def on_word_selected(word):
            self.words[self.selected_word_idx] = word
            sound.confirm()
            self.updated_flag = True

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
        pyxel.cls(BACKGROUND)
        smart_word_rows = draw_smart_text(
            self.text,
            self.words,
            self.known_words,
            self.selected_word_idx,
            (self.frame > FPS // 2),
            self.scroll)

        _, max_row = layout_smart_text(self.text, self.words)
        if max_row > TEXT_ROWS - 1:
            draw_scrollbar(self.scroll, max_row)

def draw_scrollbar(line: int, lines: int, style='mini'):
    max_line = lines - TEXT_ROWS + 2
    x = SCREEN_W - 2
    y = int(SCREEN_H * (line / max_line))
    h = SCREEN_H // max_line

    if style == 'black':
        pyxel.line(x, 0, x, SCREEN_H- 1, col=FOREGROUND)
        pyxel.line(x+1, y, x+1, y+h, col=FOREGROUND)
    elif style == 'white':
        pyxel.line(x, 0, x, SCREEN_H - 1, col=FOREGROUND)
        pyxel.line(x + 1, 0, x + 1, SCREEN_H - 1, col=FOREGROUND)
        pyxel.line(x + 1, y, x + 1, y + h, col=BACKGROUND)
    elif style == 'thin':
        pyxel.line(x + 1, 0, x + 1, SCREEN_H - 1, col=FOREGROUND)
        pyxel.line(x + 1, y, x + 1, y + h, col=BACKGROUND)
        pyxel.line(x, y, x, y + h, col=FOREGROUND)
    elif style == 'mini':
        pyxel.line(x+1, y, x+1, y + h, col=FOREGROUND)