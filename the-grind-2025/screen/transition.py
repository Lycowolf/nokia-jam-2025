import random
from operator import length_hint
from typing import Self

from .base import Screen
import pyxel
from constants import SCREEN_W, SCREEN_H, FPS
from misc_types import Way
from ui import draw_text_row, font


class Transition(Screen):


    def __init__(self, state_from, state_to, length=FPS//2, shift_dir=None, fade_label=None, fade_noise=None):
        self.state_to = state_to
        state_to.draw()
        self.image_to = snapshot()

        self.state_from = state_from
        state_from.draw()
        self.image_from = snapshot()

        self.frame = 0
        self.length = length
        self.label = ''

        if shift_dir:
            self.animation = {Way.left: self.slide_left,
                              Way.right: self.slide_right,
                              Way.up: self.slide_up,
                              Way.down: self.slide_down}.get(shift_dir)
        elif fade_label:
            self.label = fade_label
            self.animation = self.fade_label_skew
            self.length = FPS
        elif fade_noise:
            self.length = FPS
            self.animation = self.fade_noise if fade_noise == "light" else self.fade_noise_dark
        else:
            self.animation = self.cut
            self.length = 1

    def draw(self):
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

    def fade_label_skew(self):
        bgr = self.image_from if self.frame < self.length // 2 else self.image_to
        phase = int(SCREEN_W * (1 - abs(1 - (2*self.frame/self.length))))

        pyxel.blt(0, 0, bgr, 0, 0, SCREEN_W, SCREEN_H)

        skew = 5
        center = SCREEN_W // 2

        for i in range(phase):
            pyxel.line(center + skew + i, 0, center - skew + i, SCREEN_H, col=0)
            pyxel.line(center + skew - i, 0, center - skew - i, SCREEN_H, col=0)


        if phase > font.text_width(self.label) // 2:
            draw_text_row(3, self.label, color=1, x_off=(SCREEN_W-font.text_width(self.label))//2)

    def fade_noise(self):
        fade = (self.frame + 1) / self.length
        pyxel.cls(0)
        pyxel.dither(1 - fade)
        pyxel.blt(0, 0, self.image_from, 0, 0, SCREEN_W, SCREEN_H)
        pyxel.dither(fade)
        pyxel.blt(0, 0, self.image_to, 0, 0, SCREEN_W, SCREEN_H)

    def fade_noise_dark(self):
        fade = (self.frame + 1) / self.length
        pyxel.cls(1)
        pyxel.dither(1 - fade)
        pyxel.blt(0, 0, self.image_from, 0, 0, SCREEN_W, SCREEN_H)
        pyxel.dither(fade)
        pyxel.blt(0, 0, self.image_to, 0, 0, SCREEN_W, SCREEN_H)

    def cut(self):
        # no animation, just switch
        pyxel.blt(0, 0, self.image_to, 0, 0, SCREEN_W, SCREEN_H)

def snapshot():
    image = pyxel.Image(SCREEN_W, SCREEN_H)

    for x in range(SCREEN_W):
        for y in range(SCREEN_H):
            image.pset(x, y, col=pyxel.pget(x, y))

    return image