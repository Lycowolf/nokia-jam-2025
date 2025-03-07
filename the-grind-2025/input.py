import pyxel
from constants import SCREEN_H
from misc_types import Way

# TODO: more keys, more mappings. Configurable?
class Map:
    up = [pyxel.KEY_KP_8, pyxel.KEY_UP, (28, 1 + SCREEN_H)]
    down = [pyxel.KEY_KP_2, pyxel.KEY_DOWN, (28, 25 + SCREEN_H)]
    left = [pyxel.KEY_KP_4, pyxel.KEY_LEFT, (1, 13 + SCREEN_H)]
    right = [pyxel.KEY_KP_6, pyxel.KEY_RIGHT, (57, 13 + SCREEN_H)]
    action = [pyxel.KEY_KP_5, pyxel.KEY_KP_ENTER, pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_X, (28, 13 + SCREEN_H)]
    back = [pyxel.KEY_KP_MULTIPLY, pyxel.KEY_Z, pyxel.KEY_KP_0, (1, 37 + SCREEN_H)]
    switch = [pyxel.KEY_KP_DIVIDE, pyxel.KEY_TAB, pyxel.KEY_LSHIFT, pyxel.KEY_A, pyxel.KEY_KP_7, (1, 1 + SCREEN_H)]
    lore = [pyxel.KEY_L, pyxel.KEY_E, pyxel.KEY_S, pyxel.KEY_KP_9, (28, 37 + SCREEN_H)]
    main_menu = [pyxel.KEY_Q, pyxel.KEY_KP_3, (57, 37 + SCREEN_H)]

    way_keys = {
        Way.up: up,
        Way.down: down,
        Way.left: left,
        Way.right: right,
    }

BUT_SZ = (25, 10)

def btn(keys: list):
    for key in keys:
        if isinstance(key, int):
            if pyxel.btn(key):
                return True
        else:
            if key[0] <= pyxel.mouse_x <= key[0] + BUT_SZ[0] and key[1] <= pyxel.mouse_y <= key[1] + BUT_SZ[1]:
                pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
    return False

def btnp(keys: list):
    for key in keys:
        if isinstance(key, int):
            if pyxel.btnp(key):
                return True
        else:
            if key[0] <= pyxel.mouse_x <= key[0] + BUT_SZ[0] and key[1] <= pyxel.mouse_y <= key[1] + BUT_SZ[1]:
                return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
    return False

def btnr(keys: list):
    for key in keys:
        if isinstance(key, int):
            if pyxel.btnr(key):
                return True
        else:
            if key[0] <= pyxel.mouse_x <= key[0] + BUT_SZ[0] and key[1] <= pyxel.mouse_y <= key[1] + BUT_SZ[1]:
                pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)
    return False

#TODO: implement autorepeat