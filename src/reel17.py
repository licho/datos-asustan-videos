import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)
from reel2 import phone

FPS = 30
FEET = 1380
FUR = (125, 90, 60)
FUR_D = (90, 62, 40)

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def moon(d, x, y, r):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 245, 215))
    for (a, b, c) in [(-0.3, -0.2, 0.18), (0.25, 0.2, 0.14), (0.1, -0.4, 0.1)]:
        d.ellipse([x + a * r - c * r, y + b * r - c * r, x + a * r + c * r, y + b * r + c * r], fill=(230, 225, 195))

def night(moon_on=True):
    img = grad((20, 25, 55), (55, 45, 85)); d = ImageDraw.Draw(img)
    rng = random.Random(2)
    for i in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, 1000)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(220, 220, 250))
    if moon_on: moon(d, 830, 420, 110)
    d.rectangle([0, 1200, W, H], fill=(55, 50, 60))
    return img

def wolf(d, x, y, s=1.0, t=0.0, mood="smug", outfit="shirt", arms="down", hat=None, howl=False):
    S = lambda v: v * s
    d.ellipse([x - S(130), y - S(16), x + S(130), y + S(16)], fill=(30, 30, 35))
    pants = (60, 80, 140)
    for sx in (-1, 1):
        d.polygon([(x + sx * S(10), y - S(190)), (x + sx * S(70), y - S(190)), (x + sx * S(75), y - S(50)), (x + sx * S(15), y - S(40))], fill=pants)
        d.polygon([(x + sx * S(15), y - S(55)), (x + sx * S(75), y - S(60)), (x + sx * S(85), y - S(30)), (x + sx * S(10), y - S(25))], fill=FUR)
        d.ellipse([x + sx * S(50) - S(55), y - S(40), x + sx * S(50) + S(55), y + S(6)], fill=FUR_D)
    top = {"shirt": (200, 60, 60), "guard": (40, 50, 80), "walker": (60, 150, 90), "delivery": (240, 140, 30), "creator": (130, 70, 180)}[outfit]
    def arm(sx, hx, hy):
        d.line([(x + sx * S(100), y - S(400)), (hx, hy)], fill=FUR, width=int(S(50)), joint="curve")
        d.ellipse([hx - S(30), hy - S(30), hx + S(30), hy + S(30)], fill=FUR_D)
        for k in (-1, 0, 1):
            d.polygon([(hx + k * S(14) - S(5), hy + S(20)), (hx + k * S(14) + S(5), hy + S(20)), (hx + k * S(14), hy + S(38))], fill=WHITE)
    d.rounded_rectangle([x - S(115), y - S(430), x + S(115), y - S(170)], int(S(50)), fill=top, outline=BLK, width=4)
    for k in range(4):
        d.polygon([(x - S(115) + k * S(57), y - S(175)), (x - S(85) + k * S(57), y - S(140)), (x - S(58) + k * S(57), y - S(175))], fill=top)
    d.polygon([(x - S(40), y - S(430)), (x + S(40), y - S(430)), (x, y - S(360))], fill=FUR)
    if outfit == "guard":
        d.rounded_rectangle([x + S(30), y - S(380), x + S(90), y - S(340)], int(S(8)), fill=(230, 200, 60))
    if outfit == "delivery":
        d.rounded_rectangle([x - S(170), y - S(440), x - S(90), y - S(230)], int(S(14)), fill=(230, 120, 20), outline=BLK, width=4)
    if arms == "down": arm(-1, x - S(150), y - S(210)); arm(1, x + S(150), y - S(210))
    elif arms == "up": arm(-1, x - S(190), y - S(580)); arm(1, x + S(190), y - S(580))
    elif arms == "desk": arm(-1, x - S(90), y - S(260)); arm(1, x + S(90), y - S(260))
    elif arms == "run": arm(-1, x - S(180), y - S(300)); arm(1, x + S(170), y - S(380))
    elif arms == "hold": arm(-1, x - S(150), y - S(210)); arm(1, x + S(200), y - S(330))
    hx, hy = x, y - S(520)
    for sx in (-1, 1):
        d.polygon([(hx + sx * S(40), hy - S(70)), (hx + sx * S(100), hy - S(170)), (hx + sx * S(110), hy - S(40))], fill=FUR, outline=BLK)
        d.polygon([(hx + sx * S(55), hy - S(75)), (hx + sx * S(95), hy - S(140)), (hx + sx * S(98), hy - S(60))], fill=(200, 150, 130))
    d.ellipse([hx - S(110), hy - S(100), hx + S(110), hy + S(100)], fill=FUR, outline=BLK, width=3)
    for sx in (-1, 1):
        d.polygon([(hx + sx * S(100), hy + S(10)), (hx + sx * S(140), hy + S(40)), (hx + sx * S(95), hy + S(60))], fill=FUR)
    ang = -0.5 if howl else 0.0
    sx0, sy0 = hx, hy + S(35)
    d.ellipse([sx0 - S(65), sy0 - S(40), sx0 + S(65), sy0 + S(55)], fill=(190, 150, 110), outline=BLK, width=3)
    d.ellipse([sx0 - S(22), sy0 - S(35), sx0 + S(22), sy0 - S(5)], fill=(30, 25, 25))
    if howl:
        d.ellipse([sx0 - S(28), sy0 + S(5), sx0 + S(28), sy0 + S(50)], fill=(80, 15, 25), outline=BLK, width=3)
    elif mood in ("smug", "happy"):
        d.arc([sx0 - S(45), sy0, sx0 + S(45), sy0 + S(40)], 20, 160, fill=BLK, width=max(2, int(S(6))))
        for k in (-1, 1): d.polygon([(sx0 + k * S(25) - S(7), sy0 + S(25)), (sx0 + k * S(25) + S(7), sy0 + S(25)), (sx0 + k * S(25), sy0 + S(45))], fill=WHITE, outline=BLK)
    else:
        d.arc([sx0 - S(35), sy0 + S(20), sx0 + S(35), sy0 + S(50)], 200, 340, fill=BLK, width=max(2, int(S(6))))
    for sx in (-1, 1):
        ex, ey = hx + sx * S(45), hy - S(25)
        if howl:
            d.line([(ex - S(18), ey), (ex + S(18), ey)], fill=BLK, width=max(2, int(S(6))))
        else:
            d.ellipse([ex - S(20), ey - S(18), ex + S(20), ey + S(18)], fill=(250, 210, 60), outline=BLK, width=3)
            d.ellipse([ex - S(6), ey - S(10), ex + S(6), ey + S(10)], fill=BLK)
            tilt = S(8) if mood != "sad" else -S(8)
            d.line([(ex - S(26), ey - S(30) + sx * tilt), (ex + S(26), ey - S(30) - sx * tilt)], fill=FUR_D, width=max(2, int(S(9))))
    if hat == "cap":
        d.chord([hx - S(105), hy - S(125), hx + S(105), hy - S(5)], 180, 360, fill=(40, 50, 80), outline=BLK, width=3)
        d.rectangle([hx - S(10), hy - S(70), hx + S(150), hy - S(55)], fill=(40, 50, 80), outline=BLK, width=3)
        d.ellipse([hx - S(22), hy - S(110), hx + S(22), hy - S(75)], fill=(230, 200, 60))

def dog(d, x, y, s, t, kind=0, bow=False):
    S = lambda v: v * s
    col = [(200, 160, 100), (90, 80, 70), (240, 230, 210), (170, 110, 60)][kind % 4]
    off = math.sin(t * 10 + kind) * S(4)
    d.ellipse([x - S(60), y - S(70), x + S(60), y - S(20)], fill=col, outline=BLK, width=3)
    for k in (-40, -15, 15, 40): d.line([(x + S(k), y - S(30)), (x + S(k), y + off * (1 if k > 0 else -1))], fill=col, width=int(S(12)))
    hy = y - S(85) if not bow else y - S(40)
    d.ellipse([x + S(35), hy - S(30), x + S(95), hy + S(30)], fill=col, outline=BLK, width=3)
    d.ellipse([x + S(55), hy - S(10), x + S(65), hy], fill=BLK)
    d.ellipse([x + S(85), hy + S(2), x + S(97), hy + S(12)], fill=BLK)
    d.polygon([(x + S(40), hy - S(25)), (x + S(50), hy - S(55)), (x + S(62), hy - S(25))], fill=dk(col, 0.8))
    d.line([(x - S(60), y - S(55)), (x - S(85), y - S(85) + off)], fill=col, width=int(S(10)))

def cat(d, x, y, s):
    S = lambda v: v * s
    d.ellipse([x - S(50), y - S(80), x + S(50), y], fill=(40, 40, 45))
    d.ellipse([x - S(40), y - S(140), x + S(40), y - S(70)], fill=(40, 40, 45))
    for sx in (-1, 1):
        d.polygon([(x + sx * S(10), y - S(130)), (x + sx * S(35), y - S(170)), (x + sx * S(40), y - S(115))], fill=(40, 40, 45))
        d.ellipse([x + sx * S(18) - S(9), y - S(115), x + sx * S(18) + S(9), y - S(97)], fill=(240, 220, 60))
    d.text((x + S(60), y - S(170)), "¡FSSS!", font=F(max(8, int(S(40)))), fill=RED, anchor="lm")

def bubble(d, cx, cy, w, h, lines, size=44, col=WHITE, a=1.0):
    if a <= 0: return
    w, h = w * pop(a), h * pop(a)
    if w < 10: return
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 30, fill=col, outline=BLK, width=5)
    n = len(lines)
    for i, ln in enumerate(lines):
        d.text((cx, cy - (n - 1) * size * 0.6 + i * size * 1.2), ln, font=F(max(8, int(size * pop(a)))), fill=(30, 30, 30), anchor="mm")

def paste_stamp(img, cx, cy, txt, col, a, rot=-12):
    if a <= 0: return
    sz = int(64 * (1 + 0.6 * (1 - pop(a))))
    tmp = Image.new("RGBA", (920, 220), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    td.rounded_rectangle([10, 10, 910, 210], 20, outline=col, width=14)
    td.text((460, 110), txt, font=F(sz), fill=col, anchor="mm")
    tmp = tmp.rotate(rot, expand=True)
    img.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)

CAPS = [
    (0.0, 3.0, "Si fueras *hombre lobo en 2026*… ¿de qué trabajarías *para pagar la renta*?"),
    (3.0, 9.0, "*Transformación mensual*, *cero control de impulsos* y un historial que *prefieres no mencionar*"),
    (9.0, 14.0, "*Trabajo #1:* guardia de seguridad. *Visión nocturna* y olfato *de primer nivel*"),
    (14.0, 19.0, "Pero una vez al mes *te comes al supervisor*… *\"rotación de personal\"*"),
    (19.0, 24.0, "*Trabajo #2:* paseador de perros. *Los perros te respetan*, los gatos te odian"),
    (24.0, 28.0, "Hasta que el chihuahua *te reconoce como el alfa*"),
    (28.0, 32.5, "*Trabajo #3:* repartidor. *Más rápido que una moto*, sin gasolina"),
    (32.5, 37.0, "Pero si piden *alitas*… llegan *12 huesos perfectamente limpios*"),
    (37.0, 41.5, "*Trabajo #4:* creador de contenido. *Una transformación al mes* = viral"),
    (41.5, 46.0, "Hasta que *tu ex* sube tu video *aullando a las 3 a.m.*"),
    (46.0, 50.0, "El verdadero problema *no es la luna llena*…"),
    (50.0, 57.0, "Cada mes pierdes *una camisa, dos pantalones*… y *tu depósito de renta*"),
    (57.0, 66.0, "¿De qué pondrías a trabajar *a un hombre lobo*? *Comenta*"),
]

def s_hook(t):
    img = night(); d = ImageDraw.Draw(img)
    wolf(d, 540, FEET, 0.85, t, mood="sad", arms="desk")
    d.rectangle([150, 1150, 930, 1195], fill=(110, 75, 50), outline=BLK, width=5)
    for x in (190, 890): d.rectangle([x - 16, 1195, x + 16, FEET], fill=(90, 60, 40), outline=BLK, width=3)
    d.rectangle([250, 1105, 470, 1150], fill=WHITE, outline=BLK, width=3)
    d.text((360, 1128), "RENTA", font=F(34), fill=RED, anchor="mm")
    chip(d, "GUÍA LABORAL DE LOS MONSTRUOS", 230, bg=(150, 20, 40), size=50, appear=t / 0.3)
    chip(d, "EPISODIO 2", 330, bg=(30, 30, 40), fg=YEL, size=44, appear=(t - 0.4) / 0.3)
    return img, 1.0, 1.0

def s_cv(t):
    lt = t - 3.0
    img = night(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([110, 380, 970, 1120], 16, fill=(250, 248, 238), outline=BLK, width=6)
    d.text((540, 450), "CURRÍCULUM", font=F(60), fill=(40, 40, 40), anchor="mm")
    lines = [(0.3, "Nombre: Lupo (solo de día)", (40, 40, 40)), (1.2, "Transformación: 1 vez al mes", (40, 40, 40)),
             (2.4, "Control de impulsos: 0/10", RED), (3.6, "Historial:", (40, 40, 40)), (4.0, "  prefiero no comentar", (150, 20, 40))]
    for i, (st, txt, c) in enumerate(lines):
        if lt < st: continue
        d.text((160, 560 + i * 100), txt, font=F(int(42 * cl((lt - st) / 0.25)) + 1), fill=c, anchor="lm")
    wolf(d, 880, 1650, 0.55, t, mood="smug")
    return img, 1.0, 1.0

def s_guard(t):
    lt = t - 9.0
    img = night(); d = ImageDraw.Draw(img)
    d.rectangle([620, 760, 960, 1200], fill=(200, 200, 205), outline=BLK, width=6)
    d.rectangle([660, 820, 920, 960], fill=(150, 200, 230), outline=BLK, width=4)
    d.text((790, 1050), "SEGURIDAD", font=F(42), fill=(40, 50, 80), anchor="mm")
    if lt < 5.0:
        wolf(d, 330, FEET, 0.8, t, mood="smug", outfit="guard", hat="cap")
        for k in range(3):
            r = 120 + ((lt * 200 + k * 120) % 360)
            d.arc([330 - r, 870 - r, 330 + r, 870 + r], 300, 360, fill=(250, 220, 80), width=5)
        d.text((330, 640), "3 km", font=F(56), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    else:
        lt2 = lt - 5.0
        moon(d, 830, 420, 140)
        wolf(d, 330, FEET, 0.8, t, mood="smug", outfit="guard", hat="cap")
        d.polygon([(560, 1330), (600, 1170), (640, 1330)], fill=RED, outline=BLK)
        d.polygon([(580, 1170), (620, 1170), (600, 1200)], fill=(150, 20, 30), outline=BLK)
        d.rounded_rectangle([470, 1300, 730, 1370], 10, fill=WHITE, outline=BLK, width=4)
        d.text((600, 1335), "SUPERVISOR", font=F(36), fill=BLK, anchor="mm")
        if lt2 > 1.5:
            paste_stamp(img, 540, 620, "ROTACIÓN DE PERSONAL", (200, 30, 30), (lt2 - 1.5) / 0.3)
            d = ImageDraw.Draw(img)
    chip(d, "TRABAJO #1: GUARDIA DE SEGURIDAD", 230, bg=(40, 50, 80), size=48, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_dogs(t):
    lt = t - 19.0
    img = grad((150, 200, 240), (220, 235, 245)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(110, 170, 90))
    wolf(d, 300, FEET, 0.8, t, mood="happy", outfit="walker", arms="hold")
    for i, (dx, dy) in enumerate([(600, 1330), (780, 1290), (940, 1340)]):
        hx, hy = 300 + 200 * 0.8, FEET - 330 * 0.8
        dog(d, dx, dy, 0.8, t, i, bow=(lt > 5.0))
        cy = dy - (40 if lt > 5.0 else 85) * 0.8 + 18
        d.line([(hx + 4, hy + 6), (dx + 0.8 * 45, cy)], fill=(200, 60, 60), width=5)
        d.ellipse([dx + 0.8 * 45 - 7, cy - 7, dx + 0.8 * 45 + 7, cy + 7], fill=(200, 60, 60))
    px, py = 300 + 200 * 0.8, FEET - 330 * 0.8
    d.ellipse([px - 24, py - 24, px + 24, py + 24], fill=FUR_D)
    for k in (-1, 0, 1): d.polygon([(px + k * 11 - 4, py + 16), (px + k * 11 + 4, py + 16), (px + k * 11, py + 30)], fill=WHITE)
    if lt > 2.5 and lt < 5.0: cat(d, 900, 1000, 0.9)
    if lt > 5.0:
        bubble(d, 640, 520, 720, 170, ["¿Por qué mi chihuahua", "te dice \"alfa\"?"], 44, a=(lt - 5.0) / 0.3)
        cx, cy = 300, 800
        sc = pop((lt - 5.6) / 0.3)
        d.polygon([(cx - 80 * sc, cy + 30 * sc), (cx - 80 * sc, cy - 40 * sc), (cx - 40 * sc, cy), (cx, cy - 60 * sc), (cx + 40 * sc, cy), (cx + 80 * sc, cy - 40 * sc), (cx + 80 * sc, cy + 30 * sc)], fill=(250, 200, 40), outline=BLK)
    chip(d, "TRABAJO #2: PASEADOR DE PERROS", 230, bg=(60, 150, 90), size=48, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_delivery(t):
    lt = t - 28.0
    if lt < 4.5:
        img = grad((140, 190, 235), (220, 230, 240)); d = ImageDraw.Draw(img)
        d.rectangle([0, 1200, W, H], fill=(90, 90, 100))
        for k in range(8): d.rectangle([(k * 160 - lt * 600) % (W + 160) - 80, 1290, (k * 160 - lt * 600) % (W + 160), 1300], fill=WHITE)
        wolf(d, 640, FEET, 0.8, t * 2, mood="happy", outfit="delivery", arms="run")
        for k in range(4): d.line([(380 - k * 40, 900 + k * 70), (300 - k * 40, 900 + k * 70)], fill=WHITE, width=8)
        mx = 140
        d.ellipse([mx - 80, 1240, mx - 10, 1310], fill=(30, 30, 30)); d.ellipse([mx + 60, 1240, mx + 130, 1310], fill=(30, 30, 30))
        d.polygon([(mx - 50, 1250), (mx + 100, 1250), (mx + 80, 1180), (mx - 20, 1190)], fill=(200, 40, 40), outline=BLK)
        d.text((140, 1120), "¡ESPERA!", font=F(34), fill=(40, 40, 40), anchor="mm", stroke_width=4, stroke_fill=WHITE)
        chip(d, "TRABAJO #3: REPARTIDOR", 230, bg=(240, 140, 30), size=52, appear=lt / 0.3)
        return img, 1.0, 1.0
    lt2 = lt - 4.5
    img = grad((230, 220, 200), (200, 185, 160)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(150, 120, 90))
    d.rectangle([640, 500, 1000, 1200], fill=(150, 100, 60), outline=BLK, width=6)
    guy(d, 820, FEET - 120, 0.62, mood="scared" if lt2 > 1.5 else "neutral", look=-1, t=t)
    d.rounded_rectangle([110, 800, 610, 1130], 16, fill=(240, 140, 30), outline=BLK, width=6)
    d.text((360, 845), "ALITAS x12", font=F(48), fill=WHITE, anchor="mm")
    d.rectangle([140, 885, 580, 1100], fill=(255, 240, 220), outline=BLK, width=3)
    if lt2 > 0.8:
        for k in range(int(cl((lt2 - 0.8) / 1.0) * 12)):
            bx, by = 175 + (k % 4) * 100, 920 + (k // 4) * 62
            d.line([(bx, by + 10), (bx + 60, by + 20)], fill=WHITE, width=16)
            for e in ((bx, by + 10), (bx + 60, by + 20)):
                for o in (-8, 8): d.ellipse([e[0] - 11, e[1] + o - 11, e[0] + 11, e[1] + o + 11], fill=WHITE, outline=(170, 170, 170), width=2)
            d.line([(bx, by + 10), (bx + 60, by + 20)], fill=WHITE, width=14)
    if lt2 > 2.0:
        bigtext(d, "12 HUESOS", 370, 720, int(80 * pop((lt2 - 2.0) / 0.3)), fill=RED, stroke=WHITE, sw=8)
        d.text((540, 420), "★★☆☆☆", font=F(90), fill=(250, 190, 30), anchor="mm", stroke_width=5, stroke_fill=BLK)
    return img, 1.0, 1.0

def s_creator(t):
    lt = t - 37.0
    img = grad((60, 40, 80), (120, 70, 130)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(70, 50, 70))
    d.ellipse([140, 420, 940, 1220], outline=(250, 240, 200), width=28)
    if lt < 4.5:
        wolf(d, 540, FEET, 0.8, t, mood="happy", outfit="creator", arms="up")
        views = int(cl(lt / 3.0) ** 2 * 2_400_000)
        chip(d, f"{views:,} VISTAS".replace(",", "."), 330, bg=(30, 30, 40), fg=(100, 255, 150), size=50, appear=1)
    else:
        lt2 = lt - 4.5
        d.rounded_rectangle([150, 380, 930, 1180], 30, fill=(20, 20, 25), outline=(120, 120, 130), width=10)
        d.rectangle([180, 410, 900, 1000], fill=(25, 30, 60))
        moon(d, 760, 520, 70)
        wolf(d, 480, 1100, 0.6, t, mood="smug", outfit="shirt", howl=True)
        d.text((540, 1050), "Subido por: TU EX", font=F(40), fill=WHITE, anchor="mm")
        d.text((540, 1120), "\"aullando a las 3 a.m.\"", font=F(36), fill=(200, 200, 210), anchor="mm")
        if lt2 > 1.8:
            paste_stamp(img, 540, 700, "MONETIZADO", (40, 170, 90), (lt2 - 1.8) / 0.3)
            d = ImageDraw.Draw(img)
    chip(d, "TRABAJO #4: CREADOR DE CONTENIDO", 230, bg=(130, 70, 180), size=48, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_moon(t):
    lt = t - 46.0
    img = night(moon_on=False); d = ImageDraw.Draw(img)
    moon(d, 540, 640, 230)
    if lt > 2.0: xmark(d, 540, 640, 1.6 * pop((lt - 2.0) / 0.3))
    wolf(d, 540, FEET + 60, 0.7, t, mood="sad")
    return img, 1.0, 1.0

def s_deposit(t):
    lt = t - 50.0
    img = grad((225, 215, 200), (195, 180, 160)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(140, 105, 75))
    wolf(d, 300, FEET, 0.75, t, mood="sad", outfit="shirt")
    items = [(0.5, "1 CAMISA", (200, 60, 60)), (1.5, "2 PANTALONES", (60, 80, 140))]
    for i, (st, txt, c) in enumerate(items):
        if lt < st: continue
        sc = pop((lt - st) / 0.3)
        x, y = 760, 760 + i * 200
        d.polygon([(x - 120 * sc, y - 60 * sc), (x + 120 * sc, y - 60 * sc), (x + 90 * sc, y + 60 * sc), (x - 40 * sc, y + 40 * sc), (x - 110 * sc, y + 70 * sc)], fill=c, outline=BLK)
        d.text((x, y + 110 * sc), txt, font=F(max(8, int(40 * sc))), fill=(40, 40, 40), anchor="mm")
    if lt > 3.5:
        paste_stamp(img, 540, 500, "DEPÓSITO: PERDIDO", (200, 30, 30), (lt - 3.5) / 0.3)
        d = ImageDraw.Draw(img)
    chip(d, "EL VERDADERO PROBLEMA", 230, bg=(30, 30, 40), fg=YEL, size=52, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 57.0
    img = night(); d = ImageDraw.Draw(img)
    wolf(d, 540, FEET + 40, 0.9, t, mood="smug", arms="up", howl=(int(lt * 2) % 4 == 0))
    sc = pop(lt / 0.35)
    d.rounded_rectangle([540 - 380 * sc, 330 - 90 * sc, 540 + 380 * sc, 330 + 90 * sc], int(26 * sc), fill=(150, 20, 40), outline=WHITE, width=6)
    d.text((540, 300), "¿DE QUÉ LO PONDRÍAS", font=F(max(8, int(48 * sc))), fill=WHITE, anchor="mm")
    d.text((540, 365), "A TRABAJAR?", font=F(max(8, int(48 * sc))), fill=YEL, anchor="mm")
    if lt > 1.5: chip(d, "COMENTA  ·  SÍGUEME", 500, bg=(30, 30, 40), fg=WHITE, size=48, appear=(lt - 1.5) / 0.3)
    return img, 1.0, 1.0

SCENES = [(0, 3, s_hook), (3, 9, s_cv), (9, 19, s_guard), (19, 28, s_dogs), (28, 37, s_delivery), (37, 46, s_creator),
          (46, 50, s_moon), (50, 57, s_deposit), (57, 99, s_end)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img = r[0]
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce: rich_caption(d, txt, appear=(t - cs) / 0.25)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = 0.3 + 0.7 * fi
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r17.png"); sys.exit()
    from warp17 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(65.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
