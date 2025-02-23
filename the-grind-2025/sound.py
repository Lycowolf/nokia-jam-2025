import pyxel

def init():
    tone = pyxel.Tone()
    tone.gain = 2.0
    tone.noise = 0
    # Waveform is approximation (mostly by ear) of how the 3310 sounds
    # TODO: do a FFT of a real sound, synthesize it and sample it at 32 points
    tone.waveform.from_list([15, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7])
    tones = [tone]
    pyxel.tones.from_list(tones)


def play(notes: str, speed: int):
    pyxel.sounds[0].set(
        notes,
        "t", # t is the first one (the one we overrode)
        "7",
        "n", # the only effect Nokia 3310 realistically can do is none
        speed
    )