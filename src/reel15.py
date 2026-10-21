import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)

FPS = 30
FEET = 1380
AL = (175, 225, 165)

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def office(night=False):
    img = grad((215, 225, 232), (190, 200, 210)) if not night else grad((30, 35, 60), (50, 55, 80))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(150, 150, 160) if not night else (60, 60, 75))
    d.rectangle([660, 280, 980, 600], fill=(150, 200, 235) if not night else (15, 20, 45), outline=(240, 240, 240), width=12)
    for k in range(1, 4): d.line([(660 + k * 80, 280), (660 + k * 80, 600)], fill=(240, 240, 240), width=5)
    d.ellipse([90, 320, 230, 460], fill=WHITE, outline=BLK, width=6)
    d.line([(160, 390), (160, 345)], fill=BLK, width=6); d.line([(160, 390), (195, 400)], fill=BLK, width=6)
    return img

def alien_cw(d, x, y, s=1.0, t=0.0, mood="blank", arms="down", blink=False, antenna=True):
    S = lambda v: v * s
    d.ellipse([x - S(120), y - S(16), x + S(120), y + S(16)], fill=(70, 72, 75))
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx * S(10) - (S(55) if sx < 0 else 0), y - S(190), x + sx * S(10) + (S(55) if sx > 0 else 0), y - S(10)], int(S(18)), fill=(60, 65, 80))
        d.ellipse([x + sx * S(45) - S(45), y - S(40), x + sx * S(45) + S(45), y + S(4)], fill=(25, 25, 30))
    suit = (90, 100, 120)
    def arm(sx, hx, hy):
        d.line([(x + sx * S(90), y - S(390)), (hx, hy)], fill=dk(suit, 0.85), width=int(S(40)), joint="curve")
        d.ellipse([hx - S(24), hy - S(24), hx + S(24), hy + S(24)], fill=AL)
    if arms == "up": arm(1, x + S(160), y - S(600))
    d.rounded_rectangle([x - S(100), y - S(420), x + S(100), y - S(170)], int(S(45)), fill=suit, outline=BLK, width=4)
    d.polygon([(x - S(35), y - S(420)), (x + S(35), y - S(420)), (x, y - S(330))], fill=WHITE)
    d.polygon([(x - S(12), y - S(400)), (x + S(12), y - S(400)), (x + S(16), y - S(270)), (x, y - S(250)), (x - S(16), y - S(270))], fill=(60, 170, 90))
    if arms == "down": arm(-1, x - S(130), y - S(200)); arm(1, x + S(130), y - S(200))
    elif arms == "up": arm(-1, x - S(130), y - S(200))
    elif arms == "desk": arm(-1, x - S(80), y - S(250)); arm(1, x + S(80), y - S(250))
    hx, hy = x, y - S(510)
    if antenna:
        for sx in (-1, 1):
            ax = hx + sx * S(30)
            d.line([(ax, hy - S(90)), (ax + sx * S(20), hy - S(150) + math.sin(t * 6 + sx) * S(6))], fill=(80, 140, 80), width=max(2, int(S(6))))
            d.ellipse([ax + sx * S(20) - S(10), hy - S(160) - S(10) + math.sin(t * 6 + sx) * S(6), ax + sx * S(20) + S(10), hy - S(160) + S(10) + math.sin(t * 6 + sx) * S(6)], fill=(250, 220, 80))
    d.ellipse([hx - S(110), hy - S(115), hx + S(110), hy + S(95)], fill=AL, outline=BLK, width=3)
    d.chord([hx - S(112), hy - S(122), hx + S(112), hy - S(10)], 180, 360, fill=(40, 40, 45))
    d.line([(hx - S(10), hy - S(118)), (hx - S(20), hy - S(30))], fill=(70, 70, 75), width=max(2, int(S(5))))
    for sx in (-1, 1):
        ex, ey = hx + sx * S(42), hy + S(10)
        if blink:
            d.line([(ex - S(32), ey), (ex + S(32), ey)], fill=BLK, width=max(2, int(S(6))))
        else:
            d.polygon([(ex - S(36), ey - S(6) + sx * 0), (ex - S(6) * sx, ey - S(26)), (ex + S(36), ey + S(4)), (ex + S(6) * sx, ey + S(26))], fill=(15, 15, 25))
            d.ellipse([ex - S(10), ey - S(16), ex + S(2), ey - S(4)], fill=WHITE)
    my = hy + S(60)
    if mood == "smile":
        d.arc([hx - S(45), my - S(30), hx + S(45), my + S(15)], 20, 160, fill=BLK, width=max(2, int(S(5))))
    else:
        d.line([(hx - S(25), my), (hx + S(25), my)], fill=BLK, width=max(2, int(S(5))))

TT = 1210  # table top; legs reach the characters' feet (FEET)

def desk(d, x0, x1, y=None):
    top = TT
    for x in (x0 + 40, x1 - 40):
        d.rectangle([x - 18, top + 40, x + 18, FEET], fill=(120, 85, 55), outline=BLK, width=3)
    d.rectangle([x0, top, x1, top + 40], fill=(150, 110, 75), outline=BLK, width=5)
    d.rectangle([x0 + 20, top + 40, x1 - 20, top + 60], fill=(120, 85, 55), outline=BLK, width=3)

def bubble(d, cx, cy, w, h, lines, size=44, tail=None, col=WHITE, a=1.0):
    if a <= 0: return
    w, h = w * pop(a), h * pop(a)
    if w < 10: return
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 30, fill=col, outline=BLK, width=5)
    if tail: d.polygon([(cx + tail[0] - 20, cy + h / 2 - 3), (cx + tail[0] + 20, cy + h / 2 - 3), (cx + tail[0] + tail[1], cy + h / 2 + 60)], fill=col, outline=BLK)
    n = len(lines)
    for i, ln in enumerate(lines):
        d.text((cx, cy - (n - 1) * size * 0.6 + i * size * 1.2), ln, font=F(max(8, int(size * pop(a)))), fill=(30, 30, 30), anchor="mm")

def blob(d, cx, cy, r, t):
    pts = []
    for k in range(24):
        a = k / 24 * 2 * math.pi
        rr = r * (1 + 0.12 * math.sin(a * 3 + t * 6) + 0.08 * math.sin(a * 5 - t * 4))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.7))
    d.polygon(pts, fill=(90, 200, 70), outline=(40, 120, 40))
    for sx in (-1, 1):
        d.ellipse([cx + sx * r * 0.3 - 14, cy - r * 0.2 - 14, cx + sx * r * 0.3 + 14, cy - r * 0.2 + 14], fill=WHITE, outline=BLK, width=2)
        d.ellipse([cx + sx * r * 0.3 - 5, cy - r * 0.2 - 5, cx + sx * r * 0.3 + 5, cy - r * 0.2 + 5], fill=BLK)

CAPS = [
    (0.0, 5.0, "¿Tu compañero de trabajo es un *alienígena infiltrado*? Vigila estas *señales*"),
    (5.0, 9.0, "*#1: nunca come.* Siempre \"ya comió\"… *nunca lo ves masticar*"),
    (9.0, 12.0, "Y cuando trae comida… *es una sustancia verde que se mueve sola*"),
    (12.0, 17.0, "*#2: no entiende el sarcasmo*"),
    (17.0, 22.0, "\"¿Y si mejor la *teletransportamos*?\""),
    (22.0, 24.0, "Lo peor: *tiene razón*"),
    (24.0, 30.0, "*#3: nunca se enferma.* Todos con gripe… él *3 días bajo el aire acondicionado*"),
    (30.0, 36.0, "\"Mi sistema inmunológico fue diseñado *para el vacío*\"… *qué envidia*"),
    (36.0, 41.0, "*#4: sabe demasiado.* Tu *tarjeta*, tu *ex*…"),
    (41.0, 46.0, "…y *cuánto ganas*, aunque *ni Recursos Humanos* te lo dice"),
    (46.0, 53.0, "*#5: nunca se desconecta.* 11 p.m., 3 a.m., 5 a.m.… *en línea*"),
    (53.0, 58.0, "Llegas a la oficina: *en tu lugar*… *con tu café*"),
    (58.0, 64.0, "*Señal definitiva:* el jefe pide *horas extra sin cobrar*…"),
    (64.0, 70.0, "\"No duermo, no siento estrés y *mi especie no reconoce los derechos laborales*\""),
    (70.0, 76.0, "No es un alienígena… *es el empleado ideal de tu empresa*"),
    (76.0, 86.0, "¿Lo *denuncias*… o le pides que *te recomiende para su planeta*?"),
]

def s_hook(t):
    img = office(); d = ImageDraw.Draw(img)
    alien_cw(d, 640, FEET, 0.9, t, arms="desk", blink=(int(t * 10) % 37 == 0))
    desk(d, 380, 1000)
    d.rectangle([540, TT - 150, 740, TT - 10], fill=(40, 40, 50), outline=BLK, width=5)
    d.rectangle([620, TT - 10, 660, TT], fill=(40, 40, 50))
    g = ease(t / 1.5)
    mx, my = lerp(200, 640, g), lerp(1500, 830, g)
    d.ellipse([mx - 140, my - 140, mx + 140, my + 140], outline=(80, 60, 40), width=22)
    d.line([(mx + 100, my + 100), (mx + 220, my + 220)], fill=(80, 60, 40), width=36)
    chip(d, "MODO DETECTIVE", 230, bg=(30, 110, 210), size=58, appear=t / 0.3)
    return img, 1.0, 1.0

def s_eat(t):
    lt = t - 5.0
    img = office(); d = ImageDraw.Draw(img)
    guy(d, 260, FEET, 0.75, mood="neutral", arms="down", look=1, t=t)
    alien_cw(d, 780, FEET, 0.8, t)
    desk(d, 60, 1020)
    d.ellipse([170, TT - 30, 350, TT + 5], fill=WHITE, outline=BLK, width=4)
    chip(d, "SEÑAL #1: NUNCA COME", 230, bg=(150, 60, 200), size=56, appear=lt / 0.3)
    if lt < 4.0:
        bubble(d, 780, 520, 360, 120, ["Ya comí."], 52, tail=(0, 0), a=(lt - 0.5) / 0.3)
    else:
        d.rounded_rectangle([660, TT - 80, 900, TT], 14, fill=(220, 235, 245), outline=BLK, width=4)
        blob(d, 780, TT - 80, 100, t)
        bubble(d, 780, 520, 420, 120, ["*se mueve*"], 48, a=(lt - 4.4) / 0.3)
    return img, 1.0, 1.0

def s_sarcasm(t):
    lt = t - 12.0
    img = office(); d = ImageDraw.Draw(img)
    guy(d, 260, FEET, 0.75, mood="neutral", look=1, t=t)
    alien_cw(d, 800, FEET, 0.8, t)
    desk(d, 60, 1020)
    chip(d, "SEÑAL #2: NO ENTIENDE EL SARCASMO", 230, bg=(220, 120, 40), size=46, appear=lt / 0.3)
    if lt > 1.0 and lt < 5.0:
        bubble(d, 330, 520, 560, 170, ["Qué bueno, otra junta", "que pudo ser un correo"], 40, tail=(-60, -20), a=(lt - 1.0) / 0.3)
    if lt > 5.0:
        bubble(d, 700, 500, 640, 220, ["¿Enviar una junta por correo?", "¿No sería más eficiente", "teletransportarla?"], 38, tail=(80, 20), col=(225, 245, 220), a=(lt - 5.0) / 0.3)
    if lt > 10.0:
        bigtext(d, "TIENE RAZÓN", 540, 780, int(84 * pop((lt - 10.0) / 0.3)), fill=YEL, stroke=BLK, sw=8)
    return img, 1.0, 1.0

def s_sick(t):
    lt = t - 24.0
    img = office(); d = ImageDraw.Draw(img)
    d.rectangle([600, 300, 960, 360], fill=(230, 230, 235), outline=BLK, width=5)
    for k in range(5):
        ph = (lt * 1.2 + k * 0.2) % 1
        y = 380 + ph * 500
        d.line([(640 + k * 60, y), (660 + k * 60, y + 60)], fill=(150, 200, 240), width=8)
    guy(d, 270, FEET, 0.75, mood="scared", look=1, t=t)
    hx, hy = 270, FEET - 505 * 0.75
    d.line([(hx + 40, hy + 50), (hx + 120, hy + 30)], fill=(220, 220, 230), width=10)
    d.ellipse([hx + 112, hy + 22, hx + 128, hy + 38], fill=RED)
    for k in range(6):
        d.ellipse([60 + k * 50, 1300 + (k % 2) * 20, 120 + k * 50, 1340 + (k % 2) * 20], fill=WHITE, outline=(180, 180, 190), width=3)
    alien_cw(d, 780, FEET, 0.8, t, blink=False)
    chip(d, "SEÑAL #3: NUNCA SE ENFERMA", 230, bg=(40, 140, 80), size=52, appear=lt / 0.3)
    if lt < 6.0:
        d.text((780, 470), "3 DÍAS SIN PARPADEAR", font=F(40), fill=(30, 30, 30), anchor="mm", stroke_width=4, stroke_fill=WHITE)
    if lt > 6.0:
        bubble(d, 680, 500, 640, 170, ["Mi sistema inmunológico fue", "diseñado para el vacío"], 38, tail=(80, 20), col=(225, 245, 220), a=(lt - 6.0) / 0.3)
    if lt > 10.0:
        bigtext(d, "QUÉ ENVIDIA", 300, 760, int(70 * pop((lt - 10.0) / 0.3)), fill=YEL, stroke=BLK, sw=8)
    return img, 1.0, 1.0

def s_knows(t):
    lt = t - 36.0
    img = office(); d = ImageDraw.Draw(img)
    guy(d, 330, FEET, 0.8, mood="scared", look=1, t=t)
    alien_cw(d, 720, FEET, 0.8, t, mood="smile")
    chip(d, "SEÑAL #4: SABE DEMASIADO", 230, bg=(190, 30, 50), size=52, appear=lt / 0.3)
    items = [(0.8, "TARJETA", (60, 120, 200)), (2.6, "TU EX", (220, 80, 120)), (5.0, "TU SUELDO", (40, 150, 80))]
    for i, (st, txt, c) in enumerate(items):
        if lt < st: continue
        sc = pop((lt - st) / 0.3)
        cx, cy = 230 + i * 310, 470 + (i % 2) * 140
        d.rounded_rectangle([cx - 140 * sc, cy - 60 * sc, cx + 140 * sc, cy + 60 * sc], int(20 * sc), fill=c, outline=BLK, width=5)
        d.text((cx, cy), txt, font=F(max(8, int(44 * sc))), fill=WHITE, anchor="mm")
    if lt > 7.0:
        d.text((850, 820), "RR.HH.: ???", font=F(46), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    return img, 1.0, 1.0

def s_online(t):
    lt = t - 46.0
    if lt < 7.0:
        img = office(night=True); d = ImageDraw.Draw(img)
        d.rounded_rectangle([110, 330, 970, 1200], 30, fill=(245, 245, 250), outline=BLK, width=6)
        d.rectangle([110, 330, 970, 430], fill=(70, 60, 140))
        d.ellipse([140, 350, 200, 410], fill=AL, outline=BLK, width=3)
        d.text((220, 380), "Compañero", font=F(44), fill=WHITE, anchor="lm")
        d.ellipse([880, 365, 910, 395], fill=(60, 220, 90))
        msgs = [(0.8, "11:00 p.m.", "¿Sigues ahí?", "Sí."), (2.8, "3:00 a.m.", "¿Y ahora?", "Sí."), (4.4, "5:00 a.m.", "...", "Sí.")]
        for i, (st, hr, q, a) in enumerate(msgs):
            if lt < st: continue
            y = 480 + i * 240
            d.text((540, y), hr, font=F(32), fill=(120, 120, 130), anchor="mm")
            d.rounded_rectangle([520, y + 30, 940, y + 100], 24, fill=(200, 230, 255))
            d.text((540, y + 65), q, font=F(36), fill=(30, 30, 30), anchor="lm")
            if lt > st + 0.4:
                d.rounded_rectangle([140, y + 120, 380, y + 190], 24, fill=(225, 245, 220))
                d.text((160, y + 155), a, font=F(36), fill=(30, 30, 30), anchor="lm")
                d.text((400, y + 155), "0.3 s", font=F(28), fill=(60, 170, 90), anchor="lm")
        chip(d, "SEÑAL #5: NUNCA SE DESCONECTA", 230, bg=(70, 60, 140), size=48, appear=lt / 0.3)
        return img, 1.0, 1.0
    lt2 = lt - 7.0
    img = office(); d = ImageDraw.Draw(img)
    alien_cw(d, 600, FEET, 0.85, t, mood="smile", arms="desk")
    desk(d, 330, 950)
    d.rounded_rectangle([700, TT - 120, 790, TT], 12, fill=WHITE, outline=BLK, width=5)
    d.arc([770, TT - 95, 830, TT - 35], 270, 90, fill=BLK, width=8)
    d.text((745, TT - 60), "TÚ", font=F(30), fill=RED, anchor="mm")
    guy(d, 160, FEET + 80, 0.6, mood="scared", look=1, t=t)
    if lt2 > 1.5:
        bigtext(d, "¡CON TU CAFÉ!", 540, 480, int(80 * pop((lt2 - 1.5) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0

def s_final(t):
    lt = t - 58.0
    img = office(); d = ImageDraw.Draw(img)
    scared = lt >= 2
    guy(d, 180, FEET, 0.72, mood="scared" if scared else "neutral", look=0, t=t, hoodie=(90, 130, 200))
    guy(d, 440, FEET, 0.72, mood="scared" if scared else "neutral", look=0, t=t)
    alien_cw(d, 790, FEET, 0.72, t, arms="up" if lt > 5.0 else "down", mood="smile" if lt > 5 else "blank")
    desk(d, 40, 1040)
    for x, c in ((180, (250, 250, 250)), (440, (250, 240, 200)), (790, (230, 240, 250))):
        d.rectangle([x - 60, TT - 18, x + 60, TT + 2], fill=c, outline=(150, 150, 150), width=2)
    chip(d, "SEÑAL DEFINITIVA", 230, bg=RED, size=58, appear=lt / 0.3)
    if lt < 6.0:
        bubble(d, 540, 520, 760, 170, ["¿Quién se queda horas", "extra sin cobrar?"], 46, a=(lt - 0.4) / 0.3)
        if scared: d.text((310, 860), "...", font=F(80), fill=(60, 60, 60), anchor="mm")
    else:
        bubble(d, 540, 520, 900, 270, ["No necesito dormir, no siento estrés", "y mi especie no reconoce", "los derechos laborales."], 38, col=(225, 245, 220), a=(lt - 6.0) / 0.3)
    return img, 1.0, 1.0

def s_twist(t):
    lt = t - 70.0
    img = grad((250, 230, 150), (240, 190, 90)); d = ImageDraw.Draw(img)
    for k in range(16):
        a = k / 16 * 2 * math.pi + t * 0.3
        d.polygon([(540, 820), (540 + math.cos(a) * 1400, 820 + math.sin(a) * 1400), (540 + math.cos(a + 0.18) * 1400, 820 + math.sin(a + 0.18) * 1400)], fill=(255, 240, 180))
    d.rounded_rectangle([250, 450, 830, 1150], 20, fill=(140, 95, 50), outline=BLK, width=8)
    # portrait: alien bust clipped to the picture window
    win = (290, 490, 790, 1000)
    tmp = Image.new("RGB", (W, H), (200, 220, 235)); td = ImageDraw.Draw(tmp)
    for k in range(6): td.rectangle([290, 490 + k * 85, 790, 532 + k * 85], fill=(190, 210, 228))
    alien_cw(td, 540, 1250, 1.05, t, mood="smile", antenna=True)
    img.paste(tmp.crop(win), win[:2])
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([250, 1000, 830, 1150], 20, fill=(140, 95, 50), outline=BLK, width=8)
    d.text((540, 1075), "EMPLEADO DEL MES", font=F(46), fill=YEL, anchor="mm")
    if lt < 2.5:
        bigtext(d, "NO ES UN ALIENÍGENA…", 540, 300, int(62 * pop(lt / 0.3)), fill=WHITE, stroke=BLK, sw=8)
    else:
        bigtext(d, "ES EL EMPLEADO IDEAL", 540, 300, int(66 * pop((lt - 2.5) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 76.0
    img = office(); d = ImageDraw.Draw(img)
    alien_cw(d, 540, FEET, 0.9, t, mood="smile", arms="up")
    for i, (txt, c, y) in enumerate([("DENUNCIARLO", (200, 40, 50), 400), ("QUE ME RECOMIENDE", (40, 150, 80), 560)]):
        if lt < 0.3 + i * 1.2: continue
        sc = pop((lt - 0.3 - i * 1.2) / 0.3)
        d.rounded_rectangle([540 - 380 * sc, y - 65 * sc, 540 + 380 * sc, y + 65 * sc], int(24 * sc), fill=c, outline=WHITE, width=6)
        d.text((540, y), txt, font=F(max(8, int(56 * sc))), fill=WHITE, anchor="mm")
    if lt > 3.0: chip(d, "COMENTA  ·  SÍGUEME", 230, bg=(30, 30, 40), fg=YEL, size=52, appear=(lt - 3.0) / 0.3)
    return img, 1.0, 1.0

SCENES = [(0, 5, s_hook), (5, 12, s_eat), (12, 24, s_sarcasm), (24, 36, s_sick), (36, 46, s_knows), (46, 58, s_online),
          (58, 70, s_final), (70, 76, s_twist), (76, 99, s_end)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img, b, z = r[0], r[1], r[2]
    shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce: rich_caption(d, txt, appear=(t - cs) / 0.25)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = b * (0.3 + 0.7 * fi)
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r15.png"); sys.exit()
    from warp15 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(85.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
