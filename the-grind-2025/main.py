import pyxel

import sound
import ui
from constants import *
import screen

class Game:
    screen: screen.Screen

    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H + KEYBOARD_H, fps=FPS, title="Nokia 3310 Jam 2025", display_scale=DISPLAY_SCALE)

        pyxel.mouse(False)
        sound.init()
        pyxel.load("assets/images.pyxres")
        ui.switch_palette(CHOSEN_PALETTE[0])
        # self.screen = screen.TitleScreen()
        # self.screen = screen.CaseMenuScreen()
        self.screen = screen.Settings()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.screen = self.screen.update()

    def draw(self):
        pyxel.cls(BACKGROUND)
        pyxel.clip(0, 0, SCREEN_W, SCREEN_H)
        self.screen.draw()
        pyxel.clip()
        pyxel.dither(1)
        pyxel.blt(0, SCREEN_H, 0, 0, SCREEN_H, SCREEN_W, KEYBOARD_H)
        pyxel.rectb(pyxel.mouse_x - 1, pyxel.mouse_y - 1, 3, 3, FOREGROUND)
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 1, 1, BACKGROUND)

Game()