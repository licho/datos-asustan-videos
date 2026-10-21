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
