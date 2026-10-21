import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, guy, W, H, YEL, RED, WHITE, BLK, SKIN, FEET)

FPS = 30
DUR = 70.0

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img
SKY = grad((90, 60, 140), (240, 150, 120))
SKY_RED = grad((60, 0, 10), (200, 40, 30))
LAB = grad((215, 225, 235), (180, 195, 210))
STREET = grad((120, 180, 235), (250, 220, 170))

# ---------------- criatura ----------------
EYES = [(-0.45, -0.25, 0.16), (0.0, -0.42, 0.2), (0.45, -0.22, 0.15), (-0.2, 0.05, 0.11), (0.25, 0.02, 0.12),
        (-0.62, 0.12, 0.08), (0.65, 0.15, 0.09), (0.05, -0.12, 0.07)]

def creature(d, cx, cy, r, t, mood="neutral", napkin=False):
    body = (110, 60, 170) if mood != "angry" else (150, 30, 60)
    belly = (150, 100, 210) if mood != "angry" else (200, 60, 70)
    if mood == "angry":
        for k in range(4, 0, -1):
            rr = r * (1.05 + 0.06 * k + 0.02 * math.sin(t * 12 + k))
            d.ellipse([cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8], fill=lc((255, 60, 30), (120, 0, 10), k / 4))
    # tentáculos
    tt = 0 if mood == "frozen" else t
    amp = 0.35 if mood == "angry" else 0.12
    for i in range(7):
        bx = cx + (i - 3) * r * 0.26
        pts = []
        for k in range(14):
            s = k / 13
            px = bx + math.sin(tt * (4 if mood == "angry" else 2) + i + s * 4) * r * amp * s
            py = cy + r * 0.55 + s * r * 0.9
            pts.append((px, py))
        for k in range(len(pts) - 1):
            wdt = int(r * 0.16 * (1 - k / 14) + 4)
            d.line([pts[k], pts[k + 1]], fill=body, width=wdt)
            d.ellipse([pts[k][0] - wdt / 2, pts[k][1] - wdt / 2, pts[k][0] + wdt / 2, pts[k][1] + wdt / 2], fill=body)
        for k in range(3, 12, 3):
            d.ellipse([pts[k][0] - r * 0.025, pts[k][1] - r * 0.025, pts[k][0] + r * 0.025, pts[k][1] + r * 0.025], fill=belly)
    d.ellipse([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], fill=body, outline=BLK, width=max(3, int(r * 0.015)))
    d.ellipse([cx - r * 0.7, cy - r * 0.1, cx + r * 0.7, cy + r * 0.72], fill=belly)
    # ojos
    look = 0 if mood == "frozen" else math.sin(t * 0.8) * 0.3
    for i, (ex, ey, es) in enumerate(EYES):
        x, y, rr = cx + ex * r, cy + ey * r, es * r
        if mood == "happy":
            d.arc([x - rr, y - rr * 0.6, x + rr, y + rr], 200, 340, fill=BLK, width=max(3, int(rr * 0.25)))
            continue
        blink = (int(t * 0.7 + i * 0.37) % 9 == 0) and mood not in ("frozen", "angry")
        if blink:
            d.line([(x - rr, y), (x + rr, y)], fill=BLK, width=max(3, int(rr * 0.2))); continue
        big = 1.25 if mood == "frozen" else 1.0
        d.ellipse([x - rr * big, y - rr * big, x + rr * big, y + rr * big], fill=WHITE if mood != "angry" else (255, 220, 200), outline=BLK, width=max(2, int(rr * 0.12)))
        pc = (220, 20, 20) if mood == "angry" else BLK
        pr = rr * (0.3 if mood == "frozen" else 0.45)
        d.ellipse([x + look * rr - pr, y - pr, x + look * rr + pr, y + pr], fill=pc)
        if mood == "angry":
            d.line([(x - rr * 1.2, y - rr * 1.3 - (1 if ex < 0 else -1) * rr * 0.4), (x + rr * 1.2, y - rr * 1.3 + (1 if ex < 0 else -1) * rr * 0.4)], fill=BLK, width=max(3, int(rr * 0.3)))
    # boca
    my = cy + r * 0.38
    if mood == "angry":
        d.rectangle([cx - r * 0.35, my - r * 0.05, cx + r * 0.35, my + r * 0.18], fill=(40, 0, 10), outline=BLK, width=4)
        for k in range(7):
            x0 = cx - r * 0.35 + k * r * 0.1
            d.polygon([(x0, my - r * 0.05), (x0 + r * 0.1, my - r * 0.05), (x0 + r * 0.05, my + r * 0.05)], fill=WHITE)
            d.polygon([(x0, my + r * 0.18), (x0 + r * 0.1, my + r * 0.18), (x0 + r * 0.05, my + r * 0.09)], fill=WHITE)
    elif mood == "happy":
        d.chord([cx - r * 0.3, my - r * 0.12, cx + r * 0.3, my + r * 0.22], 0, 180, fill=(60, 10, 40), outline=BLK, width=4)
        for sx in (-1, 1):
            d.ellipse([cx + sx * r * 0.55 - r * 0.1, cy - r * 0.02, cx + sx * r * 0.55 + r * 0.1, cy + r * 0.08], fill=(240, 120, 160))
    elif mood == "curious":
        d.ellipse([cx - r * 0.06, my - r * 0.05, cx + r * 0.06, my + r * 0.07], fill=(60, 10, 40), outline=BLK, width=3)
    elif mood == "frozen":
        d.line([(cx - r * 0.12, my), (cx + r * 0.12, my)], fill=BLK, width=max(3, int(r * 0.02)))
    else:
        d.arc([cx - r * 0.2, my - r * 0.08, cx + r * 0.2, my + r * 0.08], 20, 160, fill=BLK, width=max(3, int(r * 0.02)))
    if napkin:
        d.polygon([(cx - r * 0.3, my + r * 0.22), (cx + r * 0.3, my + r * 0.22), (cx, my + r * 0.62)], fill=WHITE, outline=BLK)

def bubble(d, x, y, text, size=52, tail=None, maxw=760, fill=WHITE, fg=BLK):
    f = F(size); words = text.split(); lines = []; cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = test
    lines.append(cur)
    lw = max(d.textlength(l, font=f) for l in lines); lh = size * 1.2
    bw, bh = lw + size * 1.2, lh * len(lines) + size * 0.8
    x0, y0 = x - bw / 2, y - bh / 2
    edge = (y + bh / 2 - 4) if (tail and tail[1] > y) else (y - bh / 2 + 4)
    tx0 = min(max(tail[0], x0 + 60), x0 + bw - 60) if tail else x
    if tail:
        d.polygon([(tx0 - 30, edge), (tx0 + 30, edge), tail], fill=fill, outline=BLK)
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], int(size * 0.6), fill=fill, outline=BLK, width=5)
    if tail:
        d.line([(tx0 - 26, edge), (tx0 + 26, edge)], fill=fill, width=10)
    for i, l in enumerate(lines):
        d.text((x, y0 + size * 0.4 + lh * i + lh / 2), l, font=f, fill=fg, anchor="mm")

def skyline(d, y, s=1.0, col=(50, 40, 80)):
    rng = random.Random(5)
    x = -20
    while x < W:
        w = rng.randint(50, 110) * s; h = rng.randint(60, 220) * s
        d.rectangle([x, y - h, x + w, y], fill=col)
        for wy in range(int(y - h + 14), int(y - 10), 26):
            for wx in range(int(x + 10), int(x + w - 10), 24):
                if rng.random() < 0.5: d.rectangle([wx, wy, wx + 10, wy + 12], fill=(255, 220, 120))
        x += w + 6
    d.rectangle([0, y, W, H], fill=(40, 35, 55))

def portal(d, cx, cy, r, t):
    for k in range(8, 0, -1):
        rr = r * k / 8
        d.ellipse([cx - rr * 1.6, cy - rr * 0.5, cx + rr * 1.6, cy + rr * 0.5], fill=lc((255, 240, 255), (90, 20, 140), k / 8))

def tank(d, x, y, s, t):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(130), y - S(70), x + S(130), y], S(30), fill=(90, 110, 60), outline=BLK, width=4)
    d.rounded_rectangle([x - S(60), y - S(120), x + S(60), y - S(60)], S(20), fill=(110, 130, 70), outline=BLK, width=4)
    ang = -0.5 + 0.1 * math.sin(t * 2)
    d.line([(x, y - S(95)), (x + math.cos(ang) * S(190), y - S(95) + math.sin(ang) * S(190))], fill=(70, 85, 45), width=int(S(22)))
    for k in range(5): d.ellipse([x - S(110) + k * S(55), y - S(25), x - S(70) + k * S(55), y + S(15)], fill=(40, 40, 40))

def taquero(d, x, y, s, t, mood="neutral", arms="down"):
    guy(d, x, y, s, mood=mood, arms=arms, t=t, hoodie=(245, 245, 245))
    S = lambda v: v * s
    hx, hy = x, y - S(505)
    d.chord([hx - S(104), hy - S(112), hx + S(104), hy + S(40)], 180, 360, fill=(200, 40, 40))
    d.rounded_rectangle([hx - S(10), hy - S(40), hx + S(150), hy - S(20)], S(10), fill=(170, 30, 30))
    d.rounded_rectangle([x - S(80), y - S(330), x + S(80), y - S(150)], S(20), fill=(250, 250, 250), outline=(200, 200, 200), width=3)

def president(d, x, y, s, t):
    guy(d, x, y, s, mood="neutral", arms="push", t=t, hoodie=(40, 45, 70))
    S = lambda v: v * s
    d.polygon([(x - S(30), y - S(410)), (x + S(30), y - S(410)), (x, y - S(380))], fill=WHITE)
    d.polygon([(x - S(12), y - S(395)), (x + S(12), y - S(395)), (x + S(18), y - S(270)), (x, y - S(250)), (x - S(18), y - S(270))], fill=(200, 30, 40))
    d.line([(x - S(90), y - S(400)), (x + S(90), y - S(170))], fill=(20, 120, 60), width=int(S(26)))
    # charola con oro y misil
    tx, ty = x + S(185), y - S(300)
    d.rounded_rectangle([tx - S(150), ty - S(10), tx + S(150), ty + S(14)], S(8), fill=(200, 200, 210), outline=BLK, width=3)
    for k in range(3):
        d.polygon([(tx - S(130) + k * S(55), ty - S(10)), (tx - S(85) + k * S(55), ty - S(10)), (tx - S(92) + k * S(55), ty - S(42)), (tx - S(123) + k * S(55), ty - S(42))], fill=(240, 190, 40), outline=BLK)
    d.rounded_rectangle([tx + S(40), ty - S(150), tx + S(80), ty - S(10)], S(16), fill=(220, 220, 225), outline=BLK, width=3)
    d.polygon([(tx + S(40), ty - S(150)), (tx + S(80), ty - S(150)), (tx + S(60), ty - S(195))], fill=RED, outline=BLK)

def scientist(d, x, y, s, t, mood="neutral"):
    guy(d, x, y, s, mood=mood, t=t, hoodie=(240, 240, 240))
    S = lambda v: v * s
    hx, hy = x, y - S(500)
    for sx in (-1, 1):
        d.ellipse([hx + sx * S(38) - S(32), hy - S(27), hx + sx * S(38) + S(32), hy + S(37)], outline=BLK, width=int(S(7)))
    d.line([(hx - S(6), hy + S(5)), (hx + S(6), hy + S(5))], fill=BLK, width=int(S(6)))

def trompo(d, x, y, s, t, k_pastor=1.0, pineapple=True):
    S = lambda v: v * s
    d.line([(x, y - S(470)), (x, y + S(20))], fill=(120, 120, 130), width=int(S(14)))
    meat = lc((200, 170, 120), (205, 80, 40), k_pastor)
    for i in range(12):
        yy = y - S(60) - i * S(30)
        w = S(70) + math.sin(i / 11 * math.pi) * S(45)
        d.rounded_rectangle([x - w, yy - S(30), x + w, yy], S(10), fill=dk(meat, 0.9 + 0.1 * (i % 2)), outline=dk(meat, 0.7), width=2)
    if pineapple and k_pastor > 0.5:
        d.ellipse([x - S(45), y - S(470), x + S(45), y - S(390)], fill=(240, 200, 40), outline=BLK, width=3)
        for a in (-0.6, -0.2, 0.2, 0.6):
            d.polygon([(x, y - S(460)), (x + a * S(80), y - S(540)), (x + a * S(40), y - S(470))], fill=(60, 160, 60))
    d.rectangle([x - S(70), y + S(10), x + S(70), y + S(40)], fill=(80, 80, 90))

def taco(d, x, y, s):
    S = lambda v: v * s
    d.chord([x - S(60), y - S(60), x + S(60), y + S(60)], 180, 360, fill=(240, 210, 140), outline=BLK, width=3)
    d.ellipse([x - S(45), y - S(30), x + S(45), y + S(5)], fill=(205, 80, 40))
    d.ellipse([x - S(10), y - S(40), x + S(10), y - S(25)], fill=(240, 200, 40))
    d.ellipse([x + S(15), y - S(35), x + S(30), y - S(22)], fill=(60, 160, 60))

def confetti(d, t, n=60):
    rng = random.Random(7)
    for i in range(n):
        x = rng.uniform(0, W); sp = rng.uniform(200, 400)
        y = (rng.uniform(-H, 0) + t * sp) % H
        c = rng.choice([(255, 214, 0), (225, 35, 45), (60, 160, 230), (60, 180, 90), (240, 120, 200)])
        d.rectangle([x, y, x + 14, y + 24], fill=c)

def card(d, cx, cy, s, ang=0.0):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(160), cy - S(100), cx + S(160), cy + S(100)], S(22), fill=(230, 180, 40), outline=BLK, width=6)
    d.rounded_rectangle([cx - S(120), cy - S(40), cx - S(60), cy + S(5)], S(8), fill=(200, 200, 205), outline=BLK, width=3)
    for k in range(4): d.rectangle([cx - S(120) + k * S(62), cy + S(40), cx - S(80) + k * S(62), cy + S(55)], fill=(120, 90, 20))
    d.text((cx + S(60), cy - S(55)), "TARJETA", font=F(S(34)), fill=(120, 90, 20), anchor="mm")

def land(d, flood=0.0):
    d.rectangle([0, 0, W, H], fill=(60, 130, 200))
    for (x, y, rx, ry) in [(330, 700, 240, 300), (720, 640, 200, 200), (620, 1020, 260, 180), (280, 1100, 140, 120)]:
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(110, 180, 90), outline=(70, 130, 60), width=6)
    for i, (x, y) in enumerate([(330, 640), (700, 650), (600, 1030)]):
        if flood > i / 3 + 0.05:
            k = cl((flood - i / 3) * 3)
            d.ellipse([x - 150 * k, y - 120 * k, x + 150 * k, y + 120 * k], fill=(70, 150, 225))
            d.text((x, y), "≈≈≈", font=F(50), fill=WHITE, anchor="mm")

CAPS = [
    (0.0, 5.0, "¿Qué pasaría si una entidad de *800 kilómetros* apareciera sobre la Tierra?"),
    (5.0, 10.0, "Los ejércitos se movilizan. Las bolsas colapsan. Anuncian *el fin de la humanidad*"),
    (10.0, 14.0, "Tras horas de análisis, descifran su mensaje…"),
    (14.0, 19.0, "Apareció justo encima de *la Narvarte*… lo mejor que se nos ocurrió fue: *tacos*"),
    (19.0, 22.0, "El presidente le ofrece *oro, petróleo y armas nucleares*"),
    (22.0, 25.0, "La criatura responde…"),
    (25.0, 30.0, "Un *taquero de la colonia* sube con una orden de pastor…"),
    (30.0, 35.0, "…la criatura se queda inmóvil y derrama una lágrima que *inunda tres países*"),
    (35.0, 39.0, "Y dice…"),
    (39.0, 41.0, "Todo iba bien… hasta que preguntó *si aceptaban tarjeta*"),
    (41.0, 43.0, "\"Solo efectivo, joven.\""),
    (43.0, 46.0, "Y ahí sí… *se enojó*"),
    (46.0, 50.0, "*Dato real:* el taco al pastor nació del *shawarma* de inmigrantes *libaneses*"),
    (50.0, 55.0, "Lo inquietante: la *teoría de cuerdas* propone que podría haber *más dimensiones*"),
    (55.0, 61.0, "Y algunos físicos hablan de *multiversos*. Nada está comprobado… ¿y si alguien del otro lado *tiene hambre*?"),
    (61.0, 65.0, "Qué *bendecidos* somos de tener *tacos* en nuestro universo"),
    (65.0, 90.0, "¿Tú qué le habrías servido? *Te leo en los comentarios*"),
]

def street_sign(d, x, y, text):
    d.rectangle([x - 8, y, x + 8, y + 420], fill=(90, 90, 95))
    d.rounded_rectangle([x - 230, y - 70, x + 230, y + 50], 14, fill=(30, 110, 70), outline=WHITE, width=6)
    d.text((x, y - 36), "COL.", font=F(34), fill=WHITE, anchor="mm")
    d.text((x, y + 8), text, font=F(64), fill=WHITE, anchor="mm")

def render(v, t=None):
    if t is None: t = v
    shake = 0
    if v < 5.0:
        img = SKY.copy(); d = ImageDraw.Draw(img)
        portal(d, 540, 150, 420, t)
        k = ease(v / 3.0)
        creature(d, 540, lerp(-300, 520, k), 470, t, "neutral")
        skyline(d, 1380, 0.8)
        if v > 1.2:
            chip(d, f"TAMAÑO: {int(800 * cl((v - 1.2) / 1.2))} KM", 1060, bg=RED, appear=(v - 1.2) / 0.3)
    elif v < 10.0:
        lt = v - 5.0
        img = SKY.copy(); d = ImageDraw.Draw(img)
        creature(d, 540, 330, 420, t, "neutral")
        skyline(d, 1380, 0.8)
        if lt < 1.7:
            for i, x in enumerate((220, 540, 860)): tank(d, x, 1360, 0.9, t + i)
            chip(d, "EJÉRCITOS EN ALERTA", 880, bg=(90, 110, 60), appear=lt / 0.3)
        elif lt < 3.4:
            d.rounded_rectangle([140, 820, 940, 1320], 30, fill=(20, 24, 30), outline=WHITE, width=6)
            k = cl((lt - 1.7) / 1.2)
            pts = [(180 + i * 35, min(1290, 900 + (i * 7 if i < 10 else 70 + (i - 10) ** 2 * 6 * k))) for i in range(21)]
            d.line(pts, fill=(255, 60, 60), width=12)
            d.text((540, 870), "BOLSA  ▼ -99%", font=F(60), fill=(255, 80, 80), anchor="mm")
        else:
            scientist(d, 480, 1380, 0.85, t, "scared")
            d.line([(700, 1130), (595, 1206)], fill=(120, 80, 40), width=14)
            d.ellipse([573, 1184, 617, 1228], fill=SKIN)
            d.rounded_rectangle([600, 1000, 940, 1130], 16, fill=WHITE, outline=BLK, width=6)
            d.text((770, 1065), "EL FIN", font=F(70), fill=RED, anchor="mm")
    elif v < 14.0:
        lt = v - 10.0
        img = LAB.copy(); d = ImageDraw.Draw(img)
        d.rectangle([0, 1250, W, H], fill=(150, 160, 175))
        d.rounded_rectangle([170, 300, 910, 760], 30, fill=(20, 30, 40), outline=(90, 100, 120), width=12)
        for i in range(60):
            x = 210 + i * 11.5
            a = math.sin(i * 0.7 + t * 6) * (40 + 60 * abs(math.sin(i * 0.3)))
            d.line([(x, 530 - a), (x, 530 + a)], fill=(80, 230, 140), width=6)
        d.text((540, 340), "SEÑAL INTERDIMENSIONAL", font=F(34), fill=(80, 230, 140), anchor="mm")
        scientist(d, 300, 1390, 0.75, t, "neutral" if lt < 2 else "scared")
        scientist(d, 780, 1390, 0.75, t + 1, "neutral" if lt < 2 else "scared")
        if lt > 1.8:
            bubble(d, 540, 850, "TRADUCCIÓN: \"Estoy hambriento.\"", size=56, maxw=800, fill=(255, 245, 200))
    elif v < 19.0:
        lt = v - 14.0
        img = STREET.copy(); d = ImageDraw.Draw(img)
        creature(d, 540, 200, 420, t, "curious")
        d.rectangle([0, 1180, W, H], fill=(120, 110, 100))
        street_sign(d, 540, 720, "NARVARTE")
        for i, x in enumerate((60, 400, 740)):
            d.rounded_rectangle([x, 1000, x + 280, 1190], 14, fill=[(200, 60, 50), (40, 120, 200), (240, 170, 40)][i], outline=BLK, width=5)
            d.rectangle([x, 1000, x + 280, 1040], fill=(245, 245, 245))
            d.text((x + 140, 1110), "TACOS", font=F(52), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
        if lt > 2.3:
            chip(d, "MEJOR IDEA: TACOS", 880, bg=(30, 140, 80), appear=(lt - 2.3) / 0.3)
    elif v < 25.0:
        lt = v - 19.0
        img = SKY.copy(); d = ImageDraw.Draw(img)
        creature(d, 540, 330, 400, t, "neutral" if lt < 3.0 else "curious")
        skyline(d, 1380, 0.8)
        president(d, 380, 1390, 0.8, t)
        if lt > 3.0:
            bubble(d, 560, 830, "¿Pero tienen salsa verde?", size=58, tail=(560, 660))
    elif v < 30.0:
        lt = v - 25.0
        img = STREET.copy(); d = ImageDraw.Draw(img)
        k = ease(lt / 4.0)
        creature(d, 540, lerp(-60, 120, k), 420, t, "curious")
        d.rectangle([0, 1250, W, H], fill=(120, 110, 100))
        trompo(d, 830, 1030, 0.75, t)
        gx = 600; gy = lerp(880, 620, ease((lt - 1.0) / 3.0))
        d.line([(gx, 0), (gx, gy - 40)], fill=(60, 60, 60), width=6)
        d.rounded_rectangle([gx - 150, gy - 40, gx + 150, gy], 16, fill=WHITE, outline=BLK, width=5)
        for i in range(3): taco(d, gx - 90 + i * 90, gy - 40, 0.6)
        taquero(d, 340, 1200, 0.62, t, "neutral", "push")
        d.rounded_rectangle([90, 1040, 990, 1260], 20, fill=(200, 60, 50), outline=BLK, width=6)
        d.rectangle([90, 1040, 990, 1080], fill=(240, 240, 240))
        d.text((540, 1150), "TAQUERÍA LA COLONIA", font=F(54), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    elif v < 35.0:
        lt = v - 30.0
        if lt < 3.0:
            img = SKY.copy(); d = ImageDraw.Draw(img)
            creature(d, 540, 420, 420, t, "frozen")
            if lt > 0.8:
                ex, ey = 540 + 0.45 * 420, 420 - 0.22 * 420
                ty = ey + 60 + ease((lt - 0.8) / 2.0) * 800
                d.ellipse([ex - 40, ty - 40, ex + 40, ty + 50], fill=(120, 200, 255), outline=(40, 120, 200), width=5)
                d.polygon([(ex - 36, ty - 15), (ex + 36, ty - 15), (ex, ty - 90)], fill=(120, 200, 255))
            skyline(d, 1380, 0.8)
        else:
            img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
            land(d, cl((lt - 3.0) / 1.6))
            chip(d, "3 PAÍSES INUNDADOS", 300, bg=(40, 120, 200), appear=(lt - 3.2) / 0.3)
    elif v < 39.0:
        lt = v - 35.0
        img = SKY.copy(); d = ImageDraw.Draw(img)
        confetti(d, t)
        creature(d, 540, 400, 400, t, "happy")
        skyline(d, 1380, 0.8)
        bubble(d, 540, 960, "Está bueno… ¿me da 5 de pastor y 1 de suadero?", size=52, maxw=780, tail=(540, 780))
        chip(d, "LA HUMANIDAD HA SOBREVIVIDO ✓", 1300, bg=(30, 140, 80), size=46, appear=(lt - 1.0) / 0.3)
    elif v < 46.0:
        lt = v - 39.0
        angry = lt >= 4.0
        img = (SKY_RED if angry else SKY).copy(); d = ImageDraw.Draw(img)
        creature(d, 540, 400, 400, t, "angry" if angry else "happy")
        body = (150, 30, 60) if angry else (110, 60, 170)
        wob = math.sin(t * (8 if angry else 2)) * (14 if angry else 6)
        card(d, 880, 790 + wob, 0.8)
        ctrl = [(850, 560), (1040, 600), (1000, 700), (930, 720 + wob)]
        pts = []
        for i in range(21):
            u = i / 20
            x = (1-u)**3*ctrl[0][0] + 3*(1-u)**2*u*ctrl[1][0] + 3*(1-u)*u*u*ctrl[2][0] + u**3*ctrl[3][0]
            y = (1-u)**3*ctrl[0][1] + 3*(1-u)**2*u*ctrl[1][1] + 3*(1-u)*u*u*ctrl[2][1] + u**3*ctrl[3][1]
            pts.append((x, y))
        for k in range(20):
            wd = int(54 - k * 1.6)
            d.line([pts[k], pts[k + 1]], fill=body, width=wd)
            d.ellipse([pts[k][0] - wd / 2, pts[k][1] - wd / 2, pts[k][0] + wd / 2, pts[k][1] + wd / 2], fill=body)
        tx, ty = pts[-1]
        d.ellipse([tx - 24, ty - 16, tx + 24, ty + 16], fill=body, outline=BLK, width=3)
        d.rectangle([0, 1250, W, H], fill=(120, 110, 100) if not angry else (90, 40, 40))
        taquero(d, 330, 1240, 0.55, t, "neutral" if not angry else "scared")
        d.rounded_rectangle([90, 1100, 600, 1260], 20, fill=(200, 60, 50), outline=BLK, width=6)
        if lt < 2.0:
            bubble(d, 540, 960, "¿Aceptan tarjeta?", size=56, tail=(560, 780))
        elif lt < 4.0:
            bubble(d, 420, 800, "Solo efectivo, joven.", size=54, tail=(330, 880), fill=(255, 245, 200))
        else:
            shake = 14
            chip(d, "AHORA SÍ: FIN DEL MUNDO", 1350, bg=BLK, fg=RED, size=58, appear=(lt - 4.1) / 0.3)
            for k in range(6):
                a = t * 3 + k
                x = 540 + math.cos(a) * 520; y = 900 + math.sin(a * 1.3) * 300
                d.line([(x, y), (x + 40, y - 120), (x - 10, y - 140), (x + 30, y - 260)], fill=(255, 230, 120), width=10)
    elif v < 50.0:
        lt = v - 46.0
        img = Image.new("RGB", (W, H), (245, 235, 215)); d = ImageDraw.Draw(img)
        if lt < 2.0:
            d.rectangle([0, 0, W, H], fill=(150, 200, 235))
            d.ellipse([-200, 420, 520, 1100], fill=(200, 190, 140), outline=(150, 140, 100), width=6)
            d.ellipse([620, 300, 1240, 760], fill=(200, 190, 140), outline=(150, 140, 100), width=6)
            p1, p2 = (900, 520), (260, 760)
            for i in range(20):
                s = i / 20
                if s > ease(lt / 1.4): break
                x = lerp(p1[0], p2[0], s); y = lerp(p1[1], p2[1], s) - math.sin(s * math.pi) * 220
                d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED)
            for (x, y), name in ((p1, "LÍBANO"), (p2, "PUEBLA")):
                d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=YEL, outline=BLK, width=5)
                d.text((x, y + 60), name, font=F(54), fill=BLK, anchor="mm", stroke_width=5, stroke_fill=WHITE)
            chip(d, "SHAWARMA → TACOS ÁRABES", 300, bg=(40, 90, 160), appear=lt / 0.3)
        else:
            k = ease((lt - 2.0) / 1.2)
            trompo(d, 540, 1220, 1.2, t, k_pastor=k, pineapple=True)
            chip(d, "→ TACOS AL PASTOR", 300, bg=(200, 80, 40), size=50)
            if k > 0.9: bigtext(d, "+ PIÑA + ADOBO", 540, 440, 70, fill=YEL)
    elif v < 61.0:
        lt = v - 50.0
        from reel13 import SPACE
        img = SPACE.copy(); d = ImageDraw.Draw(img)
        if lt < 5.0:
            for i in range(5):
                y0 = 560 + i * 150
                pts = [(x, y0 + math.sin(x * 0.02 + t * (3 + i) + i) * (40 + 15 * i) * math.sin(math.pi * x / W)) for x in range(80, 1001, 10)]
                d.line(pts, fill=lc((120, 220, 255), (255, 120, 220), i / 4), width=8)
            chip(d, "TEORÍA DE CUERDAS", 300, bg=(60, 80, 180), appear=lt / 0.3)
            if lt > 1.5: bigtext(d, "¿MÁS DIMENSIONES?", 540, 420, 70, fill=WHITE)
        else:
            k = ease((lt - 5.0) / 1.5)
            rng = random.Random(11)
            bubs = [(rng.uniform(160, 920), rng.uniform(560, 1180), rng.uniform(70, 140)) for _ in range(9)]
            for i, (x, y, r) in enumerate(bubs):
                rr = r * k
                if rr < 2: continue
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=lc((30, 30, 70), (70, 40, 110), i / 8), outline=(170, 180, 255), width=4)
                for j in range(6):
                    sx, sy = x + math.cos(j * 1.7 + i) * rr * 0.5, y + math.sin(j * 2.3 + i) * rr * 0.5
                    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=WHITE)
            x, y, r = bubs[4]
            if lt > 9.0:
                creature(d, x, y + r * 0.15, r * 0.55, t, "curious")
                for sx in (-1, 1):
                    hx = x + sx * r * 0.75
                    d.line([(hx, y - r * 0.2), (hx, y + r * 0.45)], fill=(200, 200, 210), width=8)
            chip(d, "¿MULTIVERSOS?", 300, bg=(140, 60, 170), appear=(lt - 5.0) / 0.3)
            if lt > 8.0: chip(d, "NADA COMPROBADO… AÚN", 420, bg=BLK, size=44, appear=(lt - 8.0) / 0.3)
    elif v < 65.0:
        lt = v - 61.0
        from reel13 import SPACE, earth
        img = SPACE.copy(); d = ImageDraw.Draw(img)
        for k in range(6, 0, -1):
            rr = 260 + k * 40 + 10 * math.sin(t * 2 + k)
            d.ellipse([540 - rr, 760 - rr, 540 + rr, 760 + rr], fill=lc((255, 240, 170), (40, 30, 80), k / 6))
        a = t * 1.5
        if math.sin(a) < 0: taco(d, 540 + math.cos(a) * 400, 760 + math.sin(a) * 160, 1.4)
        earth(d, 540, 760, 240)
        for sx in (-1, 1):
            d.ellipse([540 + sx * 80 - 26, 720 - 30, 540 + sx * 80 + 26, 720 + 30], fill=WHITE, outline=BLK, width=4)
            d.arc([540 + sx * 80 - 22, 712, 540 + sx * 80 + 22, 742], 200, 340, fill=BLK, width=7)
        d.arc([480, 780, 600, 860], 20, 160, fill=BLK, width=9)
        if math.sin(a) >= 0: taco(d, 540 + math.cos(a) * 400, 760 + math.sin(a) * 160, 1.4)
        rng = random.Random(3)
        for i in range(24):
            x, y = rng.uniform(80, 1000), rng.uniform(300, 1250)
            if (int(t * 4) + i) % 3 == 0:
                d.polygon([(x, y - 18), (x + 6, y), (x, y + 18), (x - 6, y)], fill=YEL); d.polygon([(x - 18, y), (x, y - 6), (x + 18, y), (x, y + 6)], fill=YEL)
        chip(d, "BENDECIDOS CON TACOS", 300, bg=(200, 120, 20), appear=(lt - 0.3) / 0.3)
    else:
        lt = v - 65.0
        img = STREET.copy(); d = ImageDraw.Draw(img)
        creature(d, 540, 640, 330, t, "happy", napkin=True)
        d.rectangle([0, 1080, W, H], fill=(120, 80, 50))
        d.rectangle([0, 1080, W, 1110], fill=(150, 100, 60))
        for i in range(3): taco(d, 380 + i * 160, 1070, 1.0)
        bigtext(d, "¿TÚ QUÉ LE HABRÍAS", 540, 200, 70, fill=WHITE)
        bigtext(d, "SERVIDO?", 540, 290, 80, fill=YEL)
        if lt > 2.0:
            sc = pop((lt - 2.0) / 0.35)
            d.rounded_rectangle([540 - 330 * sc, 1250 - 80 * sc, 540 + 330 * sc, 1250 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
            d.text((540, 1250), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
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
        sheet.save("sheet_r24.png"); sys.exit()
    try:
        from warp24 import v_of_T, DUR as D2
    except ImportError:
        v_of_T = lambda T: T; D2 = DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(D2 * FPS)):
        p.stdin.write(render(v_of_T(i / FPS), i / FPS).tobytes())
    p.stdin.close(); p.wait()
