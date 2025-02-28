import pyxel
from input import Map, btnp
from constants import *
from scenario import haunted_mansion, tutorial
from .transition import Transition
from .base import Screen
import screen


class PreTitle(Screen):
    """Just sets color for a transition"""
    def __init__(self):
        super().__init__()

    def update(self) -> Screen:
            return Transition(self, Title(), fade_noise="light")

    def draw(self) -> None:
        pyxel.cls(BACKGROUND)


class Title(Screen):
    timer: int = 2 * FPS # seconds

    def __init__(self):
        super().__init__()
        pyxel.load("assets/images.pyxres")


    def update(self) -> Screen:
        self.timer -= 1
        if self.timer == 0 or btnp(Map.action):
            # start = investigation_test.setup_test_scenario()
            start = tutorial.setup_scenario()
            # start = haunted_mansion.setup_scenario(skip_intro=False)
            return Transition(self, screen.CaseMenuScreen(), fade_noise="dark")

        return self

    def draw(self) -> None:
        pyxel.cls(BACKGROUND)
        pyxel.blt(0, 0, IMAGE_TITLE["bank"], IMAGE_TITLE["u"], IMAGE_TITLE["v"], SCREEN_W, SCREEN_H)