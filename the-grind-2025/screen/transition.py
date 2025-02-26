from typing import Self

from .base import Screen
import pyxel
from constants import SCREEN_W, SCREEN_H, FPS
from misc_types import Way


class Transition(Screen):


    def __init__(self, state_from, state_to, shift_dir=None, **kwargs):
        self.state_to = state_to
        state_to.draw()
        self.image_to = snapshot()

        self.state_from = state_from
        state_from.draw()
        self.image_from = snapshot()

        self.frame = 0
        self.length = FPS // 2

        self.animation = {Way.left: self.slide_left,
                          Way.right: self.slide_right,
                          Way.up: self.slide_up,
                          Way.down: self.slide_down,
                          }.get(shift_dir, self.slide_down)

    def draw(self):
        shift = int(SCREEN_W * (self.frame / self.length))
        self.animation()

    def update(self) -> Self:
        self.frame += 1
        if self.frame >= self.length:
            return self.state_to
        else:
            return self

    def slide_left(self):
        shift = int(SCREEN_W * (self.frame / self.length))

        pyxel.blt(shift, 0, self.image_from, 0, 0, SCREEN_W, SCREEN_H)
        pyxel.blt(shift - SCREEN_W, 0, self.image_to, 0, 0, SCREEN_W, SCREEN_H)

    def slide_right(self):
        shift = int(SCREEN_W * (self.frame / self.length))

        pyxel.blt(-shift, 0, self.image_from, 0, 0, SCREEN_W, SCREEN_H)
        pyxel.blt(SCREEN_W - shift, 0, self.image_to, 0, 0, SCREEN_W, SCREEN_H)

    def slide_up(self):
        shift = int(SCREEN_H * (self.frame / self.length))

        pyxel.blt(0, shift, self.image_from, 0, 0, SCREEN_W, SCREEN_H)
        pyxel.blt(0, shift - SCREEN_H, self.image_to, 0, 0, SCREEN_W, SCREEN_H)

    def slide_down(self):
        shift = int(SCREEN_H * (self.frame / self.length))

        pyxel.blt(0, -shift, self.image_from, 0, 0, SCREEN_W, SCREEN_H)
        pyxel.blt(0, SCREEN_H - shift, self.image_to, 0, 0, SCREEN_W, SCREEN_H)




def snapshot():
    image = pyxel.Image(SCREEN_W, SCREEN_H)

    for x in range(SCREEN_W):
        for y in range(SCREEN_H):
            image.pset(x, y, col=pyxel.pget(x, y))

    return image