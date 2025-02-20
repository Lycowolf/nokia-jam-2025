import pyxel

pyxel.init(128, 128)

tone = pyxel.Tone()
tone.gain = 2.0
tone.noise = 0
tone.waveform.from_list([15, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7])
tones = [tone]
pyxel.tones.from_list(tones)

pyxel.sounds[0].set(
    #"f3c3e3c3a2a2a2",
    "c3",
    "t",
    "7",
    "n",
    120
)

pyxel.play(0, snd=0)

def update():
    pass

def draw():
    pass

pyxel.run(update, draw)