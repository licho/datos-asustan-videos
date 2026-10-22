import sys, math, subprocess, random, time
sys.path.insert(0, "/home/claude/datos-asustan-videos")
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import *
from lib.props import planet_earth, moon_disc
from lib.fondos import make_space
SPACE = make_space()
rnd = random.Random(3); STARS = [(rnd.uniform(0, W), rnd.uniform(0, 1400), rnd.uniform(1.5, 3.5), rnd.uniform(0, 6)) for _ in range(90)]

def frame(t):
    img = space_bg(t); d = ImageDraw.Draw(img)                     # fondo radial con estrellas que titilan
    # Luna: entra girando con back_out, flota, se aplasta, se estira y desaparece
    mx, my = 800, 600 + yoyo(t, 1.2, .9, 0, 12)
    s_in = tw(t, .35, .8, 0, 1, back_out); rot = tw(t, .35, .8, -90, 0, back_out) + yoyo(t, 1.2, .9, 0, 6)
    sx = sy = s_in
    if t >= 3.0: sx, sy = tw(t, 3.0, .12, 1, 1.25, power_in), tw(t, 3.0, .12, 1, .75, power_in)
    if t >= 3.12: sx, sy = tw(t, 3.12, .2, 1.25, .2, power_in), tw(t, 3.12, .2, .75, 1.6, power_in)
    al = 1 if t < 3.12 else tw(t, 3.12, .2, 1, 0, power_in)
    d = glow(img, mx, my, tw(t, .35, .8, 40, 170, cubic_out) * (1 if t < 3.1 else tw(t, 3.1, .5, 1, 2.2, cubic_out)), alpha=.45 * (1 if t < 3.1 else tw(t, 3.1, .5, 1, 0, cubic_out)))
    def moon_sh(dd, cx, cy):
        moon_disc(dd, cx, cy, 110); sphere_shade(dd._image, cx, cy, 110, .25, .35)
    d = layer(img, moon_sh, mx, my, 300, sx, sy, rot, al)
    # pedacitos con frenado suave (expo_out)
    if t >= 3.15:
        for i in range(14):
            a = i / 14 * 6.283; R = (180 + (i % 3) * 50) * tw(t, 3.15, .9, 0, 1, expo_out); r = 35 * tw(t, 3.15, .9, 1, .1, expo_out)
            if r > 2: d.ellipse([mx + math.cos(a) * R - r, my + math.sin(a) * R - r, mx + math.cos(a) * R + r, my + math.sin(a) * R + r], fill=(242, 240, 228))
    if 3.15 <= t < 4.7:
        sc = tw(t, 3.15, .5, 0, 1, back_out); ry = tw(t, 4.3, .4, 0, -60, cubic_out)
        d = layer(img, lambda dd, cx, cy: bigtext(dd, "¡PUF!", cx, cy, 120, fill=YEL), mx, my + ry, 520, sc, sc, tw(t, 3.15, .5, 25, 0, back_out), tw(t, 4.3, .4, 1, 0))
    # Tierra: entra elástica, flota, mira a la Luna, se asusta y tiembla
    ex = 330 + shake(t, 3.3, .4, 10); ey = tw(t, .1, .9, 1360, 1060, elastic_out) + yoyo(t, 1.0, 1.1, 0, -14)
    es = tw(t, .1, .9, .7, 1, elastic_out)
    look = (tw(t, 1.4, .5, 0, .9, quad_out), tw(t, 1.4, .5, 0, -.8, quad_out)) if t < 3.3 else (0, 0)
    eye = 1 if t < 3.3 else tw(t, 3.3, .25, 1, 1.35, back_out)
    def earth_sh(dd, cx, cy):
        planet_earth(dd, cx, cy, 230, mood="happy" if t < 3.3 else "scared", look=look, eye=eye, shade=True)
    d = layer(img, earth_sh, ex, ey, 560, es, es, 0, tw(t, .1, .4, 0, 1))
    chip(d, "¿QUÉ PASARÍA SI…?", CHIP1, bg=PURPLE, appear=tw(t, 0, .45, 0, 1, linear))
    caption_words(d, "¿Qué pasaría si mañana *la Luna desapareciera*?", t - .2)
    return img

if __name__ == "__main__":
    t0 = time.time()
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "/tmp/dqa_out/py3_luna.mp4"], stdin=subprocess.PIPE)
    for i in range(int(5.5 * 30)): p.stdin.write(frame(i / 30).tobytes())
    p.stdin.close(); p.wait(); print(f"render: {time.time() - t0:.1f} s")
