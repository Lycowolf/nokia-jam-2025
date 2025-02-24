import pyxel
from constants import *
import re

WORD_RE = re.compile(r"([^ \uE020]+)([ \uE020]*)") # E020 is inverted space
font = pyxel.Font(FONT)

def switch_palette(name: str) -> None:
    """switch palette. If it doesn't exist, do nothing"""
    if name in PALETTES:
        # load only palette; the pyxel python binding exposes wrong type
        pyxel.load(f"assets/palettes/{name}.pyxres", excl_images=True, excl_musics=True, excl_sounds=True, excl_tilemaps=True)

def draw_text_row(row, text: str, color: int = 1, x_off: int = 0) -> None:
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

def check_word(word: str, known_words: set[str]) -> str:
    if word not in known_words:
        print(f"Word {word} not in the set of known words {known_words}")
    return word

def invert_text_blink(text, uninvert_selected) -> str:
    if uninvert_selected:
        return text
    out_text = ""
    for c in text:
        out_text += chr(ord(c) + FONT_INVERTED_OFFSET)
    return out_text

def draw_smart_text(text: str, words: list[str], known_words: set[str], selected: int, blink_phase: bool = False, scroll: int = 0) -> list[int]:
    """
    Replace markers with (inverted) words while checking they are known and draw the result, scrolling down by
    scroll lines The selected word will be inverted only if blink_phase == False.
    Return the line numbers of every word (for use in scroll control).
    """
    row_num = - scroll
    row_text = ""
    word_rows = []
    smart_word_num = 0
    is_smart = False

    for match in re.finditer(WORD_RE, text):
        next_word = match[0]
        if match[1] == SMART_TEXT_MARKER:
            is_smart = True
            try:
                replacement = check_word(words[smart_word_num], known_words)
            except IndexError:
                print(f"No word for index {smart_word_num}")
                replacement = "-noidx-"
            if smart_word_num == selected:
                replacement = invert_text_blink(replacement, blink_phase)
            else:
                replacement = invert_text_blink(replacement, False)
            smart_word_num += 1
            next_word = replacement + match[2]

        try_text = row_text + next_word
        if font.text_width(try_text) > SCREEN_W:
            draw_text_row(row_num, row_text)
            row_num += 1
            row_text = next_word
        else:
            row_text = try_text

        if is_smart:
            word_rows.append(row_num)
            is_smart = False
    # draw remaining text
    draw_text_row(row_num, row_text)
    if is_smart:
        word_rows.append(row_num)
    return word_rows