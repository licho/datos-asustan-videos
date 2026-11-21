"""Sonidos y música del video del Sol (efectos sintetizados con el mezclador del motor).
Uso: python3 audio.py out/sol_audio.wav [voz.mp3]
Los tiempos salen de tl.py (estimados o de src/timing.json si ya hay voz)."""
import json, subprocess, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
import lib  # configura el motor con los datos del canal
from reels_engine.audio import Mix, SR, lp

TL = json.loads(subprocess.check_output(["python3", os.path.join(HERE, "tl.py")], cwd=HERE, stderr=subprocess.DEVNULL))
START = {i: s for i, s, d in TL}; DUR = {i: d for i, s, d in TL}
total = TL[-1][1] + TL[-1][2]
m = Mix(total)

# --- efectos extra
def click(st, g=.5): m.add(st, m.tone(np.linspace(2200, 1400, int(.03 * SR)), .03) * m.env(int(.03 * SR), .001, .01), g, raw=True)
def tick(st, g=.12): m.add(st, lp(m.noise(.02), .7) * m.env(int(.02 * SR), .0005, .004), g, raw=True)
def wind(st, d, g=.22):
    n = int(d * SR); x = lp(m.noise(d), .015); x /= (np.max(np.abs(x)) or 1)
    sw = .55 + .45 * np.sin(np.linspace(0, d * 1.3, n)) ; fade = np.minimum(1, np.minimum(np.arange(n) / SR / .6, (n - np.arange(n)) / SR / .6))
    m.add(st, x * sw * fade, g, raw=True)
def chatter(st, d, g=.10):
    for k in np.arange(0, d, .07): m.add(st + k, lp(m.noise(.015), .5) * m.env(int(.015 * SR), .0005, .004), g, raw=True)
def crackle(st, g=.25):
    for k in range(7): m.add(st + k * .045 + (k % 3) * .01, lp(m.noise(.03), .45) * m.env(int(.03 * SR), .0005, .008), g * (1 - k / 9), raw=True)
def bubble(st, g=.12): m.add(st, m.tone(np.linspace(500, 1100, int(.08 * SR)), .08) * m.env(int(.08 * SR), .002, .03), g, raw=True)
def msg(st, g=.25): m.add(st, (m.tone(1320, .12) + m.tone(1760, .12) * .6) * m.env(int(.12 * SR), .002, .05), g, raw=True)

def at(line, sec): return START[line] + sec
fx = lambda name, line, sec, **kw: getattr(m, name)(at(line, sec), **kw)

# 0 gancho
fx("pop", 0, .02, g=.25); click(at(0, 1.35)); fx("sting", 0, 1.38, g=.35); fx("ding", 0, 1.95, g=.15); fx("boing", 0, 3.55, g=.2)
# cortes: whoosh en cada línea
for i in range(1, 13): fx("whoosh", i, .05, g=.28)
fx("pop", 1, .1, g=.2); fx("ding", 1, .45, g=.12)
for k in np.arange(.2, DUR[2] - .3, .25): tick(at(2, k))
fx("ding", 2, DUR[2] - .35, g=.2)
fx("rumble", 3, 0, d=1.6, g=.6); fx("thud", 3, .1, g=.7); fx("whoosh", 3, 1.35, g=.4); fx("skid", 3, 1.45, g=.25); fx("whoosh", 3, 2.4, g=.3)
fx("sadtrom", 4, .5, g=.14); fx("thud", 4, DUR[4] * .55, g=.6)
wind(at(5, 0), DUR[5] + DUR[6] + DUR[7] + DUR[8]); crackle(at(5, .6)); crackle(at(5, 2.0)); fx("ding", 5, DUR[5] * .5, g=.12)
chatter(at(6, .3), DUR[6] - .6)
fx("sadtrom", 7, .4, g=.12); fx("boing", 7, DUR[7] * .45, g=.25)
fx("thud", 8, .1, g=.5); crackle(at(8, .3), g=.3); fx("ding", 8, DUR[8] * .45, g=.12)
for k in np.arange(.6, DUR[8], .55): bubble(at(8, k + (k * 7 % .2)))
fx("rumble", 9, 0, d=DUR[9] * .42, g=.35); fx("whoosh", 9, DUR[9] * .42 - .25, g=.4)
for i in range(10): fx("pop", 9, DUR[9] * .42 + .2 + i * .08, g=.12, f0=400 + i * 40, f1=900 + i * 60)
fx("buzzer", 10, DUR[10] * .6, g=.2); fx("rumble", 10, DUR[10] * .6, d=1.2, g=.4); fx("pop", 10, DUR[10] * .4, g=.25); fx("boing", 10, DUR[10] * .5, g=.2)
fx("whoosh", 11, DUR[11] * .4, g=.35); msg(at(11, DUR[11] * .45 + .2)); msg(at(11, DUR[11] * .45 + .9))
fx("jingle", 12, .2, g=.12); fx("ding", 12, .85, g=.15)
m.music("pad")

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "sol_audio.wav")
voice = sys.argv[2] if len(sys.argv) > 2 else None
m.render(out, voice)
print(out, round(total, 2))
