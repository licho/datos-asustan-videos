"""Animales nuevos dibujados directo en lib (cartoon). Todos miran a la derecha salvo flip=True.
(x, y) = centro del cuerpo; para animales en el piso, y = piso."""
import math
from .core import BLK, WHITE, RED, YEL, dk, lc, F

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
    if mood == "confused": d.text((hx, y - S(250)), "?", font=F(int(S(90))), fill=BLK, anchor="mm", stroke_width=W_(5), stroke_fill=WHITE)

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

def emu(d, x, y, s=1.0, t=0.0, flip=False, run=True, mood="normal"):
    """Emú de caricatura (plumaje café, cuello azulado, patas largas). y = piso. run=True: patas corriendo."""
    S = lambda v: v * s; f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    B, N, L = (120, 100, 80), (120, 140, 175), (110, 105, 95)
    ph = t * 14 if run else 0
    for k in (0, 1):
        a = math.sin(ph + k * math.pi) * (.6 if run else 0)
        hip = (x + f * S(10 + k * 20), y - S(250)); knee = (hip[0] + f * math.sin(a) * S(80) - f * S(20), y - S(130))
        foot = (knee[0] - f * math.sin(a) * S(30) + f * S(15), y - max(0, math.cos(ph + k * math.pi)) * S(40) * (1 if run else 0))
        d.line([hip, knee, foot], fill=BLK, width=W_(30), joint="curve"); d.line([hip, knee, foot], fill=L, width=W_(21), joint="curve")
        for dx in (-25, 0, 25): d.line([foot, (foot[0] + f * S(30) + S(dx) * .6, foot[1] + S(4))], fill=BLK, width=W_(6))
    d.ellipse([x - S(180), y - S(430), x + S(150), y - S(215)], fill=B, outline=BLK, width=W_(5))
    for k in range(8):
        px = x - S(150) + k * S(34); d.polygon([(px, y - S(240)), (px + S(18), y - S(190)), (px + S(36), y - S(240))], fill=B, outline=BLK)
    d.ellipse([x - S(175), y - S(425), x + S(145), y - S(225)], fill=B)
    for k in range(5): d.arc([x - S(120) + k * S(50), y - S(380), x - S(60) + k * S(50), y - S(300)], 200, 340, fill=dk(B, .8), width=W_(5))
    nx = x + f * S(120); neck = [(nx, y - S(360)), (nx + f * S(35), y - S(440)), (nx + f * S(30), y - S(495))]
    d.line(neck, fill=BLK, width=W_(48), joint="curve"); d.line(neck, fill=N, width=W_(40), joint="curve")
    hx, hy = nx + f * S(40), y - S(515)
    d.ellipse([hx - S(48), hy - S(42), hx + S(48), hy + S(42)], fill=N, outline=BLK, width=W_(4))
    d.polygon([(hx + f * S(35), hy - S(8)), (hx + f * S(95), hy + S(8)), (hx + f * S(35), hy + S(22))], fill=(70, 60, 55), outline=BLK)
    er = S(20) if mood == "crazy" else S(16)
    d.ellipse([hx + f * S(5) - er, hy - S(18) - er, hx + f * S(5) + er, hy - S(18) + er], fill=WHITE, outline=BLK, width=W_(3))
    px = hx + f * S(10) + (math.sin(t * 9) * S(5) if mood == "crazy" else 0)
    d.ellipse([px - S(7), hy - S(25), px + S(7), hy - S(11)], fill=BLK)

def army_ant(d, x, y, s=1.0, t=0.0, flip=False, helmet=False):
    """Hormiga guerrera (café rojizo, mandíbulas grandes) de lado; y = piso, mira a la derecha. Largo ≈ 230·s. helmet=True: casquito verde."""
    S = lambda v: v * s; f = -1 if flip else 1; W_ = lambda v: max(1, int(v * s)); C = (150, 60, 30)
    for i, dx in enumerate((-30, 10, 45)):
        for k, side in enumerate((-1, 1)):
            sw = math.sin(t * 16 + i * 2 + k * math.pi) * S(14)
            base = (x + f * S(dx), y - S(45)); knee = (base[0] + f * S(15) + sw, y - S(75)); foot = (base[0] + f * S(30) * side + sw, y)
            d.line([base, knee, foot], fill=BLK, width=W_(7))
    d.ellipse([x - f * S(40) - S(70), y - S(110), x - f * S(40) + S(70), y - S(20)], fill=C, outline=BLK, width=W_(4))
    d.ellipse([x - S(35), y - S(85), x + S(35), y - S(40)], fill=C, outline=BLK, width=W_(4))
    hx, hy = x + f * S(70), y - S(80)
    d.ellipse([hx - S(42), hy - S(36), hx + S(42), hy + S(36)], fill=C, outline=BLK, width=W_(4))
    for k in (-1, 1):
        d.arc([hx + f * S(20) - S(40), hy + k * S(6) - S(25), hx + f * S(20) + S(40), hy + k * S(6) + S(25)], 300 if f > 0 else 120, 60 if f > 0 else 240, fill=BLK, width=W_(8))
    d.line([(hx, hy - S(30)), (hx + f * S(30), hy - S(75)), (hx + f * S(70), hy - S(70))], fill=BLK, width=W_(5))
    d.ellipse([hx + f * S(12) - S(9), hy - S(17), hx + f * S(12) + S(9), hy - S(1)], fill=WHITE, outline=BLK, width=W_(2))
    d.ellipse([hx + f * S(15) - S(4), hy - S(12), hx + f * S(15) + S(4), hy - S(5)], fill=BLK)
    if helmet:
        d.chord([hx - S(46), hy - S(64), hx + S(46), hy + S(10)], 180, 360, fill=(80, 100, 60), outline=BLK, width=W_(3))

def ant_column(d, path, t, s=0.4, gap=95, speed=180, helmet=False):
    """Columna de hormigas marchando sobre una línea path=[(x,y),...] (pies en la línea). Avanzan con el tiempo."""
    segs = []; total = 0
    for a, b in zip(path, path[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); segs.append((a, b, L)); total += L
    off = (t * speed) % (gap * s / .4)
    pos = off; k = 0
    while pos < total:
        acc = 0
        for a, b, L in segs:
            if acc + L >= pos:
                u = (pos - acc) / L; px, py = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
                army_ant(d, px, py, s, t + k * .37, flip=b[0] < a[0], helmet=helmet); break
            acc += L
        pos += gap * s / .4; k += 1

def hawk(d, x, y, s=1.0, t=0.0, flip=False, dive=False):
    """Halcón de caricatura volando, mirando a la derecha (flip=True: a la izquierda); (x, y) = centro del cuerpo.
    Pico ganchudo amarillo, ceja enojada, alas con plumas en punta, cola de abanico rayada y garras amarillas.
    dive=True: en picada, alas hacia atrás y garras por delante. A s=1 mide ~330 de largo y ~600 de envergadura."""
    f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    P = lambda u, v: (x + f * u * s, y + v * s)
    BR, DK, CR, YL = (140, 90, 50), (95, 60, 35), (245, 232, 205), (250, 200, 40)
    def wing(u0, v0, ang, span, col, flap):
        a = math.radians(ang + flap)
        ca, sa = math.cos(a), math.sin(a)
        R = lambda L, w: P(u0 + L * ca * span - w * sa * span, v0 - L * sa * span - w * ca * span)
        pts = [R(0, 0), R(.55, .06), R(1.0, .02)]
        for k in range(5):                                    # plumas en punta (dedos)
            L0 = 1.0 - k * .1
            pts += [R(L0 - .02, -.06), R(L0 - .08, -.03)]
        for k in range(4): pts += [R(.48 - k * .12, -.24), R(.42 - k * .12, -.2)]
        pts.append(R(0, -.22))
        d.polygon(pts, fill=col, outline=BLK); d.line(pts + [pts[0]], fill=BLK, width=W_(4), joint="curve")
        for k in range(3): d.line([R(.15 + k * .12, -.04), R(.12 + k * .12, -.17)], fill=dk(col, .75), width=W_(3))
    flap = 0 if dive else math.sin(t * 8) * 22
    # cola de abanico rayada
    tail = [P(-110, -10), P(-230, -45), P(-245, 0), P(-230, 45), P(-110, 20)]
    d.polygon(tail, fill=BR, outline=BLK); d.line(tail + [tail[0]], fill=BLK, width=W_(4))
    for k in range(2): d.line([P(-165 - k * 35, -30 + k * 0), P(-165 - k * 35, 30)], fill=DK, width=W_(6))
    # ala de atrás
    if dive: wing(-10, -20, 140, 300, DK, 0)
    else: wing(20, -30, 95, 280, DK, flap)
    # garras
    if dive:
        for k, dv in enumerate((0, 22)):
            d.line([P(40, 40 + dv), P(130, 75 + dv)], fill=YL, width=W_(12))
            for c in (-1, 0, 1): d.line([P(130, 75 + dv), P(152, 75 + dv + c * 14)], fill=BLK, width=W_(5))
    else:
        for dv in (0, 18):
            d.line([P(-30, 40), P(-80, 70 + dv)], fill=YL, width=W_(11))
            for c in (-1, 1): d.line([P(-80, 70 + dv), P(-98, 70 + dv + c * 10)], fill=BLK, width=W_(5))
    # cuerpo
    d.ellipse([P(-130, -55)[0] if f > 0 else P(110, -55)[0], y - 55 * s, P(110, 55)[0] if f > 0 else P(-130, 55)[0], y + 55 * s], fill=BR, outline=BLK, width=W_(5))
    belly = [P(-60, 10), P(30, 0), P(100, 15), P(70, 50), P(-40, 50)]
    d.polygon(belly, fill=CR)
    for k in range(5): d.line([P(-30 + k * 25, 22), P(-36 + k * 25, 40)], fill=BR, width=W_(5))
    # cabeza
    hx, hy = 125, -30
    d.ellipse([min(P(hx - 55, 0)[0], P(hx + 55, 0)[0]), y + (hy - 52) * s, max(P(hx - 55, 0)[0], P(hx + 55, 0)[0]), y + (hy + 52) * s], fill=BR, outline=BLK, width=W_(5))
    cheek = [P(hx - 10, hy + 5), P(hx + 50, hy - 5), P(hx + 45, hy + 40), P(hx - 5, hy + 45)]
    d.polygon(cheek, fill=CR)
    beak = [P(hx + 42, hy - 18), P(hx + 92, hy - 6), P(hx + 98, hy + 18), P(hx + 82, hy + 8), P(hx + 44, hy + 12)]
    d.polygon(beak, fill=YL, outline=BLK); d.line(beak + [beak[0]], fill=BLK, width=W_(4))
    d.polygon([P(hx + 86, hy - 4), P(hx + 98, hy + 18), P(hx + 84, hy + 9)], fill=(60, 60, 65))
    ex, ey = P(hx + 22, hy - 12)
    d.ellipse([ex - 17 * s, ey - 17 * s, ex + 17 * s, ey + 17 * s], fill=YL, outline=BLK, width=W_(3))
    d.ellipse([ex - 8 * s, ey - 8 * s, ex + 8 * s, ey + 8 * s], fill=BLK)
    d.line([P(hx - 5, hy - 40), P(hx + 48, hy - 20)], fill=DK, width=W_(11))      # ceja enojada
    # ala de enfrente
    if dive: wing(0, -10, 155, 330, BR, 0)
    else: wing(0, -20, 118, 310, BR, flap)

def _poly(d, pts, col, w):
    d.polygon(pts, fill=col, outline=BLK); d.line(pts + [pts[0]], fill=BLK, width=w, joint="curve")

def tyranno(d, x, y, s=1.0, t=0.0, mood="grin", mouth=0.3, run=False, napkin=False, collar=None, flip=False, col=(95, 160, 95)):
    """Tiranosaurio de caricatura (más detallado que trex): cabezota, bracitos, panza clara y rayas. y = piso, mira a la derecha.
    mood: grin | angry | sad | tired (con sudor). mouth 0..1 = qué tan abierta la boca. run: patas corriendo.
    napkin: servilleta al cuello. collar: color del collar de mascota (o None). A s=1 mide ~640 de largo y ~600 de alto.
    Cabeza ~ (x + 230s, y - 470s); boca ~ (x + 300s, y - 430s)."""
    f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    P = lambda u, v: (x + f * u * s, y + v * s)
    DK, BL = dk(col, .72), lc(col, (245, 235, 190), .55)
    def oval(u, v, ru, rv, c, w=5):
        q = [P(u + ru * math.cos(a / 18 * math.pi), v + rv * math.sin(a / 18 * math.pi)) for a in range(36)]
        _poly(d, q, c, W_(w))
    sw = math.sin(t * 9) if run else 0
    bob = abs(math.sin(t * 9)) * 12 if run else 0
    Q = lambda u, v: P(u, v - bob)
    # pata de atrás (lejana)
    for leg, (ph, c) in enumerate(((math.pi, DK), (0, col))):
        a = math.sin(t * 9 + ph) * .5 if run else (.08 if leg else -.08)
        hx, hy = 10 + leg * 20, -250
        kx, ky = hx + 70 * math.sin(a) + 40, -120
        fx, fy = hx + 150 * math.sin(a) - 10, -18 if not run else -18 - max(0, math.sin(t * 9 + ph)) * 40
        if leg == 0:
            _poly(d, [Q(hx - 50, hy), Q(hx + 60, hy - 20), Q(kx + 30, ky), Q(kx - 25, ky + 10)], c, W_(5))
        d.line([Q(kx, ky), P(fx, fy)], fill=BLK, width=W_(48)); d.line([Q(kx, ky), P(fx, fy)], fill=c, width=W_(38))
        _poly(d, [P(fx - 45, fy - 10), P(fx + 70, fy - 6), P(fx + 80, fy + 18), P(fx - 45, fy + 18)], c, W_(4))
        for k in range(3): _poly(d, [P(fx + 30 + k * 18, fy - 4), P(fx + 44 + k * 18, fy - 4), P(fx + 37 + k * 18, fy + 8)], (240, 235, 220), W_(2))
    # cola
    tw_ = math.sin(t * 3) * 25
    _poly(d, [Q(-60, -330), Q(-380, -230 + tw_), Q(-395, -215 + tw_), Q(-60, -230)], col, W_(5))
    for k in range(4): d.line([Q(-110 - k * 60, -322 + k * 22 + tw_ * k / 5), Q(-110 - k * 60, -248 + k * 2 + tw_ * k / 5)], fill=DK, width=W_(7))
    # cuerpo y panza
    oval(10, -310, 165, 125, col)
    oval(60, -280, 95, 85, BL, 3)
    for k in range(4): d.line([Q(20 + k * 22, -230 + k * 2), Q(100, -238 + k * 4)], fill=dk(BL, .85), width=W_(3))
    for k in range(4): d.line([Q(-120 + k * 45, -415 + abs(k - 1.5) * 8), Q(-110 + k * 45, -365)], fill=DK, width=W_(9))
    # pata cercana encima del cuerpo
    a = math.sin(t * 9) * .5 if run else .08
    oval(40 + 70 * math.sin(a) * .3, -220, 70, 90, col)
    # cuello
    _poly(d, [Q(80, -400), Q(170, -470), Q(210, -390), Q(140, -330)], col, W_(5))
    if collar:
        _poly(d, [Q(120, -420), Q(185, -470), Q(200, -440), Q(135, -392)], collar, W_(4))
        oval(175, -405, 18, 18, (250, 210, 60), 3)
    # bracitos
    for k, dv in enumerate((0, 25)):
        ax0, ay0 = 150, -330 + dv
        wave = math.sin(t * 6 + k) * 8
        d.line([Q(ax0, ay0), Q(ax0 + 45, ay0 + 10 + wave), Q(ax0 + 62, ay0 - 8 + wave)], fill=BLK, width=W_(20), joint="curve")
        d.line([Q(ax0, ay0), Q(ax0 + 45, ay0 + 10 + wave), Q(ax0 + 62, ay0 - 8 + wave)], fill=DK if k else col, width=W_(12), joint="curve")
    # cabeza: mandíbula de abajo (gira con mouth) y cráneo
    m = mouth * 70
    jaw = [Q(150, -440), Q(355, -440 + m * .8), Q(350, -405 + m), Q(170, -385)]
    _poly(d, jaw, col, W_(5))
    if mouth > .05:
        _poly(d, [Q(165, -440), Q(345, -440), Q(345, -440 + m * .75), Q(175, -425)], (170, 50, 60), W_(3))
        for k in range(5): _poly(d, [Q(190 + k * 32, -440 + m * .1 * k / 4 + m * .55 * k / 4), Q(203 + k * 32, -455 + m * .65 * k / 4), Q(216 + k * 32, -440 + m * .6 * k / 4)], WHITE, W_(2))
    skull = [Q(140, -520), Q(250, -545), Q(360, -500), Q(372, -455), Q(350, -440), Q(150, -440), Q(130, -470)]
    _poly(d, skull, col, W_(5))
    for k in range(6): _poly(d, [Q(180 + k * 30, -442), Q(193 + k * 30, -418), Q(206 + k * 30, -442)], WHITE, W_(2))
    oval(335, -495, 9, 6, BLK, 1)
    ex, ey = Q(230, -495)
    r = 24 * s
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=WHITE, outline=BLK, width=W_(4))
    pr = 11 * s
    d.ellipse([ex + f * 6 * s - pr, ey - pr, ex + f * 6 * s + pr, ey + pr], fill=BLK)
    if mood == "angry": d.line([Q(195, -540), Q(265, -515)], fill=BLK, width=W_(12))
    elif mood == "sad":
        d.line([Q(200, -515), Q(260, -535)], fill=BLK, width=W_(10))
        tl = (t * 70) % 60
        d.line([Q(232, -470), Q(236, -450 + tl)], fill=(110, 180, 255), width=W_(12))
    elif mood == "tired":
        d.line([Q(205, -510), Q(258, -510)], fill=BLK, width=W_(9))
        for k in range(2): oval(150 + k * 30, -540 + ((t * 80 + k * 30) % 50), 9, 14, (120, 190, 255), 2)
    else: d.line([Q(200, -530), Q(262, -528)], fill=BLK, width=W_(9))
    if napkin:
        _poly(d, [Q(150, -390), Q(260, -400), Q(200, -300)], WHITE, W_(4))
        d.line([Q(170, -385), Q(240, -392)], fill=(200, 60, 60), width=W_(5))

def raptor(d, x, y, s=1.0, t=0.0, feathers=True, mood="sly", run=False, napkin=False, flip=False):
    """Velocirraptor; y = piso, mira a la derecha. feathers=True: el real (plumas cafés y de colores, tamaño de pavo, ~300s de largo);
    feathers=False: el de película (verde, escamas, sin plumas). mood: sly | angry | scared."""
    f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    P = lambda u, v: (x + f * u * s, y + v * s)
    col = (170, 120, 70) if feathers else (110, 140, 80)
    DK = dk(col, .7)
    sw = math.sin(t * 12) * .6 if run else 0
    for leg, ph in enumerate((math.pi, 0)):
        a = math.sin(t * 12 + ph) * .6 if run else (.1 if leg else -.15)
        kx, ky = 10 + 40 * math.sin(a), -70
        fx = -10 + 80 * math.sin(a)
        c = DK if leg == 0 else col
        d.line([P(0, -120), P(kx + 20, ky), P(fx, -8)], fill=BLK, width=W_(20), joint="curve"); d.line([P(0, -120), P(kx + 20, ky), P(fx, -8)], fill=c, width=W_(12), joint="curve")
        _poly(d, [P(fx - 15, -14), P(fx + 35, -12), P(fx + 38, 0), P(fx - 15, 0)], c, W_(3))
        d.line([P(fx + 2, -14), P(fx + 12, -34)], fill=(240, 235, 220), width=W_(6))   # garra famosa
    tail = [P(-40, -150), P(-230, -170), P(-235, -150), P(-40, -110)]
    _poly(d, tail, col, W_(4))
    if feathers:
        for k in range(4): _poly(d, [P(-120 - k * 35, -165), P(-150 - k * 35, -195 + k * 4), P(-160 - k * 35, -155)], (200, 90, 60) if k % 2 else (90, 120, 160), W_(2))
    _poly(d, [P(-60, -165), P(60, -175), P(90, -130), P(40, -95), P(-50, -105)], col, W_(4))
    if feathers:
        for k in range(4): d.arc([P(-40 + k * 30, -170)[0] - 18 * s, P(0, -170)[1] - 12 * s, P(-40 + k * 30, -170)[0] + 18 * s, P(0, -170)[1] + 12 * s], 0, 180, fill=DK, width=W_(4))
        _poly(d, [P(40, -140), P(110, -125), P(70, -95), P(30, -105)], (200, 90, 60), W_(3))        # ala con plumas
        for k in range(3): d.line([P(70 + k * 12, -110), P(80 + k * 12, -88)], fill=(90, 120, 160), width=W_(5))
    else:
        for k in range(5): d.ellipse([P(-30 + k * 22, -150)[0] - 5 * s, P(0, -150)[1] - 5 * s, P(-30 + k * 22, -150)[0] + 5 * s, P(0, -150)[1] + 5 * s], fill=DK)
        d.line([P(50, -140), P(95, -115), P(105, -128)], fill=BLK, width=W_(14)); d.line([P(50, -140), P(95, -115), P(105, -128)], fill=col, width=W_(8))
    _poly(d, [P(50, -170), P(90, -230), P(120, -215), P(85, -150)], col, W_(4))
    head = [P(80, -230), P(130, -255), P(195, -235), P(200, -215), P(120, -205)]
    _poly(d, head, col, W_(4))
    if feathers:
        for k in range(3): _poly(d, [P(85 + k * 12, -245), P(70 + k * 12, -285 + k * 6), P(100 + k * 12, -250)], (200, 90, 60) if k % 2 else (90, 120, 160), W_(2))
    d.line([P(135, -218), P(195, -220)], fill=BLK, width=W_(4))
    for k in range(3): _poly(d, [P(150 + k * 14, -219), P(156 + k * 14, -210), P(162 + k * 14, -219)], WHITE, W_(1))
    ex, ey = P(130, -237); r = 11 * s
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(250, 210, 60) if mood != "scared" else WHITE, outline=BLK, width=W_(3))
    d.ellipse([ex + f * 2 * s - 5 * s, ey - 5 * s, ex + f * 2 * s + 5 * s, ey + 5 * s], fill=BLK)
    if mood in ("sly", "angry"): d.line([P(112, -255 if mood == "angry" else -250), P(150, -245 if mood == "angry" else -250)], fill=BLK, width=W_(6))
    if napkin: _poly(d, [P(85, -200), P(140, -200), P(110, -150)], WHITE, W_(3))

def pigeon(d, x, y, s=1.0, t=0.0, flip=False, mood="normal", fly=False, look=False):
    """Paloma de ciudad; y = piso (o centro del cuerpo si fly=True). Mira a la derecha. mood: normal | sly.
    look=True: voltea la cabeza hacia la cámara (los dos ojos). Mide ~170s de largo."""
    f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    P = lambda u, v: (x + f * u * s, y + v * s)
    G, DK, NK = (150, 155, 170), (100, 105, 120), (110, 170, 140)
    by = -70 if not fly else 0
    if not fly:
        for dx in (-10, 15):
            d.line([P(dx, by + 40), P(dx + 5, 0)], fill=(230, 110, 110), width=W_(7))
            for c in (-1, 1): d.line([P(dx + 5, 0), P(dx + 5 + c * 12, 0)], fill=(230, 110, 110), width=W_(5))
    _poly(d, [P(-60, by - 10), P(-110, by + 5), P(-105, by + 25), P(-55, by + 18)], DK, W_(3))
    q = [P(-70 + 140 * (.5 + .5 * math.cos(a / 16 * math.pi)), by + 10 + 38 * math.sin(a / 16 * math.pi)) for a in range(32)]
    _poly(d, q, G, W_(4))
    if fly:
        fl = math.sin(t * 14) * 45
        _poly(d, [P(-30, by - 10), P(10, by - 90 - fl), P(50, by - 70 - fl), P(30, by - 10)], DK, W_(3))
    else:
        _poly(d, [P(-50, by), P(30, by - 5), P(10, by + 25), P(-45, by + 25)], DK, W_(3))
        for k in range(2): d.line([P(-30 + k * 25, by + 5), P(-30 + k * 25, by + 20)], fill=(60, 60, 70), width=W_(4))
    hx, hy = 70, by - 30
    d.ellipse([P(hx - 35, hy - 30)[0] if f > 0 else P(hx + 35, 0)[0], y + (hy - 30) * s, P(hx + 35, 0)[0] if f > 0 else P(hx - 35, 0)[0], y + (hy + 30) * s], fill=G, outline=BLK, width=W_(4))
    _poly(d, [P(hx - 20, hy + 15), P(hx + 25, hy + 18), P(hx + 10, hy + 45), P(hx - 25, hy + 40)], NK, W_(2))
    if look:
        for sx in (-1, 1):
            ex, ey = P(hx + sx * 13, hy - 6)
            d.ellipse([ex - 9 * s, ey - 9 * s, ex + 9 * s, ey + 9 * s], fill=(240, 130, 40), outline=BLK, width=W_(2)); d.ellipse([ex - 4 * s, ey - 4 * s, ex + 4 * s, ey + 4 * s], fill=BLK)
        _poly(d, [P(hx - 6, hy + 4), P(hx + 6, hy + 4), P(hx, hy + 18)], (240, 200, 120), W_(2))
    else:
        _poly(d, [P(hx + 30, hy - 4), P(hx + 58, hy + 4), P(hx + 30, hy + 8)], (240, 200, 120), W_(2))
        ex, ey = P(hx + 10, hy - 8)
        d.ellipse([ex - 9 * s, ey - 9 * s, ex + 9 * s, ey + 9 * s], fill=(240, 130, 40), outline=BLK, width=W_(2)); d.ellipse([ex - 4 * s, ey - 4 * s, ex + 4 * s, ey + 4 * s], fill=BLK)
        if mood == "sly": d.line([P(hx - 6, hy - 22), P(hx + 24, hy - 14)], fill=BLK, width=W_(5))

def shrew(d, x, y, s=1.0, t=0.0, mood="scared", flip=False):
    """Mamífero chiquito de la época de los dinosaurios (tipo musaraña): café, hocico largo y bigotes. y = piso. ~150s de largo."""
    f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    P = lambda u, v: (x + f * u * s, y + v * s)
    C = (150, 110, 80)
    sh = math.sin(t * 50) * 2 if mood == "scared" else 0
    d.line([P(-60, -20), P(-110, -10), P(-130, -25)], fill=(230, 170, 170), width=W_(6))
    q = [P(-70 + 140 * (.5 + .5 * math.cos(a / 16 * math.pi)) + sh, -38 + 34 * math.sin(a / 16 * math.pi)) for a in range(32)]
    _poly(d, q, C, W_(4))
    _poly(d, [P(50 + sh, -55), P(110 + sh, -30), P(55 + sh, -15)], C, W_(4))
    d.ellipse([P(108, -36)[0] - 6 * s + sh, y - 36 * s, P(108, -36)[0] + 6 * s + sh, y - 24 * s], fill=(230, 120, 140))
    d.ellipse([P(30, -78)[0] - 14 * s + sh, y - 80 * s, P(30, -78)[0] + 14 * s + sh, y - 54 * s], fill=(200, 150, 120), outline=BLK, width=W_(3))
    ex, ey = P(68, -45)
    d.ellipse([ex - 9 * s + sh, ey - 9 * s, ex + 9 * s + sh, ey + 9 * s], fill=WHITE, outline=BLK, width=W_(2)); d.ellipse([ex - 4 * s + sh, ey - 4 * s, ex + 4 * s + sh, ey + 4 * s], fill=BLK)
    for k in (-1, 1): d.line([P(95, -32), P(130, -32 + k * 12)], fill=BLK, width=W_(2))
    for dx in (-35, 30): d.line([P(dx, -8), P(dx, 0)], fill=(230, 170, 170), width=W_(8))

def elephant(d, x, y, s=1.0, t=0.0, sit=False, flip=False):
    """Elefante gris de caricatura; y = piso, mira a la derecha. sit=True: sentado de nalgas con las patas de atrás al frente
    (para aplastar algo). ~420s de largo parado, ~330s de alto sentado."""
    f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s))
    P = lambda u, v: (x + f * u * s, y + v * s)
    G, DK, LT = (165, 170, 185), (130, 135, 150), (190, 195, 205)
    def oval(u, v, ru, rv, c, w=5):
        q = [P(u + ru * math.cos(a / 18 * math.pi), v + rv * math.sin(a / 18 * math.pi)) for a in range(36)]
        _poly(d, q, c, W_(w))
    if sit:
        oval(-40, -170, 140, 165, G)
        oval(-10, -150, 80, 110, LT, 3)
        oval(-30, -60, 100, 60, G)                                               # muslo
        for dx in (95, 145): _poly(d, [P(dx - 28, -230), P(dx + 28, -230), P(dx + 30, 0), P(dx - 30, 0)], G if dx == 115 else DK, W_(4))
        oval(40, -42, 40, 44, G, 4); oval(48, -42, 27, 31, (230, 225, 210), 3)   # planta de la pata de atrás
        for k in range(3): oval(72, -68 + k * 26, 7, 9, (250, 248, 235), 2)
        hx, hy = 120, -320
        tail = [P(-150, -80), P(-200, -40)]
    else:
        for dx in (-110, 90): _poly(d, [P(dx - 30, -140), P(dx + 30, -140), P(dx + 30, 0), P(dx - 30, 0)], DK, W_(4))
        oval(0, -200, 200, 120, G)
        for dx in (-70, 130): _poly(d, [P(dx - 30, -140), P(dx + 30, -140), P(dx + 30, 0), P(dx - 30, 0)], G, W_(4))
        hx, hy = 190, -250
        tail = [P(-198, -230), P(-235, -150)]
    d.line(tail, fill=BLK, width=W_(6))
    oval(hx - 35, hy + 10, 70, 100, DK)                                             # oreja
    oval(hx + 25, hy, 80, 78, G)
    sw = math.sin(t * 3) * 10
    tr = [P(hx + 85, hy - 5), P(hx + 125, hy + 60), P(hx + 135, hy + 140 + sw), P(hx + 160, hy + 125 + sw), P(hx + 170, hy + 140 + sw), P(hx + 135, hy + 165 + sw), P(hx + 100, hy + 145), P(hx + 95, hy + 70), P(hx + 60, hy + 35)]
    _poly(d, tr, G, W_(4))
    _poly(d, [P(hx + 60, hy + 45), P(hx + 92, hy + 95), P(hx + 76, hy + 52)], (250, 248, 235), W_(2))
    ex, ey = P(hx + 45, hy - 20)
    d.ellipse([ex - 10 * s, ey - 10 * s, ex + 10 * s, ey + 10 * s], fill=BLK)
    d.line([P(hx + 25, hy - 45), P(hx + 65, hy - 38)], fill=BLK, width=W_(5))
