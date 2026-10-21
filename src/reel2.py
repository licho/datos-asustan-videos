import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark,
                  W, H, YEL, RED, WHITE, BLK, SKIN)

FPS = 30
GREEN = (110, 210, 90)

# ---------------- drawing helpers ----------------
def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

BG_ROOM = grad((28, 30, 42), (10, 10, 16))
BG_GERM = grad((20, 50, 30), (5, 18, 10))
BG_LAB = grad((235, 238, 242), (190, 198, 208))
BG_DARK = grad((12, 12, 18), (0, 0, 0))

def desk_glow(img):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for i in range(12):
        r = 700 - i * 50
        ld.ellipse([540 - r, 900 - r * 0.7, 540 + r, 900 + r * 0.7], fill=(255, 220, 150, 8))
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")

BG_DESK = desk_glow(BG_ROOM)

def keyboard(d, cx, cy, w, dirt=0.0, seed=1, flipped=False, glow=None):
    h = w * 0.38; x0, y0 = cx - w / 2, cy - h / 2
    sc = w / 900
    if glow:
        d.rounded_rectangle([x0 - 14*sc, y0 - 14*sc, x0 + w + 14*sc, y0 + h + 14*sc], int(36*sc), fill=glow)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(28*sc), fill=(45, 48, 56), outline=BLK, width=max(2, int(6*sc)))
    if flipped:
        for fx in (0.12, 0.88):
            d.rounded_rectangle([x0 + w*fx - 40*sc, y0 + 20*sc, x0 + w*fx + 40*sc, y0 + 50*sc], int(10*sc), fill=(25, 25, 30))
        d.rounded_rectangle([cx - 120*sc, cy - 30*sc, cx + 120*sc, cy + 30*sc], int(8*sc), fill=(70, 72, 80))
        return
    pad = 24 * sc; cols = 14; rows = 5
    kw = (w - 2 * pad) / cols; kh = (h - 2 * pad) / rows
    for r in range(rows):
        if r == rows - 1:
            spans = [(0, 2), (2, 3.5), (3.5, 10.5), (10.5, 12), (12, 14)]
        else:
            spans = [(c, c + 1) for c in range(cols)]
        for a, b in spans:
            kx0 = x0 + pad + a * kw + 3*sc; kx1 = x0 + pad + b * kw - 3*sc
            ky0 = y0 + pad + r * kh + 3*sc; ky1 = y0 + pad + (r + 1) * kh - 3*sc
            d.rounded_rectangle([kx0, ky0 + 5*sc, kx1, ky1], int(8*sc), fill=(150, 152, 160))
            d.rounded_rectangle([kx0, ky0, kx1, ky1 - 5*sc], int(8*sc), fill=(225, 228, 234))
    if dirt > 0:
        rng = random.Random(seed)
        for i in range(int(160 * dirt)):
            px = rng.uniform(x0 + pad, x0 + w - pad); py = rng.uniform(y0 + pad, y0 + h - pad)
            s = rng.uniform(2, 7) * sc
            col = rng.choice([(110, 85, 55), (140, 110, 70), (90, 90, 90), (200, 170, 90)])
            d.ellipse([px - s, py - s, px + s, py + s], fill=col)
        for i in range(int(4 * dirt)):
            px = rng.uniform(x0 + pad, x0 + w - pad); py = rng.uniform(y0 + pad, y0 + h - pad)
            pts = [(px + j * 14 * sc, py + math.sin(j * 0.9) * 10 * sc) for j in range(8)]
            d.line(pts, fill=(40, 30, 25), width=max(1, int(3*sc)))

def germ(d, x, y, r, kind, t=0.0, phase=0.0, shade=1.0):
    wob = math.sin(t * 5 + phase)
    y = y + wob * r * 0.08
    C = lambda c: dk(c, shade)
    if kind == "ecoli":
        col = C((120, 210, 95))
        for i in range(4):
            pts = [(x - r*1.5 - j*r*0.25, y - r*0.4 + i*r*0.27 + math.sin(j*1.3 + t*9 + i) * r*0.12) for j in range(7)]
            d.line(pts, fill=C((80, 150, 60)), width=max(2, int(r*0.08)))
        d.rounded_rectangle([x - r*1.6, y - r*0.75, x + r*1.6, y + r*0.75], int(r*0.75), fill=col, outline=BLK, width=max(2, int(r*0.08)))
        ex = x + r*0.5
    elif kind == "coli":
        col = C((95, 155, 235))
        for a in range(10):
            ang = a / 10 * 2 * math.pi
            d.line([(x + math.cos(ang)*r*0.95, y + math.sin(ang)*r*0.95), (x + math.cos(ang)*r*1.3, y + math.sin(ang)*r*1.3 + math.sin(t*8+a)*r*0.05)], fill=C((60, 110, 190)), width=max(2, int(r*0.07)))
        d.ellipse([x - r*1.1, y - r*0.9, x + r*1.1, y + r*0.9], fill=col, outline=BLK, width=max(2, int(r*0.08)))
        ex = x
    else:  # staph cluster
        col = C((240, 195, 60))
        for (a, b) in [(-0.7, 0.45), (0.7, 0.45), (0, 0.75), (-0.75, -0.35), (0.75, -0.35)]:
            d.ellipse([x + a*r - r*0.55, y + b*r - r*0.55, x + a*r + r*0.55, y + b*r + r*0.55], fill=C((225, 175, 45)), outline=BLK, width=max(2, int(r*0.06)))
        d.ellipse([x - r*0.75, y - r*0.75, x + r*0.75, y + r*0.75], fill=col, outline=BLK, width=max(2, int(r*0.08)))
        ex = x
    # face
    for sx in (-1, 1):
        cx, cy = ex + sx * r*0.32, y - r*0.15
        d.ellipse([cx - r*0.2, cy - r*0.22, cx + r*0.2, cy + r*0.22], fill=WHITE, outline=BLK, width=max(1, int(r*0.05)))
        d.ellipse([cx - r*0.08 + r*0.05, cy - r*0.06, cx + r*0.08 + r*0.05, cy + r*0.1], fill=BLK)
        d.line([(cx - r*0.22, cy - r*0.34 - sx*r*0.06), (cx + r*0.22, cy - r*0.34 + sx*r*0.06)], fill=BLK, width=max(2, int(r*0.08)))
    d.chord([ex - r*0.38, y + r*0.0, ex + r*0.38, y + r*0.5], 0, 180, fill=(60, 10, 20), outline=BLK, width=max(1, int(r*0.05)))
    for k in range(4):
        tx = ex - r*0.3 + k * r*0.2
        d.polygon([(tx, y + r*0.25), (tx + r*0.1, y + r*0.25), (tx + r*0.05, y + r*0.36)], fill=WHITE)

GERMS = ["ecoli", "coli", "staph"]

def toilet_seat(d, cx, cy, s=1.0, sparkle_t=None):
    d.rounded_rectangle([cx - 150*s, cy - 260*s, cx + 150*s, cy - 140*s], int(30*s), fill=(240, 242, 245), outline=BLK, width=6)
    d.ellipse([cx - 170*s, cy - 160*s, cx + 170*s, cy + 200*s], fill=(245, 247, 250), outline=BLK, width=6)
    d.ellipse([cx - 100*s, cy - 90*s, cx + 100*s, cy + 140*s], fill=(150, 200, 230), outline=BLK, width=5)
    if sparkle_t is not None:
        for i, (a, b) in enumerate([(-120, -200), (130, -60), (-60, 170)]):
            k = 0.6 + 0.4 * math.sin(sparkle_t * 6 + i * 2)
            sx, sy = cx + a*s, cy + b*s; L = 30 * k * s
            d.polygon([(sx, sy - L), (sx + L*0.25, sy), (sx, sy + L), (sx - L*0.25, sy)], fill=YEL)
            d.polygon([(sx - L, sy), (sx, sy - L*0.25), (sx + L, sy), (sx, sy + L*0.25)], fill=YEL)

def magnifier(img, cx, cy, R, t, n_germs):
    lens = Image.new("RGB", (2*R, 2*R), (225, 228, 234)); ld = ImageDraw.Draw(lens)
    for i in range(0, 2*R, 150):
        ld.line([(i, 0), (i, 2*R)], fill=(150, 152, 160), width=10)
        ld.line([(0, i), (2*R, i)], fill=(150, 152, 160), width=10)
    rng = random.Random(3)
    for i in range(40):
        px, py, s = rng.uniform(0, 2*R), rng.uniform(0, 2*R), rng.uniform(4, 14)
        ld.ellipse([px - s, py - s, px + s, py + s], fill=(130, 100, 60))
    for i in range(n_germs):
        gx = rng.uniform(R*0.35, R*1.65); gy = rng.uniform(R*0.35, R*1.65)
        germ(ld, gx + math.sin(t*2 + i)*10, gy, rng.uniform(32, 52), GERMS[i % 3], t, i)
    mask = Image.new("L", (2*R, 2*R), 0); ImageDraw.Draw(mask).ellipse([0, 0, 2*R, 2*R], fill=255)
    img.paste(lens, (int(cx - R), int(cy - R)), mask)
    d = ImageDraw.Draw(img)
    d.line([(cx + R*0.7, cy + R*0.7), (cx + R*1.45, cy + R*1.45)], fill=(90, 55, 30), width=44)
    d.ellipse([cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14], outline=(60, 60, 70), width=28)
    d.arc([cx - R*0.75, cy - R*0.75, cx + R*0.75, cy + R*0.75], 200, 250, fill=WHITE, width=12)

def person(d, cx, cy, s, col):
    d.ellipse([cx - 32*s, cy - 110*s, cx + 32*s, cy - 46*s], fill=col)
    d.rounded_rectangle([cx - 50*s, cy - 40*s, cx + 50*s, cy + 70*s], int(30*s), fill=col)

def pizza(d, cx, cy, s):
    d.polygon([(cx - 110*s, cy - 90*s), (cx + 110*s, cy - 90*s), (cx, cy + 130*s)], fill=(250, 200, 80), outline=BLK)
    d.rounded_rectangle([cx - 125*s, cy - 120*s, cx + 125*s, cy - 80*s], int(18*s), fill=(200, 130, 60), outline=BLK, width=4)
    for (a, b) in [(-45, -40), (35, -30), (0, 30)]:
        d.ellipse([cx + a*s - 22*s, cy + b*s - 22*s, cx + a*s + 22*s, cy + b*s + 22*s], fill=(200, 50, 40))
    rng = random.Random(9)
    for i in range(14):
        px, py = cx + rng.uniform(-150, 150)*s, cy + rng.uniform(130, 180)*s
        d.ellipse([px - 6*s, py - 5*s, px + 6*s, py + 5*s], fill=(230, 180, 90))

def dirty_hand(d, cx, cy, s):
    d.rounded_rectangle([cx - 80*s, cy - 40*s, cx + 80*s, cy + 120*s], int(50*s), fill=SKIN, outline=BLK, width=4)
    for i in range(4):
        fx = cx - 66*s + i * 44*s
        d.rounded_rectangle([fx - 18*s, cy - 140*s + (i in (0, 3)) * 25*s, fx + 18*s, cy - 10*s], int(18*s), fill=SKIN, outline=BLK, width=4)
    d.rounded_rectangle([cx + 70*s, cy - 10*s, cx + 140*s, cy + 30*s], int(18*s), fill=SKIN, outline=BLK, width=4)
    rng = random.Random(5)
    for i in range(9):
        px, py, r = cx + rng.uniform(-60, 60)*s, cy + rng.uniform(-110, 100)*s, rng.uniform(8, 18)*s
        d.ellipse([px - r, py - r*0.7, px + r, py + r*0.7], fill=(120, 90, 55))

def dust(d, cx, cy, s, t):
    for (a, b, r) in [(-60, 10, 70), (40, -10, 80), (90, 40, 55), (-20, 50, 65), (0, -40, 60)]:
        d.ellipse([cx + a*s - r*s, cy + b*s - r*s, cx + a*s + r*s, cy + b*s + r*s], fill=(150, 150, 155))
    for i in range(3):
        dx = cx + (-60 + i*60)*s; dy = cy + 120*s + ((t*80 + i*30) % 60)*s
        d.polygon([(dx, dy - 22*s), (dx - 13*s, dy), (dx + 13*s, dy)], fill=(100, 170, 240))
        d.ellipse([dx - 13*s, dy - 12*s, dx + 13*s, dy + 13*s], fill=(100, 170, 240))

def culprit_card(d, cx, cy, sc, label):
    S = lambda v: v * sc
    d.rounded_rectangle([cx - S(300) + 10, cy - S(150) + 12, cx + S(300) + 10, cy + S(150) + 12], int(S(36)), fill=BLK)
    d.rounded_rectangle([cx - S(300), cy - S(150), cx + S(300), cy + S(150)], int(S(36)), fill=(250, 248, 240), outline=BLK, width=6)
    d.text((cx + S(80), cy), label, font=F(S(46)), fill=(30, 30, 30), anchor="mm", align="center")

def phone(d, cx, cy, s, glow=1.0):
    d.rounded_rectangle([cx - 160*s, cy - 320*s, cx + 160*s, cy + 320*s], int(50*s), fill=(20, 20, 24), outline=(90, 90, 100), width=8)
    d.rounded_rectangle([cx - 140*s, cy - 290*s, cx + 140*s, cy + 290*s], int(30*s), fill=lc((10, 10, 20), (60, 120, 200), glow))
    d.rounded_rectangle([cx - 40*s, cy - 280*s, cx + 40*s, cy - 262*s], int(9*s), fill=(20, 20, 24))
    for r_ in range(4):
        for c_ in range(3):
            ix = cx - 85*s + c_ * 85*s; iy = cy - 180*s + r_ * 100*s
            d.rounded_rectangle([ix - 30*s, iy - 30*s, ix + 30*s, iy + 30*s], int(14*s), fill=lc((40, 40, 50), [(240, 90, 80), (90, 200, 120), (250, 200, 60), (120, 140, 240)][(r_ + c_) % 4], glow))

def air_can(d, x, y, s):
    d.rounded_rectangle([x - 55*s, y - 40*s, x + 55*s, y + 220*s], int(20*s), fill=(60, 130, 220), outline=BLK, width=5)
    d.rectangle([x - 55*s, y + 50*s, x + 55*s, y + 110*s], fill=WHITE)
    d.text((x, y + 80*s), "AIRE", font=F(30*s), fill=(60, 130, 220), anchor="mm")
    d.rounded_rectangle([x - 30*s, y - 75*s, x + 30*s, y - 40*s], int(8*s), fill=(200, 200, 205), outline=BLK, width=4)
    d.line([(x - 20*s, y - 60*s), (x - 160*s, y - 10*s)], fill=(220, 40, 40), width=int(10*s))

def bottle(d, x, y, s):
    d.rounded_rectangle([x - 60*s, y - 100*s, x + 60*s, y + 130*s], int(24*s), fill=(235, 245, 255), outline=BLK, width=5)
    d.rectangle([x - 22*s, y - 140*s, x + 22*s, y - 100*s], fill=(60, 130, 220), outline=BLK, width=4)
    d.rectangle([x - 60*s, y - 20*s, x + 60*s, y + 60*s], fill=(60, 130, 220))
    d.text((x, y + 20*s), "70%", font=F(40*s), fill=WHITE, anchor="mm")

def step_badge(d, n, cx=140, cy=470, sc=1.0):
    d.ellipse([cx - 80*sc, cy - 80*sc, cx + 80*sc, cy + 80*sc], fill=YEL, outline=BLK, width=8)
    d.text((cx, cy), str(n), font=F(100*sc), fill=BLK, anchor="mm")

# ---------------- captions (nominal timeline) ----------------
CAPS = [
    (0.0, 2.6, "¿Sabes cuánta *suciedad* hay en tu teclado?"),
    (2.6, 5.0, "Spoiler: *más de la que quieres saber*"),
    (5.0, 9.5, "Revisaron *30 teclados* de oficina en Londres…"),
    (9.5, 13.0, "…y uno estaba *5 veces más sucio* que el asiento del baño"),
    (13.0, 19.0, "Un escritorio puede tener hasta *400 veces más bacterias* que un inodoro"),
    (19.0, 20.5, "¿Qué vive ahí?"),
    (20.5, 22.0, "*E. coli*…"),
    (22.0, 23.5, "*Coliformes*…"),
    (23.5, 26.0, "…y *estafilococo dorado*"),
    (26.0, 27.5, "¿Por qué? *Tres culpables*"),
    (27.5, 29.5, "*Comer* frente a la compu…"),
    (29.5, 31.5, "No *lavarte las manos*…"),
    (31.5, 34.0, "…y el *polvo*, que guarda humedad"),
    (34.0, 38.0, "Más de *1 de cada 10* nunca lo ha limpiado"),
    (38.0, 40.8, "Así lo limpias. *1:* apágalo o desconéctalo"),
    (40.8, 43.3, "*2:* voltéalo y sacúdelo"),
    (43.3, 45.8, "*3:* aire comprimido entre las teclas"),
    (45.8, 49.3, "*4:* paño con alcohol isopropílico. *Nunca directo.*"),
    (49.3, 52.0, "*5:* lávate las manos"),
    (52.0, 54.5, "Por cierto… ¿sabes qué tocas *todavía más*?"),
    (54.5, 57.0, "*Tu celular.*"),
]
STEPS = [38.8, 41.0, 43.5, 46.0, 49.5]

# ---------------- scenes ----------------
def s1(t):
    img = BG_DESK.copy(); d = ImageDraw.Draw(img)
    keyboard(d, 540, 1000, 960, dirt=0.6, seed=2)
    p = ease((t - 0.6) / 1.2)
    lx = lerp(300, 560, p) + math.sin(t * 1.5) * 40
    magnifier(img, lx, 860, 230, t, int(cl((t - 0.8) / 2.5) * 9))
    d = ImageDraw.Draw(img)
    chip(d, "¿QUÉ TAN SUCIO ESTÁ?", 300, bg=(120, 70, 200), size=62, appear=t / 0.4)
    return img, 1.0, 1.0 + 0.05 * t / 5

def s2(t):
    lt = t - 5
    if lt < 4.3:
        img = BG_LAB.copy(); d = ImageDraw.Draw(img)
        for i in range(30):
            r_, c_ = divmod(i, 5)
            cx, cy = 140 + c_ * 200, 450 + r_ * 150
            st = 0.1 + i * 0.06
            if lt < st: continue
            sc = pop((lt - st) / 0.25)
            bad = (i == 17 and lt > 3.0)
            keyboard(d, cx, cy, 175 * sc, dirt=0.4, seed=i, glow=(240, 40, 40) if bad and int(lt * 6) % 2 == 0 else None)
        bigtext(d, "30", 900, 300, int(110 * pop(lt / 0.35)), fill=YEL)
        chip(d, "ESTUDIO EN LONDRES", 300, bg=(40, 40, 50), appear=lt / 0.4) if False else None
        return img, 1.0, 1.0
    lt2 = lt - 4.3
    img = BG_LAB.copy(); d = ImageDraw.Draw(img)
    sl = ease(lt2 / 0.4)
    keyboard(d, lerp(-300, 260, sl), 800, 420, dirt=1.0, seed=17)
    for i in range(5):
        germ(d, lerp(-300, 260, sl) - 170 + i * 85, 640 + (i % 2) * 40, 34, GERMS[i % 3], t, i)
    toilet_seat(d, lerp(1400, 800, sl), 800, 0.9, sparkle_t=t)
    bigtext(d, "VS", 545, 560, 90, fill=WHITE, stroke=BLK)
    if lt2 > 1.4:
        sc = pop((lt2 - 1.4) / 0.3)
        bigtext(d, "x5", 290, 1100, int(220 * sc), fill=RED, stroke=WHITE, sw=14)
        bigtext(d, "MÁS SUCIO", 290, 1230, int(52 * sc), fill=BLK, stroke=WHITE, sw=6)
    shake = 1.4 < lt2 < 1.7
    return img, 1.0, 1.0, shake

def s3(t):
    lt = t - 13
    img = BG_GERM.copy(); d = ImageDraw.Draw(img)
    rng = random.Random(4)
    n = int(cl(lt / 3.0) * 26)
    for i in range(n):
        gx, gy = rng.uniform(80, 1000), rng.uniform(380, 1350)
        if 640 < gy < 980 and 150 < gx < 930: gy += 380
        germ(d, gx, gy, rng.uniform(26, 44), GERMS[i % 3], t, i, shade=0.7)
    val = int(400 * ease((lt - 0.4) / 2.6))
    d.rounded_rectangle([120, 620, 960, 980], 50, fill=(0, 0, 0), outline=YEL, width=8)
    bigtext(d, f"{val}x", 540, 760, 230, fill=YEL, sw=10)
    d.text((540, 905), "MÁS BACTERIAS QUE UN INODORO", font=F(42), fill=WHITE, anchor="mm")
    d.text((540, 1030), "Estudio: Universidad de Arizona", font=F(34), fill=(200, 230, 200), anchor="mm")
    chip(d, "TU ESCRITORIO", 300, bg=RED, appear=lt / 0.4)
    return img, 1.0, 1.0 + 0.04 * lt / 6, (2.9 < lt < 3.2)

def s4(t):
    lt = t - 19
    img = BG_GERM.copy(); d = ImageDraw.Draw(img)
    info = [("ecoli", "E. coli", 1.5, 330, 620), ("coli", "Coliformes", 3.0, 760, 860), ("staph", "Estafilococo\ndorado", 4.5, 330, 1120)]
    for kind, name, st, x, y in info:
        if lt < st: continue
        sc = pop((lt - st) / 0.35)
        germ(d, x, y, 120 * sc, kind, t, st)
        tx = 790 if x < 540 else 290
        d.multiline_text((tx, y), name, font=F(max(8, int(54 * sc))), fill=YEL, anchor="mm", align="center",
                         stroke_width=6, stroke_fill=BLK)
    chip(d, "LOS INQUILINOS", 300, bg=(40, 140, 60), appear=lt / 0.4)
    return img, 1.0, 1.0

def s5(t):
    lt = t - 26
    img = BG_ROOM.copy(); d = ImageDraw.Draw(img)
    cards = [(1.5, "Comer en\nel escritorio", 560), (3.5, "Manos\nsin lavar", 870), (5.5, "Polvo +\nhumedad", 1180)]
    for i, (st, label, cy) in enumerate(cards):
        if lt < st: continue
        sc = pop((lt - st) / 0.35)
        S = lambda v: v * sc
        d.rounded_rectangle([540 - S(420) + 10, cy - S(135) + 12, 540 + S(420) + 10, cy + S(135) + 12], int(S(36)), fill=BLK)
        d.rounded_rectangle([540 - S(420), cy - S(135), 540 + S(420), cy + S(135)], int(S(36)), fill=(250, 248, 240), outline=BLK, width=6)
        d.multiline_text((540 + S(110), cy), label, font=F(max(8, S(52))), fill=(30, 30, 30), anchor="mm", align="center")
        ix = 540 - S(250)
        if i == 0: pizza(d, ix, cy - S(10), 0.55 * sc)
        elif i == 1: dirty_hand(d, ix, cy + S(20), 0.6 * sc)
        else: dust(d, ix, cy - S(20), 0.6 * sc, t)
    chip(d, "LOS CULPABLES", 300, bg=RED, appear=lt / 0.4)
    return img, 1.0, 1.0

def s6(t):
    lt = t - 34
    img = BG_ROOM.copy(); d = ImageDraw.Draw(img)
    for i in range(10):
        r_, c_ = divmod(i, 5)
        cx, cy = 180 + c_ * 180, 720 + r_ * 260
        st = 0.2 + i * 0.08
        if lt < st: continue
        sc = pop((lt - st) / 0.25)
        bad = (i == 7 and lt > 1.6)
        person(d, cx, cy, 1.2 * sc, (230, 50, 50) if bad else (150, 160, 175))
        if bad:
            bigtext(d, "¡NUNCA!", cx, cy - 190, int(40 * pop((lt - 1.6) / 0.3)), fill=WHITE, stroke=RED, sw=6)
    bigtext(d, "1 de cada 10", 540, 470, int(96 * pop(lt / 0.35)), fill=YEL)
    return img, 1.0, 1.0

def s7(t):
    lt = t - 38
    img = BG_DESK.copy(); d = ImageDraw.Draw(img)
    step = sum(1 for s in STEPS if t >= s)
    dirt = [1.0, 1.0, 0.7, 0.4, 0.1, 0.0][step]
    cx, cy = 540, 900
    if step == 2:
        ls = t - STEPS[1]
        shake = math.sin(ls * 30) * 25 * (ls > 0.4)
        flip = ease(ls / 0.4)
        if flip < 1:
            keyboard(d, cx, cy, 820 * (1 - 0.0 * flip), dirt=1.0, seed=3)
        else:
            keyboard(d, cx + shake, cy - 120, 820, flipped=True)
        rng = random.Random(11)
        for i in range(60):
            born = 0.4 + rng.random() * 1.6
            if ls < born: continue
            age = ls - born
            px = cx + rng.uniform(-380, 380); py = cy - 60 + age * age * 900
            py = min(py, 1300 - rng.uniform(0, 30))
            s = rng.uniform(5, 12)
            d.ellipse([px - s, py - s, px + s, py + s], fill=rng.choice([(200, 160, 80), (130, 100, 60), (110, 110, 110)]))
        if ls > 1.2:
            bigtext(d, "¡UGH!", 860, 640, int(80 * pop((ls - 1.2) / 0.3)), fill=YEL)
    else:
        keyboard(d, cx, cy, 820, dirt=dirt, seed=3)
    if step == 1:
        ls = t - STEPS[0]
        sep = ease((ls - 0.5) / 0.5) * 120
        d.line([(cx + 410, cy - 60), (cx + 470, cy - 160), (900 + sep * 0.3, 640)], fill=(30, 30, 30), width=14, joint="curve")
        px = 900 + sep
        d.rounded_rectangle([px - 10, 590, px + 70, 690], 12, fill=(240, 240, 240), outline=BLK, width=5)
        for yy in (615, 665): d.rectangle([px + 70, yy - 6, px + 110, yy + 6], fill=(200, 170, 60))
        d.rectangle([980, 570, 1060, 710], fill=(250, 250, 250), outline=BLK, width=5)
        if 0.9 < ls < 1.6:
            bigtext(d, "OFF", 820, 520, int(70 * pop((ls - 0.9) / 0.25)), fill=RED, stroke=WHITE, sw=8)
    if step == 3:
        ls = t - STEPS[2]
        air_can(d, 900, 520, 1.0)
        rng = random.Random(21)
        for i in range(30):
            age = (ls * 2 + rng.random()) % 1.0
            px = lerp(740, 300, age) + rng.uniform(-60, 60) * age; py = lerp(520, 880, age) + rng.uniform(-60, 60) * age
            r = 10 + 30 * age
            d.ellipse([px - r, py - r, px + r, py + r], outline=(230, 240, 255), width=4)
    if step == 4:
        ls = t - STEPS[3]
        wx = lerp(220, 860, (math.sin(ls * 3) + 1) / 2)
        d.rounded_rectangle([wx - 110, cy - 120, wx + 110, cy + 40], 30, fill=(250, 250, 255), outline=BLK, width=5)
        for k in range(3): d.line([(wx - 80, cy - 80 + k * 40), (wx + 80, cy - 80 + k * 40)], fill=(210, 220, 235), width=6)
        bottle(d, 880, 560, 0.9)
        if ls > 1.3:
            sc = pop((ls - 1.3) / 0.3)
            d.rounded_rectangle([80, 1110, 520, 1330], 30, fill=(255, 240, 240), outline=RED, width=6)
            d.text((300, 1160), "NO rocíes", font=F(max(8, 44 * sc)), fill=RED, anchor="mm")
            d.text((300, 1220), "directo sobre", font=F(max(8, 40 * sc)), fill=RED, anchor="mm")
            d.text((300, 1275), "el teclado", font=F(max(8, 40 * sc)), fill=RED, anchor="mm")
    if step == 5:
        ls = t - STEPS[4]
        for sx in (-1, 1):
            hx = 540 + sx * (90 + math.sin(ls * 10) * 20)
            d.rounded_rectangle([hx - 90, 520, hx + 90, 760], 60, fill=SKIN, outline=BLK, width=5)
        rng = random.Random(31)
        for i in range(18):
            age = (ls * 0.8 + rng.random()) % 1.0
            bx = 540 + rng.uniform(-260, 260); by = lerp(760, 380, age)
            r = rng.uniform(16, 36)
            d.ellipse([bx - r, by - r, bx + r, by + r], outline=(180, 220, 255), width=5)
        if ls > 0.8:
            check(d, 860, 420, pop((ls - 0.8) / 0.3) * 1.6)
    if step >= 1:
        ls = t - STEPS[step - 1]
        step_badge(d, step, sc=pop(ls / 0.3))
    chip(d, "TUTORIAL: LÍMPIALO", 300, bg=(30, 110, 210), appear=lt / 0.4)
    sh = step == 2 and (t - STEPS[1]) > 0.4
    return img, 1.0, 1.0, False

def s8(t):
    lt = t - 52
    img = BG_DARK.copy(); d = ImageDraw.Draw(img)
    glow = ease((lt - 0.5) / 1.5)
    phone(d, 540, 880, 1.15, glow=glow)
    rng = random.Random(8)
    n = int(cl((lt - 1.0) / 2.5) * 14)
    for i in range(n):
        ang = rng.uniform(0, 2 * math.pi); rr = rng.uniform(80, 300)
        gx = 540 + math.cos(ang) * rr * 0.7; gy = 880 + math.sin(ang) * rr * 1.1
        germ(d, gx, gy, rng.uniform(26, 40), GERMS[i % 3], t, i)
    buzz = 2.5 < lt < 3.6
    if lt > 2.5:
        bigtext(d, "TU CELULAR", 540, 360, int(100 * pop((lt - 2.5) / 0.3)), fill=RED, stroke=WHITE, sw=10)
    b = 0.85
    fade = 1.0 - ease((lt - 4.5) / 0.5)
    return img, b * fade, 1.0 + 0.06 * ease(lt / 4), buzz

def s9(t):
    lt = t - 57
    img = Image.new("RGB", (W, H), (8, 8, 10)); d = ImageDraw.Draw(img)
    sc = pop(lt / 0.4)
    bigtext(d, "¿Hace cuánto", 540, 640, int(86 * sc), fill=WHITE)
    bigtext(d, "NO LIMPIAS", 540, 765, int(110 * sc), fill=YEL)
    bigtext(d, "el tuyo?", 540, 890, int(86 * sc), fill=WHITE)
    ay = 1080 + 25 * math.sin(lt * 8)
    d.polygon([(470, ay), (610, ay), (540, ay + 90)], fill=RED, outline=WHITE)
    d.rectangle([512, ay - 90, 568, ay], fill=RED)
    if lt > 0.6:
        bigtext(d, "Cuéntame en los comentarios", 540, 1310, int(48 * pop((lt - 0.6) / 0.3)), fill=WHITE)
    if lt > 1.2:
        bigtext(d, "PARTE 2: tu celular…", 540, 380, int(44 * pop((lt - 1.2) / 0.3)), fill=(170, 170, 170), sw=4)
    return img, ease(lt / 0.3), 1.0

SCENES = [(0, 5, s1), (5, 13, s2), (13, 19, s3), (19, 26, s4), (26, 34, s5), (34, 38, s6), (38, 52, s7), (52, 57, s8), (57, 60, s9)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img, b, z = r[0], r[1], r[2]
    shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce:
            rich_caption(d, txt, appear=(t - cs) / 0.25)
    if z > 1.001:
        cw, ch = W / z, H / z
        img = img.crop((int((W-cw)/2), int((H-ch)/2), int((W+cw)/2), int((H+ch)/2))).resize((W, H), Image.BILINEAR)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    if fn is not s9: b = b * (0.3 + 0.7 * fi)
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    if shake:
        k = int(t * FPS)
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1)
        arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = []
        for ts in [float(x) for x in sys.argv[2:]]:
            out.append(Image.fromarray(render(ts)).resize((270, 480)))
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r2.png"); sys.exit()
    from warp2 import v_of_T, DUR
    out = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(59.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
