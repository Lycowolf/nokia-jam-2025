import math

SCREEN_W = 84
SCREEN_H = 48
DISPLAY_SCALE = 6
FPS = 15

PALETTES = {"original", "harsh", "gray"}

# this font is special: Basic Latin (u0020 - u007F) glyphs/codepoints are copied to Private Use Area (uE020 - uE07F)
# end black/white inverted
FONT = "assets/simple-6px.bdf"
FONT_HEIGHT = 6
FONT_INVERTED_OFFSET = 0xE000
# half a line at the top and the bottom is reserved for UI
TEXT_ROWS = SCREEN_H // FONT_HEIGHT - 1
MIDDLE_ROW = math.floor(TEXT_ROWS / 2)
TEXT_OFFSET_Y = FONT_HEIGHT // 2

SMART_TEXT_MARKER = "{}"
NEWLINE_MARKER = "\n[ \t]*" # eat whitespace after newline, to enable using indented multiline strings