import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)
from reel2 import phone

FPS = 30
PALE = (205, 215, 225)
CAPE = (25, 20, 35)
CAPE_IN = (170, 20, 40)
FEET = 1380

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def vampire(d, x, y, s=1.0, t=0.0, mood="smug", outfit="cape", eyes_glow=0.0, arms="down", hat=None):
    S = lambda v: v * s
    d.ellipse([x - S(120), y - S(16), x + S(120), y + S(16)], fill=(40, 40, 50))
    if outfit == "cape":
        d.polygon([(x - S(150), y - S(420)), (x + S(150), y - S(420)), (x + S(210), y - S(60)), (x - S(210), y - S(60))], fill=CAPE_IN)
        d.polygon([(x - S(150), y - S(420)), (x - S(110), y - S(420)), (x - S(170), y - S(60)), (x - S(210), y - S(60))], fill=CAPE)
        d.polygon([(x + S(150), y - S(420)), (x + S(110), y - S(420)), (x + S(170), y - S(60)), (x + S(210), y - S(60))], fill=CAPE)
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx * S(10) - (S(55) if sx < 0 else 0), y - S(190), x + sx * S(10) + (S(55) if sx > 0 else 0), y - S(10)], int(S(18)), fill=(30, 30, 40))
        d.ellipse([x + sx * S(45) - S(45), y - S(40), x + sx * S(45) + S(45), y + S(4)], fill=(10, 10, 15))
    body = {"cape": (40, 35, 50), "store": (40, 120, 200), "call": (230, 230, 235), "lab": (245, 245, 250), "suit": (45, 45, 60)}[outfit]
    d.rounded_rectangle([x - S(100), y - S(420), x + S(100), y - S(170)], int(S(50)), fill=body, outline=BLK, width=4)
    if outfit in ("cape", "suit"):
        d.polygon([(x - S(40), y - S(420)), (x + S(40), y - S(420)), (x, y - S(300))], fill=WHITE)
        d.polygon([(x - S(16), y - S(390)), (x + S(16), y - S(390)), (x, y - S(330))], fill=CAPE_IN)
    if outfit == "store":
        d.rounded_rectangle([x - S(60), y - S(360), x + S(60), y - S(320)], int(S(8)), fill=WHITE)
        d.text((x, y - S(340)), "NOCHE", font=F(max(8, S(26))), fill=(40, 120, 200), anchor="mm")
    if outfit == "lab":
        d.line([(x, y - S(410)), (x, y - S(180))], fill=(180, 180, 190), width=max(2, int(S(5))))
    sl = dk(body, 0.8)
    def arm(sx, hx, hy):
        d.line([(x + sx * S(90), y - S(390)), (hx, hy)], fill=sl, width=int(S(40)), joint="curve")
        d.ellipse([hx - S(24), hy - S(24), hx + S(24), hy + S(24)], fill=PALE)
    if arms == "down": arm(-1, x - S(130), y - S(200)); arm(1, x + S(130), y - S(200))
    elif arms == "up": arm(-1, x - S(180), y - S(560)); arm(1, x + S(180), y - S(560))
    elif arms == "desk": arm(-1, x - S(80), y - S(250)); arm(1, x + S(80), y - S(250))
    elif arms == "phone": arm(-1, x - S(130), y - S(200)); arm(1, x + S(70), y - S(470))
    if outfit == "cape":
        d.polygon([(x - S(150), y - S(420)), (x - S(60), y - S(420)), (x - S(110), y - S(520))], fill=CAPE)
        d.polygon([(x + S(150), y - S(420)), (x + S(60), y - S(420)), (x + S(110), y - S(520))], fill=CAPE)
    hx, hy = x, y - S(500)
    d.ellipse([hx - S(95), hy - S(105), hx + S(95), hy + S(100)], fill=PALE, outline=BLK, width=3)
    d.chord([hx - S(100), hy - S(118), hx + S(100), hy + S(30)], 180, 360, fill=(15, 15, 20))
    d.polygon([(hx - S(30), hy - S(60)), (hx + S(30), hy - S(60)), (hx, hy - S(10))], fill=(15, 15, 20))
    for sx in (-1, 1):
        d.polygon([(hx + sx * S(98), hy - S(10)), (hx + sx * S(130), hy - S(60)), (hx + sx * S(92), hy + S(30))], fill=PALE, outline=BLK)
    ec = lc((255, 255, 255), (255, 60, 60), eyes_glow)
    for sx in (-1, 1):
        ex, ey = hx + sx * S(36), hy + S(5)
        if mood == "sleepy":
            d.line([(ex - S(20), ey), (ex + S(20), ey)], fill=BLK, width=max(2, int(S(6))))
        else:
            d.ellipse([ex - S(20), ey - S(20), ex + S(20), ey + S(20)], fill=ec, outline=BLK, width=3)
            d.ellipse([ex - S(7), ey - S(5), ex + S(7), ey + S(9)], fill=(180, 0, 20) if eyes_glow > 0.5 else BLK)
        d.line([(ex - S(26), ey - S(32) + (sx * S(8) if mood != "sad" else -sx * S(8))), (ex + S(26), ey - S(32) - (sx * S(8) if mood != "sad" else -sx * S(8)))], fill=BLK, width=max(2, int(S(7))))
    my = hy + S(50)
    if mood in ("smug", "happy"):
        d.arc([hx - S(40), my - S(25), hx + S(40), my + S(20)], 20, 160, fill=BLK, width=max(2, int(S(6))))
    elif mood == "sad":
        d.arc([hx - S(35), my, hx + S(35), my + S(35)], 200, 340, fill=BLK, width=max(2, int(S(6))))
    else:
        d.ellipse([hx - S(22), my - S(10), hx + S(22), my + S(25)], fill=(60, 10, 20), outline=BLK, width=2)
    for sx in (-1, 1):
        fx = hx + sx * S(16)
        d.polygon([(fx - S(8), my + S(4)), (fx + S(8), my + S(4)), (fx, my + S(26))], fill=WHITE, outline=BLK)
    if hat == "cap":
        d.chord([hx - S(100), hy - S(120), hx + S(100), hy + S(10)], 180, 360, fill=(40, 120, 200), outline=BLK, width=3)
        d.rectangle([hx, hy - S(60), hx + S(150), hy - S(45)], fill=(40, 120, 200), outline=BLK, width=3)
    if hat == "headset":
        d.arc([hx - S(110), hy - S(130), hx + S(110), hy + S(60)], 190, 350, fill=(40, 40, 40), width=max(3, int(S(12))))
        d.ellipse([hx - S(125), hy - S(25), hx - S(90), hy + S(25)], fill=(40, 40, 40))
        d.line([(hx - S(105), hy + S(20)), (hx - S(40), hy + S(70))], fill=(40, 40, 40), width=max(2, int(S(6))))

def doc(d, cx, cy, w, h, lines, t0, t, title=None):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 16, fill=(250, 248, 238), outline=BLK, width=6)
    if title: d.text((cx, cy - h / 2 + 60), title, font=F(60), fill=(40, 40, 40), anchor="mm")
    for i, (lt0, txt, col) in enumerate(lines):
        if t < t0 + lt0: continue
        a = cl((t - t0 - lt0) / 0.25)
        d.text((cx - w / 2 + 50, cy - h / 2 + 150 + i * 90), txt, font=F(int(42 * a) + 1), fill=col, anchor="lm")

def stamp(d, cx, cy, txt, col, a, rot=-12):
    if a <= 0: return
    sz = int(70 * (1 + 0.6 * (1 - pop(a))))
    tmp = Image.new("RGBA", (900, 220), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    td.rounded_rectangle([10, 10, 890, 210], 20, outline=col, width=14)
    td.text((450, 110), txt, font=F(sz), fill=col, anchor="mm")
    tmp = tmp.rotate(rot, expand=True)
    return tmp

def paste_stamp(img, cx, cy, txt, col, a, rot=-12):
    s = stamp(None, cx, cy, txt, col, a, rot) if False else None
    if a <= 0: return
    sz = int(70 * (1 + 0.6 * (1 - pop(a))))
    tmp = Image.new("RGBA", (900, 220), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    td.rounded_rectangle([10, 10, 890, 210], 20, outline=col, width=14)
    td.text((450, 110), txt, font=F(sz), fill=col, anchor="mm")
    tmp = tmp.rotate(rot, expand=True)
    img.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)

def night_room(lamp=True):
    img = grad((30, 25, 50), (60, 45, 70)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(70, 50, 45))
    d.rectangle([680, 280, 960, 600], fill=(20, 25, 60), outline=(120, 100, 90), width=14)
    d.ellipse([820, 320, 900, 400], fill=(240, 240, 210))
    return img

def blood_bag(d, x, y, s, col=(190, 20, 40), empty=False):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(50), y - S(70), x + S(50), y + S(70)], int(S(20)), fill=(235, 235, 240) if empty else col, outline=BLK, width=3)
    d.rectangle([x - S(30), y - S(30), x + S(30), y + S(10)], fill=WHITE)
    d.text((x, y - S(10)), "O-", font=F(max(8, S(26))), fill=(190, 20, 40), anchor="mm")
    d.line([(x, y - S(70)), (x, y - S(100))], fill=(200, 200, 200), width=4)

CAPS = [
    (0.0, 3.0, "Si fueras *vampiro en 2026*… ¿de qué trabajarías *para pagar la renta*?"),
    (3.0, 9.0, "*400 años* vivo, *cero experiencia comprobable*… último empleo: *aterrorizar campesinos*"),
    (9.0, 13.0, "*Trabajo #1:* turno nocturno. *Nadie cuestiona tu palidez*"),
    (13.0, 17.0, "Pero cada que piden *jugo de tomate*… *Recursos Humanos* recibe una denuncia"),
    (17.0, 23.0, "*Trabajo #2:* vendedor por teléfono. *Siglos de experiencia* manipulando gente"),
    (23.0, 27.0, "Su debilidad: si el cliente *lo invita a pasar*… *rechaza la oferta*"),
    (27.0, 30.0, "*Trabajo #3:* banco de sangre. *El trabajo de tus sueños*"),
    (30.0, 36.0, "Pero hay *auditorías*… y faltan *12 bolsas de O negativo*"),
    (36.0, 41.0, "*Trabajo #4:* criptomonedas. Sobreviviste *guerras, pestes y revoluciones*…"),
    (41.0, 45.0, "…hasta que tu portafolio *pierde el 90% en una noche*"),
    (45.0, 50.0, "El problema no es *la sangre*, ni *el ajo*, ni *el sol*…"),
    (50.0, 55.0, "Es que tras *400 años trabajando*… *no tienes casa propia*"),
    (55.0, 60.0, "No apareces en el *historial crediticio*… *ni en los espejos*"),
    (60.0, 68.0, "¿De qué pondrías a trabajar *a un vampiro*? *Comenta*"),
]

def desk_top(d, x0, y0, x1, y1, col=(110, 75, 50), floor=None):
    """Mesa con patas: tablero de (x0,y0) a (x1,y1) y patas hasta el piso."""
    floor = floor or FEET
    for lx in (x0 + 40, x1 - 70):
        d.rectangle([lx, y1, lx + 30, floor], fill=dk(col, .8), outline=BLK, width=4)
    d.rectangle([x0, y0, x1, y1], fill=col, outline=BLK, width=5)

def s_hook(t):
    img = night_room(); d = ImageDraw.Draw(img)
    vampire(d, 540, FEET, 0.9, t, mood="sad", arms="desk")
    desk_top(d, 150, 1150, 930, 1190)
    d.rectangle([250, 1100, 470, 1150], fill=WHITE, outline=BLK, width=3)
    d.text((360, 1125), "RENTA", font=F(36), fill=RED, anchor="mm")
    d.rectangle([760, 1060, 790, 1150], fill=(240, 235, 210)); d.ellipse([764, 1030 + math.sin(t * 9) * 4, 786, 1062], fill=(255, 200, 60))
    chip(d, "GUÍA LABORAL DE LOS MONSTRUOS", 230, bg=(150, 20, 40), size=50, appear=t / 0.3)
    return img, 1.0, 1.0

def s_cv(t):
    lt = t - 3.0
    img = night_room(); d = ImageDraw.Draw(img)
    doc(d, 540, 760, 860, 760, [(0.3, "Nombre: El Conde (sin apellido)", (40, 40, 40)),
                                (1.0, "Edad: 400 años (aprox.)", (40, 40, 40)),
                                (2.0, "Experiencia: no comprobable", RED),
                                (3.2, "Último empleo:", (40, 40, 40)),
                                (3.6, "  aterrorizar campesinos", (150, 20, 40))], 3.0, t, title="CURRÍCULUM")
    vampire(d, 870, 1600, 0.6, t, mood="smug")
    return img, 1.0, 1.0 + 0.03 * ease(lt / 6)

def store_bg(t):
    img = grad((40, 40, 70), (230, 235, 240)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 520], fill=(20, 25, 50))
    d.ellipse([100, 120, 190, 210], fill=(240, 240, 210))
    for k in range(4): d.rectangle([60 + k * 260, 560, 260 + k * 260, 1050], fill=(210, 215, 220), outline=(150, 150, 160), width=4)
    for k in range(4):
        for j in range(4):
            d.rectangle([80 + k * 260, 590 + j * 110, 240 + k * 260, 660 + j * 110], fill=[(220, 60, 60), (60, 160, 90), (240, 190, 60), (80, 120, 220)][(k + j) % 4])
    d.rectangle([0, 1200, W, H], fill=(200, 200, 205))
    d.rounded_rectangle([780, 320, 1000, 460], 20, fill=WHITE, outline=BLK, width=5)
    d.text((890, 390), "3:00", font=F(64), fill=RED, anchor="mm")
    return img

def s_job1(t):
    lt = t - 9.0
    img = store_bg(t); d = ImageDraw.Draw(img)
    vampire(d, 380, FEET - 60, 0.85, t, mood="smug", outfit="store", hat="cap", eyes_glow=cl((lt - 4.5) / 0.5))
    d.rectangle([80, 1130, 1000, 1330], fill=(130, 90, 60), outline=BLK, width=6)
    chip(d, "TRABAJO #1: TURNO NOCTURNO", 230, bg=(30, 110, 210), size=52, appear=lt / 0.3)
    if lt > 4.0:
        sc = pop((lt - 4.0) / 0.3)
        d.rounded_rectangle([600, 760 - 70 * sc, 1040, 760 + 70 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=5)
        d.text((820, 760), "¿Jugo de tomate?", font=F(max(8, 44 * sc)), fill=(40, 40, 40), anchor="mm")
        d.rectangle([840, 1000, 900, 1130], fill=(200, 30, 30), outline=BLK, width=4)
    if lt > 5.6:
        a = cl((lt - 5.6) / 1.4)
        px, py = lerp(380, 900, a), lerp(1000, 380, a)
        d.rectangle([px - 90, py - 110, px + 90, py + 110], fill=WHITE, outline=BLK, width=4)
        d.text((px, py - 60), "RR.HH.", font=F(32), fill=(40, 40, 40), anchor="mm")
        d.text((px, py), "DENUNCIA", font=F(30), fill=RED, anchor="mm")
    return img, 1.0, 1.0

def s_job2(t):
    lt = t - 17.0
    img = grad((235, 235, 240), (200, 205, 215)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(150, 155, 165))
    if lt < 6.0:
        d.rectangle([600, 330, 1000, 700], fill=WHITE, outline=BLK, width=5)
        pts = [(630 + k * 50, 670 - (k ** 1.6) * 18 * cl(lt / 3)) for k in range(8)]
        d.line(pts, fill=(40, 180, 90), width=10)
        d.text((800, 370), "VENTAS", font=F(40), fill=(40, 40, 40), anchor="mm")
        vampire(d, 360, FEET, 0.85, t, mood="smug", outfit="call", hat="headset", arms="desk")
        desk_top(d, 100, 1130, 1000, 1200, col=(130, 90, 60))
        for i, (st, txt) in enumerate([(1.5, "SEGUROS ✓"), (2.6, "TARJETAS ✓"), (3.8, "HIPOTECA 30 AÑOS ✓")]):
            if lt > st: d.text((800, 780 + i * 80), txt, font=F(44), fill=(40, 160, 80), anchor="mm", stroke_width=4, stroke_fill=WHITE)
        chip(d, "TRABAJO #2: VENTAS POR TELÉFONO", 230, bg=(150, 60, 200), size=48, appear=lt / 0.3)
    else:
        lt2 = lt - 6.0
        d.rectangle([600, 450, 960, 1200], fill=(150, 100, 60), outline=BLK, width=6)
        d.rectangle([640, 490, 920, 1160], fill=(240, 235, 220))
        guy(d, 780, 1170, 0.7, mood="neutral", t=t)
        sc = pop(lt2 / 0.3)
        d.rounded_rectangle([560, 260 - 60 * sc, 1040, 260 + 60 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=5)
        d.text((800, 260), "¡Pásale!", font=F(max(8, 56 * sc)), fill=(40, 40, 40), anchor="mm")
        vampire(d, 300, FEET, 0.85, t, mood="o", outfit="cape")
        if lt2 > 1.5: paste_stamp(img, 540, 650, "OFERTA RECHAZADA", (200, 30, 30), (lt2 - 1.5) / 0.3)
    return img, 1.0, 1.0

def s_job3(t):
    lt = t - 27.0
    img = grad((230, 240, 245), (200, 215, 225)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(180, 190, 200))
    d.rectangle([560, 330, 1020, 1200], fill=(240, 245, 250), outline=BLK, width=6)
    for r in range(3):
        d.line([(570, 560 + r * 220), (1010, 560 + r * 220)], fill=(150, 160, 170), width=6)
        for c in range(4):
            missing = lt > 3.0 and (r * 4 + c) % 2 == 0
            blood_bag(d, 625 + c * 110, 470 + r * 220, 0.8, empty=missing)
    vampire(d, 300, FEET, 0.85, t, mood="happy" if lt < 3.0 else "o", outfit="lab")
    if lt > 3.0:
        d.ellipse([280, 900, 320, 920], fill=(190, 20, 40))
    chip(d, "TRABAJO #3: BANCO DE SANGRE", 230, bg=(190, 20, 40), size=52, appear=lt / 0.3)
    if lt > 3.4:
        sc = pop((lt - 3.4) / 0.3)
        d.rounded_rectangle([120, 330, 520, 330 + 300 * sc], 16, fill=WHITE, outline=BLK, width=5)
        if sc > 0.9:
            d.text((320, 380), "AUDITORÍA", font=F(44), fill=(40, 40, 40), anchor="mm")
            d.text((320, 470), "O-: -12", font=F(70), fill=RED, anchor="mm")
            d.text((320, 560), "¿?", font=F(60), fill=(40, 40, 40), anchor="mm")
    return img, 1.0, 1.0

def s_job4(t):
    lt = t - 36.0
    img = night_room(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 330, 990, 900], 20, fill=(15, 20, 30), outline=(120, 120, 130), width=8)
    crash = cl((lt - 5.0) / 0.8)
    pts = []
    for k in range(16):
        x = 130 + k * 54
        y = 760 - k * 22 - math.sin(k * 1.3) * 25
        if k > 10: y = lerp(y, 760 - 10 * 22 + (k - 10) * 80, crash) if crash > 0 else y
        pts.append((x, y))
    d.line(pts, fill=(60, 220, 120) if crash < 0.3 else (230, 50, 50), width=10)
    if crash > 0:
        bigtext(d, "-90%", 540, 520, int(150 * pop((lt - 5.0) / 0.3)), fill=(230, 50, 50), stroke=WHITE, sw=10)
    vampire(d, 540, FEET + 60, 0.75, t, mood="smug" if crash < 0.5 else "sad", outfit="cape", arms="desk")
    desk_top(d, 150, 1150, 930, 1190)
    chip(d, "TRABAJO #4: CRIPTOMONEDAS", 230, bg=(220, 140, 30), size=52, appear=lt / 0.3)
    return img, 1.0, 1.0, (5.0 < lt < 5.4)

def garlic(d, cx, cy, r):
    for k in (-1, 0, 1):
        d.ellipse([cx + k * r * 0.45 - r * 0.6, cy - r * 0.6, cx + k * r * 0.45 + r * 0.6, cy + r * 0.7], fill=(245, 240, 225), outline=BLK, width=4)
    d.polygon([(cx - r * 0.15, cy - r * 0.6), (cx + r * 0.15, cy - r * 0.6), (cx, cy - r * 1.2)], fill=(230, 225, 200), outline=BLK)

def s_not(t):
    lt = t - 45.0
    img = grad((40, 30, 60), (90, 50, 80)); d = ImageDraw.Draw(img)
    items = [(0.3, 220), (1.4, 540), (2.6, 860)]
    for i, (st, x) in enumerate(items):
        if lt < st: continue
        sc = pop((lt - st) / 0.3)
        y = 650
        if i == 0:
            d.polygon([(x, y - 110 * sc), (x - 70 * sc, y + 20 * sc), (x + 70 * sc, y + 20 * sc)], fill=(200, 20, 40))
            d.ellipse([x - 72 * sc, y - 40 * sc, x + 72 * sc, y + 90 * sc], fill=(200, 20, 40))
        elif i == 1: garlic(d, x, y, 90 * sc)
        else:
            d.ellipse([x - 80 * sc, y - 80 * sc, x + 80 * sc, y + 80 * sc], fill=(255, 210, 60))
            for k in range(10):
                a = k / 10 * 2 * math.pi
                d.line([(x + math.cos(a) * 95 * sc, y + math.sin(a) * 95 * sc), (x + math.cos(a) * 130 * sc, y + math.sin(a) * 130 * sc)], fill=(255, 210, 60), width=10)
        if lt > st + 0.4: xmark(d, x, y, 1.1)
    vampire(d, 540, FEET + 80, 0.7, t, mood="sad")
    return img, 1.0, 1.0

def s_bank(t):
    lt = t - 50.0
    img = grad((225, 220, 205), (190, 180, 160)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(120, 95, 70))
    d.rectangle([60, 330, 340, 760], fill=(200, 215, 225), outline=(150, 120, 60), width=14)
    d.text((200, 800), "ESPEJO", font=F(32), fill=(80, 60, 40), anchor="mm")
    if lt > 5.0:
        d.text((200, 545), "(vacío)", font=F(38), fill=(120, 130, 140), anchor="mm")
    d.rectangle([420, 300, 1040, 520], fill=(60, 90, 140), outline=BLK, width=5)
    d.text((730, 410), "BANCO", font=F(80), fill=WHITE, anchor="mm")
    vampire(d, 700, FEET, 0.8, t, mood="sad" if lt > 2.0 else "smug", outfit="suit")
    d.rectangle([400, 1150, 1040, FEET], fill=(95, 65, 45), outline=BLK, width=5)          # mostrador del banco hasta el piso
    for px in (560, 720, 880): d.rectangle([px - 60, 1190, px + 60, FEET - 30], outline=(70, 48, 33), width=5)
    d.rectangle([380, 1120, 1060, 1155], fill=(140, 100, 70), outline=BLK, width=5)
    if lt < 5.0:
        sc = pop(lt / 0.3)
        d.rounded_rectangle([120, 880 - 60 * sc, 520, 880 + 60 * sc], int(16 * sc), fill=WHITE, outline=BLK, width=4)
        d.text((320, 880), "CASA PROPIA: 0", font=F(max(8, 40 * sc)), fill=RED, anchor="mm")
    if lt > 5.0:
        paste_stamp(img, 600, 1000, "CRÉDITO RECHAZADO", (200, 30, 30), (lt - 5.0) / 0.3)
        d = ImageDraw.Draw(img)
        chip(d, "HISTORIAL: NO ENCONTRADO", 230, bg=(30, 30, 40), fg=YEL, size=52, appear=(lt - 5.0) / 0.3)
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 60.0
    img = night_room(); d = ImageDraw.Draw(img)
    vampire(d, 540, FEET + 40, 0.9, t, mood="smug", arms="up", eyes_glow=0.6)
    sc = pop(lt / 0.35)
    d.rounded_rectangle([540 - 380 * sc, 330 - 90 * sc, 540 + 380 * sc, 330 + 90 * sc], int(26 * sc), fill=(150, 20, 40), outline=WHITE, width=6)
    d.text((540, 300), "¿DE QUÉ LO PONDRÍAS", font=F(max(8, 48 * sc)), fill=WHITE, anchor="mm")
    d.text((540, 365), "A TRABAJAR?", font=F(max(8, 48 * sc)), fill=YEL, anchor="mm")
    if lt > 1.5: chip(d, "COMENTA  ·  SÍGUEME", 500, bg=(30, 30, 40), fg=WHITE, size=48, appear=(lt - 1.5) / 0.3)
    return img, 1.0, 1.0

SCENES = [(0, 3, s_hook), (3, 9, s_cv), (9, 17, s_job1), (17, 27, s_job2), (27, 36, s_job3), (36, 45, s_job4),
          (45, 50, s_not), (50, 60, s_bank), (60, 80, s_end)]

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
        sheet.save("sheet_r14.png"); sys.exit()
    from warp14 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(67.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
