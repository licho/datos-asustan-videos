import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN, FEET)
from reel2 import phone

FPS = 30

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def make_space():
    img = grad((5, 5, 25), (20, 10, 45)); d = ImageDraw.Draw(img)
    rng = random.Random(1)
    for i in range(220):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1, 3.5)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(230, 230, 255))
    return img
SPACE = make_space()

def earth(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 110, 210), outline=(150, 200, 255), width=10)
    for (a, b, w, h) in [(-0.4, -0.3, 0.5, 0.35), (0.25, -0.1, 0.4, 0.5), (-0.2, 0.35, 0.35, 0.25)]:
        d.ellipse([cx + a * r - w * r / 2, cy + b * r - h * r / 2, cx + a * r + w * r / 2, cy + b * r + h * r / 2], fill=(70, 170, 90))

def asteroid(d, cx, cy, r, t=0.0, face="angry", fire=0.0, ang=-2.4):
    if fire > 0:
        for k in range(14, 0, -1):
            fx, fy = cx + math.cos(ang) * r * k * 0.28 * (1 + fire), cy + math.sin(ang) * r * k * 0.28 * (1 + fire)
            fr = r * (1.05 - k * 0.06) + math.sin(t * 20 + k) * r * 0.05
            col = lc((255, 240, 120), (220, 60, 20), k / 14)
            d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=col)
    pts = []
    rng = random.Random(3)
    for i in range(14):
        a = i / 14 * 2 * math.pi
        rr = r * rng.uniform(0.85, 1.08)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=(130, 110, 95), outline=BLK)
    for (a, b, c) in [(-0.4, -0.3, 0.22), (0.35, 0.35, 0.18), (0.45, -0.4, 0.12), (-0.3, 0.45, 0.13)]:
        d.ellipse([cx + a * r - c * r, cy + b * r - c * r, cx + a * r + c * r, cy + b * r + c * r], fill=(105, 88, 75), outline=(80, 65, 55), width=max(1, int(r * 0.03)))
    if face:
        for sx in (-1, 1):
            ex, ey = cx + sx * r * 0.3, cy - r * 0.05
            d.ellipse([ex - r * 0.17, ey - r * 0.17, ex + r * 0.17, ey + r * 0.17], fill=WHITE, outline=BLK, width=max(2, int(r * 0.04)))
            d.ellipse([ex - r * 0.07, ey - r * 0.04, ex + r * 0.07, ey + r * 0.1], fill=BLK)
            if face == "angry":
                d.line([(ex - r * 0.2, ey - r * 0.25 - sx * r * 0.08), (ex + r * 0.2, ey - r * 0.25 + sx * r * 0.08)], fill=BLK, width=max(3, int(r * 0.07)))
        if face == "angry":
            d.chord([cx - r * 0.3, cy + r * 0.2, cx + r * 0.3, cy + r * 0.55], 0, 180, fill=(60, 10, 20), outline=BLK, width=max(2, int(r * 0.04)))
        else:
            d.arc([cx - r * 0.25, cy + r * 0.25, cx + r * 0.25, cy + r * 0.5], 200, 340, fill=BLK, width=max(2, int(r * 0.05)))

def bus(d, x, y, s):
    S = lambda v: v * s
    d.rounded_rectangle([x, y - S(110), x + S(260), y - S(20)], int(S(16)), fill=(240, 190, 40), outline=BLK, width=5)
    for k in range(5): d.rectangle([x + S(15 + k * 48), y - S(95), x + S(50 + k * 48), y - S(60)], fill=(150, 200, 240), outline=BLK, width=2)
    for wx in (S(50), S(210)): d.ellipse([x + wx - S(22), y - S(42), x + wx + S(22), y + S(2)], fill=(40, 40, 40))

def building(d, x, y, w, h, floors, col=(180, 150, 120), lit=True):
    d.rectangle([x, y - h, x + w, y], fill=col, outline=BLK, width=5)
    fh = h / floors
    for f in range(floors):
        for k in range(3):
            wx = x + 15 + k * (w - 30) / 3
            d.rectangle([wx, y - h + f * fh + fh * 0.25, wx + (w - 30) / 3 - 14, y - h + f * fh + fh * 0.75],
                        fill=(250, 230, 150) if lit else (120, 170, 210), outline=BLK, width=2)

def dino(d, x, y, s, t, sign=None):
    S = lambda v: v * s
    g = (110, 180, 90); dg = (80, 140, 65)
    d.polygon([(x - S(150), y - S(150)), (x - S(330), y - S(110)), (x - S(150), y - S(100))], fill=g, outline=BLK)
    d.ellipse([x - S(180), y - S(260), x + S(120), y - S(60)], fill=g, outline=BLK, width=5)
    for k in range(4):
        d.polygon([(x - S(140) + k * S(55), y - S(250)), (x - S(115) + k * S(55), y - S(300)), (x - S(90) + k * S(55), y - S(245))], fill=(230, 120, 60), outline=BLK)
    d.rectangle([x - S(120), y - S(80), x - S(70), y], fill=dg, outline=BLK, width=4)
    d.rectangle([x + S(20), y - S(80), x + S(70), y], fill=dg, outline=BLK, width=4)
    d.polygon([(x + S(40), y - S(220)), (x + S(120), y - S(380)), (x + S(200), y - S(360)), (x + S(110), y - S(180))], fill=g, outline=BLK)
    d.ellipse([x + S(80), y - S(470), x + S(260), y - S(350)], fill=g, outline=BLK, width=5)
    d.ellipse([x + S(170), y - S(450), x + S(215), y - S(405)], fill=WHITE, outline=BLK, width=3)
    d.ellipse([x + S(185), y - S(450), x + S(205), y - S(428)], fill=BLK)
    d.ellipse([x + S(195), y - S(400), x + S(235), y - S(375)], fill=BLK)
    if sign:
        d.line([(x + S(60), y - S(150)), (x + S(60), y - S(420))], fill=(110, 75, 40), width=int(S(14)))
        d.rounded_rectangle([x - S(80), y - S(560), x + S(200), y - S(400)], int(S(18)), fill=WHITE, outline=BLK, width=5)
        d.text((x + S(60), y - S(480)), sign, font=F(S(110)), fill=RED, anchor="mm")

def window_frame(d, x, y, w, h, broken=0.0):
    d.rectangle([x, y, x + w, y + h], fill=(160, 210, 240), outline=(240, 240, 240), width=16)
    if broken > 0:
        rng = random.Random(5)
        cx, cy = x + w / 2, y + h / 2
        for k in range(10):
            a = rng.uniform(0, 2 * math.pi)
            d.line([(cx, cy), (cx + math.cos(a) * w * 0.6 * broken, cy + math.sin(a) * h * 0.6 * broken)], fill=WHITE, width=5)
        for k in range(int(broken * 18)):
            sx, sy = cx + rng.uniform(-1, 1) * w * broken * 1.3, cy + rng.uniform(-0.3, 1.2) * h * broken
            sz = rng.uniform(12, 30)
            d.polygon([(sx, sy - sz), (sx + sz * 0.7, sy + sz * 0.6), (sx - sz * 0.6, sy + sz * 0.4)], fill=(200, 235, 255), outline=(120, 160, 190))

def table(d, cx, y, s):
    S = lambda v: v * s
    d.rectangle([cx - S(300), y - S(330), cx + S(300), y - S(290)], fill=(140, 95, 55), outline=BLK, width=5)
    for sx in (-1, 1): d.rectangle([cx + sx * S(270) - S(18), y - S(290), cx + sx * S(270) + S(18), y], fill=(120, 80, 45), outline=BLK, width=4)

def crouch_guy(d, x, y, s, t):
    S = lambda v: v * s
    d.ellipse([x - S(130), y - S(230), x + S(130), y], fill=(240, 120, 40), outline=None)
    d.ellipse([x - S(90), y - S(330), x + S(90), y - S(150)], fill=SKIN)
    d.chord([x - S(96), y - S(342), x + S(96), y - S(180)], 180, 360, fill=(55, 38, 28))
    for sx in (-1, 1):
        d.line([(x + sx * S(110), y - S(140)), (x + sx * S(40), y - S(330))], fill=dk((240, 120, 40), 0.8), width=int(S(44)))
        d.ellipse([x + sx * S(40) - S(26), y - S(356), x + sx * S(40) + S(26), y - S(304)], fill=SKIN)
    for sx in (-1, 1):
        ex, ey = x + sx * S(32), y - S(240)
        d.ellipse([ex - S(18), ey - S(18), ex + S(18), ey + S(18)], fill=WHITE, outline=BLK, width=3)
        d.ellipse([ex - S(6), ey - S(6), ex + S(6), ey + S(6)], fill=BLK)

def ship(d, x, y, s):
    S = lambda v: v * s
    d.rectangle([x - S(40), y - S(30), x + S(40), y + S(30)], fill=(220, 220, 230), outline=BLK, width=4)
    for sx in (-1, 1):
        x0, x1 = sorted((x + sx * S(50), x + sx * S(180)))
        d.rectangle([x0, y - S(14), x1, y + S(14)], fill=(60, 80, 160), outline=BLK, width=3)
        for k in range(4): d.line([(x + sx * (S(50) + k * S(33)), y - S(14)), (x + sx * (S(50) + k * S(33)), y + S(14))], fill=(150, 170, 230), width=2)

CAPS = [
    (0.0, 2.5, "Un *asteroide* viene directo a la Tierra"),
    (2.5, 5.0, "Y esta vez *no hay perforadores* para salvarnos"),
    (5.0, 10.0, "Todo depende del *tamaño*: si mide como un *edificio de 6 pisos*… *explota en el cielo*"),
    (10.0, 14.0, "*Rusia, 2013:* una roca de *~20 metros* estalló sobre Cheliábinsk"),
    (14.0, 17.0, "Primero, *un destello*… luego, *la onda de choque*"),
    (17.0, 21.0, "*Más de 1,600 personas* buscaron atención médica"),
    (21.0, 24.0, "Por *vidrios rotos*… se *asomaron a la ventana*"),
    (24.0, 27.5, "¿Y si mide *10 kilómetros*? Ya pasó: hace *66 millones de años*"),
    (27.5, 31.0, "Pregúntale a los *dinosaurios*… ah, *no puedes*"),
    (31.0, 35.0, "Si ves un *destello gigante*: *aléjate de las ventanas*, agáchate y cúbrete"),
    (35.0, 38.0, "La *onda de choque* llega *después de la luz*"),
    (38.0, 44.0, "La NASA ya encontró *~95%* de los asteroides de *más de 1 km* cercanos"),
    (44.0, 50.0, "Sigue las *alertas oficiales*… y *no grabes el fin del mundo en vertical*"),
    (50.0, 55.0, "En 2022, la NASA *estrelló una nave* contra un asteroide… *a propósito*"),
    (55.0, 58.0, "Y cambió su órbita *32 minutos*"),
    (58.0, 61.0, "O sea, *ya sabemos empujar rocas espaciales*"),
    (61.0, 68.0, "*Sígueme* para más *manuales de supervivencia*"),
]

def s_hook(t):
    img = SPACE.copy(); d = ImageDraw.Draw(img)
    earth(d, 540, 1750, 700)
    ax = lerp(950, 650, ease(t / 5)); ay = lerp(250, 650, ease(t / 5))
    asteroid(d, ax, ay, 150 + 40 * t / 5, t, "angry", fire=0.6)
    chip(d, "IMPACTO INMINENTE", 300 if False else 1050, bg=RED, size=60, appear=t / 0.3) if False else None
    if t > 2.5:
        sc = pop((t - 2.5) / 0.3)
        d.rounded_rectangle([90, 830 - 70 * sc, 90 + 470 * sc, 830 + 70 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=6)
        d.text((90 + 235 * sc, 830), "PERFORADORES", font=F(max(8, 46 * sc)), fill=BLK, anchor="mm")
        xmark(d, 90 + 235 * sc, 830, 0.9 * sc)
    chip(d, "¡ALERTA!", 230, bg=RED, size=64, appear=t / 0.3)
    return img, 1.0, 1.0, (t < 0.4)

def s_size(t):
    lt = t - 5.0
    img = grad((140, 200, 240), (220, 235, 245)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, H], fill=(110, 170, 90))
    bus(d, 60, 1250, 1.0)
    building(d, 400, 1250, 220, 520, 6)
    d.polygon([(660, 1250), (870, 700), (1080, 1250)], fill=(120, 110, 130), outline=BLK)
    d.polygon([(820, 830), (870, 700), (920, 830)], fill=WHITE)
    for lab, x in [("BUS", 190), ("6 PISOS", 510), ("MONTAÑA", 870)]:
        d.text((x, 1300), lab, font=F(44), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)
    if lt > 1.0:
        a = ease((lt - 1.0) / 1.5)
        asteroid(d, lerp(900, 510, a), lerp(200, 560, a), 95, t, "angry", fire=0.4)
    if lt > 3.0:
        k = pop((lt - 3.0) / 0.4)
        for i in range(12):
            ang = i / 12 * 2 * math.pi
            d.line([(510, 560), (510 + math.cos(ang) * 240 * k, 560 + math.sin(ang) * 240 * k)], fill=(255, 220, 80), width=14)
        d.ellipse([510 - 130 * k, 560 - 130 * k, 510 + 130 * k, 560 + 130 * k], fill=(255, 245, 190))
        bigtext(d, "¡BOOM EN EL CIELO!", 540, 380, int(64 * k) + 1, fill=RED, stroke=WHITE, sw=8)
    chip(d, "TODO DEPENDE DEL TAMAÑO", 230, bg=(30, 30, 40), fg=YEL, size=54, appear=lt / 0.3)
    return img, 1.0, 1.0

def city(snow=True, flash=0.0):
    img = grad(lc((150, 170, 200), (255, 255, 240), flash), lc((210, 220, 235), (255, 255, 240), flash)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(235, 240, 250) if snow else (120, 120, 120))
    for i, (x, w, h, f) in enumerate([(20, 200, 520, 6), (240, 180, 650, 8), (440, 220, 460, 5), (680, 170, 600, 7), (870, 200, 500, 6)]):
        building(d, x, 1200, w, h, f, col=lc((170, 160, 150), (255, 255, 240), flash * 0.7), lit=False)
    return img

def s_chely(t):
    lt = t - 10.0
    flash = 0.0
    if 4.0 < lt < 6.0: flash = 1 - abs(lt - 4.6) / 1.4 if lt > 4.6 else (lt - 4.0) / 0.6
    img = city(flash=cl(flash)); d = ImageDraw.Draw(img)
    if lt < 4.6:
        a = ease(lt / 4.6)
        x, y = lerp(1100, 560, a), lerp(250, 600, a)
        for k in range(30):
            tx, ty = x + k * 18, y - k * 11
            r = 30 - k * 0.8
            d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=lc((255, 250, 200), (250, 140, 40), k / 30))
        asteroid(d, x, y, 40, t, None)
    chip(d, "RUSIA · 2013 · ~20 m", 230, bg=(30, 30, 40), fg=YEL, size=56, appear=lt / 0.3)
    if lt > 4.0: bigtext(d, "DESTELLO", 540, 450, int(80 * pop((lt - 4.0) / 0.3)), fill=YEL, stroke=BLK, sw=8)
    if lt > 5.6:
        k = (lt - 5.6) * 1.4
        for j in range(3):
            r = (k - j * 0.25) * 900
            if r > 0: d.ellipse([560 - r, 600 - r, 560 + r, 600 + r], outline=(255, 255, 255), width=14)
        bigtext(d, "ONDA DE CHOQUE", 540, 900, int(66 * pop((lt - 5.6) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0, (5.6 < lt < 6.4)

def s_glass(t):
    lt = t - 17.0
    img = grad((200, 185, 165), (170, 150, 130)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, W, H], fill=(140, 100, 70))
    broken = cl((lt - 4.1) / 0.4)
    window_frame(d, 380, 330, 520, 640, broken)
    guy(d, 640, FEET + 40, 0.85, mood="scared" if broken > 0 else "neutral", look=0, t=t)
    if broken == 0:
        d.ellipse([540, 520, 740, 720], fill=(255, 255, 220))
    if lt < 4.0:
        sc = pop(lt / 0.35)
        d.rounded_rectangle([100, 150 + 160 - 70 * sc, 980, 310 + 70 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=6)
        d.text((540, 310), "+1,600 PERSONAS", font=F(max(8, 80 * sc)), fill=RED, anchor="mm")
    else:
        bigtext(d, "¡NO TE ASOMES!", 540, 250, int(80 * pop((lt - 4.0) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0, (4.1 < lt < 4.5)

def s_dino(t):
    lt = t - 24.0
    sky = cl(lt / 3.0)
    img = grad(lc((150, 200, 240), (240, 120, 60), sky), lc((230, 220, 190), (250, 180, 90), sky)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, H], fill=(150, 130, 80))
    for k in range(3):
        px = 80 + k * 380
        d.line([(px, 1250), (px + 30, 950)], fill=(110, 80, 50), width=18)
        for j in range(5):
            a = -math.pi / 2 + (j - 2) * 0.55
            d.line([(px + 30, 950), (px + 30 + math.cos(a) * 140, 950 + math.sin(a) * 70 + 40)], fill=(60, 140, 60), width=16)
    asteroid(d, lerp(700, 620, ease(lt / 7)), lerp(200, 380, ease(lt / 7)), 230 + 60 * ease(lt / 7), t, "angry", fire=0.5)
    dino(d, 420, 1330, 1.25, t, sign="F" if lt > 3.5 else None)
    chip(d, "10 km · HACE 66 MILLONES DE AÑOS", 230, bg=(30, 30, 40), fg=YEL, size=48, appear=lt / 0.3)
    return img, 1.0, 1.0 + 0.04 * ease(lt / 7)

def s_tips(t):
    lt = t - 31.0
    img = grad((200, 185, 165), (170, 150, 130)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, W, H], fill=(140, 100, 70))
    window_frame(d, 60, 360, 300, 420)
    d.ellipse([140, 470, 280, 610], fill=(255, 255, 220))
    gx = lerp(320, 700, ease((lt - 0.6) / 1.2))
    if lt < 2.2:
        guy(d, gx, FEET + 40, 0.75, mood="scared", look=1, t=t * 2)
    else:
        table(d, 700, FEET + 40, 1.0)
        crouch_guy(d, 700, FEET + 30, 0.8, t)
    if lt < 4.0:
        chip(d, "ALÉJATE DE LAS VENTANAS", 230, bg=RED, size=54, appear=lt / 0.3)
        if lt > 2.2: chip(d, "AGÁCHATE Y CÚBRETE", 330, bg=(30, 110, 210), size=54, appear=(lt - 2.2) / 0.3)
    else:
        lt2 = lt - 4.0
        d.rounded_rectangle([90, 180, 990, 420], 30, fill=WHITE, outline=BLK, width=6)
        d.text((270, 260), "1. LUZ", font=F(64), fill=(220, 170, 20), anchor="mm")
        if lt2 > 0.8:
            d.text((540, 260), "→", font=F(80), fill=BLK, anchor="mm")
            d.text((780, 260), "2. ONDA", font=F(64), fill=RED, anchor="mm")
        d.text((540, 360), "TIENES SEGUNDOS: ÚSALOS", font=F(44), fill=(60, 60, 60), anchor="mm")
    return img, 1.0, 1.0

def s_nasa(t):
    lt = t - 38.0
    img = SPACE.copy(); d = ImageDraw.Draw(img)
    cx, cy = 540, 820
    for r in (150, 280, 410):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 200, 120), width=4)
    a = t * 1.5
    d.line([(cx, cy), (cx + math.cos(a) * 420, cy + math.sin(a) * 420)], fill=(100, 255, 150), width=8)
    earth(d, cx, cy, 70)
    rng = random.Random(4)
    for i in range(19):
        aa = rng.uniform(0, 2 * math.pi); rr = rng.uniform(170, 400)
        x, y = cx + math.cos(aa) * rr, cy + math.sin(aa) * rr
        found = i < int(cl((lt - 0.5) / 2.5) * 18)
        asteroid(d, x, y, 22, t, None)
        if found: d.ellipse([x - 34, y - 34, x + 34, y + 34], outline=(100, 255, 150), width=5)
    if lt > 1.0:
        bigtext(d, "~95%", 540, 360, int(130 * pop((lt - 1.0) / 0.35)), fill=(100, 255, 150), stroke=BLK, sw=10)
    chip(d, "RADAR PLANETARIO", 230, bg=(30, 140, 80), size=56, appear=lt / 0.3)
    if lt > 3.0: chip(d, "ASTEROIDES DE +1 km", 1300, bg=(30, 30, 40), fg=YEL, size=50, appear=(lt - 3.0) / 0.3)
    return img, 1.0, 1.0

def s_film(t):
    lt = t - 44.0
    img = grad((60, 30, 50), (240, 120, 60)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, H], fill=(60, 60, 70))
    asteroid(d, 780, 360, 170, t, "angry", fire=0.6)
    if lt < 2.5:
        chip(d, "SIGUE LAS ALERTAS OFICIALES", 1000, bg=(30, 110, 210), size=50, appear=lt / 0.3)
        d.rounded_rectangle([140, 600, 460, 820], 20, fill=(240, 240, 240), outline=BLK, width=6)
        d.text((300, 680), "ALERTA", font=F(56), fill=RED, anchor="mm")
        d.text((300, 760), "EVACUAR", font=F(48), fill=BLK, anchor="mm")
        guy(d, 300, FEET + 120, 0.7, mood="scared", look=1, t=t)
    else:
        guy(d, 380, FEET + 120, 0.8, mood="neutral", arms="up", look=1, t=t)
        phone(d, 380, 760, 0.55, glow=1.0)
        if int(t * 2) % 2: d.ellipse([340, 640, 370, 670], fill=RED)
        xmark(d, 380, 820, 1.4 * pop((lt - 3.3) / 0.3)) if lt > 3.3 else None
        if lt > 3.3: chip(d, "¡EVACÚA, NO GRABES!", 300, bg=RED, size=58, appear=(lt - 3.3) / 0.3)
    return img, 1.0, 1.0

def s_dart(t):
    lt = t - 50.0
    img = SPACE.copy(); d = ImageDraw.Draw(img)
    cx, cy = 540, 820
    shrink = ease((lt - 3.0) / 2.0)
    R = 330 - 50 * shrink
    d.ellipse([cx - R, cy - R * 0.55, cx + R, cy + R * 0.55], outline=(120, 140, 220), width=4)
    asteroid(d, cx, cy, 130, t, "neutral")
    period = 2.2 - 0.2 * shrink
    a = lt * 2 * math.pi / period
    mx, my = cx + math.cos(a) * R, cy + math.sin(a) * R * 0.55
    if lt < 2.2:
        sx = lerp(-150, 540 + 330, ease(lt / 2.2)); sy = lerp(300, 820, ease(lt / 2.2))
        mx, my = 540 + 330, 820
        asteroid(d, mx, my, 50, t, "neutral")
        ship(d, sx, sy, 0.8)
    else:
        asteroid(d, mx, my, 50, t, "angry" if lt > 3 else "neutral")
        if lt < 3.0:
            k = pop((lt - 2.2) / 0.3)
            d.ellipse([870 - 110 * k, 820 - 110 * k, 870 + 110 * k, 820 + 110 * k], fill=(255, 230, 120))
            bigtext(d, "¡PUM!", 870, 620, int(80 * k) + 1, fill=RED, stroke=WHITE, sw=8)
    chip(d, "NASA · 2022 · A PROPÓSITO", 230, bg=(30, 30, 40), fg=YEL, size=52, appear=lt / 0.3)
    if lt > 5.0:
        sc = pop((lt - 5.0) / 0.35)
        d.rounded_rectangle([540 - 270 * sc, 1300 - 80 * sc, 540 + 270 * sc, 1300 + 80 * sc], int(24 * sc), fill=(100, 255, 150), outline=BLK, width=6)
        d.text((540, 1300), "-32 MIN", font=F(max(8, 100 * sc)), fill=BLK, anchor="mm")
    return img, 1.0, 1.0, (2.2 < lt < 2.6)

def s_end(t):
    lt = t - 58.0
    img = grad((120, 180, 240), (230, 240, 250)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, H], fill=(110, 170, 90))
    off = 60 * ease(lt / 3)
    asteroid(d, 690 + off, 1030, 210, t, "neutral")
    guy(d, 330 + off, FEET + 120, 0.8, mood="relief", arms="push", look=1, t=t)
    for k in range(3):
        d.line([(170 + off - k * 40, 900 + k * 60), (90 + off - k * 40, 900 + k * 60)], fill=WHITE, width=8)
    if lt < 3.0:
        chip(d, "YA SABEMOS EMPUJAR ROCAS", 230, bg=(30, 140, 80), size=52, appear=lt / 0.3)
    if lt > 3.0:
        sc = pop((lt - 3.0) / 0.35)
        d.rounded_rectangle([540 - 330 * sc, 330 - 80 * sc, 540 + 330 * sc, 330 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
        d.text((540, 330), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
    return img, 1.0, 1.0

SCENES = [(0, 5, s_hook), (5, 10, s_size), (10, 17, s_chely), (17, 24, s_glass), (24, 31, s_dino), (31, 38, s_tips),
          (38, 44, s_nasa), (44, 50, s_film), (50, 58, s_dart), (58, 80, s_end)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img, b, z = r[0], r[1], r[2]
    shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce: rich_caption(d, txt, appear=(t - cs) / 0.25)
    if z > 1.001:
        cw, ch = W / z, H / z
        img = img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = b * (0.3 + 0.7 * fi)
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    if shake:
        k = int(t * FPS)
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1); arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r13.png"); sys.exit()
    from warp13 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(67.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
