import pyxel

D_WIDTH = 84
D_HEIGHT = 48

KEY_MAP = {
    "up": [pyxel.KEY_KP_8, pyxel.KEY_UP],
    "down": [pyxel.KEY_KP_2, pyxel.KEY_DOWN],
    "left": [pyxel.KEY_KP_4, pyxel.KEY_LEFT],
    "right": [pyxel.KEY_KP_6, pyxel.KEY_RIGHT],
}

PALETTE = (15, 0)

SCORE = 0

PADDLE_SIZE = 11
PADDLE_X = 10
PADDLE_Y = 10
PADDLE_SPEED = 2

BALL_SIZE = 4
BALL_X = BALL_SIZE * 4
BALL_Y = BALL_SIZE * 3
BALL_VEL_X = -0.3
BALL_VEL_Y = -0.3

PAUSED = False

pyxel.init(D_WIDTH, D_HEIGHT, display_scale=6, fps=60)

tone = pyxel.Tone()
tone.gain = 2.0
tone.noise = 0
# Waveform is approximation (mostly by ear) of how the 3310 sounds
# TODO: do a FFT of a real sound, synthesize it and sample it at 32 points
tone.waveform.from_list([15, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7])
tones = [tone]
pyxel.tones.from_list(tones)

pyxel.sounds[0].set(
    "c3e3g3",
    "t", # t is the first one (the one we overrode)
    "7",
    "n", # the only effect Nokia 3310 realistically can do is none
    5
)

def signum(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return +1

def intervals_intersect(min1, max1, min2, max2):
    #print(f"INTERSECT: {min1 <= max2 and max1 >= min2} {min1}, {max1}, {min2}, {max2}")
    return min1 <= max2 and max1 >= min2


# returns: distance that the object travels after collision, None if no collision
def line_collision(coord, velocity, line_coord):
    #print(f"COLL: {coord}, {velocity}, {line_coord}")
    if signum(coord - line_coord) != signum(coord + velocity - line_coord):
        #print(f"RETURN: {line_coord - (coord + velocity)}")
        return line_coord - (coord + velocity)
    else:
        return None


def limit_object_coords(value, size, minimum, maximum):
    out = value
    out = min(maximum - size, out)
    out = max(minimum, out)
    return out


def limit_paddles():
    global PADDLE_X, PADDLE_Y
    PADDLE_X = limit_object_coords(PADDLE_X, PADDLE_SIZE, 0, D_WIDTH)
    PADDLE_Y = limit_object_coords(PADDLE_Y, PADDLE_SIZE, 0, D_HEIGHT)


def update_paddles():
    global PADDLE_X, PADDLE_Y
    for key in KEY_MAP["right"]:
        if pyxel.btn(key):
            PADDLE_X += PADDLE_SPEED
    for key in KEY_MAP["left"]:
        if pyxel.btn(key):
            PADDLE_X += -PADDLE_SPEED
    for key in KEY_MAP["up"]:
        if pyxel.btn(key):
            PADDLE_Y += -PADDLE_SPEED
    for key in KEY_MAP["down"]:
        if pyxel.btn(key):
            PADDLE_Y += +PADDLE_SPEED

def score():
    global SCORE
    SCORE += 1
    pyxel.play(0, snd=0)


def update_ball(): # TODO: refactor: use vectors for everything
    global BALL_X, BALL_Y, BALL_VEL_X, BALL_VEL_Y, SCORE
    if 0 - BALL_VEL_X <= BALL_X <= D_WIDTH - BALL_SIZE - BALL_VEL_X:  # no bounce
        BALL_X += BALL_VEL_X
    else:
        coord = line_collision(BALL_X, BALL_VEL_X, 0)
        if coord:
            if intervals_intersect(BALL_Y, BALL_Y + BALL_SIZE, PADDLE_Y, PADDLE_Y + PADDLE_SIZE):
                score()
            BALL_X = 0 + coord
        coord = line_collision(BALL_X + BALL_SIZE, BALL_VEL_X, D_WIDTH)
        if coord:
            if intervals_intersect(BALL_Y, BALL_Y + BALL_SIZE, PADDLE_Y, PADDLE_Y + PADDLE_SIZE):
                score()
            BALL_X = D_WIDTH - BALL_SIZE + coord
        BALL_VEL_X = -BALL_VEL_X
    if 0 - BALL_VEL_Y <= BALL_Y <= D_HEIGHT - BALL_SIZE - BALL_VEL_Y:  # no bounce
        BALL_Y += BALL_VEL_Y
    else:
        coord = line_collision(BALL_Y, BALL_VEL_Y, 0)
        if coord:
            if intervals_intersect(BALL_X, BALL_X + BALL_SIZE, PADDLE_X, PADDLE_X + PADDLE_SIZE):
                score()
            BALL_Y = 0 + coord
        coord = line_collision(BALL_Y + BALL_SIZE, BALL_VEL_Y, D_HEIGHT)
        if coord:
            if intervals_intersect(BALL_X, BALL_X + BALL_SIZE, PADDLE_X, PADDLE_X + PADDLE_SIZE):
                score()
            BALL_Y = D_HEIGHT - BALL_SIZE + coord
        BALL_VEL_Y = -BALL_VEL_Y
    #print(f"BALL: {BALL_X}:{BALL_Y} {BALL_VEL_X}:{BALL_VEL_Y}")


def update():
    global PAUSED
    if pyxel.btnp(pyxel.KEY_SPACE):
        PAUSED = not PAUSED
    if not PAUSED:
        update_paddles()
        limit_paddles()
        update_ball()


def draw():
    pyxel.cls(PALETTE[1])
    # pyxel.text(D_WIDTH // 2, D_HEIGHT // 2, f"{SCORE}", 11)
    # pyxel.text(0, D_HEIGHT // 2 + 10, f"{BALL_X}:{BALL_Y} {BALL_VEL_X}:{BALL_VEL_Y}", 11)
    pyxel.text(D_WIDTH // 2 - 4, D_HEIGHT // 2 - 4, f"{SCORE}", 11)
    # paddles
    pyxel.rect(PADDLE_X, 0, PADDLE_SIZE, 1, PALETTE[0])
    pyxel.rect(PADDLE_X, D_HEIGHT - 1, PADDLE_SIZE, 1, PALETTE[0])
    pyxel.rect(0, PADDLE_Y, 1, PADDLE_SIZE, PALETTE[0])
    pyxel.rect(D_WIDTH - 1, PADDLE_Y, 1, PADDLE_SIZE, PALETTE[0])
    # ball
    pyxel.rect(BALL_X, BALL_Y, BALL_SIZE, BALL_SIZE, PALETTE[0])

pyxel.run(update, draw)