import sys, math, subprocess, random, time
sys.path.insert(0, "/home/claude/datos-asustan-videos")
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import *
from lib.personajes import guy, anchors
from lib import produce
FEET, S = 1300, .72
rnd = random.Random(2); STARS = [(rnd.uniform(0, W), rnd.uniform(380, 1250), rnd.uniform(1.5, 3.5), rnd.uniform(0, 6)) for _ in range(90)]

def guy_layer(img, x, feet, s, sx=1, sy=1, rot=0, **kw):
    """El muchacho en una capa, anclado a los pies: se aplasta/estira sin despegarse del piso."""
    H2 = 760
    def fn(dd, cx, cy): guy(dd, cx, cy + 330, s, **kw)
    return layer(img, fn, x, feet - 330 * sy, H2, sx, sy, rot)

def frame(t):
    img, d = canvas(((10, 12, 30), (30, 30, 55)))
    for x, y, r, ph in STARS:
        c = int(150 + 100 * (.5 + .5 * math.sin(t * 3 + ph))); d.ellipse([x - r, y - r, x + r, y + r], fill=(c, c, 255))
    d.rectangle([0, 1290, W, 1380], fill=(40, 40, 50))
    # 1) entra caminando: rebote por paso, balanceo, y frena con back_out
    x = tw(t, 0, 1.0, -150, 540, back_out)
    walking = t < 1.0
    step = abs(math.sin(t * 9)) if walking else 0
    sy = 1 - .04 * step if walking else 1
    rot = math.sin(t * 9) * 3 if walking else 0
    if 1.0 <= t < 1.6: sy = tw(t, 1.0, .6, .9, 1, elastic_out)                  # aterriza y se acomoda
    # 2) anticipación y alza los brazos con el celular
    arms = "up" if t >= 1.75 else "down"
    if 1.55 <= t < 1.75: sy = tw(t, 1.55, .2, 1, .92, quad_out)               # se agacha antes
    if 1.75 <= t < 2.1: sy = tw(t, 1.75, .35, 1.08, 1, back_out)               # y se estira
    # 3) brinco de susto al ver que no hay Luna
    jump = 0
    if 2.9 <= t < 3.6: jump = -tw(t, 2.9, .25, 0, 90, cubic_out) if t < 3.15 else -tw(t, 3.15, .45, 90, 0, bounce_out)
    scared = t >= 2.9
    # 4) mira a un lado y a otro buscando la Luna
    look = yoyo(t, 3.6, .5, -1, 1) if t >= 3.6 else 0
    d = guy_layer(img, x, FEET + jump, S, 1, sy, rot, mood="scared" if scared else "neutral", arms=arms, look=look, t=t)
    if arms == "up":                                                               # celular en la mano (anclado)
        a = anchors(x, FEET + jump - (1 - sy) * 0, S); hx, hy = a["hand_r_up"]; hy -= (sy - 1) * 400 * S
        sc = tw(t, 1.75, .3, 0, 1, back_out)
        if sc > .05:
            w, h = 70 * sc, 115 * sc
            d.rounded_rectangle([hx - w, hy - 2.1 * h, hx + w, hy + 10], 18, fill=(70, 70, 80), outline=BLK, width=5)
            d.rectangle([hx - w + 14, hy - 2.1 * h + 18, hx + w - 14, hy - 8], fill=(5, 5, 10))
            if t >= 2.4: d.text((hx, hy - h), "?", font=F(int(80 * tw(t, 2.4, .3, .3, 1, back_out))), fill=(170, 170, 190), anchor="mm")
            d.ellipse([hx - 20, hy - 20, hx + 20, hy + 20], fill=SKIN, outline=BLK, width=2)
    if t >= 3.0:                                                                   # gota de sudor que resbala
        a = anchors(x, FEET + jump, S); gx, gy = a["head"][0] + 75, a["head"][1] - 40 + tw(t, 3.0, 1.2, 0, 70, quad_out)
        d.polygon([(gx, gy - 26), (gx - 14, gy), (gx + 14, gy)], fill=(120, 190, 250)); d.ellipse([gx - 14, gy - 12, gx + 14, gy + 16], fill=(120, 190, 250), outline=BLK, width=2)
    chip(d, "SIN LUNA", CHIP1, bg=GRAY, appear=tw(t, 0, .45, 0, 1, linear))
    caption_words(d, "Y tu foto de la luna con el celular… *pues ya no*", t - .2)
    return img

if __name__ == "__main__":
    t0 = time.time()
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "/tmp/dqa_out/humano_curvas.mp4"], stdin=subprocess.PIPE)
    for i in range(int(5 * 30)): p.stdin.write(frame(i / 30).tobytes())
    p.stdin.close(); p.wait(); print(f"render: {time.time() - t0:.1f} s")
    # versión actual de la misma escena (spec de la Luna, línea 2)
    m = produce.load("/home/claude/datos-asustan-videos/specs/s32_luna.py"); s0 = m.NSTART[2]
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "/tmp/dqa_out/humano_actual.mp4"], stdin=subprocess.PIPE)
    for i in range(int(5 * 30)): p.stdin.write(produce.render_frame(m, s0 + i / 30 * (m.NSTART[3] - s0) / 5, s0 + i / 30).tobytes())
    p.stdin.close(); p.wait()
