import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, guy, W, H, YEL, RED, WHITE, BLK, SKIN, FEET)
from reel13 import SPACE

FPS = 30
DUR = 66.0

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img
DAY = grad((110, 180, 240), (240, 230, 200))
DUSK = grad((240, 120, 60), (250, 210, 120))
NIGHT = grad((5, 8, 30), (30, 30, 70))

CONT = [(0.0, -0.35, 0.45, 0.3), (0.9, 0.1, 0.4, 0.5), (2.0, -0.1, 0.5, 0.35), (2.9, 0.35, 0.35, 0.25), (4.1, -0.2, 0.45, 0.4), (5.2, 0.3, 0.3, 0.3)]

def spin_earth(img, cx, cy, r, ang, mood="happy"):
    tmp = Image.new("RGBA", (int(2 * r) + 4, int(2 * r) + 4), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    o = r + 2
    td.ellipse([o - r, o - r, o + r, o + r], fill=(50, 110, 210, 255))
    for (lon, lat, w, h) in CONT:
        a = lon + ang
        x = math.sin(a)
        if math.cos(a) < -0.1: continue
        px = o + x * r * 0.95; py = o + lat * r
        ww = w * r * max(0.15, math.cos(a))
        td.ellipse([px - ww, py - h * r, px + ww, py + h * r], fill=(70, 170, 90, 255))
    mask = Image.new("L", tmp.size, 0); ImageDraw.Draw(mask).ellipse([o - r, o - r, o + r, o + r], fill=255)
    img.paste(tmp, (int(cx - o), int(cy - o)), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 200, 255), width=max(4, int(r * 0.03)))
    # cara
    for sx in (-1, 1):
        ex, ey = cx + sx * r * 0.32, cy - r * 0.12
        er = r * 0.14 if mood != "shock" else r * 0.18
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=WHITE, outline=BLK, width=max(3, int(r * 0.025)))
        pr = er * (0.35 if mood == "shock" else 0.5)
        d.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=BLK)
    if mood == "happy":
        d.arc([cx - r * 0.3, cy + r * 0.0, cx + r * 0.3, cy + r * 0.4], 20, 160, fill=BLK, width=max(4, int(r * 0.04)))
    elif mood == "shock":
        d.ellipse([cx - r * 0.12, cy + r * 0.15, cx + r * 0.12, cy + r * 0.45], fill=(70, 10, 20), outline=BLK, width=4)
    else:
        d.line([(cx - r * 0.2, cy + r * 0.25), (cx + r * 0.2, cy + r * 0.25)], fill=BLK, width=max(4, int(r * 0.04)))

def stamp_guy(img, x, y, s, ang, mood="scared", arms="up", t=0.0, hoodie=(240, 120, 40)):
    tmp = Image.new("RGBA", (int(900 * s), int(900 * s)), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    guy(td, 450 * s, 750 * s, s, mood=mood, arms=arms, t=t, hoodie=hoodie)
    rot = tmp.rotate(ang, resample=Image.BICUBIC, center=(450 * s, 450 * s))
    img.paste(rot, (int(x - 450 * s), int(y - 450 * s)), rot)

def plane(d, x, y, s):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(120), y - S(18), x + S(120), y + S(18)], S(18), fill=WHITE, outline=BLK, width=4)
    d.polygon([(x - S(10), y), (x - S(60), y + S(80)), (x - S(20), y + S(80)), (x + S(40), y)], fill=(200, 210, 230), outline=BLK)
    d.polygon([(x - S(110), y - S(10)), (x - S(140), y - S(60)), (x - S(100), y - S(60)), (x - S(80), y - S(10))], fill=(200, 210, 230), outline=BLK)
    for k in range(5): d.ellipse([x + S(20) + k * S(18), y - S(8), x + S(30) + k * S(18), y + S(2)], fill=(80, 140, 220))

def gauge(d, cx, cy, r, val, vmax, label):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(30, 30, 40), outline=WHITE, width=6)
    for k in range(11):
        a = math.pi + k / 10 * math.pi
        d.line([(cx + math.cos(a) * r * 0.85, cy + math.sin(a) * r * 0.85), (cx + math.cos(a) * r * 0.97, cy + math.sin(a) * r * 0.97)], fill=WHITE, width=5)
    a = math.pi + cl(val / vmax) * math.pi
    d.line([(cx, cy), (cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8)], fill=RED, width=12)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=RED)
    d.text((cx, cy + 50), label, font=F(56), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)

def building(d, x, y, w, h, col, rng, lit=False):
    d.rectangle([x, y - h, x + w, y], fill=col, outline=BLK, width=4)
    for wy in range(int(y - h + 20), int(y - 30), 50):
        for wx in range(int(x + 16), int(x + w - 30), 46):
            d.rectangle([wx, wy, wx + 26, wy + 30], fill=(255, 220, 120) if lit and rng.random() < 0.6 else (170, 210, 240))

def car(d, x, y, s, col):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(90), y - S(60), x + S(90), y - S(20)], S(16), fill=col, outline=BLK, width=4)
    d.rounded_rectangle([x - S(50), y - S(95), x + S(45), y - S(55)], S(14), fill=col, outline=BLK, width=4)
    d.rectangle([x - S(38), y - S(88), x + S(35), y - S(62)], fill=(170, 210, 240))
    for sx in (-1, 1): d.ellipse([x + sx * S(55) - S(22), y - S(42), x + sx * S(55) + S(22), y + S(2)], fill=(30, 30, 30))

def cow(d, x, y, s):
    S = lambda v: v * s
    d.ellipse([x - S(90), y - S(70), x + S(90), y + S(30)], fill=WHITE, outline=BLK, width=4)
    d.ellipse([x - S(40), y - S(55), x + S(10), y - S(10)], fill=BLK)
    d.ellipse([x + S(70), y - S(80), x + S(140), y - S(20)], fill=WHITE, outline=BLK, width=4)
    d.ellipse([x + S(105), y - S(60), x + S(118), y - S(47)], fill=BLK)
    for k in range(4): d.rectangle([x - S(70) + k * S(45), y + S(15), x - S(55) + k * S(45), y + S(60)], fill=WHITE, outline=BLK, width=3)

def speedlines(d, t, n=26, col=WHITE):
    rng = random.Random(2)
    for i in range(n):
        y = rng.uniform(250, 1350); ln = rng.uniform(80, 260); sp = rng.uniform(1600, 2600)
        x = (rng.uniform(0, W) + t * sp) % (W + 400) - 300
        d.line([(x, y), (x + ln, y)], fill=col, width=5)

def wave(d, t, k):
    top = lerp(1400, 650, k)
    pts = [(0, H)]
    for x in range(0, W + 40, 40):
        pts.append((x, top + 120 * math.sin(x * 0.006 + t * 3) + (x / W) * 260))
    pts.append((W, H))
    d.polygon(pts, fill=(40, 110, 200))
    for x in range(0, W, 120):
        y = top + 120 * math.sin(x * 0.006 + t * 3) + (x / W) * 260
        d.ellipse([x - 40, y - 25, x + 40, y + 15], fill=(230, 245, 255))

def calendar(d, cx, cy, day, label, col):
    d.rounded_rectangle([cx - 190, cy - 170, cx + 190, cy + 170], 26, fill=WHITE, outline=BLK, width=7)
    d.rounded_rectangle([cx - 190, cy - 170, cx + 190, cy - 70], 26, fill=col, outline=BLK, width=7)
    d.text((cx, cy - 120), label, font=F(52), fill=WHITE, anchor="mm")
    d.text((cx, cy + 50), str(day), font=F(150), fill=BLK, anchor="mm")
    for sx in (-1, 1): d.rounded_rectangle([cx + sx * 110 - 14, cy - 200, cx + sx * 110 + 14, cy - 140], 10, fill=(120, 120, 130), outline=BLK, width=3)

def town(d, lit, rng):
    for i, (x, w, h, c) in enumerate([(30, 200, 420, (200, 120, 90)), (260, 180, 560, (120, 140, 180)), (470, 220, 380, (230, 190, 110)), (720, 190, 500, (150, 110, 160)), (930, 160, 340, (110, 160, 130))]):
        building(d, x, 1380, w, h, c if not lit else dk(c, 0.45), rng, lit=lit)
    d.rectangle([0, 1380, W, H], fill=(70, 70, 75))

def clock(d, cx, cy, r, t, ring=True):
    sh = math.sin(t * 40) * 8 if ring else 0
    cx += sh
    for sx in (-1, 1): d.chord([cx + sx * r * 0.6 - r * 0.35, cy - r * 1.15, cx + sx * r * 0.6 + r * 0.35, cy - r * 0.45], 180, 360, fill=(230, 60, 50), outline=BLK, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(230, 60, 50), outline=BLK, width=6)
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82], fill=WHITE, outline=BLK, width=4)
    d.line([(cx, cy), (cx, cy - r * 0.6)], fill=BLK, width=8); d.line([(cx, cy), (cx + r * 0.0, cy + r * 0.0)], fill=BLK, width=8)
    d.line([(cx, cy), (cx - r * 0.0, cy + r * 0.5)], fill=BLK, width=6)
    if ring:
        for k in range(3):
            a = -0.9 + k * 0.4
            d.arc([cx - r * 1.5, cy - r * 1.5, cx + r * 1.5, cy + r * 1.5], math.degrees(a) - 8 - 90, math.degrees(a) + 8 - 90, fill=BLK, width=6)

CAPS = [
    (0.0, 3.5, "¿Qué pasaría si la Tierra *dejara de girar* de repente?"),
    (3.5, 6.5, "Y no… no saldrías al espacio. Eso sería *lo de menos*"),
    (6.5, 9.5, "En el ecuador gira a unos *1,670 km/h*"),
    (9.5, 13.0, "Más rápido que *un avión comercial*… y ni nos mareamos"),
    (13.0, 16.0, "Ahora imagina que *frena en seco*"),
    (16.0, 22.0, "Tú, los edificios, los autos y *los océanos* seguirían hacia el este a *casi 1,700 km/h*"),
    (22.0, 26.0, "*Vientos devastadores*, océanos desbordados, ciudades arrasadas"),
    (26.0, 30.0, "¿Por qué no saldrías al espacio? Porque *la gravedad sigue ahí*"),
    (30.0, 35.0, "El problema: saldrías disparado *a través de tu ciudad*"),
    (35.0, 41.0, "Si sobrevivieras… *un día duraría un año entero*"),
    (41.0, 47.0, "*Seis meses de sol*… y *seis meses de noche*"),
    (47.0, 53.0, "Extrañarías cuando tu mayor problema era *levantarte para trabajar*"),
    (53.0, 59.0, "Aunque, siendo honestos… *ese día tampoco llegarías a la oficina*"),
]

def render(v, t=None):
    if t is None: t = v
    shake = 0
    if v < 6.5:
        img = SPACE.copy(); d = ImageDraw.Draw(img)
        spin_earth(img, 540, 800, 330, t * 1.2, "happy")
        d = ImageDraw.Draw(img)
        for k in range(3):
            a = t * 2 + k * 2.1
            d.arc([540 - 420, 800 - 140, 540 + 420, 800 + 140], math.degrees(a), math.degrees(a) + 40, fill=(200, 220, 255), width=8)
        chip(d, "¿QUÉ PASARÍA SI…?", 300, bg=RED, appear=v / 0.3)
        if v > 3.5:
            chip(d, "¿AL ESPACIO? NO", 1250, bg=BLK, size=50, appear=(v - 3.5) / 0.3)
    elif v < 13.0:
        lt = v - 6.5
        img = SPACE.copy(); d = ImageDraw.Draw(img)
        spin_earth(img, 540, 760, 250, t * 1.6, "happy")
        d = ImageDraw.Draw(img)
        gauge(d, 540, 430, 200, 1670 * ease(lt / 1.5), 2000, f"{int(1670 * ease(lt / 1.5)):,} KM/H")
        if lt > 3.0:
            px = lerp(1250, 760, ease((lt - 3.0) / 1.0)) - max(0, lt - 4.0) * 120
            plane(d, px, 1150, 1.2)
            d.text((px, 1250), "AVIÓN: ~900 KM/H", font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    elif v < 16.0:
        lt = v - 13.0
        img = SPACE.copy(); d = ImageDraw.Draw(img)
        ang = 13.0 * 1.6 + min(lt, 0.6) * 0.8
        spin_earth(img, 540, 800, 330, ang, "shock" if lt > 0.4 else "happy")
        d = ImageDraw.Draw(img)
        if lt > 0.3:
            shake = 12 if lt < 1.4 else 0
            bigtext(d, "¡SKRRRT!", 540, 330, 140, fill=YEL)
            for k in range(4):
                d.line([(140 + k * 30, 600 + k * 120), (60 + k * 30, 640 + k * 120)], fill=WHITE, width=10)
            chip(d, "VELOCIDAD: 0", 1250, bg=RED, appear=(lt - 0.5) / 0.3)
    elif v < 26.0:
        lt = v - 16.0
        img = DAY.copy(); d = ImageDraw.Draw(img)
        rng = random.Random(4)
        drift = ease(lt / 1.2)
        town(d, False, rng) if lt < 0.6 else None
        if lt >= 0.6:
            d.rectangle([0, 1380, W, H], fill=(70, 70, 75))
            # objetos saliendo hacia el este (derecha)
            for i, (bx, by, kind) in enumerate([(-200, 900, "bld"), (100, 1300, "car"), (400, 700, "cow"), (-500, 1100, "car2"), (-800, 600, "bld2")]):
                x = (bx + (t - 16.6) * 900 + i * 380) % (W + 900) - 450
                if kind == "bld": building(d, x, by, 160, 300, (200, 120, 90), random.Random(i))
                elif kind == "bld2": building(d, x, by, 140, 240, (120, 140, 180), random.Random(i))
                elif kind == "car": car(d, x, by, 0.9, (60, 120, 220))
                elif kind == "car2": car(d, x, by, 0.9, (230, 70, 60))
                else: cow(d, x, by, 0.9)
            speedlines(d, t)
            stamp_guy(img, 620, 1050, 0.55, -70, t=t); d = ImageDraw.Draw(img)
            chip(d, "→ ESTE A 1,700 KM/H", 300, bg=RED, appear=(lt - 0.6) / 0.3)
        if lt > 6.0:
            wave(d, t, ease((lt - 6.0) / 2.0))
            chip(d, "OLAS + VIENTOS + CIUDADES ARRASADAS", 420, bg=(40, 90, 160), size=40, appear=(lt - 6.2) / 0.3)
    elif v < 35.0:
        lt = v - 26.0
        img = DAY.copy(); d = ImageDraw.Draw(img)
        if lt < 4.0:
            spin_earth(img, 540, 1000, 300, 0, "neutral")
            d = ImageDraw.Draw(img)
            for k in range(2):
                y = 400 + k * 50
                d.polygon([(540 - 26, y), (540 + 26, y), (540, y + 40)], fill=(60, 180, 90), outline=BLK)
            chip(d, "GRAVEDAD: SIGUE AQUÍ ✓", 300, bg=(30, 140, 80), appear=lt / 0.3)
            stamp_guy(img, 540, 597, 0.35, 0, mood="neutral", arms="down", t=t)
        else:
            k = (lt - 4.0) / 5.0
            rng = random.Random(9)
            for i, (x, w, h, c) in enumerate([(-40, 260, 700, (200, 120, 90)), (300, 240, 820, (120, 140, 180)), (620, 260, 640, (230, 190, 110)), (900, 260, 760, (150, 110, 160))]):
                building(d, x, 1380, w, h, c, rng)
            d.rectangle([0, 1380, W, H], fill=(70, 70, 75))
            gx = lerp(-200, 1300, k)
            for i, (x, w, h) in enumerate([(-40, 260, 700), (300, 240, 820), (620, 260, 640), (900, 260, 760)]):
                if gx > x + w / 2:
                    hx = x + w / 2
                    d.polygon([(hx - 90, 900), (hx - 30, 820), (hx + 60, 870), (hx + 100, 990), (hx + 20, 1060), (hx - 80, 1010)], fill=(30, 30, 40))
                    for j in range(5): d.rectangle([hx - 120 + j * 50, 880 + (j % 2) * 140, hx - 100 + j * 50, 900 + (j % 2) * 140], fill=(200, 200, 210))
            speedlines(d, t, 18, (255, 255, 255))
            stamp_guy(img, gx, 960, 0.5, -80, t=t); d = ImageDraw.Draw(img)
            bigtext(d, "¡CRASH!", 540, 330, 120, fill=YEL)
    elif v < 47.0:
        lt = v - 35.0
        night = lt >= 6.0
        img = (NIGHT if night else DAY).copy(); d = ImageDraw.Draw(img)
        if night:
            rng = random.Random(1)
            for i in range(80):
                x, y = rng.uniform(0, W), rng.uniform(0, 900)
                d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=WHITE)
            d.ellipse([780, 180, 920, 320], fill=(240, 240, 220)); d.ellipse([820, 160, 960, 300], fill=(5, 8, 30))
        else:
            d.ellipse([440, 160, 640, 360], fill=(255, 220, 60), outline=(255, 160, 40), width=10)
        town(d, night, random.Random(4))
        if not night:
            day = int(lerp(1, 182, cl((lt - 0.8) / 4.5)))
            calendar(d, 540, 760, day, "DÍA", (240, 150, 40))
            if lt > 3.0: chip(d, "1 DÍA = 1 AÑO", 1240, bg=RED, appear=(lt - 3.0) / 0.3)
        else:
            day = int(lerp(183, 365, cl((lt - 6.2) / 2.4)))
            calendar(d, 540, 760, day, "NOCHE", (60, 60, 130))
            chip(d, "6 MESES DE NOCHE", 1240, bg=(60, 60, 130), appear=(lt - 6.0) / 0.3)
    elif v < 59.0:
        lt = v - 47.0
        if lt < 6.0:
            img = Image.new("RGB", (W, H), (230, 220, 240)); d = ImageDraw.Draw(img)
            d.rectangle([600, 300, 1000, 760], fill=(5, 8, 30), outline=(120, 80, 60), width=20)
            d.line([(800, 300), (800, 760)], fill=(120, 80, 60), width=14)
            for i in range(10): d.ellipse([620 + (i * 37) % 360, 320 + (i * 53) % 420, 626 + (i * 37) % 360, 326 + (i * 53) % 420], fill=WHITE)
            d.rectangle([0, 1100, W, H], fill=(170, 140, 120))
            d.rounded_rectangle([20, 1020, 300, 1180], 30, fill=(240, 240, 250), outline=BLK, width=6)
            d.rounded_rectangle([30, 990, 150, 1040], 20, fill=WHITE, outline=BLK, width=4)
            stamp_guy(img, 470, 1030, 0.5, 0, mood="scared", arms="down", t=t, hoodie=(120, 160, 230)); d = ImageDraw.Draw(img)
            clock(d, 820, 1010, 90, t, ring=True)
            d.text((820, 1150), "7:00", font=F(60), fill=BLK, anchor="mm")
            chip(d, "¿HORA DE TRABAJAR?", 220, bg=(120, 160, 230), appear=lt / 0.3)
        else:
            img = DUSK.copy(); d = ImageDraw.Draw(img)
            d.rectangle([0, 1380, W, H], fill=(70, 70, 75))
            pts = [(200, 1380), (230, 900), (330, 1000), (420, 820), (560, 960), (650, 860), (760, 1050), (860, 950), (880, 1380)]
            d.polygon(pts, fill=(120, 110, 120), outline=BLK)
            for k in range(8): d.rectangle([260 + k * 70, 1100 + (k % 3) * 60, 300 + k * 70, 1130 + (k % 3) * 60], fill=(60, 50, 60))
            d.rectangle([528, 740, 552, 900], fill=(110, 80, 50), outline=BLK, width=3)
            d.rounded_rectangle([300, 640, 780, 760], 16, fill=WHITE, outline=BLK, width=6)
            d.text((540, 700), "OFICINA", font=F(80), fill=BLK, anchor="mm")
            d.line([(300, 640), (780, 760)], fill=RED, width=14); d.line([(780, 640), (300, 760)], fill=RED, width=14)
            chip(d, "HOY NO HAY OFICINA", 300, bg=RED, appear=(lt - 6.2) / 0.3)
    else:
        lt = v - 59.0
        img = SPACE.copy(); d = ImageDraw.Draw(img)
        spin_earth(img, 540, 780, 260, t * 1.2, "happy")
        d = ImageDraw.Draw(img)
        bigtext(d, "¿TÚ QUÉ HARÍAS", 540, 300, 80, fill=WHITE)
        bigtext(d, "SI SE DETIENE?", 540, 400, 80, fill=YEL)
        if lt > 1.5:
            sc = pop((lt - 1.5) / 0.35)
            d.rounded_rectangle([540 - 330 * sc, 1250 - 80 * sc, 540 + 330 * sc, 1250 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
            d.text((540, 1250), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
        d.text((540, 1480), "COMENTA ↓", font=F(70), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=BLK)
    for cs, ce, txt in CAPS:
        if cs <= v < ce: rich_caption(d, txt, appear=(v - cs) / 0.25)
    arr = np.asarray(img)
    if shake:
        arr = np.roll(arr, int(math.sin(t * 60) * shake), axis=1)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r25.png"); sys.exit()
    try:
        from warp25 import v_of_T, DUR as D2
    except ImportError:
        v_of_T = lambda T: T; D2 = DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(D2 * FPS)):
        p.stdin.write(render(v_of_T(i / FPS), i / FPS).tobytes())
    p.stdin.close(); p.wait()
