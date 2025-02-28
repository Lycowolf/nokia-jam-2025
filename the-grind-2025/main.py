import pyxel

import sound
from constants import *
import screen

class Game:
    screen: screen.Screen

    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, fps=FPS, title="Nokia 3310 Jam 2025", display_scale=DISPLAY_SCALE)
        sound.init()
        # self.screen = screen.TitleScreen()
        self.screen = screen.CaseMenuScreen()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.screen = self.screen.update()

    def draw(self):
        self.screen.draw()

Game()