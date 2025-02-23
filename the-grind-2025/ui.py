import pyxel
from constants import *
import re

WORD_RE = re.compile(r"[^ ]+ *")
font = pyxel.Font(FONT)

def draw_text_row(row, text: str, color: int = 1, x_off: int = 0):
    """
    Text-printing primitive: prints a line of text to a specified screen row.
    Rows outside the allowed area are ignored.
    """
    if 0 <= row < TEXT_ROWS:
        pyxel.text(x_off, row * FONT_HEIGHT + TEXT_OFFSET_Y, text, color, font)

def draw_wrapped_text(text: str, starting_line: int = 0):
    row_num = - starting_line
    row_text = ""
    for match in re.finditer(WORD_RE, text):
        next_word = match[0]
        try_text = row_text + next_word
        if font.text_width(try_text) > SCREEN_W:
            draw_text_row(row_num, row_text)
            row_num += 1
            row_text = next_word
        else:
            row_text = try_text
    draw_text_row(row_num, row_text)

def check_word(word: str, known_words: set[str]):
    if word not in known_words:
        print(f"Word {word} not in the set of known words {known_words}")
    return word

def invert_text(text):
    out_text = ""
    for c in text:
        out_text += chr(ord(c) + FONT_INVERTED_OFFSET)
    return out_text

def prepare_smart_text(text: str, words: list[str], known_words: set[str], selected: int, blink_uninvert: bool = False):
    static_segments = text.split(SMART_TEXT_MARKER)
    last_segment = len(static_segments) - 1

    if last_segment != len(words):
        print(f"number of placeholders in '{text}' doesn't match the number of words in {words}")

    if last_segment == 0:
        draw_wrapped_text(text)
        return

    out_text = ""
    for i, segment in enumerate(static_segments):
        out_text += segment
        if i == last_segment:
            return out_text

        try:
            replacement = check_word(words[i], known_words)
        except IndexError:
            print(f"No word for index {i}")
            replacement = "-noidx-"
        if i == selected and blink_uninvert:
            out_text += replacement
        else:
            out_text += invert_text(replacement)