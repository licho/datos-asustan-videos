import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)

FPS = 30
ASKIN = (150, 100, 65)
GROUND = 1250

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def make_jungle():
    img = grad((120, 190, 220), (200, 230, 210)); d = ImageDraw.Draw(img)
    rng = random.Random(2)
    for layer, col in enumerate([(60, 120, 70), (40, 100, 55), (30, 80, 45)]):
        for i in range(14):
            x = rng.uniform(-60, W + 60); y = 700 + layer * 120 + rng.uniform(-40, 40); r = rng.uniform(120, 220)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.rectangle([0, GROUND - 40, W, H], fill=(150, 115, 70))
    d.rectangle([0, GROUND - 40, W, GROUND - 20], fill=(90, 150, 60))
    return img
JUNGLE = make_jungle()

def make_site():
    img = grad((255, 200, 140), (250, 235, 200)); d = ImageDraw.Draw(img)
    d.ellipse([760, 220, 940, 400], fill=(255, 230, 120))
    d.rectangle([0, GROUND - 40, W, H], fill=(200, 175, 130))
    for i in range(6):
        d.rectangle([0, 1080 + i * 6, W, 1083 + i * 6], fill=(120, 190, 210))
    return img
SITE = make_site()
BG_HOUSE = grad((240, 235, 225), (205, 200, 190))
BG_DARK = grad((40, 25, 20), (10, 8, 6))

def alux(d, x, y, s=1.0, t=0.0, mood="grin", face=1, arm=None, shade=1.0):
    """Original cartoon alux: small Maya guardian in white clothes with embroidered border and red headband."""
    C = lambda c: dk(c, shade)
    hop = abs(math.sin(t * 5)) * 10 * s if mood == "laugh" else 0
    y = y - hop
    S = lambda v: v * s
    d.ellipse([x - S(80), y - S(12), x + S(80), y + S(12)], fill=(60, 50, 40))
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx * S(28) - S(18), y - S(90), x + sx * S(28) + S(18), y - S(10)], int(S(14)), fill=C(ASKIN))
        d.ellipse([x + sx * S(30) - S(28), y - S(26), x + sx * S(30) + S(28), y + S(4)], fill=C((120, 70, 40)))
    # tunic
    d.polygon([(x - S(70), y - S(80)), (x + S(70), y - S(80)), (x + S(55), y - S(230)), (x - S(55), y - S(230))], fill=C((245, 242, 232)), outline=BLK)
    for k in range(6):
        bx = x - S(66) + k * S(26)
        d.polygon([(bx, y - S(80)), (bx + S(13), y - S(104)), (bx + S(26), y - S(80))], fill=C([(220, 50, 70), (40, 160, 120), (240, 180, 40)][k % 3]))
    # arms
    for sx in (-1, 1):
        hx, hy = x + sx * S(95), y - S(140)
        if arm == "up" and sx == face: hx, hy = x + sx * S(110), y - S(290)
        if arm == "hold" and sx == face: hx, hy = x + sx * S(105), y - S(180)
        d.line([(x + sx * S(50), y - S(210)), (hx, hy)], fill=C(ASKIN), width=int(S(26)), joint="curve")
        d.ellipse([hx - S(17), hy - S(17), hx + S(17), hy + S(17)], fill=C(ASKIN))
    # head (big)
    hx, hy = x, y - S(330)
    for sx in (-1, 1):
        d.ellipse([hx + sx * S(118) - S(26), hy - S(10) - S(34), hx + sx * S(118) + S(26), hy - S(10) + S(34)], fill=C(ASKIN), outline=BLK)
    d.ellipse([hx - S(120), hy - S(115), hx + S(120), hy + S(115)], fill=C(ASKIN), outline=BLK, width=max(2, int(S(5))))
    d.chord([hx - S(122), hy - S(125), hx + S(122), hy + S(40)], 185, 355, fill=C((25, 20, 20)))
    d.rectangle([hx - S(118), hy - S(70), hx + S(118), hy - S(44)], fill=C((210, 40, 50)))
    d.polygon([(hx + S(60), hy - S(70)), (hx + S(95), hy - S(190)), (hx + S(85), hy - S(70))], fill=C((40, 170, 120)), outline=BLK)
    # eyes
    for sx in (-1, 1):
        ex, ey = hx + sx * S(48), hy + S(5)
        if mood == "wink" and sx == 1:
            d.arc([ex - S(28), ey - S(12), ex + S(28), ey + S(28)], 200, 340, fill=BLK, width=max(2, int(S(8))))
        elif mood == "angry":
            d.ellipse([ex - S(26), ey - S(20), ex + S(26), ey + S(26)], fill=WHITE, outline=BLK, width=max(2, int(S(4))))
            d.ellipse([ex - S(10), ey - S(4), ex + S(10), ey + S(16)], fill=BLK)
            d.line([(ex - S(32), ey - S(30) - sx * S(-12)), (ex + S(32), ey - S(30) + sx * S(-12))], fill=BLK, width=max(2, int(S(10))))
        else:
            d.ellipse([ex - S(28), ey - S(32), ex + S(28), ey + S(32)], fill=WHITE, outline=BLK, width=max(2, int(S(4))))
            d.ellipse([ex - S(12) + S(6) * face, ey - S(10), ex + S(12) + S(6) * face, ey + S(16)], fill=BLK)
            d.ellipse([ex - S(5) + S(6) * face, ey - S(6), ex + S(3) + S(6) * face, ey + S(2)], fill=WHITE)
    # mouth
    if mood == "angry":
        d.arc([hx - S(35), hy + S(55), hx + S(35), hy + S(95)], 200, 340, fill=BLK, width=max(2, int(S(8))))
    else:
        d.chord([hx - S(55), hy + S(30), hx + S(55), hy + S(95)], 0, 180, fill=(90, 20, 30), outline=BLK, width=max(2, int(S(4))))
        d.rectangle([hx - S(40), hy + S(60), hx + S(40), hy + S(70)], fill=WHITE)
    d.ellipse([hx - S(14), hy + S(22), hx + S(14), hy + S(42)], fill=C(dk(ASKIN, 0.8)))

def jiji(d, x, y, t, size=46):
    k = int(t * 4) % 2
    d.text((x, y - 8 * k), "jijiji", font=F(size), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)

def bridge(d, t, broken=0.0, fixed=False):
    deck_y = 800
    for i, px in enumerate([180, 540, 900]):
        bend = broken * math.sin(t * 6 + i) * 30
        d.polygon([(px - 40, GROUND - 40), (px + 40, GROUND - 40), (px + 30 + bend, deck_y), (px - 30 + bend, deck_y)], fill=(170, 165, 160), outline=BLK)
        if broken > 0:
            for k in range(3):
                rx = px - 20 + k * 20
                d.line([(rx, deck_y - 10), (rx + 30 * broken * (1 if k % 2 else -1), deck_y - 70)], fill=(140, 70, 40), width=6)
    sag = broken * 70
    pts = [(0, deck_y), (W / 2, deck_y + sag), (W, deck_y)]
    d.line(pts, fill=(130, 125, 120), width=46)
    d.line([(0, deck_y - 23), (W / 2, deck_y - 23 + sag), (W, deck_y - 23)], fill=(90, 90, 95), width=8)
    if fixed:
        for k in range(3):
            sx, sy = 260 + k * 280, 680 + (k % 2) * 30; L = 30 + 8 * math.sin(t * 6 + k)
            d.polygon([(sx, sy - L), (sx + L * 0.25, sy), (sx, sy + L), (sx - L * 0.25, sy)], fill=YEL)
            d.polygon([(sx - L, sy), (sx, sy - L * 0.25), (sx + L, sy), (sx, sy + L * 0.25)], fill=YEL)

def casita(d, x, y, s):
    S = lambda v: v * s
    for k in range(3):
        w = S(200 - k * 50); h = S(50)
        d.rectangle([x - w / 2, y - h * (k + 1), x + w / 2, y - h * k], fill=(215, 200, 170), outline=BLK, width=4)
    d.rectangle([x - S(30), y - S(110), x + S(30), y - S(50)], fill=(60, 40, 30))

def offering(d, x, y, s):
    S = lambda v: v * s
    d.ellipse([x - S(110), y - S(30), x + S(110), y + S(30)], fill=(230, 230, 225), outline=BLK, width=4)
    for (a, b, c) in [(-50, -30, (240, 200, 60)), (0, -40, (200, 80, 50)), (50, -28, (240, 220, 160))]:
        d.ellipse([x + S(a) - S(32), y + S(b) - S(26), x + S(a) + S(32), y + S(b) + S(26)], fill=c, outline=BLK, width=3)
    d.rounded_rectangle([x + S(140), y - S(110), x + S(210), y + S(20)], int(S(14)), fill=(190, 120, 60), outline=BLK, width=4)

def fridge(d, x, y, s, open_=0.0):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(140), y - S(560), x + S(140), y], int(S(20)), fill=(235, 238, 242), outline=BLK, width=6)
    d.line([(x - S(140), y - S(360)), (x + S(140), y - S(360))], fill=BLK, width=5)
    if open_ > 0:
        d.rectangle([x - S(130), y - S(350), x + S(130), y - S(10)], fill=(200, 230, 245))
        d.polygon([(x + S(140), y - S(360)), (x + S(140) + S(200) * open_, y - S(380)), (x + S(140) + S(200) * open_, y + S(20)), (x + S(140), y)], fill=(225, 228, 232), outline=BLK)
    d.rounded_rectangle([x + S(100), y - S(320), x + S(115), y - S(240)], int(S(6)), fill=(120, 120, 130))

def keys(d, x, y, s, ang=0.0):
    S = lambda v: v * s
    d.ellipse([x - S(26), y - S(26), x + S(26), y + S(26)], outline=(200, 170, 50), width=max(3, int(S(9))))
    ex, ey = x + math.cos(ang) * S(80), y + math.sin(ang) * S(80)
    d.line([(x + math.cos(ang) * S(24), y + math.sin(ang) * S(24)), (ex, ey)], fill=(200, 170, 50), width=max(3, int(S(14))))

def post(d, cx, cy, s, t):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(320), cy - S(170), cx + S(320), cy + S(170)], int(S(24)), fill=WHITE, outline=BLK, width=5)
    d.ellipse([cx - S(290), cy - S(140), cx - S(220), cy - S(70)], fill=(160, 170, 190))
    d.rounded_rectangle([cx - S(200), cy - S(125), cx - S(40), cy - S(95)], int(S(10)), fill=(200, 205, 215))
    d.text((cx - S(290), cy - S(20)), "jajaja los aluxes", font=F(S(42)), fill=(30, 30, 30), anchor="lm")
    d.text((cx - S(290), cy + S(40)), "no existen 🙄" if False else "no existen", font=F(S(42)), fill=(30, 30, 30), anchor="lm")
    d.line([(cx - S(300), cy + S(100)), (cx + S(300), cy + S(100))], fill=(220, 220, 225), width=3)

def thief(d, x, y, s, t):
    S = lambda v: v * s
    guy(d, x, y, s, mood="scared", t=t * 2, hoodie=(40, 40, 50))
    d.rectangle([x - S(100), y - S(560), x + S(100), y - S(520)], fill=(20, 20, 25))

def cloud_rain(d, x, y, s, t):
    S = lambda v: v * s
    for (a, b, r) in [(-90, 10, 80), (0, -20, 100), (90, 10, 80)]:
        d.ellipse([x + S(a) - S(r), y + S(b) - S(r), x + S(a) + S(r), y + S(b) + S(r)], fill=(150, 160, 175))
    for i in range(10):
        dx = x + S(-140 + i * 30); dy = y + S(60) + ((t * 400 + i * 47) % S(260))
        d.line([(dx, dy), (dx - 6, dy + S(30))], fill=(80, 150, 230), width=5)

def corn(d, x, y, s):
    S = lambda v: v * s
    d.line([(x, y), (x, y - S(260))], fill=(70, 140, 60), width=int(S(14)))
    for k, sx in enumerate((-1, 1, -1)):
        yy = y - S(80 + k * 60)
        d.polygon([(x, yy), (x + sx * S(110), yy - S(50)), (x + sx * S(30), yy - S(10))], fill=(90, 170, 70))
    d.ellipse([x + S(8), y - S(200), x + S(48), y - S(120)], fill=(240, 200, 60), outline=BLK)

def badge(d, n, sc):
    d.ellipse([140 - 80 * sc, 470 - 80 * sc, 140 + 80 * sc, 470 + 80 * sc], fill=YEL, outline=BLK, width=8)
    d.text((140, 470), str(n), font=F(max(8, 100 * sc)), fill=BLK, anchor="mm")

def bubble(d, x, y, text, size=40, sc=1.0):
    if sc < 0.05: return
    f = F(max(8, size * sc)); w = d.textlength(text, font=f)
    d.rounded_rectangle([x - w / 2 - 26 * sc, y - 46 * sc, x + w / 2 + 26 * sc, y + 46 * sc], int(30 * sc), fill=WHITE, outline=BLK, width=5)
    d.polygon([(x - 20 * sc, y + 44 * sc), (x + 10 * sc, y + 44 * sc), (x - 30 * sc, y + 90 * sc)], fill=WHITE, outline=BLK)
    d.text((x, y), text, font=f, fill=(30, 30, 30), anchor="mm")

CAPS = [
    (0.0, 3.5, "¡En Cancún hay un puente que *se negaba a quedarse de pie*!"),
    (3.5, 6.5, "Varillas *dobladas*, herramientas que *desaparecían*…"),
    (6.5, 9.0, "“No les pidieron permiso a los *aluxes*”"),
    (9.0, 11.5, "La solución: *su propia casita* debajo del puente"),
    (11.5, 14.0, "Y dicen que desde entonces… *todo bien*"),
    (14.0, 17.0, "Pequeños *guardianes mayas* de la selva, la milpa y los cenotes"),
    (17.0, 20.0, "Casi nunca los ves… pero sí oyes *sus risitas*"),
    (20.0, 24.0, "Así sobrevives a un *alux*. *1:* pide permiso antes de construir"),
    (24.0, 26.0, "Aunque los vecinos *te vean raro*"),
    (26.0, 28.5, "*2:* déjale ofrenda: comida y bebida"),
    (28.5, 31.0, "No, *las sobras no cuentan*"),
    (31.0, 34.5, "*3:* ¿tus llaves aparecen en el refri?"),
    (34.5, 37.0, "No estás loco. *Es él.* Pídeselas amablemente"),
    (37.0, 42.0, "*4:* nunca te burles de ellos. *Ni en Facebook*"),
    (42.0, 49.0, "*5:* si le caes bien, cuida tu terreno, espanta ladrones… *y trae lluvia*"),
    (49.0, 54.0, "¿Le pediste permiso a tu *alux* antes de ver este video?"),
    (54.0, 60.0, "Cuéntame: ¿en tu casa también *desaparecen cosas*?"),
]
STEPS = [21.0, 26.0, 31.0, 37.0, 42.0]

def s1(t):
    img = SITE.copy(); d = ImageDraw.Draw(img)
    broken = ease((t - 0.3) / 1.2) * (1 - 0.0)
    bridge(d, t, broken=broken)
    rng = random.Random(5)
    for i, tool in enumerate(["martillo", "pala", "casco"]):
        st = 3.6 + i * 0.6
        if t < st: continue
        p = ease((t - st) / 1.2)
        x = 250 + i * 280; y = lerp(1180, 520, p)
        d.ellipse([x - 40, y - 26, x + 40, y + 26], fill=[(120, 90, 60), (150, 150, 160), (250, 200, 40)][i], outline=BLK, width=4)
        if p > 0.9:
            d.text((x, y - 60), "?", font=F(60), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    if t > 5.5:
        for i, (x, y) in enumerate([(120, 1250), (960, 1250)]):
            alux(d, x, y + 40, 0.45, t + i, mood="laugh", face=1 if i == 0 else -1)
            jiji(d, x, y - 260, t + i)
    chip(d, "CANCÚN", 300, bg=(30, 110, 210), size=64, appear=t / 0.4)
    return img, 1.0, 1.0 + 0.04 * t / 9, (0.4 < t < 1.2)

def s2(t):
    lt = t - 9
    img = SITE.copy(); d = ImageDraw.Draw(img)
    bridge(d, t, broken=0.0, fixed=lt > 2.5)
    sc = pop(lt / 0.5)
    casita(d, 540, GROUND - 30, 1.2 * sc)
    if lt > 1.0:
        offering(d, 330, GROUND - 10, 0.7 * pop((lt - 1.0) / 0.4))
    if lt > 2.5:
        alux(d, 800, GROUND + 30, 0.55, t, mood="grin", face=-1, arm="up")
        bigtext(d, "TODO BIEN", 540, 520, int(100 * pop((lt - 2.5) / 0.3)), fill=YEL)
    return img, 1.0, 1.0

def s3(t):
    lt = t - 14
    img = JUNGLE.copy(); d = ImageDraw.Draw(img)
    for x in (120, 240, 860, 980):
        corn(d, x, GROUND - 20, 1.0)
    d.ellipse([700, GROUND + 20, 1060, GROUND + 140], fill=(40, 150, 190), outline=(20, 90, 120), width=6)
    sc = pop(lt / 0.5)
    alux(d, 470, GROUND + 60, 1.25 * sc, t, mood="laugh" if lt > 3 else "grin")
    if lt > 3.0:
        jiji(d, 200, 620, t, 60); jiji(d, 850, 560, t + 1, 52); jiji(d, 760, 900, t + 2, 44)
    chip(d, "¿QUÉ ES UN ALUX?", 300, bg=(200, 60, 60), appear=lt / 0.4)
    return img, 1.0, 1.0

def s4(t):
    lt = t - 20
    step = sum(1 for s in STEPS if t >= s)
    ls = t - STEPS[step - 1] if step else lt
    if step in (0, 1, 2, 5): img = JUNGLE.copy()
    else: img = BG_HOUSE.copy()
    d = ImageDraw.Draw(img)
    if step <= 1:
        guy(d, 330, GROUND + 60, 0.95, mood="neutral", arms="down", look=1, t=t)
        bubble(d, 640, 560, "¿Me das permiso?", 44, pop((ls - 0.3) / 0.3))
        if t > 23.8:
            guy(d, 900, GROUND + 60, 0.55, mood="scared", look=-1, t=t, hoodie=(90, 140, 200))
            d.text((900, 820), "¿?", font=F(70), fill=RED, anchor="mm", stroke_width=6, stroke_fill=WHITE)
    elif step == 2:
        offering(d, 360, GROUND - 40, 1.4 * pop(ls / 0.4))
        alux(d, 790, GROUND + 40, 0.75, t, mood="grin", face=-1)
        if t > 28.5:
            sc = pop((t - 28.5) / 0.3)
            d.rounded_rectangle([340 - 120 * sc, 640 - 110 * sc, 340 + 120 * sc, 640 + 110 * sc], int(30 * sc), fill=(60, 60, 60))
            d.text((340, 640), "sobras", font=F(max(8, 44 * sc)), fill=WHITE, anchor="mm")
            xmark(d, 340, 640, 0.75 * sc)
    elif step == 3:
        fridge(d, 760, GROUND + 40, 1.3, open_=ease((ls - 1.2) / 0.5))
        p = ease((ls - 0.4) / 1.0)
        keys(d, lerp(250, 760, p), lerp(600, 1000, p) - math.sin(p * math.pi) * 250, 1.0, ang=ls * 8)
        guy(d, 260, GROUND + 60, 0.9, mood="scared", t=t)
        if ls > 3.0:
            alux(d, 540, GROUND + 60, 0.55, t, mood="laugh", arm="hold")
            jiji(d, 540, 900, t)
        if ls < 3.0:
            bubble(d, 380, 520, "¿Y mis llaves?", 40, pop((ls - 0.2) / 0.3))
    elif step == 4:
        post(d, 540, 720, 1.25, t)
        if ls > 1.2:
            xmark(d, 540, 720, pop((ls - 1.2) / 0.3) * 1.1)
        if ls > 2.2:
            alux(d, 540, GROUND + 80, 0.6, t, mood="angry")
    else:
        for x in (140, 300):
            corn(d, x, GROUND - 20, 1.0)
        alux(d, 520, GROUND + 60, 0.75, t, mood="grin", arm="up")
        if ls > 1.0:
            tx = lerp(800, 1300, ease((ls - 1.0) / 2.0))
            thief(d, tx, GROUND + 60, 0.7, t)
        if ls > 3.0:
            cloud_rain(d, 260, 560, 1.0, t)
    if step >= 1:
        badge(d, step, pop(ls / 0.3))
    chip(d, "CÓMO SOBREVIVIR A UN ALUX", 300, bg=(40, 140, 80), size=50, appear=lt / 0.4)
    return img, 1.0, 1.0

def s5(t):
    lt = t - 49
    img = BG_DARK.copy(); d = ImageDraw.Draw(img)
    z = pop(lt / 0.5)
    alux(d, 540, 1500, 2.1 * z, t, mood="wink" if 1.5 < lt < 4.0 or lt > 4.6 else "grin", face=-1)
    if lt > 4.0:
        jiji(d, 540, 360, t, 90)
    return img, 1.0, 1.0

def s6(t):
    lt = t - 54
    img = Image.new("RGB", (W, H), (8, 8, 10)); d = ImageDraw.Draw(img)
    sc = pop(lt / 0.4)
    bigtext(d, "¿En tu casa", 540, 640, int(90 * sc), fill=WHITE)
    bigtext(d, "DESAPARECEN", 540, 770, int(110 * sc), fill=YEL)
    bigtext(d, "cosas?", 540, 900, int(90 * sc), fill=WHITE)
    ay = 1060 + 25 * math.sin(lt * 8)
    d.polygon([(470, ay), (610, ay), (540, ay + 90)], fill=RED, outline=WHITE)
    d.rectangle([512, ay - 90, 568, ay], fill=RED)
    if lt > 0.8:
        alux(d, 900, 1420, 0.45, t, mood="laugh", face=-1)
    return img, ease(lt / 0.3), 1.0

SCENES = [(0, 9, s1), (9, 14, s2), (14, 20, s3), (20, 49, s4), (49, 54, s5), (54, 60, s6)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img, b, z = r[0], r[1], r[2]
    shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce and fn is not s6:
            rich_caption(d, txt, appear=(t - cs) / 0.25)
    if z > 1.001:
        cw, ch = W / z, H / z
        img = img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    if fn is not s6: b = b * (0.3 + 0.7 * fi)
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    if shake:
        k = int(t * FPS)
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1)
        arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r4.png"); sys.exit()
    from warp4 import v_of_T, DUR
    out = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(59.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
