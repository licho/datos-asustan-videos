import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN, FEET)
from reel2 import pizza, phone
from reel5 import mite

FPS = 30
GREEN = (60, 170, 80)

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def room(mess=0.0, dark=0.0, seed=1):
    wall = lc((150, 190, 215), (120, 130, 110), mess)
    img = grad(wall, dk(wall, 0.8)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, W, H], fill=lc((185, 140, 100), (120, 95, 70), mess))
    for x in range(0, W, 120): d.line([(x, 1150), (x - 60, H)], fill=dk(lc((185, 140, 100), (120, 95, 70), mess), 0.85), width=3)
    d.rectangle([660, 300, 960, 640], fill=(140, 200, 240), outline=(245, 245, 240), width=14)
    d.line([(810, 300), (810, 640)], fill=(245, 245, 240), width=10)
    d.rectangle([80, 330, 330, 520], fill=(250, 240, 220), outline=(60, 60, 60), width=8)
    d.polygon([(110, 500), (190, 400), (240, 460), (280, 420), (310, 500)], fill=(90, 160, 90))
    rng = random.Random(seed)
    if mess > 0.2:  # stains on the wall
        for i in range(int(mess * 8)):
            x, y = rng.uniform(40, 1040), rng.uniform(700, 1100)
            r = rng.uniform(20, 60) * mess
            d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=dk(wall, 0.75))
    if mess > 0.05:  # clothes piles
        for i in range(int(mess * 10)):
            x, y = rng.uniform(40, 1040), rng.uniform(1180, 1420)
            c = rng.choice([(200, 60, 60), (60, 90, 180), (230, 200, 70), (80, 80, 80), (240, 240, 240)])
            d.pieslice([x - 80, y - 50, x + 80, y + 40], 180, 360, fill=c, outline=BLK, width=4)
        for i in range(int(mess * 40)):
            x, y = rng.uniform(0, W), rng.uniform(1160, 1450)
            d.ellipse([x - 6, y - 4, x + 6, y + 4], fill=(210, 170, 110))
    if dark > 0:
        arr = np.asarray(img).astype(np.float32) * (1 - 0.8 * dark)
        img = Image.fromarray(arr.astype(np.uint8))
    return img

ROOMS = {k: room(k / 10, seed=k) for k in range(11)}

def bed(d, x, y, s=1.0, dirty=0.0):
    S = lambda v: v * s
    d.rectangle([x - S(330), y - S(120), x + S(330), y], fill=(110, 75, 50), outline=BLK, width=6)
    d.rectangle([x - S(330), y - S(330), x - S(290), y], fill=(110, 75, 50), outline=BLK, width=6)
    sheet = lc((235, 240, 250), (205, 190, 150), dirty)
    d.rounded_rectangle([x - S(300), y - S(200), x + S(320), y - S(100)], int(S(30)), fill=sheet, outline=BLK, width=5)
    d.rounded_rectangle([x - S(290), y - S(250), x - S(130), y - S(170)], int(S(30)), fill=lc((250, 250, 255), (215, 205, 165), dirty), outline=BLK, width=5)
    rng = random.Random(4)
    for i in range(int(dirty * 12)):
        px, py = x + rng.uniform(-250, 280) * s, y - rng.uniform(110, 190) * s
        r = rng.uniform(10, 26) * s
        d.ellipse([px - r, py - r * 0.6, px + r, py + r * 0.6], fill=dk(sheet, 0.82))

def counter(d, label, appear=1.0):
    chip(d, label, 230, bg=(30, 30, 40), fg=YEL, size=64, appear=appear)

def fly(d, x, y, s, t, phase=0):
    S = lambda v: v * s
    flap = abs(math.sin(t * 40 + phase))
    for sx in (-1, 1):
        d.ellipse([x + sx * S(6) - S(18), y - S(22) - S(10) * flap, x + sx * S(6) + S(18), y - S(2)], fill=(220, 235, 245), outline=(120, 120, 140), width=2)
    d.ellipse([x - S(14), y - S(10), x + S(14), y + S(14)], fill=(70, 50, 40), outline=BLK, width=2)
    for sx in (-1, 1): d.ellipse([x + sx * S(8) - S(6), y - S(12), x + sx * S(8) + S(6), y], fill=(220, 40, 40))

def roach(d, x, y, s, t, ang=0.0, phase=0, eyes=True):
    S = lambda v: v * s
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda a, b: (x + a * ca - b * sa, y + a * sa + b * ca)
    for k in (-1, 0, 1):
        for sx in (-1, 1):
            w = math.sin(t * 25 + phase + k) * S(10)
            d.line([P(S(k * 30), sx * S(20)), P(S(k * 30 + w), sx * S(60))], fill=(60, 35, 20), width=max(2, int(S(7))))
    d.polygon([P(-S(70), -S(32)), P(S(55), -S(30)), P(S(75), 0), P(S(55), S(30)), P(-S(70), S(32)), P(-S(85), 0)], fill=(130, 70, 35), outline=BLK)
    d.line([P(-S(70), 0), P(S(55), 0)], fill=(90, 45, 20), width=max(2, int(S(4))))
    for sx in (-1, 1):
        d.line([P(S(70), sx * S(10)), P(S(150), sx * S(45) + math.sin(t * 6 + phase) * S(10))], fill=(60, 35, 20), width=max(2, int(S(4))))
    if eyes:
        for sx in (-1, 1):
            ex, ey = P(S(50), sx * S(14))
            d.ellipse([ex - S(10), ey - S(10), ex + S(10), ey + S(10)], fill=WHITE, outline=BLK, width=2)
            d.ellipse([ex - S(4), ey - S(4), ex + S(4), ey + S(4)], fill=BLK)

def banana(d, x, y, s, rot=0.0):
    S = lambda v: v * s
    c = lc((240, 210, 60), (90, 60, 30), rot)
    d.chord([x - S(140), y - S(120), x + S(140), y + S(60)], 20, 160, fill=c, outline=BLK, width=5)
    rng = random.Random(2)
    for i in range(int(rot * 10)):
        px, py = x + rng.uniform(-90, 90) * s, y + rng.uniform(10, 50) * s
        d.ellipse([px - S(8), py - S(6), px + S(8), py + S(6)], fill=(50, 35, 20))

def fungus(d, x, y, r, t, col, phase=0.0):
    wob = math.sin(t * 4 + phase) * r * 0.05
    for k in range(18):
        a = k / 18 * 2 * math.pi
        d.line([(x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9),
                (x + math.cos(a) * (r * 1.3 + wob), y + math.sin(a) * (r * 1.3 + wob))], fill=dk(col, 0.7), width=max(2, int(r * 0.08)))
        d.ellipse([x + math.cos(a) * r * 1.35 - r * 0.08, y + math.sin(a) * r * 1.35 - r * 0.08,
                   x + math.cos(a) * r * 1.35 + r * 0.08, y + math.sin(a) * r * 1.35 + r * 0.08], fill=col)
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=BLK, width=max(2, int(r * 0.07)))
    for sx in (-1, 1):
        cx, cy = x + sx * r * 0.32, y - r * 0.1
        d.ellipse([cx - r * 0.18, cy - r * 0.2, cx + r * 0.18, cy + r * 0.2], fill=WHITE, outline=BLK, width=2)
        d.ellipse([cx - r * 0.07, cy - r * 0.05, cx + r * 0.07, cy + r * 0.11], fill=BLK)
    d.arc([x - r * 0.35, y + r * 0.05, x + r * 0.35, y + r * 0.5], 10, 170, fill=BLK, width=max(2, int(r * 0.07)))

def pillow(d, cx, cy, s):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(420), cy - S(220), cx + S(420), cy + S(220)], int(S(120)), fill=(225, 220, 195), outline=BLK, width=8)
    for k in range(-2, 3):
        d.arc([cx - S(380), cy - S(180) + k * S(40), cx + S(380), cy + S(180) + k * S(40)], 200, 340, fill=(200, 195, 170), width=4)
    rng = random.Random(11)
    for i in range(12):
        px, py = cx + rng.uniform(-330, 330) * s, cy + rng.uniform(-150, 150) * s
        r = rng.uniform(15, 40) * s
        d.ellipse([px - r, py - r * 0.6, px + r, py + r * 0.6], fill=(205, 195, 150))

def pie(d, cx, cy, r, frac, appear):
    r = r * appear
    if r < 4: return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 225, 210), outline=BLK, width=6)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=(140, 95, 55), outline=BLK, width=6)
    d.text((cx + r * 0.38, cy - r * 0.15), "40%", font=F(max(8, r * 0.38)), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)

def shoe(d, x, y, s):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(110), y - S(70), x + S(60), y], int(S(30)), fill=(60, 60, 70), outline=BLK, width=5)
    d.rounded_rectangle([x - S(20), y - S(50), x + S(130), y], int(S(25)), fill=(60, 60, 70), outline=BLK, width=5)
    d.rectangle([x - S(115), y - S(10), x + S(135), y + S(8)], fill=(240, 240, 240), outline=BLK, width=4)
    for k in range(8):
        px = x - S(100) + k * S(30)
        d.ellipse([px - S(14), y + S(4), px + S(14), y + S(24)], fill=(110, 75, 40))

CAPS = [
    (0.0, 3.0, "¿Qué pasa si *no limpias tu cuarto* en un año?"),
    (3.0, 6.0, "Spoiler: tendrás *inquilinos*… y *ninguno paga renta*"),
    (6.0, 12.0, "*Día 3:* la pizza que \"ibas a bajar al rato\"… *moho en días*"),
    (12.0, 16.0, "*Semana 2:* llegan las *moscas de la fruta*"),
    (16.0, 20.0, "Hasta *500 huevos* por hembra… adultas en *8 a 10 días*"),
    (20.0, 27.0, "*Mes 1:* sueltas *500 millones* de células de piel al día… *buffet para ácaros*"),
    (27.0, 33.0, "*Mes 3:* cerca del *40% del polvo* viene de afuera"),
    (33.0, 37.0, "*Mes 6:* visitas que *corren al prender la luz*"),
    (37.0, 39.0, "*Y no vienen solas…*"),
    (39.0, 47.0, "En un estudio, almohadas usadas tenían *de 4 a 16 especies de hongos*. *Cada una.*"),
    (47.0, 53.0, "Lava sábanas *cada semana*, saca platos y basura *el mismo día*"),
    (53.0, 57.0, "Ventila y dedícale *15 minutos diarios*"),
    (57.0, 61.0, "Menos de lo que pasas *viendo videos como este*"),
    (61.0, 66.0, "Si tu cuarto ya es así… *es un ecosistema*"),
    (66.0, 72.0, "*Sígueme* y etiqueta a quien *necesita ver esto*"),
]

def s_hook(t):
    img = ROOMS[0].copy(); d = ImageDraw.Draw(img)
    bed(d, 600, 1300, 1.0, 0)
    guy(d, 330, FEET + 120, 0.85, mood="neutral", look=1, t=t)
    counter(d, "DÍA 1", appear=t / 0.3)
    if t > 3.0:
        sc = pop((t - 3.0) / 0.35)
        d.rounded_rectangle([600 - 250 * sc, 760 - 70 * sc, 600 + 250 * sc, 760 + 70 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=6)
        d.text((600, 760), "SE RENTA", font=F(max(8, 70 * sc)), fill=RED, anchor="mm")
        fly(d, 860, 900, 1.6, t); roach(d, 880, 1150, 0.7, t, ang=math.pi)
        mite(d, 980, 1080, 0.6, t)
    return img, 1.0, 1.0

def s_pizza(t):
    lt = t - 6.0
    img = ROOMS[2].copy(); d = ImageDraw.Draw(img)
    counter(d, "DÍA 3", appear=lt / 0.3)
    d.ellipse([260, 980, 820, 1180], fill=(240, 240, 235), outline=BLK, width=6)
    pizza(d, 540, 1040, 1.3)
    mold = cl((lt - 2.0) / 3.0)
    rng = random.Random(5)
    for i in range(int(mold * 14)):
        px, py = 540 + rng.uniform(-120, 120), 1000 + rng.uniform(-90, 80)
        r = rng.uniform(16, 34)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(110, 170, 90), outline=(70, 120, 60), width=3)
    for k in range(3):
        ph = (lt * 0.8 + k * 0.33) % 1
        x0 = 400 + k * 140; y0 = 900 - ph * 250
        pts = [(x0 + math.sin(ph * 10 + j) * 25, y0 - j * 25) for j in range(6)]
        d.line(pts, fill=(120, 190, 80), width=10, joint="curve")
    if lt > 3.0: chip(d, "MOHO: EN CUESTIÓN DE DÍAS", 420, bg=GREEN, size=52, appear=(lt - 3.0) / 0.3)
    return img, 1.0, 1.0 + 0.04 * ease(lt / 6)

def s_flies(t):
    lt = t - 12.0
    img = ROOMS[3].copy(); d = ImageDraw.Draw(img)
    counter(d, "SEMANA 2", appear=lt / 0.3)
    d.rectangle([300, 1100, 800, 1140], fill=(150, 110, 70), outline=BLK, width=4)
    banana(d, 540, 1060, 1.3, rot=0.8)
    n = 3 + int(cl(lt / 6) * 28)
    rng = random.Random(8)
    for i in range(n):
        a = t * rng.uniform(1, 2.5) + i
        fx = 540 + math.cos(a) * rng.uniform(80, 420); fy = 800 + math.sin(a * 1.3) * rng.uniform(60, 300)
        fly(d, fx, fy, rng.uniform(0.8, 1.4), t, i)
    if lt > 4.0:
        sc = pop((lt - 4.0) / 0.3)
        d.rounded_rectangle([540 - 300 * sc, 420 - 60 * sc, 540 + 300 * sc, 420 + 60 * sc], int(20 * sc), fill=YEL, outline=BLK, width=6)
        d.text((540, 420), "500 HUEVOS", font=F(max(8, 70 * sc)), fill=BLK, anchor="mm")
    if lt > 6.0:
        chip(d, "GENERACIÓN 2 🡒 EN TU CUARTO", 560, bg=RED, size=46, appear=(lt - 6.0) / 0.3)
    return img, 1.0, 1.0

def s_mites(t):
    lt = t - 20.0
    img = ROOMS[5].copy(); d = ImageDraw.Draw(img)
    counter(d, "MES 1", appear=lt / 0.3)
    bed(d, 540, 1350, 1.2, dirty=0.7)
    rng = random.Random(3)
    for i in range(40):
        px = rng.uniform(150, 950); py = (rng.uniform(500, 1100) + lt * 120) % 700 + 450
        d.ellipse([px - 7, py - 5, px + 7, py + 5], fill=(245, 225, 200), outline=(200, 170, 140))
    if lt > 1.5:
        sc = pop((lt - 1.5) / 0.3)
        d.rounded_rectangle([540 - 330 * sc, 380 - 60 * sc, 540 + 330 * sc, 380 + 60 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=6)
        d.text((540, 380), "500 MILLONES / DÍA", font=F(max(8, 60 * sc)), fill=RED, anchor="mm")
    if lt > 3.8:
        sc = pop((lt - 3.8) / 0.3)
        d.rounded_rectangle([540 - 260 * sc, 560 - 55 * sc, 540 + 260 * sc, 560 + 55 * sc], int(16 * sc), fill=(200, 40, 40), outline=BLK, width=6)
        d.text((540, 560), "BUFFET LIBRE", font=F(max(8, 62 * sc)), fill=WHITE, anchor="mm")
        for i, mx in enumerate((300, 540, 780)):
            mite(d, mx, 1130 - 20 * math.sin(t * 6 + i), 0.9, t, phase=i)
            d.polygon([(mx - 30, 1080), (mx + 30, 1080), (mx, 1120)], fill=WHITE, outline=BLK)
    return img, 1.0, 1.0

def s_dust(t):
    lt = t - 27.0
    img = ROOMS[7].copy(); d = ImageDraw.Draw(img)
    counter(d, "MES 3", appear=lt / 0.3)
    shoe(d, 300, 1300, 1.3)
    rng = random.Random(6)
    for i in range(60):
        px = (rng.uniform(0, W) + lt * rng.uniform(-30, 30)) % W
        py = rng.uniform(450, 1150) + math.sin(t + i) * 20
        r = rng.uniform(3, 8)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(200, 190, 170))
    pie(d, 720, 760, 230, 0.4, pop((lt - 1.0) / 0.4) if lt > 1.0 else 0)
    if lt > 1.0: d.text((720, 1030), "VIENE DE AFUERA", font=F(54), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=BLK)
    if lt > 3.5:
        g = ease((lt - 3.5) / 1.0)
        for k, fx in enumerate((620, 760, 900)):
            h = 150 * g
            d.line([(fx, 1300), (fx, 1300 - h)], fill=(60, 150, 60), width=10)
            d.ellipse([fx - 30 * g, 1300 - h - 30 * g, fx + 30 * g, 1300 - h + 30 * g], fill=[(240, 90, 120), (250, 210, 60), (150, 110, 230)][k], outline=BLK, width=3)
        chip(d, "PARTE DEL JARDÍN", 420, bg=GREEN, size=56, appear=(lt - 3.5) / 0.3)
    return img, 1.0, 1.0

def s_roach(t):
    lt = t - 33.0
    on = lt > 1.0 and lt < 4.0
    img = (ROOMS[9] if on else Image.fromarray((np.asarray(ROOMS[9]).astype(np.float32) * 0.18).astype(np.uint8))).copy()
    d = ImageDraw.Draw(img)
    counter(d, "MES 6", appear=lt / 0.3)
    d.rounded_rectangle([90, 760, 170, 880], 10, fill=(240, 240, 230), outline=BLK, width=4)
    d.rectangle([115, 790 if on else 820, 145, 830 if on else 860], fill=(200, 200, 190), outline=BLK, width=3)
    if on:
        rng = random.Random(9)
        for i in range(9):
            sx0, sy0 = rng.uniform(200, 900), rng.uniform(1100, 1450)
            ang = rng.uniform(0, 2 * math.pi)
            dist = (lt - 1.0) * 900
            roach(d, sx0 + math.cos(ang) * dist, sy0 + math.sin(ang) * dist * 0.4, 0.75, t * 2, ang, i)
        chip(d, "¡CLICK!", 420, bg=YEL, fg=BLK, size=60, appear=(lt - 1.0) / 0.2)
    if lt >= 4.0:
        rng = random.Random(12)
        for i in range(int(cl((lt - 4.0) / 1.0) * 26)):
            ex, ey = rng.uniform(60, 1020), rng.uniform(500, 1450)
            blink = (int(t * 3 + i) % 7) != 0
            for sx in (-1, 1):
                if blink:
                    d.ellipse([ex + sx * 18 - 12, ey - 12, ex + sx * 18 + 12, ey + 12], fill=(250, 250, 220))
                    d.ellipse([ex + sx * 18 - 4, ey - 4, ex + sx * 18 + 4, ey + 4], fill=BLK)
    return img, 1.0, 1.0, (1.0 < lt < 1.3)

def s_pillow(t):
    lt = t - 39.0
    img = grad((40, 30, 60), (15, 10, 25)); d = ImageDraw.Draw(img)
    pillow(d, 540, 860, 1.0)
    cols = [(120, 190, 90), (90, 150, 220), (230, 190, 60), (200, 110, 200), (240, 130, 90), (130, 210, 200), (180, 180, 80), (220, 90, 110)]
    n = int(cl((lt - 1.0) / 4.5) * 16)
    rng = random.Random(14)
    for i in range(n):
        fx, fy = 540 + rng.uniform(-330, 330), 860 + rng.uniform(-150, 150)
        fungus(d, fx, fy, rng.uniform(28, 46) * pop((lt - 1.0 - i * 0.28) / 0.3), t, cols[i % len(cols)], i)
    if lt > 1.0:
        d.text((540, 1150), "DE 4 A 16 ESPECIES", font=F(76), fill=YEL, anchor="mm", stroke_width=8, stroke_fill=BLK)
    chip(d, "ESTUDIO REAL · U. DE MANCHESTER", 330, bg=(40, 140, 80), size=48, appear=lt / 0.4)
    if lt > 6.2:
        bigtext(d, "CADA UNA", 540, 560, int(84 * pop((lt - 6.2) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0 + 0.05 * ease(lt / 8)

TIPS = [(47.0, "Lava sábanas cada semana"), (49.5, "Platos y basura: mismo día"), (53.0, "Ventila tu cuarto"), (54.5, "15 minutos diarios")]

def s_tips(t):
    lt = t - 47.0
    img = ROOMS[0].copy(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 330, 990, 1080], 40, fill=(250, 248, 235), outline=BLK, width=8)
    d.text((540, 410), "PLAN DE RESCATE", font=F(70), fill=(40, 40, 40), anchor="mm")
    for i, (st, txt) in enumerate(TIPS):
        if t < st: continue
        a = cl((t - st) / 0.25)
        y = 540 + i * 135
        d.rounded_rectangle([150, y - 45, 240, y + 45], 18, outline=BLK, width=6, fill=WHITE)
        if t > st + 0.3: check(d, 195, y, 0.8)
        d.text((275, y), txt, font=F(int(44 * a) + 1), fill=(30, 30, 30), anchor="lm")
    if t > 57.0:
        lt2 = t - 57.0
        sc = pop(lt2 / 0.3)
        d.rounded_rectangle([140, 1180 - 60 * sc, 940, 1180 + 60 * sc], int(20 * sc), fill=(30, 30, 40), outline=YEL, width=6)
        d.text((540, 1180), "15 MIN  <  TU SCROLL", font=F(max(8, 64 * sc)), fill=YEL, anchor="mm")
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 61.0
    img = ROOMS[10].copy(); d = ImageDraw.Draw(img)
    rng = random.Random(21)
    for i in range(14):
        x = rng.uniform(0, W); h = rng.uniform(180, 420) * ease(lt / 1.2)
        d.line([(x, 1450), (x + rng.uniform(-60, 60), 1450 - h)], fill=(50, 140, 60), width=16)
        d.ellipse([x - 50, 1450 - h - 40, x + 50, 1450 - h + 40], fill=(70, 170, 80), outline=(30, 90, 40), width=4)
    d.rectangle([520, 820, 540, 1150], fill=(110, 75, 40))
    d.rounded_rectangle([260, 650, 820, 850], 20, fill=(90, 60, 35), outline=BLK, width=6)
    d.text((540, 710), "RESERVA NATURAL", font=F(56), fill=(250, 240, 210), anchor="mm")
    d.text((540, 790), "TU CUARTO", font=F(48), fill=YEL, anchor="mm")
    guy(d, 230, FEET + 80, 0.75, mood="neutral", t=t, hoodie=(110, 120, 60))
    hx, hy = 230, FEET + 80 - 505 * 0.75
    d.ellipse([hx - 130, hy - 70, hx + 130, hy - 30], fill=(150, 110, 60), outline=BLK, width=4)
    d.rounded_rectangle([hx - 70, hy - 130, hx + 70, hy - 50], 20, fill=(150, 110, 60), outline=BLK, width=4)
    fly(d, 800, 1000, 1.5, t); roach(d, 850, 1350, 0.6, t, ang=math.pi); mite(d, 640, 1380, 0.6, t)
    if lt > 5.0:
        sc = pop((lt - 5.0) / 0.35)
        d.rounded_rectangle([540 - 330 * sc, 380 - 80 * sc, 540 + 330 * sc, 380 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
        d.text((540, 380), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
    return img, 1.0, 1.0

SCENES = [(0, 6, s_hook), (6, 12, s_pizza), (12, 20, s_flies), (20, 27, s_mites), (27, 33, s_dust), (33, 39, s_roach),
          (39, 47, s_pillow), (47, 61, s_tips), (61, 80, s_end)]

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
        sheet.save("sheet_r12.png"); sys.exit()
    from warp12 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(71.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
