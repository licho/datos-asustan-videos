"""Animales nuevos dibujados directo en lib (cartoon). Todos miran a la derecha salvo flip=True.
(x, y) = centro del cuerpo; para animales en el piso, y = piso."""
import math
from .core import BLK, WHITE, RED, YEL, dk, lc

def _P(x, y, s, flip):
    fx = -1 if flip else 1
    return lambda px, py: (x + fx * px * s, y + py * s)

def mosquito(d, x, y, s=1.0, t=0.0, flip=False, female=False, mask=False, hat=False, mood="normal", fly=True):
    """Mosquito (patrón rayado tipo Aedes). mood: normal | angry | happy. Centro en el tórax."""
    P = _P(x, y, s, flip); W_ = lambda v: max(2, int(v * s))
    BODY, STRIPE, LEGC = (60, 60, 70), (235, 235, 240), (45, 45, 50)
    def ell(cx, cy, rx, ry, **kw):
        (ax, ay), (bx, by) = P(cx - rx, cy - ry), P(cx + rx, cy + ry)
        d.ellipse([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], **kw)
    # alas (detrás)
    flap = math.sin(t * 55) if fly else 0.3
    for k, off in enumerate((0, 18)):
        tipy = -150 + 70 * flap + off
        d.polygon([P(-5, -40), P(-90, tipy - 10), P(-170, tipy + 25), P(-60, -20)], fill=lc((200, 225, 245), (240, 245, 250), k * .5), outline=(120, 150, 180))
    # patas
    for bx, k1, k2 in ((-25, -70, -150), (0, 10, -40), (25, 70, 150)):
        sw = math.sin(t * 9 + bx) * 6 if fly else 0
        d.line([P(bx, 35), P(bx + k1 * .5, 95 + sw), P(bx + k2 * .55, 190 + sw)], fill=LEGC, width=W_(5), joint="curve")
        d.line([P(bx + 6, 35), P(bx + k1 * .35 + 10, 100 - sw), P(bx + k2 * .4 + 14, 185 - sw)], fill=LEGC, width=W_(5), joint="curve")
    # abdomen rayado
    ell(-120, 15, 100, 34, fill=BODY, outline=BLK, width=W_(4))
    for k in range(5):
        cx = -190 + k * 33
        (ax, ay), (bx, by) = P(cx, -12), P(cx + 9, 40)
        d.rectangle([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], fill=STRIPE)
    ell(-120, 15, 100, 34, outline=BLK, width=W_(4))
    # tórax
    ell(0, -5, 52, 46, fill=BODY, outline=BLK, width=W_(4))
    d.line([P(-20, -35), P(5, -10), P(-20, 20)], fill=STRIPE, width=W_(6))
    # trompa
    if not mask:
        d.line([P(95, 10), P(200, 70)], fill=BLK, width=W_(6))
    # cabeza
    ell(70, -5, 36, 34, fill=BODY, outline=BLK, width=W_(4))
    # antenas
    for k, (ex, ey) in enumerate(((120, -80), (95, -95))):
        d.line([P(78, -30), P(ex, ey)], fill=LEGC, width=W_(4))
        if not female:
            for j in range(1, 5):
                u = j / 5; px, py = 78 + (ex - 78) * u, -30 + (ey + 30) * u
                d.line([P(px - 9, py - 6), P(px + 9, py + 6)], fill=LEGC, width=W_(2))
    # ojo
    ell(82, -12, 19, 19, fill=WHITE, outline=BLK, width=W_(3))
    pr = 9 if mood != "angry" else 7
    ell(88, -10, pr, pr, fill=(170, 20, 20) if mood == "angry" else BLK)
    if mood == "angry":
        d.line([P(62, -38), P(102, -26)], fill=BLK, width=W_(6))
    if mood == "happy":
        d.arc([*P(66, 4), *P(96, 22)] if not flip else [*P(96, 4), *P(66, 22)], 0, 180, fill=BLK, width=W_(3))
    if female:   # moño rosa
        d.polygon([P(55, -42), P(30, -62), P(30, -26)], fill=(240, 100, 160), outline=BLK)
        d.polygon([P(55, -42), P(80, -62), P(80, -26)], fill=(240, 100, 160), outline=BLK)
        ell(55, -42, 9, 9, fill=(250, 140, 190), outline=BLK, width=W_(2))
    if mask:     # cubrebocas y gorro de cirujano
        d.polygon([P(68, 2), P(112, 0), P(110, 30), P(72, 30)], fill=(150, 210, 220), outline=BLK)
        d.line([P(72, 8), P(40, -5)], fill=WHITE, width=W_(3))
        d.chord([*P(36, -60), *P(104, -10)] if not flip else [*P(104, -60), *P(36, -10)], 180, 360, fill=(110, 190, 200), outline=BLK, width=W_(3))
    if hat:      # gorro de fiesta
        d.polygon([P(50, -34), P(90, -34), P(68, -110)], fill=(250, 200, 40), outline=BLK)
        ell(68, -112, 9, 9, fill=RED, outline=BLK, width=W_(2))

def shark(d, x, y, s=1.0, t=0.0, flip=False, mood="neutral"):
    """Tiburón de lado. mood: neutral | cry | grin. Centro del cuerpo."""
    P = _P(x, y, s, flip); W_ = lambda v: max(2, int(v * s))
    G, B = (120, 140, 160), (235, 240, 245)
    sw = math.sin(t * 4) * 12
    d.polygon([P(-170, 0), P(-280, -90 + sw), P(-245, 0), P(-280, 85 + sw)], fill=G, outline=BLK)          # cola
    d.polygon([P(-30, -60), P(10, -170), P(60, -55)], fill=G, outline=BLK)                                    # aleta dorsal
    body = [P(-190, 0), P(-120, -60), P(20, -75), P(150, -50), P(220, 0), P(150, 50), P(20, 70), P(-120, 50)]
    d.polygon(body, fill=G, outline=BLK, width=W_(4))
    d.polygon([P(-120, 30), P(20, 50), P(150, 35), P(205, 12), P(150, 50), P(20, 70), P(-120, 50)], fill=B)
    d.polygon([P(0, 35), P(-60, 110), P(50, 45)], fill=dk(G, .85), outline=BLK)                              # aleta pectoral
    for k in range(3): d.line([P(60 + k * 16, -20), P(54 + k * 16, 15)], fill=dk(G, .7), width=W_(3))     # agallas
    ex, ey = 130, -20
    (ax, ay), (bx, by) = P(ex - 15, ey - 15), P(ex + 15, ey + 15)
    d.ellipse([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], fill=WHITE, outline=BLK, width=W_(3))
    (ax, ay), (bx, by) = P(ex - 6, ey - 4), P(ex + 6, ey + 8)
    d.ellipse([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], fill=BLK)
    if mood == "cry":
        d.line([P(110, -48), P(150, -38)], fill=BLK, width=W_(5))
        d.arc([*P(140, 20), *P(200, 50)] if not flip else [*P(200, 20), *P(140, 50)], 200, 340, fill=BLK, width=W_(4))
        for k in range(2):
            ph = (t * 1.5 + k * .5) % 1
            tx, ty = P(128, 0 + ph * 120)
            r = 9 * s
            d.ellipse([tx - r, ty - r, tx + r, ty + r * 1.4], fill=(120, 190, 250), outline=BLK)
    else:
        d.line([P(140, 32), P(205, 14)], fill=BLK, width=W_(4))
        for k in range(4):
            px = 148 + k * 14
            d.polygon([P(px, 30 - k * 4), P(px + 7, 18 - k * 4), P(px + 12, 28 - k * 4)], fill=WHITE, outline=BLK)

def snake(d, x, y, s=1.0, t=0.0, flip=False, mood="neutral"):
    """Serpiente enroscada; y = piso."""
    P = _P(x, y, s, flip); W_ = lambda v: max(2, int(v * s))
    G, D = (90, 170, 70), (50, 110, 40)
    for k, (rx, ry, cy) in enumerate(((160, 50, -45), (130, 45, -100), (100, 40, -150))):
        (ax, ay), (bx, by) = P(-rx, cy - ry), P(rx, cy + ry)
        d.ellipse([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], fill=G if k % 2 == 0 else lc(G, D, .3), outline=BLK, width=W_(4))
        for j in range(-2, 3):
            (px, py) = P(j * rx * .35, cy - ry * .2)
            d.ellipse([px - 8 * s, py - 6 * s, px + 8 * s, py + 6 * s], fill=D)
    sway = math.sin(t * 2) * 10
    pts = [P(40, -170), P(70 + sway, -250), P(55 + sway, -320)]
    d.line(pts, fill=BLK, width=W_(52), joint="curve"); d.line(pts, fill=G, width=W_(44), joint="curve")
    hx, hy = 70 + sway, -350
    (ax, ay), (bx, by) = P(hx - 55, hy - 38), P(hx + 55, hy + 38)
    d.ellipse([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], fill=G, outline=BLK, width=W_(4))
    for ox in (-18, 22):
        (ax, ay), (bx, by) = P(hx + ox - 12, hy - 22), P(hx + ox + 12, hy + 2)
        d.ellipse([min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)], fill=YEL, outline=BLK, width=W_(2))
        cx_ = (ax + bx) / 2; d.line([(cx_, ay + 4 * s), (cx_, by - 4 * s)], fill=BLK, width=W_(4))
    if int(t * 3) % 2 == 0:
        d.line([P(hx + 50, hy + 15), P(hx + 95, hy + 22), P(hx + 110, hy + 10)], fill=RED, width=W_(4))
        d.line([P(hx + 95, hy + 22), P(hx + 112, hy + 34)], fill=RED, width=W_(4))

def lion(d, x, y, s=1.0, t=0.0, mood="neutral"):
    """León sentado de frente; y = piso."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    BODY, MANE = (225, 170, 70), (170, 95, 35)
    d.ellipse([x - S(130), y - S(260), x + S(130), y], fill=BODY, outline=BLK, width=W_(4))
    for ox in (-60, 60):
        d.rounded_rectangle([x + S(ox) - S(30), y - S(150), x + S(ox) + S(30), y], S(20), fill=BODY, outline=BLK, width=W_(4))
    hy = y - S(330); n = 18
    pts = []
    for k in range(n * 2):
        a = k / (n * 2) * 2 * math.pi; r = S(165) if k % 2 == 0 else S(130)
        pts.append((x + math.cos(a) * r, hy + math.sin(a) * r))
    d.polygon(pts, fill=MANE, outline=BLK)
    for ox in (-80, 80): d.ellipse([x + S(ox) - S(28), hy - S(110), x + S(ox) + S(28), hy - S(55)], fill=BODY, outline=BLK, width=W_(3))
    d.ellipse([x - S(110), hy - S(100), x + S(110), hy + S(110)], fill=BODY, outline=BLK, width=W_(4))
    for ox in (-42, 42):
        d.ellipse([x + S(ox) - S(17), hy - S(40), x + S(ox) + S(17), hy - S(6)], fill=WHITE, outline=BLK, width=W_(3))
        d.ellipse([x + S(ox) - S(7), hy - S(30), x + S(ox) + S(7), hy - S(14)], fill=BLK)
    d.ellipse([x - S(55), hy + S(10), x + S(55), hy + S(80)], fill=(245, 225, 180), outline=BLK, width=W_(3))
    d.polygon([(x - S(18), hy + S(14)), (x + S(18), hy + S(14)), (x, hy + S(34))], fill=(90, 50, 40))
    d.arc([x - S(30), hy + S(30), x, hy + S(60)], 0, 180, fill=BLK, width=W_(3)); d.arc([x, hy + S(30), x + S(30), hy + S(60)], 0, 180, fill=BLK, width=W_(3))

def crab(d, x, y, s=1.0, t=0.0, mood="normal"):
    """Cangrejo de frente; y = piso. mood: normal | confused."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); R = (225, 80, 60)
    for side in (-1, 1):
        for k in range(3):
            bx = x + side * S(70 + k * 18); sw = math.sin(t * 8 + k) * S(6)
            d.line([(bx, y - S(70)), (bx + side * S(55), y - S(95) + sw), (bx + side * S(75), y)], fill=dk(R, .75), width=W_(9), joint="curve")
        cx = x + side * S(150); cy = y - S(170) + math.sin(t * 3 + side) * S(8)
        d.line([(x + side * S(80), y - S(100)), (cx, cy + S(30))], fill=R, width=W_(16))
        d.pieslice([cx - S(45), cy - S(40), cx + S(45), cy + S(40)], 20 if side > 0 else 200, 340 if side > 0 else 160, fill=R, outline=BLK, width=W_(4))
    d.ellipse([x - S(110), y - S(150), x + S(110), y - S(40)], fill=R, outline=BLK, width=W_(5))
    for side in (-1, 1):
        ex = x + side * S(40)
        d.line([(ex, y - S(140)), (ex, y - S(200))], fill=dk(R, .8), width=W_(8))
        d.ellipse([ex - S(18), y - S(228), ex + S(18), y - S(192)], fill=WHITE, outline=BLK, width=W_(3))
        off = S(6) * (side if mood == "confused" else 1)
        d.ellipse([ex - S(7) + off, y - S(217), ex + S(7) + off, y - S(203)], fill=BLK)
    if mood == "confused": d.arc([x - S(30), y - S(105), x + S(30), y - S(75)], 200, 340, fill=BLK, width=W_(4))
    else: d.arc([x - S(35), y - S(120), x + S(35), y - S(80)], 20, 160, fill=BLK, width=W_(4))

def coral(d, x, y, s=1.0, t=0.0, kind="branch", col=(240, 120, 150), spawn=0.0):
    """Coral; y = fondo marino. kind: branch | brain. spawn 0..1 suelta huevecillos."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    if kind == "brain":
        d.chord([x - S(120), y - S(150), x + S(120), y + S(40)], 180, 360, fill=col, outline=BLK, width=W_(4))
        for k in range(4): d.arc([x - S(100) + k * S(20), y - S(130) + k * S(15), x + S(100) - k * S(20), y + S(20) - k * S(5)], 190, 350, fill=dk(col, .75), width=W_(4))
    else:
        def br(x0, y0, ang, L, depth):
            x1, y1 = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L + math.sin(t * 1.5 + depth) * S(2)
            d.line([(x0, y0), (x1, y1)], fill=BLK, width=W_(30 - depth * 6)); d.line([(x0, y0), (x1, y1)], fill=col, width=W_(22 - depth * 6))
            if depth < 2:
                br(x1, y1, ang - .45, L * .75, depth + 1); br(x1, y1, ang + .45, L * .75, depth + 1)
            else: d.ellipse([x1 - S(12), y1 - S(12), x1 + S(12), y1 + S(12)], fill=col, outline=BLK, width=W_(3))
        br(x, y, -math.pi / 2, S(110), 0)
    import random as _r
    rnd = _r.Random(int(x))
    for k in range(int(spawn * 18)):
        ph = (t * .4 + k / 18) % 1
        px = x + rnd.uniform(-S(90), S(90)) + math.sin(t + k) * S(10); py = y - S(150) - ph * S(500)
        d.ellipse([px - S(7), py - S(7), px + S(7), py + S(7)], fill=(255, 210, 220), outline=dk(col, .7))

def mammoth(d, x, y, s=1.0, t=0.0, flip=False):
    """Mamut lanudo de lado; y = piso."""
    S = lambda v: v * s; f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s)); B, D = (130, 85, 50), (95, 60, 35)
    for dx in (-110, -40, 60, 120):
        d.rounded_rectangle([x + f * S(dx) - S(32), y - S(170), x + f * S(dx) + S(32), y], int(S(16)), fill=D, outline=BLK, width=W_(4))
    d.ellipse([x - S(200), y - S(340), x + S(170), y - S(110)], fill=B, outline=BLK, width=W_(5))
    for k in range(9):
        px = x - S(180) + k * S(42); d.polygon([(px, y - S(150)), (px + S(20), y - S(95)), (px + S(40), y - S(150))], fill=B)
    hx = x + f * S(190); hy = y - S(260)
    d.ellipse([hx - S(95), hy - S(105), hx + S(95), hy + S(80)], fill=B, outline=BLK, width=W_(5))
    d.ellipse([hx - f * S(55) - S(55), hy - S(60), hx - f * S(55) + S(55), hy + S(50)], fill=D, outline=BLK, width=W_(3))
    sw = math.sin(t * 2) * S(15)
    trunk = [(hx + f * S(70), hy + S(20)), (hx + f * S(110), hy + S(110)), (hx + f * S(95) + sw, hy + S(200)), (hx + f * S(130) + sw, hy + S(240))]
    d.line(trunk, fill=BLK, width=W_(44), joint="curve"); d.line(trunk, fill=B, width=W_(36), joint="curve")
    d.arc([hx + f * S(10) - S(60), hy + S(10), hx + f * S(10) + S(130), hy + S(170)] if f > 0 else [hx - S(130), hy + S(10), hx + S(60), hy + S(170)], 20 if f > 0 else 70, 160 if f > 0 else 200, fill=(245, 240, 225), width=W_(16))
    d.ellipse([hx + f * S(35) - S(11), hy - S(40), hx + f * S(35) + S(11), hy - S(18)], fill=BLK)

def stego(d, x, y, s=1.0, t=0.0, mood="normal", flip=False):
    """Estegosaurio; y = piso. mood: normal | confused."""
    S = lambda v: v * s; f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s)); G, P = (120, 170, 90), (220, 120, 70)
    for k in range(7):
        px = x - S(150) + k * S(50); hgt = S(70 + 50 * math.sin(k / 6 * math.pi))
        d.polygon([(px - S(28), y - S(220)), (px, y - S(220) - hgt), (px + S(28), y - S(220))], fill=P, outline=BLK)
    d.polygon([(x - f * S(170), y - S(160)), (x - f * S(360), y - S(120)), (x - f * S(170), y - S(110))], fill=G, outline=BLK)
    for k in range(2): d.polygon([(x - f * S(320 + k * 25), y - S(125)), (x - f * S(340 + k * 25), y - S(190)), (x - f * S(300 + k * 25), y - S(128))], fill=(240, 230, 200), outline=BLK)
    for dx in (-110, -40, 50, 120): d.rounded_rectangle([x + f * S(dx) - S(26), y - S(140), x + f * S(dx) + S(26), y], int(S(12)), fill=dk(G, .85), outline=BLK, width=W_(4))
    d.ellipse([x - S(200), y - S(260), x + S(200), y - S(90)], fill=G, outline=BLK, width=W_(5))
    hx = x + f * S(250); d.line([(x + f * S(150), y - S(170)), (hx, y - S(130))], fill=BLK, width=W_(50)); d.line([(x + f * S(150), y - S(170)), (hx, y - S(130))], fill=G, width=W_(42))
    d.ellipse([hx - S(55), y - S(170), hx + S(55), y - S(90)], fill=G, outline=BLK, width=W_(4))
    d.ellipse([hx + f * S(10) - S(13), y - S(150), hx + f * S(10) + S(13), y - S(124)], fill=WHITE, outline=BLK, width=2)
    d.ellipse([hx + f * S(14) - S(6), y - S(144), hx + f * S(14) + S(6), y - S(132)], fill=BLK)
    if mood == "confused": d.text((hx, y - S(240)), "?", font=None, fill=BLK)

def trex(d, x, y, s=1.0, t=0.0, flip=False, roar=False):
    """Tiranosaurio; y = piso."""
    S = lambda v: v * s; f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s)); G = (90, 150, 110)
    d.polygon([(x - f * S(60), y - S(260)), (x - f * S(330), y - S(150)), (x - f * S(60), y - S(190))], fill=G, outline=BLK)
    for dx, k in ((-50, 0), (40, 1)):
        d.polygon([(x + f * S(dx) - S(35), y - S(210)), (x + f * S(dx) + S(35), y - S(210)), (x + f * S(dx) + S(20), y), (x + f * S(dx) - S(30), y)], fill=dk(G, .85), outline=BLK)
    d.ellipse([x - S(120), y - S(380), x + S(130), y - S(160)], fill=G, outline=BLK, width=W_(5))
    hx, hy = x + f * S(170), y - S(450)
    d.line([(x + f * S(60), y - S(340)), (hx - f * S(30), hy + S(30))], fill=BLK, width=W_(90)); d.line([(x + f * S(60), y - S(340)), (hx - f * S(30), hy + S(30))], fill=G, width=W_(80))
    jaw = S(40) if roar else S(10)
    d.rounded_rectangle([hx - S(90), hy - S(60), hx + S(110), hy + S(25)], int(S(30)), fill=G, outline=BLK, width=W_(5))
    d.rounded_rectangle([hx - S(70), hy + S(10) + jaw, hx + S(100), hy + S(55) + jaw], int(S(20)), fill=G, outline=BLK, width=W_(5))
    for k in range(5): d.polygon([(hx - S(40) + k * S(30), hy + S(25)), (hx - S(30) + k * S(30), hy + S(45)), (hx - S(20) + k * S(30), hy + S(25))], fill=WHITE, outline=BLK)
    d.ellipse([hx + f * S(10) - S(16), hy - S(45), hx + f * S(10) + S(16), hy - S(13)], fill=WHITE, outline=BLK, width=3); d.ellipse([hx + f * S(14) - S(7), hy - S(36), hx + f * S(14) + S(7), hy - S(22)], fill=BLK)
    d.line([(x + f * S(100), y - S(300)), (x + f * S(150), y - S(260)), (x + f * S(165), y - S(275))], fill=BLK, width=W_(16))
