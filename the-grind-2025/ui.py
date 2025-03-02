import pyxel
from constants import *
import re
from collections.abc import Callable

WORD_RE = re.compile(r"(" + SMART_TEXT_MARKER + r"|" + NEWLINE_MARKER + r"|[^\s\uE020]+)([ \t\uE020]*)") # E020 is inverted space
NEWLINE_MARKER_RE = re.compile(NEWLINE_MARKER)
font = pyxel.Font(FONT)

def switch_palette(name: str) -> None:
    """switch palette. If it doesn't exist, do nothing"""
    if name in PALETTES:
        # load only palette; the pyxel python binding exposes wrong type
        pyxel.load(f"assets/palettes/{name}.pyxres", excl_images=True, excl_musics=True, excl_sounds=True, excl_tilemaps=True)

def draw_text_coords(x, y, text, color=FOREGROUND):
    text_w = font.text_width(text)
    if x < 0:
        x = SCREEN_W - text_w + x - 1 # -1 means "sits flush at the edge"
    if y < 0:
        y = SCREEN_H - FONT_HEIGHT + y - 1
    pyxel.text(x, y, text, color, font)

def draw_text_row(row: int, text: str, color: int = FOREGROUND, x_off: int = 0) -> None:
    """
    Text-printing primitive: prints a line of text to a specified screen row.
    Rows outside the allowed area are ignored.
    Negative values of x_off signify offset from the right side
    """

    if x_off < 0:
        x_off = SCREEN_W - font.text_width(text) + x_off

    if 0 <= row < TEXT_ROWS:
        pyxel.text(x_off, row * FONT_HEIGHT + TEXT_OFFSET_Y, text, color, font)

def draw_centered_text_row(row: int, text: str, color: int = FOREGROUND):
    offset = (SCREEN_W - font.text_width(text)) // 2
    draw_text_row(row, text, color, offset)

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

def draw_smart_text(text: str,
                    words: list[str],
                    known_words: set[str],
                    selected: int,
                    blink_phase: bool = False,
                    scroll: int = 0,
                    draw_function: Callable[[int, str], None] = draw_text_row
                    ) -> tuple[list[int], int]:
    """
    Replace markers with (inverted) words while checking they are known and draw the result, scrolling down by
    scroll lines The selected word will be inverted only if blink_phase == False.
    Return the line numbers of every smart word and number of last row (for use in scroll control).
    """
    row_num = - scroll
    row_text = ""
    word_rows = []
    smart_word_num = 0
    is_smart = False

    for match in re.finditer(WORD_RE, text):
        if NEWLINE_MARKER_RE.match(match[1]):
            draw_function(row_num, row_text)
            row_text = ""
            row_num += 1
            continue

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
            draw_function(row_num, row_text)
            row_num += 1
            row_text = next_word
        else:
            row_text = try_text
        if is_smart:
            word_rows.append(row_num)
            is_smart = False

    # draw remaining text
    draw_function(row_num, row_text)
    if is_smart:
        word_rows.append(row_num)
    return word_rows, row_num

# TODO: optimize this (e. g. memoize)
def layout_smart_text(text: str, words: list[str]) -> tuple[list[int], int]:
    """Runs draw_smart_text but doesn't draw anything, just returns the smart word row numbers"""
    return draw_smart_text(text, words, set(words), 0, False, 0, lambda x, y: None)


def words_on_screen(text: str, words: list[str], scroll: int) -> tuple[set[int], set[int], set[int], int]:
    """
    Lays out the smart text and returns the row where every smart word sits (and the number of the last inhabited row).
    """
    layout, max_row = layout_smart_text(text, words)
    prev_row = set()
    on_screen = set()
    next_row = set()
    for word_idx, row in enumerate(layout):
        if row == scroll - 1:
            prev_row.add(word_idx)
        elif scroll <= row < scroll + TEXT_ROWS:
            on_screen.add(word_idx)
        elif row == scroll + TEXT_ROWS:
            next_row.add(word_idx)
    return prev_row, on_screen, next_row, max_row