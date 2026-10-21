import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 60.0
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc = {}
def F(s):
    s = max(8, int(s))
    if s not in _fc: _fc[s] = ImageFont.truetype(FB, s)
    return _fc[s]

def cl(v, a=0.0, b=1.0): return max(a, min(b, v))
def lerp(a, b, t): return a + (b - a) * t
def ease(t): t = cl(t); return t * t * (3 - 2 * t)
def pop(t):
    t = cl(t); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def lc(c1, c2, t): return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))
def dk(c, f): return tuple(int(v * f) for v in c)

YEL = (255, 214, 0); RED = (225, 35, 45); WHITE = (255, 255, 255); BLK = (0, 0, 0)
FEET = 1350; HORIZ = 1150; CAP_Y = 1500

# ---------------- text helpers ----------------
def rich_caption(d, text, y=CAP_Y, size=70, maxw=960, appear=1.0):
    size = int(size * (0.8 + 0.2 * pop(appear)))
    f = F(size)
    hl = False; words = []
    for w in text.split():
        pieces = []
        for j, part in enumerate(w.split("*")):
            if j > 0: hl = not hl
            if part: pieces.append((part, hl))
        words.append(pieces)
    sp = d.textlength(" ", font=f)
    lines, cur, cw = [], [], 0
    for pcs in words:
        ww = sum(d.textlength(p, font=f) for p, _ in pcs)
        if cur and cw + sp + ww > maxw:
            lines.append((cur, cw)); cur, cw = [], 0
        cw = cw + (sp if cur else 0) + ww; cur.append((pcs, ww))
    if cur: lines.append((cur, cw))
    lh = size * 1.22
    y0 = y - lh * (len(lines) - 1) / 2
    for li, (ln, lw) in enumerate(lines):
        x = W / 2 - lw / 2
        for pcs, ww in ln:
            for p, h in pcs:
                d.text((x, y0 + li * lh), p, font=f, fill=YEL if h else WHITE, anchor="lm",
                       stroke_width=max(4, int(size * 0.14)), stroke_fill=BLK)
                x += d.textlength(p, font=f)
            x += sp

def chip(d, text, y=300, bg=RED, fg=WHITE, size=56, appear=1.0):
    size = int(size * (0.6 + 0.4 * pop(appear)))
    f = F(size); w = d.textlength(text, font=f); pad = size * 0.65
    d.rounded_rectangle([W/2 - w/2 - pad, y - size*0.8, W/2 + w/2 + pad, y + size*0.8],
                        radius=int(size*0.6), fill=bg, outline=BLK, width=6)
    d.text((W/2, y), text, font=f, fill=fg, anchor="mm")

def bigtext(d, s, x, y, size, fill=YEL, stroke=BLK, sw=None):
    d.text((x, y), s, font=F(size), fill=fill, anchor="mm",
           stroke_width=sw if sw is not None else max(4, int(size*0.12)), stroke_fill=stroke)

# ---------------- characters ----------------
SKIN = (241, 194, 150)
def guy(d, x, y, s=1.0, mood="neutral", arms="down", look=0.0, t=0.0, hoodie=(240, 120, 40)):
    S = lambda v: v * s
    d.ellipse([x-S(130), y-S(16), x+S(130), y+S(16)], fill=(70, 72, 75))
    jeans = (45, 65, 120)
    bob = math.sin(t * 8) * S(3) if mood == "scared" else 0
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx*S(10) - (S(65) if sx < 0 else 0), y-S(180), x + sx*S(10) + (S(65) if sx > 0 else 0), y-S(10)], S(20), fill=jeans)
        d.ellipse([x + sx*S(50) - S(48), y-S(42), x + sx*S(50) + S(48), y+S(4)], fill=(30, 30, 30))
    y = y + bob
    sh = dk(hoodie, 0.8)
    # arms (behind body for some poses)
    def arm(sx, hx, hy):
        d.line([(x + sx*S(95), y-S(365)), (hx, hy)], fill=sh, width=int(S(46)), joint="curve")
        d.ellipse([hx-S(26), hy-S(26), hx+S(26), hy+S(26)], fill=SKIN)
    if arms == "up":
        arm(-1, x-S(185), y-S(560)); arm(1, x+S(185), y-S(560))
    d.rounded_rectangle([x-S(110), y-S(415), x+S(110), y-S(150)], S(60), fill=hoodie)
    d.rounded_rectangle([x-S(62), y-S(265), x+S(62), y-S(195)], S(22), fill=sh)
    d.line([(x-S(22), y-S(400)), (x-S(26), y-S(330))], fill=WHITE, width=int(S(7)))
    d.line([(x+S(22), y-S(400)), (x+S(26), y-S(330))], fill=WHITE, width=int(S(7)))
    if arms == "down":
        arm(-1, x-S(135), y-S(205)); arm(1, x+S(135), y-S(205))
    elif arms == "push":
        arm(-1, x+S(150), y-S(300)); arm(1, x+S(200), y-S(285))
    elif arms == "mop":
        arm(-1, x+S(110), y-S(290)); arm(1, x+S(170), y-S(320))
    elif arms == "switch":
        arm(-1, x-S(135), y-S(205)); arm(1, x+S(190), y-S(470))
    hx, hy = x, y - S(505)
    d.ellipse([hx-S(100), hy-S(100), hx+S(100), hy+S(100)], fill=SKIN)
    d.chord([hx-S(106), hy-S(114), hx+S(106), hy+S(72)], 180, 360, fill=(55, 38, 28))
    d.polygon([(hx-S(100), hy-S(20)), (hx-S(60), hy-S(60)), (hx-S(105), hy-S(70))], fill=(55, 38, 28))
    lx = look * S(10)
    if mood == "relief":
        for sx in (-1, 1):
            d.arc([hx+sx*S(38)-S(24), hy-S(10), hx+sx*S(38)+S(24), hy+S(25)], 200, 340, fill=BLK, width=int(S(7)))
        d.arc([hx-S(40), hy+S(20), hx+S(40), hy+S(70)], 20, 160, fill=(120, 40, 30), width=int(S(8)))
    else:
        er = S(34) if mood == "scared" else S(25)
        for sx in (-1, 1):
            ex, ey = hx + sx*S(38), hy + S(5)
            d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=WHITE, outline=BLK, width=int(S(4)))
            pr = S(11) if mood == "scared" else S(12)
            d.ellipse([ex+lx-pr, ey-pr, ex+lx+pr, ey+pr], fill=BLK)
            if mood == "scared":
                d.line([(ex-S(26), ey-S(52)-sx*S(6)), (ex+S(26), ey-S(52)+sx*S(6))], fill=(55, 38, 28), width=int(S(8)))
        if mood == "scared":
            d.ellipse([hx-S(20), hy+S(45), hx+S(20), hy+S(85)], fill=(70, 20, 20))
            dy = (t * 120) % 60
            d.polygon([(hx+S(105), hy-S(40)+S(dy)), (hx+S(92), hy-S(10)+S(dy)), (hx+S(118), hy-S(10)+S(dy))], fill=(120, 190, 255))
            d.ellipse([hx+S(92), hy-S(22)+S(dy), hx+S(118), hy+S(4)+S(dy)], fill=(120, 190, 255))
        else:
            d.arc([hx-S(30), hy+S(30), hx+S(30), hy+S(65)], 20, 160, fill=(120, 40, 30), width=int(S(7)))

def zombie(d, x, y, s=1.0, t=0.0, face=-1, shade=1.0, glow=False):
    S = lambda v: v * s
    C = lambda c: dk(c, shade)
    x = x + math.sin(t * 3.1) * S(10)
    skin, shirt, pants = C((130, 175, 105)), C((105, 95, 130)), C((80, 65, 50))
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx*S(12) - (S(60) if sx < 0 else 0), y-S(180) + (S(10) if sx > 0 else 0), x + sx*S(12) + (S(60) if sx > 0 else 0), y-S(10)], S(18), fill=pants)
        d.ellipse([x + sx*S(48) - S(44), y-S(38), x + sx*S(48) + S(44), y+S(4)], fill=C((40, 35, 30)))
    body = [x-S(105), y-S(410), x+S(105), y-S(160)]
    d.rounded_rectangle(body, S(40), fill=shirt)
    zz = [(x-S(105), y-S(190))]
    for i in range(8):
        zz.append((x - S(105) + S(26.25)*(i+0.5), y - S(150) + (S(28) if i % 2 == 0 else 0)))
    zz.append((x+S(105), y-S(190)))
    d.polygon(zz, fill=shirt)
    d.line([(x-S(40), y-S(330)), (x+S(10), y-S(280))], fill=C((150, 40, 40)), width=int(S(8)))
    reach = S(210) + math.sin(t * 4) * S(12)
    for k, yy in ((0, S(370)), (1, S(330))):
        hx = x + face * reach
        d.line([(x + face*S(60), y - yy), (hx, y - yy - S(10))], fill=skin, width=int(S(42)), joint="curve")
        d.ellipse([hx-S(26), y-yy-S(36), hx+S(26), y-yy+S(16)], fill=skin)
    tilt = math.sin(t * 2.2) * S(14)
    hx, hy = x + tilt, y - S(500)
    d.ellipse([hx-S(98), hy-S(95), hx+S(98), hy+S(100)], fill=skin)
    d.chord([hx-S(100), hy-S(100), hx+S(90), hy+S(10)], 190, 330, fill=C((60, 70, 50)))
    eyc = (255, 60, 50) if glow else C((255, 255, 230))
    d.ellipse([hx-S(70), hy-S(30), hx-S(10), hy+S(30)], fill=eyc, outline=BLK, width=int(S(4)))
    d.ellipse([hx+S(18), hy-S(15), hx+S(58), hy+S(25)], fill=eyc, outline=BLK, width=int(S(4)))
    d.ellipse([hx-S(48), hy-S(6), hx-S(32), hy+S(10)], fill=(180, 0, 0) if not glow else (255, 230, 200))
    d.ellipse([hx+S(32), hy-S(2), hx+S(44), hy+S(10)], fill=(180, 0, 0) if not glow else (255, 230, 200))
    mouth = [(hx-S(45), hy+S(50))]
    for i in range(7):
        mouth.append((hx - S(45) + S(15)*(i+0.5), hy + S(50) + (S(14) if i % 2 == 0 else -S(2))))
    mouth.append((hx+S(55), hy+S(48))); mouth.append((hx+S(35), hy+S(80))); mouth.append((hx-S(30), hy+S(80)))
    d.polygon(mouth, fill=C((40, 10, 10)))

# ---------------- props ----------------
def card(d, cx, cy, sc, label):
    S = lambda v: v * sc
    d.rounded_rectangle([cx-S(150)+10, cy-S(150)+12, cx+S(150)+10, cy+S(150)+12], int(S(36)), fill=(0, 0, 0))
    d.rounded_rectangle([cx-S(150), cy-S(150), cx+S(150), cy+S(150)], int(S(36)), fill=(250, 248, 240), outline=BLK, width=6)
    d.text((cx, cy+S(115)), label, font=F(S(38)), fill=(40, 40, 40), anchor="mm")

def icon(d, kind, cx, cy, k, t=0.0):
    R = lambda a, b, c, e: [cx+a*k, cy+b*k, cx+c*k, cy+e*k]
    P = lambda pts: [(cx+a*k, cy+b*k) for a, b in pts]
    w = max(2, int(5*k))
    if kind == "agua":
        d.rounded_rectangle(R(-55, -90, 55, 110), int(30*k), fill=(140, 200, 245), outline=(40, 100, 170), width=w)
        d.rectangle(R(-25, -125, 25, -90), fill=(140, 200, 245), outline=(40, 100, 170), width=w)
        d.rounded_rectangle(R(-32, -152, 32, -120), int(8*k), fill=(30, 80, 200))
        d.rectangle(R(-55, -5, 55, 45), fill=WHITE)
        d.text((cx, cy+20*k), "AGUA", font=F(26*k), fill=(30, 80, 200), anchor="mm")
        d.line(P([(-30, -70), (-30, -20)]), fill=WHITE, width=max(2, int(10*k)))
    elif kind == "nueces":
        d.polygon(P([(-95, -120), (95, -120), (115, 125), (-115, 125)]), fill=(185, 125, 60), outline=(110, 70, 30))
        zz = [(-95, -120)] + [(-95 + 190/10*(i+0.5), -140 if i % 2 == 0 else -120) for i in range(10)] + [(95, -120)]
        d.polygon(P(zz), fill=(150, 95, 40))
        d.ellipse(R(-65, -40, 65, 90), fill=(250, 235, 200), outline=(110, 70, 30), width=w)
        for (a, b) in [(-30, 0), (10, -10), (30, 30), (-20, 45), (15, 60), (-40, 25)]:
            d.ellipse(R(a-17, b-12, a+17, b+12), fill=(205, 150, 80), outline=(120, 80, 40), width=max(1, w-2))
    elif kind == "pilas":
        for off in (-45, 45):
            d.rounded_rectangle(R(off-38, -100, off+38, 115), int(10*k), fill=(30, 30, 30))
            d.rounded_rectangle(R(off-38, -100, off+38, -30), int(10*k), fill=(215, 130, 40))
            d.rectangle(R(off-15, -120, off+15, -100), fill=(170, 170, 170))
            d.text((cx+off*k, cy+40*k), "+", font=F(50*k), fill=WHITE, anchor="mm")
    elif kind == "encendedor":
        d.rounded_rectangle(R(-45, -50, 45, 125), int(14*k), fill=(220, 40, 50), outline=(120, 10, 20), width=w)
        d.rectangle(R(-45, -100, 45, -50), fill=(185, 185, 195), outline=(90, 90, 100), width=w)
        d.ellipse(R(-5, -95, 30, -60), fill=(90, 90, 100))
        fl = 1 + 0.12*math.sin(t*25)
        d.polygon(P([(-25, -105), (0, -105 - 80*fl), (25, -105)]), fill=(255, 140, 20))
        d.polygon(P([(-12, -105), (0, -105 - 45*fl), (12, -105)]), fill=(255, 235, 80))
    elif kind == "cinta":
        d.polygon(P([(80, 40), (130, 110), (100, 125), (55, 60)]), fill=(150, 150, 155))
        d.ellipse(R(-105, -105, 105, 105), fill=(160, 160, 168), outline=(90, 90, 95), width=w)
        d.ellipse(R(-58, -58, 58, 58), fill=(205, 170, 120), outline=(90, 90, 95), width=w)
        d.ellipse(R(-44, -44, 44, 44), fill=(250, 248, 240))
    elif kind == "botiquin":
        d.arc(R(-45, -130, 45, -50), 180, 360, fill=(60, 60, 60), width=max(3, int(12*k)))
        d.rounded_rectangle(R(-115, -85, 115, 105), int(20*k), fill=WHITE, outline=(200, 30, 30), width=max(3, int(9*k)))
        d.rectangle(R(-20, -55, 20, 75), fill=(220, 30, 30))
        d.rectangle(R(-65, -10, 65, 30), fill=(220, 30, 30))
    elif kind == "papas":
        d.polygon(P([(-115, -150), (115, -150), (135, 155), (-135, 155)]), fill=(252, 200, 40), outline=(200, 110, 0))
        zz = [(-115, -150)] + [(-115 + 230/12*(i+0.5), -172 if i % 2 == 0 else -150) for i in range(12)] + [(115, -150)]
        d.polygon(P(zz), fill=(230, 160, 0))
        d.ellipse(R(-85, -70, 85, 30), fill=(230, 50, 40), outline=(140, 20, 10), width=w)
        d.text((cx, cy-20*k), "PAPAS", font=F(40*k), fill=WHITE, anchor="mm")
        for (a, b) in [(-40, 90), (30, 75), (0, 110)]:
            d.ellipse(R(a-30, b-18, a+30, b+18), fill=(255, 225, 120), outline=(200, 140, 30), width=max(1, w-2))
    elif kind == "refresco":
        d.rectangle(R(-80, -135, 80, 140), fill=(200, 25, 35))
        d.ellipse(R(-80, -160, 80, -110), fill=(200, 200, 205), outline=(120, 120, 125), width=w)
        d.ellipse(R(-80, 115, 80, 165), fill=(160, 20, 30))
        d.arc(R(-140, -40, 140, 120), 200, 340, fill=WHITE, width=max(3, int(16*k)))
        d.text((cx, cy+70*k), "SODA", font=F(42*k), fill=WHITE, anchor="mm")
        d.line(P([(-50, -100), (-50, 100)]), fill=(240, 120, 120), width=max(2, int(10*k)))

def xmark(d, cx, cy, s):
    for col, wd in ((BLK, 54), (RED, 36)):
        d.line([(cx-170*s, cy-170*s), (cx+170*s, cy+170*s)], fill=col, width=int(wd*s))
        d.line([(cx-170*s, cy+170*s), (cx+170*s, cy-170*s)], fill=col, width=int(wd*s))

def check(d, cx, cy, s):
    d.ellipse([cx-42*s, cy-42*s, cx+42*s, cy+42*s], fill=(40, 180, 80), outline=BLK, width=5)
    d.line([(cx-20*s, cy), (cx-5*s, cy+18*s), (cx+22*s, cy-16*s)], fill=WHITE, width=int(11*s), joint="curve")

def freezer(d, x0, y1):
    x1, y0 = x0 + 360, y1 - 270
    d.rounded_rectangle([x0, y0, x1, y1-20], 18, fill=(236, 240, 245), outline=(80, 90, 100), width=6)
    d.rectangle([x0+16, y0+14, x1-16, y0+60], fill=(170, 215, 245), outline=(80, 90, 100), width=4)
    d.rectangle([x0+6, y0+95, x1-6, y0+165], fill=(30, 110, 210))
    d.text(((x0+x1)/2, y0+130), "HELADOS", font=F(48), fill=WHITE, anchor="mm")
    for wx in (x0+50, x1-50):
        d.ellipse([wx-20, y1-40, wx+20, y1], fill=(40, 40, 40))

# ---------------- backgrounds ----------------
DOOR = (760, 520, 1050, 1150)
GLASS = (778, 538, 1032, 1140)

def floor(d, top, base1, base2):
    vp = (540, top - 260); n = 9
    ys = [top + (H - top) * (i / n) ** 1.5 for i in range(n + 1)]
    for r in range(n):
        for c in range(-9, 9):
            def xat(col, y):
                xb = 540 + col * 170
                return vp[0] + (xb - vp[0]) * (y - vp[1]) / (H - vp[1])
            y0, y1 = ys[r], ys[r+1]
            poly = [(xat(c, y0), y0), (xat(c+1, y0), y0), (xat(c+1, y1), y1), (xat(c, y1), y1)]
            d.polygon(poly, fill=base1 if (r + c) % 2 == 0 else base2)

def shelf(d, x0, x1, y0, y1, rng):
    d.rectangle([x0, y0, x1, y1], fill=(70, 78, 85))
    lv = 4; hh = (y1 - y0) / lv
    cols = [(220, 60, 60), (60, 140, 220), (250, 200, 50), (90, 190, 110), (240, 140, 40), (180, 90, 200), (240, 240, 240)]
    for i in range(lv):
        ty = y0 + i * hh
        x = x0 + 10
        while x < x1 - 30:
            w = rng.randint(30, 60); h = rng.randint(int(hh*0.45), int(hh*0.8))
            c = rng.choice(cols)
            d.rectangle([x, ty + hh - 12 - h, min(x + w, x1 - 10), ty + hh - 12], fill=c, outline=dk(c, 0.6), width=2)
            x += w + 6
        d.rectangle([x0, ty + hh - 12, x1, ty + hh], fill=(170, 175, 180))

def ceiling(d):
    d.rectangle([0, 0, W, 210], fill=(28, 32, 38))
    d.line([(0, 210), (W, 210)], fill=(15, 15, 18), width=6)

def make_store():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(210, HORIZ):
        d.line([(0, y), (W, y)], fill=lc((52, 70, 76), (80, 100, 104), (y-210)/(HORIZ-210)))
    ceiling(d)
    floor(d, HORIZ, (205, 208, 200), (165, 170, 165))
    d.rectangle([0, HORIZ-30, W, HORIZ], fill=(45, 50, 55))
    rng = random.Random(4)
    shelf(d, 30, 340, 600, HORIZ-30, rng)
    shelf(d, 380, 690, 600, HORIZ-30, rng)
    d.rectangle([DOOR[0]-8, DOOR[1]-8, DOOR[2]+8, DOOR[3]], fill=(150, 155, 160))
    d.rectangle(DOOR, fill=(175, 180, 186))
    d.rounded_rectangle([780, 430, 1030, 495], 14, fill=(15, 15, 15), outline=(90, 90, 90), width=4)
    d.text((905, 463), "ABIERTO 24H", font=F(34), fill=(70, 255, 120), anchor="mm")
    return img

def make_outside(w, h):
    img = Image.new("RGB", (w, h)); d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lc((8, 12, 30), (25, 30, 55), y / h))
    gy = int(h * 0.62)
    d.rectangle([0, gy, w, h], fill=(22, 24, 30))
    return img

def make_coldroom_out():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(210, HORIZ):
        d.line([(0, y), (W, y)], fill=lc((60, 75, 82), (85, 102, 108), (y-210)/(HORIZ-210)))
    ceiling(d)
    floor(d, HORIZ, (205, 208, 200), (165, 170, 165))
    d.rectangle([0, HORIZ-30, W, HORIZ], fill=(45, 50, 55))
    d.rectangle([270, 500, 810, HORIZ], fill=(120, 130, 140))
    d.rounded_rectangle([330, 410, 750, 480], 14, fill=(30, 110, 210), outline=BLK, width=5)
    d.text((540, 445), "CUARTO FRÍO", font=F(42), fill=WHITE, anchor="mm")
    return img

def make_coldroom_in():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc((20, 40, 70), (8, 18, 35), y / H))
    d.rectangle([0, HORIZ, W, H], fill=(25, 40, 60))
    for x0 in (40, 330):
        d.rectangle([x0, 520, x0 + 260, HORIZ], outline=(140, 160, 180), width=8)
        for yy in range(620, HORIZ, 150):
            d.line([(x0, yy), (x0+260, yy)], fill=(140, 160, 180), width=8)
            for bx in range(x0+15, x0+245, 60):
                d.rectangle([bx, yy-70, bx+48, yy-6], fill=(60, 90, 130), outline=(30, 50, 80), width=3)
    d.rectangle([700, 470, 1040, HORIZ], fill=(105, 120, 135), outline=(60, 70, 80), width=8)
    d.rectangle([800, 560, 940, 700], fill=(15, 20, 30), outline=(60, 70, 80), width=8)
    return img

STORE = make_store(); OUT_SMALL = make_outside(GLASS[2]-GLASS[0], GLASS[3]-GLASS[1])
G2 = (110, 360, 970, 1250); OUT_BIG = make_outside(G2[2]-G2[0], G2[3]-G2[1])
COLD_OUT = make_coldroom_out(); COLD_IN = make_coldroom_in()

def flicker(t):
    k = int(t * 12)
    r = (k * 2654435761) % 97
    return 0.55 if r < 6 else (0.8 if r < 10 else 1.0)

def draw_lights(d, b):
    col = lc((80, 90, 90), (245, 255, 250), b)
    for x in (120, 450, 780):
        d.rounded_rectangle([x, 160, x+200, 182], 8, fill=col)

def glass_overlay(d, box):
    x0, y0, x1, y1 = box
    for i, off in enumerate((40, 110)):
        d.line([(x0+off, y1-60), (x0+off+ (y1-y0)*0.25, y0+60)], fill=(150, 170, 190), width=6 if i == 0 else 3)

def small_door_zombies(img, t, n=1, appear=1.0, bang=False):
    layer = OUT_SMALL.copy(); ld = ImageDraw.Draw(layer)
    for i in range(n):
        zx = [130, 60, 200][i]; s = 0.42 * appear
        zombie(ld, zx, 560 + (8 if i else 0), s, t + i*1.7, face=-1, shade=0.45, glow=True)
        if bang:
            hb = math.sin(t * 9 + i) > 0.3
            if hb:
                ld.ellipse([zx-80, 280, zx-40, 330], fill=dk((130, 175, 105), 0.6))
    img.paste(layer, (GLASS[0], GLASS[1]))
    glass_overlay(ImageDraw.Draw(img), GLASS)

# ---------------- scenes ----------------
CAPS = [
    (0.0, 1.5, "Son las *3 a.m.* y estás en un minisúper…"),
    (1.5, 3.0, "…y afuera empiezan *los gritos*"),
    (3.0, 5.3, "Primer error: *quedarte viendo*"),
    (5.3, 8.0, "Tienes *30 segundos* antes de que lleguen más"),
    (8.0, 11.0, "Desactiva la *puerta automática*"),
    (11.0, 15.0, "Bloquéala con el *refri de helados*: pesa más de lo que crees"),
    (15.0, 17.1, "*Agua.* Mucha agua."),
    (17.1, 18.6, "*Nueces*: energía que no se echa a perder"),
    (18.6, 21.0, "*Pilas* y *encendedor*"),
    (21.0, 22.4, "*Cinta canela* para todo"),
    (22.4, 25.0, "Y el *botiquín*: siempre está detrás del mostrador"),
    (25.0, 28.5, "¿*Papitas* y *refresco*?"),
    (28.5, 32.0, "Te dan sed y te bajan la energía. *Déjalos.*"),
    (32.0, 36.0, "Tu mejor escondite: el *cuarto frío*"),
    (36.0, 42.0, "*Una sola entrada*, puerta gruesa y ves toda la tienda"),
    (42.0, 46.0, "¿Arma? El *palo del trapeador*"),
    (46.0, 50.0, "Te da distancia. Y *la distancia es vida*."),
    (50.0, 52.4, "Uff… ya estás *a salvo*"),
    (53.4, 56.0, "…¿no dijimos que la *desactivaras*?"),
]

def s1(t):
    img = STORE.copy(); d = ImageDraw.Draw(img)
    b = flicker(t); draw_lights(d, b)
    d.rounded_rectangle([170, 380, 430, 470], 12, fill=(10, 10, 10), outline=(80, 80, 80), width=4)
    d.text((300, 425), "3:00 AM", font=F(52), fill=(255, 50, 50), anchor="mm")
    small_door_zombies(img, t, 1, appear=ease((t - 1.4) / 0.6)) if t > 1.4 else (img.paste(OUT_SMALL, (GLASS[0], GLASS[1])), glass_overlay(d, GLASS))
    d = ImageDraw.Draw(img)
    scared = t > 1.6
    guy(d, 420, FEET, 1.0, mood="scared" if scared else "neutral", arms="up" if t > 1.8 else "down", look=1 if scared else 0, t=t)
    if 1.5 < t < 2.6:
        bigtext(d, "¡AAAH!", 905, 760, int(70 * pop((t-1.5)/0.3)), fill=WHITE, stroke=RED, sw=10)
    chip(d, "¿SOBREVIVIRÍAS?", 300, bg=RED, size=72, appear=t/0.4)
    return img, b, (1.0 + 0.04 * t / 3)

def s2(t):
    lt = t - 3
    img = STORE.copy(); d = ImageDraw.Draw(img)
    d.rectangle([0, 210, W, HORIZ], fill=(70, 88, 94))
    d.rectangle([G2[0]-28, G2[1]-28, G2[2]+28, G2[3]+28], fill=(175, 180, 186), outline=(110, 115, 120), width=8)
    layer = OUT_BIG.copy(); ld = ImageDraw.Draw(layer)
    gw, gh = layer.size
    ld.ellipse([gw-260, 40, gw-60, 240], fill=(60, 60, 50)); ld.ellipse([gw-200, 100, gw-120, 180], fill=(255, 240, 170))
    zs = [(0.0, 430, 4.8), (2.5, 170, 2.6), (3.5, 690, 2.0)]
    for st, zx, dur in sorted(zs, key=lambda z: -z[0]):
        if lt < st: continue
        p = ease((lt - st) / dur)
        s = lerp(0.3, 1.25 if st == 0 else 0.7, p)
        fy = lerp(560, 1150 if st == 0 else 900, p)
        zombie(ld, zx, fy, s, t + st, face=-1 if zx > 430 else 1, shade=lerp(0.35, 0.7, p), glow=True)
    img.paste(layer, (G2[0], G2[1]))
    d = ImageDraw.Draw(img)
    glass_overlay(d, G2)
    if lt > 4.3:
        for (px, py) in [(380, 760), (640, 740)]:
            d.ellipse([px-45, py-55, px+45, py+55], outline=(200, 230, 210), width=6)
    guy(d, 190, 1420, 0.72, mood="scared", arms="down", look=1, t=t)
    # timer
    n = max(20, 30 - int(lt * 2))
    cx, cy = 900, 230
    d.ellipse([cx-90, cy-90, cx+90, cy+90], fill=(15, 15, 15), outline=WHITE, width=6)
    d.arc([cx-75, cy-75, cx+75, cy+75], -90, -90 + 360 * (n - 20) / 10, fill=RED, width=14)
    d.text((cx, cy), str(n), font=F(72), fill=WHITE, anchor="mm")
    return img, 1.0, 1.0 + 0.05 * lt / 5

def s3(t):
    lt = t - 8
    img = STORE.copy(); d = ImageDraw.Draw(img)
    b = flicker(t); draw_lights(d, b)
    small_door_zombies(img, t, 2, bang=True)
    d = ImageDraw.Draw(img)
    on = lt < 1.4
    d.rounded_rectangle([600, 720, 690, 850], 12, fill=(215, 215, 210), outline=BLK, width=4)
    d.text((645, 690), "PUERTA", font=F(26), fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=BLK)
    d.rounded_rectangle([620, 745, 670, 825], 10, fill=(60, 200, 90) if on else (220, 40, 40))
    d.text((645, 785), "ON" if on else "OFF", font=F(20), fill=WHITE, anchor="mm")
    if lt < 2.6:
        gx = lerp(250, 470, ease(lt / 1.0))
        guy(d, gx, FEET, 1.0, mood="scared" if lt < 1.4 else "neutral", arms="switch" if 0.9 < lt < 1.8 else "down", look=1, t=t)
        if lt > 2.0:
            fx = lerp(-380, 0, ease((lt - 2.0) / 0.6))
            freezer(d, fx, FEET)
    else:
        p = ease((lt - 2.6) / 3.7)
        fx = lerp(0, 395, p)
        guy(d, fx - 60, FEET + 20, 1.0, mood="scared", arms="push", look=1, t=t * 2)
        freezer(d, fx, FEET + 30)
        if lt > 6.3 and lt < 7.0:
            bigtext(d, "¡PUM!", 880, 900, int(90 * pop((lt-6.3)/0.25)), fill=YEL, stroke=BLK)
    chip(d, "PASO 1: CIERRA Y BLOQUEA", 300, bg=(30, 110, 210), appear=lt/0.4)
    shake = (lt > 6.3 and lt < 6.8)
    return img, b, 1.0, shake

ITEMS = [("agua", "Agua", 15.6), ("nueces", "Nueces", 17.2), ("pilas", "Pilas", 18.7),
         ("encendedor", "Encendedor", 19.7), ("cinta", "Cinta", 21.1), ("botiquin", "Botiquín", 22.5)]
POS = [(320, 545), (760, 545), (320, 875), (760, 875), (320, 1205), (760, 1205)]

def shelf_bg():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc((40, 60, 70), (20, 30, 38), y / H))
    for yy in range(420, 1500, 330):
        d.rectangle([40, yy + 260, W-40, yy + 290], fill=(150, 155, 160))
    return img
SHELF_BG = shelf_bg()

def s4(t):
    img = SHELF_BG.copy(); d = ImageDraw.Draw(img)
    for (kind, label, st), (cx, cy) in zip(ITEMS, POS):
        if t < st: continue
        sc = pop((t - st) / 0.35)
        if sc <= 0.02: continue
        cy2 = cy + (1 - min(1, (t-st)/0.35)) * 40
        card(d, cx, cy2, sc, label)
        icon(d, kind, cx, cy2 - 25*sc, 0.75*sc, t)
        if t > st + 0.45:
            check(d, cx + 125*sc, cy2 - 125*sc, pop((t - st - 0.45) / 0.3))
    chip(d, "PASO 2: LO QUE SÍ AGARRAS", 300, bg=(40, 160, 80), appear=(t-15)/0.4)
    return img, 1.0, 1.0

def s5(t):
    lt = t - 25
    img = SHELF_BG.copy(); d = ImageDraw.Draw(img)
    for i, (kind, x, st, xs) in enumerate([("papas", 300, 0.0, 1.5), ("refresco", 780, 0.5, 2.6)]):
        if lt < st: continue
        sc = pop((lt - st) / 0.4)
        wob = math.sin(lt * 6 + i) * 6
        icon(d, kind, x, 850 + wob, 1.5 * sc, t)
        if lt > xs:
            xmark(d, x, 850, pop((lt - xs) / 0.25))
    if lt > 3.5:
        bigtext(d, "¡NO!", 540, 1220, int(120 * pop((lt-3.5)/0.3)), fill=RED, stroke=WHITE, sw=10)
    chip(d, "LO QUE NO", 300, bg=RED, appear=lt/0.4)
    shake = (1.5 < lt < 1.8) or (2.6 < lt < 2.9)
    return img, 1.0, 1.0, shake

def s6(t):
    lt = t - 32
    img = COLD_OUT.copy(); d = ImageDraw.Draw(img)
    draw_lights(d, flicker(t))
    dx0, dy0, dx1, dy1 = 300, 520, 780, HORIZ
    # interior
    d.rectangle([dx0, dy0, dx1, dy1], fill=(170, 220, 255))
    for yy in range(600, dy1, 130):
        d.line([(dx0+20, yy), (dx1-20, yy)], fill=(120, 170, 210), width=8)
    op = ease((lt - 1.0) / 1.6)
    pw = (dx1 - dx0) * (1 - 0.85 * op)
    d.rectangle([dx0, dy0, dx0 + pw, dy1], fill=(175, 185, 195), outline=(90, 100, 110), width=8)
    if pw > 160:
        d.rectangle([dx0 + pw*0.3, dy0 + 70, dx0 + pw*0.7, dy0 + 200], fill=(200, 230, 245), outline=(90, 100, 110), width=6)
        for ry in (dy0 + 30, dy1 - 30):
            for rx in (dx0 + 25, dx0 + pw - 25):
                d.ellipse([rx-8, ry-8, rx+8, ry+8], fill=(110, 115, 120))
    d.rounded_rectangle([dx0 + pw - 50, 800, dx0 + pw - 25, 940], 8, fill=(60, 60, 60))
    # guy walks in
    if lt < 5.5:
        p = ease((lt - 2.4) / 2.6)
        gx = lerp(110, 600, p); gs = lerp(1.0, 0.82, p)
        guy(d, gx, lerp(FEET, 1230, p), gs, mood="scared" if lt < 2.4 else "neutral", look=1, t=t)
    # fog
    if lt > 1.2:
        fog = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog)
        rng = random.Random(7)
        for i in range(40):
            born = 1.2 + rng.random() * 8
            age = lt - born
            if age < 0: continue
            age = age % 3.5
            fx = lerp(dx0 + 120, dx0 + 120 + rng.uniform(-420, 520), age / 3.5)
            fy = lerp(1100, 1100 + rng.uniform(-120, 260), age / 3.5)
            r = 50 + age * 45
            a = int(110 * (1 - age / 3.5))
            fd.ellipse([fx-r, fy-r*0.55, fx+r, fy+r*0.55], fill=(235, 245, 255, a))
        img = Image.alpha_composite(img.convert("RGBA"), fog).convert("RGB"); d = ImageDraw.Draw(img)
    if lt > 5.6:
        sc = pop((lt - 5.6) / 0.35)
        d.rounded_rectangle([540-400*sc, 830-90*sc, 540+400*sc, 830+90*sc], int(30*sc), fill=YEL, outline=BLK, width=8)
        d.text((540, 830), "= TU BÚNKER", font=F(max(8, 80*sc)), fill=BLK, anchor="mm")
    chip(d, "PASO 3: EL ESCONDITE", 300, bg=(30, 110, 210), appear=lt/0.4)
    return img, 1.0, 1.0 + 0.04 * lt / 10

def s7(t):
    lt = t - 42
    img = STORE.copy(); d = ImageDraw.Draw(img)
    draw_lights(d, flicker(t))
    img.paste(OUT_SMALL, (GLASS[0], GLASS[1])); glass_overlay(d, GLASS)
    hits = [1.5, 2.9, 4.3]
    knock = sum(45 * ease((lt - h) / 0.25) for h in hits if lt > h)
    thrust = max([math.exp(-((lt - h) / 0.12) ** 2) for h in hits] + [0])
    zx = lerp(1000, 900, ease(lt / 1.4)) + knock - min(knock, 0)
    zx = min(zx, 1020)
    gx, gy = 190, FEET
    guy(d, gx, gy, 0.95, mood="neutral" if lt > 1.6 else "scared", arms="mop", look=1, t=t)
    hx, hy = gx + 0.95*170, gy - 0.95*320
    reach = 250 + 100 * thrust
    ex, ey = hx + reach, hy - 25
    d.line([(hx - 60, hy + 10), (ex, ey)], fill=(150, 100, 50), width=18)
    for i in range(9):
        a = -0.6 + i * 0.15
        d.line([(ex, ey), (ex + 60*math.cos(a), ey + 70 + 30*math.sin(a)*2)], fill=(200, 200, 190), width=12)
    zombie(d, zx, FEET, 0.9, t, face=-1)
    for h in hits:
        if 0 < lt - h < 0.5:
            bigtext(d, "¡BONK!", ex + 70, ey - 150, int(80 * pop((lt-h)/0.25)), fill=YEL)
    if lt > 4.0:
        p = ease((lt - 4.0) / 0.5)
        y = 640
        x0, x1 = gx + 70, zx - 70
        if x1 > x0 + 40:
            d.line([(x0, y), (lerp(x0, x1, p), y)], fill=YEL, width=10)
            d.polygon([(x0, y), (x0 + 30, y - 22), (x0 + 30, y + 22)], fill=YEL)
            if p > 0.95: d.polygon([(x1, y), (x1 - 30, y - 22), (x1 - 30, y + 22)], fill=YEL)
        bigtext(d, "DISTANCIA = VIDA", 540, 560, int(64 * pop((lt-4.0)/0.35)), fill=WHITE, stroke=BLK)
    chip(d, "PASO 4: EL ARMA", 300, bg=(150, 60, 200), appear=lt/0.4)
    shake = any(0 < lt - h < 0.18 for h in hits)
    return img, 1.0, 1.0, shake

def s8(t):
    lt = t - 50
    img = COLD_IN.copy(); d = ImageDraw.Draw(img)
    alarm = lt >= 2.5
    if alarm:
        layer = Image.new("RGB", (130, 130), (25, 30, 45)); ld = ImageDraw.Draw(layer)
        zombie(ld, 65, 200, 0.42, t, face=-1, shade=0.8, glow=True)
        img.paste(layer, (805, 565))
        d.rectangle([800, 560, 940, 700], outline=(60, 70, 80), width=8)
    guy(d, 400, 1330, 0.95, mood="scared" if alarm else "relief", arms="up" if alarm and lt > 2.8 else "down", look=1, t=t)
    if 2.4 < lt < 4.2:
        sc = pop((lt - 2.4) / 0.25)
        bigtext(d, "DING", 690, 420, int(150 * sc), fill=YEL, stroke=BLK, sw=14)
    b = 0.75 if not alarm else (1.0 if (lt - 2.4) < 0.15 else 0.8)
    shake = 2.5 < lt < 3.3
    fade = 1.0 - ease((lt - 6.0) / 0.6)
    return img, b * fade, 1.0 + (0.08 * ease((lt - 2.5) / 0.5) if alarm else 0.02 * lt / 2.5), shake

def s9(t):
    lt = t - 57
    img = Image.new("RGB", (W, H), (8, 8, 10)); d = ImageDraw.Draw(img)
    sc = pop(lt / 0.4)
    bigtext(d, "¿Qué es lo", 540, 640, int(86*sc), fill=WHITE)
    bigtext(d, "PRIMERO", 540, 760, int(130*sc), fill=YEL)
    bigtext(d, "que agarrarías tú?", 540, 890, int(80*sc), fill=WHITE)
    ay = 1080 + 25 * math.sin(lt * 8)
    d.polygon([(540-70, ay), (540+70, ay), (540, ay + 90)], fill=RED, outline=WHITE)
    d.rectangle([540-28, ay-90, 540+28, ay], fill=RED)
    if lt > 0.6:
        bigtext(d, "Comenta y te digo si sobrevives", 540, 1310, int(48*pop((lt-0.6)/0.3)), fill=WHITE)
    if lt > 1.2:
        bigtext(d, "PARTE 2: se acaba el agua…", 540, 380, int(44*pop((lt-1.2)/0.3)), fill=(170, 170, 170), sw=4)
    return img, ease(lt / 0.3), 1.0

SCENES = [(0, 3, s1), (3, 8, s2), (8, 15, s3), (15, 25, s4), (25, 32, s5), (32, 42, s6), (42, 50, s7), (50, 57, s8), (57, 60, s9)]

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
    # scene fade-in
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = b * (0.3 + 0.7 * fi) if fn is not s9 else b
    arr = np.asarray(img)
    if b < 0.999:
        arr = (arr.astype(np.float32) * b).astype(np.uint8)
    if shake:
        k = int(t * FPS)
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1)
        arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for ts in [float(x) for x in sys.argv[2:]]:
            Image.fromarray(render(ts)).resize((540, 960)).save(f"prev_{ts:05.1f}.png")
        sys.exit()
    out = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    from warp import v_of_T, DUR as WD
    n = int(WD * FPS)
    for i in range(n):
        p.stdin.write(render(min(59.99, v_of_T(i / FPS))).tobytes())
        if i % 150 == 0: print(i, flush=True)
    p.stdin.close(); p.wait()
