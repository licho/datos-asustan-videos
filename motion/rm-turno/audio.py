"""Sonido de "El turno de noche": ambiente de terror (zumbido, estática, latidos, pasos, elevador).
Uso: python3 audio.py out/turno_audio.wav [voz.mp3]"""
import json, subprocess, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
import lib  # configura el motor
from reels_engine.audio import Mix, SR, lp

TL = json.loads(subprocess.check_output(["python3", os.path.join(HERE, "tl.py")], cwd=HERE, stderr=subprocess.DEVNULL))
START = {i: s for i, s, d in TL}; DUR = {i: d for i, s, d in TL}
total = TL[-1][1] + TL[-1][2]
m = Mix(total)
at = lambda i, sec=0: START[i] + sec
span = lambda a, b: (START[a], START[b] + DUR[b])

def fade(x, fi=.3, fo=.5):
    n = len(x); k = np.arange(n) / SR
    return x * np.minimum(1, np.minimum(k / max(fi, 1e-3), (n / SR - k) / max(fo, 1e-3)))
def hum(st, d, g=.05):
    tt = np.arange(int(d * SR)) / SR
    x = np.sin(2 * np.pi * 120 * tt) + .5 * np.sin(2 * np.pi * 240 * tt) + .2 * np.sin(2 * np.pi * 360 * tt)
    m.add(st, fade(x * (0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * tt))), g, raw=True)
def static(st, d, g=.06):
    x = m.noise(d) - lp(m.noise(d), .2); m.add(st, fade(x, .05, .2), g, raw=True)
def wind(st, d, g=.12):
    x = lp(m.noise(d), .012); x /= (np.max(np.abs(x)) or 1); m.add(st, fade(x, 1, 1), g, raw=True)
def step(st, g=.35):
    x = lp(m.noise(.09), .08) * m.env(int(.09 * SR), .002, .05); m.add(st, x, g, raw=True)
def steps(st, d, every=.55, g=.3):
    for k in np.arange(0, d, every): step(st + k, g * (0.8 + 0.2 * np.sin(k * 7)))
def keys(st, g=.18):
    for k in range(9):
        f = 3000 + (k * 911 % 2200)
        m.add(st + k * .035, m.tone(f, .09) * m.env(int(.09 * SR), .001, .05), g, raw=True)
def beat(st, n, bpm=70, g=.6):
    sp = 60 / bpm
    for k in range(n):
        for off, a in ((0, 1), (.16, .7)):
            tt = np.arange(int(.18 * SR)) / SR
            x = np.sin(2 * np.pi * (55 - 20 * tt / .18) * tt) * m.env(len(tt), .003, .12)
            m.add(st + k * sp + off, x, g * a, raw=True)
def slide(st, d=1.6, g=.25):
    x = lp(m.noise(d), .03); x /= (np.max(np.abs(x)) or 1); m.add(st, fade(x, .4, .5), g, raw=True)
def click(st, g=.35): m.add(st, m.tone(np.linspace(1800, 900, int(.03 * SR)), .03) * m.env(int(.03 * SR), .001, .01), g, raw=True)
def beep(st, g=.2, f=1000, d=.12): m.add(st, m.tone(f, d) * m.env(int(d * SR), .003, .03), g, raw=True)
def paper(st, g=.18):
    for k in range(5): m.add(st + k * .06, (m.noise(.05) - lp(m.noise(.05), .3)) * m.env(int(.05 * SR), .002, .03), g, raw=True)
def low_sting(st, g=.5):
    d = 2.2; tt = np.arange(int(d * SR)) / SR
    x = (np.sin(2 * np.pi * 46 * tt) + .6 * np.sin(2 * np.pi * 69.3 * tt) + .4 * np.sin(2 * np.pi * 97 * tt)) * np.exp(-tt * 1.4)
    m.add(st, fade(x, .01, .6), g, raw=True)

# ambiente general
wind(at(0), START[2] + .5)
hum(at(2), START[7] - START[2]); hum(at(13), START[19] - START[13], .045); hum(at(25), START[29] - START[25], .05)
# 2–3: llaves y el guardia que se va
keys(at(2, DUR[2] * .5)); steps(at(3, DUR[3] * .45), DUR[3] * .55, .3, .32); m.thud(at(3, DUR[3] - .1), g=.4)
# 5: monitores que se encienden
for k in range(6): click(at(5, DUR[5] * .3 + k * DUR[5] * .075))
# 6: primera ronda
steps(at(6), DUR[6], .6, .25)
# 7: alerta de movimiento
beep(at(7, .1), .25, 1250); beep(at(7, .35), .25, 1250); static(at(7), DUR[7], .04)
steps(at(8), DUR[8], .55, .3)
# 9–12: elevador
m.ding(at(9, DUR[9] * .5), g=.35); slide(at(10, .1), DUR[10]); click(at(12, DUR[12] * .5), .45); low_sting(at(12, DUR[12] * .5), .45)
# 13–15: nota
steps(at(13), DUR[13] * .6, .5, .25); paper(at(13, DUR[13] * .6)); paper(at(14, .1), .12)
# 16–17: intercomunicador
static(at(16, DUR[16] * .4), DUR[16] * .6 + DUR[17], .09); beep(at(16, DUR[16] * .35), .3, 880, .2)
# 18–24: las cámaras y la figura
click(at(18, .2)); static(at(19), START[25] - START[19], .045)
beat(at(21), 7, 72, .55); beat(at(23, 0), 8, 96, .6)
low_sting(at(24, DUR[24] * .8), .55)
# 25–28: la voz detrás de ti
m.sting(at(25, .05), g=.35); beat(at(25, .5), 4, 120, .6)
m.whoosh(at(26, .05), g=.4); m.whoosh(at(28, .05), g=.35)
# 29–33: el giro final
static(at(29), START[34] - START[29], .05); beat(at(29), 10, 104, .55)
m.buzzer(at(31, .1), g=.18); low_sting(at(33, .1), .7); m.rumble(at(33, .1), d=2.5, g=.5)
# 34: se apagan los monitores
for k in range(6): click(at(34, .3 + k * .32), .3)
m.music("pad")

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "turno_audio.wav")
voice = sys.argv[2] if len(sys.argv) > 2 else None
m.render(out, voice)
print(out, round(total, 2))
