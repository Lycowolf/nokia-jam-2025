import pyxel
from collections import namedtuple
from misc_types import Way

# TODO: more keys, more mappings. Configurable?
class Map:
    up = [pyxel.KEY_KP_8, pyxel.KEY_UP]
    down = [pyxel.KEY_KP_2, pyxel.KEY_DOWN]
    left = [pyxel.KEY_KP_4, pyxel.KEY_LEFT]
    right = [pyxel.KEY_KP_6, pyxel.KEY_RIGHT]
    action = [pyxel.KEY_KP_5, pyxel.KEY_KP_ENTER, pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_X]
    back = [pyxel.KEY_KP_MULTIPLY, pyxel.KEY_Z, pyxel.KEY_KP_0]
    switch = [pyxel.KEY_KP_DIVIDE, pyxel.KEY_TAB, pyxel.KEY_LSHIFT, pyxel.KEY_A, pyxel.KEY_KP_7]
    lore = [pyxel.KEY_L, pyxel.KEY_E, pyxel.KEY_S, pyxel.KEY_KP_9]

    way_keys = {
        Way.up: up,
        Way.down: down,
        Way.left: left,
        Way.right: right,
    }

def btn(keys: list):
    for key in keys:
        if pyxel.btn(key):
            return True
    return False

def btnp(keys: list):
    for key in keys:
        if pyxel.btnp(key):
            return True
    return False

def btnr(keys: list):
    for key in keys:
        if pyxel.btnr(key):
            return True
    return False

#TODO: implement autorepeat