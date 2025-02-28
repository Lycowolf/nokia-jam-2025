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
    pyxel.stop()
    pyxel.sounds[0].set(
        notes,
        "t", # t is the first one (the one we overrode)
        "7",
        "n", # the only effect Nokia 3310 realistically can do is none
        speed
    )
    pyxel.play(0, 0)

def confirm():
    # rest at the start gives us time to stop the sound if transition follows
    play("rc2g2", 4)

def mode_switch():
    #play("f2rf2d2rd2f2", 12)
    play("d2rrd2f2", 12)

def deduction_success():
    play("e2g2c2c3c3c3", 18)