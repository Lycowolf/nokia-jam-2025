import pyxel
from collections import namedtuple

# TODO: more keys, more mappings. Configurable?
class Map:
    up = [pyxel.KEY_KP_8, pyxel.KEY_UP]
    down = [pyxel.KEY_KP_2, pyxel.KEY_DOWN]
    left = [pyxel.KEY_KP_4, pyxel.KEY_LEFT]
    right = [pyxel.KEY_KP_6, pyxel.KEY_RIGHT]
    action = [pyxel.KEY_KP_5, pyxel.KEY_KP_ENTER, pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_X]
    back = [pyxel.KEY_Z, pyxel.KEY_ESCAPE]
    switch = [pyxel.KEY_TAB, pyxel.KEY_LSHIFT, pyxel.KEY_A]

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