"""Personajes humanos recurrentes construidos sobre 'guy'."""
import math
from reels_engine.humanos import guy, anchors, medal
from .core import dk, BLK

def don_tono(d, x, y, s=1.0, mood="neutral", arms="down", t=0.0):
    """Don Toño: señor de bigote y gorra (cliente eterno del minisúper)."""
    guy(d, x, y, s, mood=mood, arms=arms, t=t, hoodie=(110, 150, 90))
    S = lambda v: v * s; hy = y - S(520)
    d.polygon([(x - S(70), hy + S(30)), (x + S(70), hy + S(30)), (x + S(55), hy + S(55)), (x, hy + S(42)), (x - S(55), hy + S(55))], fill=(90, 70, 60), outline=BLK)
    d.chord([x - S(95), hy - S(115), x + S(95), hy + S(20)], 180, 360, fill=(200, 60, 50), outline=BLK, width=4)
    d.rectangle([x - S(10), hy - S(60), x + S(150), hy - S(40)], fill=(170, 50, 40), outline=BLK, width=3)

def cleopatra(d, x, y, s=1.0, t=0.0, mood="neutral", arms="down"):
    """Cleopatra (caricatura): fleco negro, diadema dorada, collar ancho y vestido blanco. y = pies. mood: neutral | bored | happy."""
    from .core import WHITE, F
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); SK, GOLD, HAIR = (205, 160, 120), (235, 190, 60), (25, 20, 25)
    d.ellipse([x - S(120), y - S(14), x + S(120), y + S(14)], fill=(70, 70, 75))
    d.polygon([(x - S(95), y - S(400)), (x + S(95), y - S(400)), (x + S(140), y), (x - S(140), y)], fill=WHITE, outline=BLK)
    d.rectangle([x - S(100), y - S(270), x + S(100), y - S(245)], fill=GOLD, outline=BLK, width=3)
    def arm(hx, hy, sx):
        d.line([(x + sx * S(95), y - S(380)), (hx, hy)], fill=SK, width=W_(36)); d.ellipse([hx - S(20), hy - S(20), hx + S(20), hy + S(20)], fill=SK)
        d.rectangle([hx - S(22), hy - S(60), hx + S(22), hy - S(40)], fill=GOLD)
    if arms == "up": arm(x - S(180), y - S(560), -1); arm(x + S(180), y - S(560), 1)
    elif arms == "point": arm(x - S(130), y - S(200), -1); arm(x + S(230), y - S(400), 1)
    else: arm(x - S(130), y - S(200), -1); arm(x + S(130), y - S(200), 1)
    d.chord([x - S(120), y - S(470), x + S(120), y - S(330)], 0, 180, fill=GOLD, outline=BLK, width=W_(4))
    for k in range(3): d.arc([x - S(100) + k * S(15), y - S(450) + k * S(15), x + S(100) - k * S(15), y - S(350) - k * S(15)], 10, 170, fill=(40, 120, 200) if k % 2 else (200, 60, 50), width=W_(6))
    hy = y - S(540)
    d.rectangle([x - S(105), hy - S(70), x + S(105), hy + S(120)], fill=HAIR)
    d.ellipse([x - S(80), hy - S(85), x + S(80), hy + S(85)], fill=SK, outline=BLK, width=W_(4))
    d.chord([x - S(108), hy - S(120), x + S(108), hy + S(10)], 180, 360, fill=HAIR); d.rectangle([x - S(85), hy - S(55), x + S(85), hy - S(20)], fill=HAIR)
    d.rectangle([x - S(100), hy - S(65), x + S(100), hy - S(48)], fill=GOLD, outline=BLK, width=3)
    d.polygon([(x - S(12), hy - S(65)), (x, hy - S(105)), (x + S(12), hy - S(65))], fill=GOLD, outline=BLK)
    for sx in (-1, 1):
        ex = x + sx * S(32); ey = hy + S(5)
        if mood == "bored": d.chord([ex - S(18), ey - S(12), ex + S(18), ey + S(14)], 0, 180, fill=BLK)
        else: d.ellipse([ex - S(16), ey - S(14), ex + S(16), ey + S(14)], fill=WHITE, outline=BLK, width=3); d.ellipse([ex - S(7), ey - S(7), ex + S(7), ey + S(7)], fill=BLK)
        d.line([(ex + sx * S(16), ey - S(2)), (ex + sx * S(34), ey - S(12))], fill=BLK, width=W_(5))
    if mood == "happy": d.arc([x - S(28), hy + S(25), x + S(28), hy + S(60)], 20, 160, fill=(150, 30, 40), width=W_(6))
    else: d.line([(x - S(22), hy + S(45)), (x + S(22), hy + S(45))], fill=(150, 30, 40), width=W_(6))

def _hat_base(x, y, s):
    S = lambda v: v * s; return S, x, y - S(505)

def soldier(d, x, y, s=1.0, t=0.0, mood="neutral", arms="down", era="modern", binoculars=False, col=None):
    """Soldadito de caricatura SIN armas (sirve para desfiles, filas, ejércitos). y = pies.
    era: modern (casco verde) | persian (gorro alto) | napoleon (chacó azul) | ancient (casco griego). binoculars=True: binoculares en los ojos."""
    from .core import F, WHITE
    cols = {"modern": (95, 115, 70), "persian": (150, 60, 110), "napoleon": (45, 65, 140), "ancient": (170, 60, 50)}
    guy(d, x, y, s, mood=mood, arms=arms, t=t, hoodie=col or cols.get(era, (95, 115, 70)))
    S, hx, hy = _hat_base(x, y, s); W_ = lambda v: max(2, int(v * s))
    if era == "modern":
        hc = (80, 100, 60)
        d.chord([hx - S(118), hy - S(125), hx + S(118), hy + S(40)], 180, 360, fill=hc, outline=BLK, width=W_(5))
        d.rounded_rectangle([hx - S(132), hy - S(48), hx + S(132), hy - S(30)], int(S(8)), fill=dk(hc, .8), outline=BLK, width=W_(4))
    elif era == "persian":
        hc = (230, 200, 120)
        d.polygon([(hx - S(100), hy - S(40)), (hx - S(70), hy - S(190)), (hx + S(10), hy - S(215)), (hx + S(100), hy - S(40))], fill=hc, outline=BLK)
        d.rectangle([hx - S(104), hy - S(58), hx + S(104), hy - S(36)], fill=(150, 60, 110), outline=BLK, width=W_(3))
    elif era == "napoleon":
        hc = (30, 30, 40)
        d.rectangle([hx - S(80), hy - S(210), hx + S(80), hy - S(50)], fill=hc, outline=BLK, width=W_(4))
        d.rectangle([hx - S(84), hy - S(80), hx + S(84), hy - S(50)], fill=(200, 40, 40), outline=BLK, width=W_(3))
        d.ellipse([hx - S(18), hy - S(200), hx + S(18), hy - S(164)], fill=WHITE, outline=BLK, width=W_(3))
        d.rectangle([hx - S(110), hy - S(56), hx + S(110), hy - S(42)], fill=hc)
    elif era == "ancient":
        hc = (210, 170, 70)
        d.chord([hx - S(112), hy - S(120), hx + S(112), hy + S(50)], 180, 360, fill=hc, outline=BLK, width=W_(5))
        d.polygon([(hx - S(20), hy - S(118)), (hx - S(60), hy - S(200)), (hx + S(70), hy - S(210)), (hx + S(20), hy - S(118))], fill=(200, 40, 40), outline=BLK)
    if binoculars:
        for sx in (-1, 1):
            d.ellipse([hx + sx * S(40) - S(32), hy - S(25), hx + sx * S(40) + S(32), hy + S(39)], fill=(40, 40, 45), outline=BLK, width=W_(4))
            d.ellipse([hx + sx * S(40) - S(18), hy - S(11), hx + sx * S(40) + S(18), hy + S(25)], fill=(120, 170, 220))
        d.rectangle([hx - S(10), hy - S(5), hx + S(10), hy + S(15)], fill=(40, 40, 45))

def napoleon(d, x, y, s=1.0, t=0.0, mood="neutral", arms="down", sweat=False):
    """Napoleón de caricatura (sin armas): saco azul con solapas rojas y sombrero bicornio. y = pies. sweat=True: gotas de sudor."""
    from .core import WHITE, YEL
    guy(d, x, y, s, mood=mood, arms=arms, t=t, hoodie=(40, 55, 120))
    S, hx, hy = _hat_base(x, y, s); W_ = lambda v: max(2, int(v * s))
    by = y - S(400)
    d.polygon([(x - S(45), by), (x, by + S(110)), (x + S(45), by)], fill=WHITE, outline=BLK)
    for sx in (-1, 1):
        d.polygon([(x + sx * S(45), by), (x + sx * S(85), by + S(10)), (x + sx * S(20), by + S(150))], fill=(200, 40, 40), outline=BLK)
        d.ellipse([x + sx * S(95) - S(28), by - S(8), x + sx * S(95) + S(28), by + S(16)], fill=YEL, outline=BLK, width=W_(3))
    d.chord([hx - S(175), hy - S(165), hx + S(175), hy + S(5)], 180, 360, fill=(25, 25, 30), outline=BLK, width=W_(5))
    d.rectangle([hx - S(175), hy - S(85), hx + S(175), hy - S(68)], fill=(25, 25, 30))
    d.ellipse([hx - S(26), hy - S(150), hx + S(26), hy - S(98)], fill=(40, 70, 170), outline=WHITE, width=W_(6))
    d.ellipse([hx - S(10), hy - S(134), hx + S(10), hy - S(114)], fill=(200, 40, 40))
    if sweat:
        for k, (dx, dy) in enumerate(((-120, -20), (115, 10), (-95, 60))):
            yy = hy + S(dy) + S((t * 90 + k * 25) % 50)
            d.polygon([(hx + S(dx), yy - S(24)), (hx + S(dx) - S(12), yy), (hx + S(dx) + S(12), yy)], fill=(120, 190, 255))
            d.ellipse([hx + S(dx) - S(12), yy - S(10), hx + S(dx) + S(12), yy + S(14)], fill=(120, 190, 255))

def scribe(d, x, y, s=1.0, t=0.0, mood="neutral", arms="down"):
    """Escriba/historiador griego: toga blanca con banda y corona de laurel. y = pies."""
    from .core import WHITE
    guy(d, x, y, s, mood=mood, arms=arms, t=t, hoodie=(240, 238, 228))
    S, hx, hy = _hat_base(x, y, s); W_ = lambda v: max(2, int(v * s))
    d.line([(x - S(95), y - S(400)), (x + S(80), y - S(200))], fill=(60, 110, 190), width=W_(30))
    for sx in (-1, 1):
        for k in range(5):
            a = math.radians(200 + k * 18) if sx < 0 else math.radians(340 - k * 18)
            lx, ly = hx + math.cos(a) * S(108), hy - S(20) + math.sin(a) * S(100)
            d.ellipse([lx - S(20), ly - S(11), lx + S(20), ly + S(11)], fill=(90, 160, 70), outline=BLK, width=W_(2))

def robo_cw(d, x, y, s=1.0, t=0.0, mood="smile", arms="down", shades=False, oil=False):
    """Compañero sospechoso de ser robot: peinado de raya perfecta, camisa, corbata y sonrisa cuadrada que no parpadea. y = pies.
    mood: smile (sonrisa de dientes) | blank | wink. shades: lentes oscuros genéricos. oil: gotas de aceite (nervios)."""
    from .core import WHITE
    guy(d, x, y, s, mood="neutral", arms=arms, t=0.0, hoodie=(120, 135, 160))
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); hx, hy = x, y - S(505)
    by = y - S(400)
    d.polygon([(x - S(45), by), (x, by + S(55)), (x + S(45), by)], fill=WHITE, outline=BLK)
    d.polygon([(x - S(14), by + S(8)), (x + S(14), by + S(8)), (x + S(20), by + S(150)), (x, by + S(175)), (x - S(20), by + S(150))], fill=(200, 50, 60), outline=BLK)
    d.chord([hx - S(106), hy - S(114), hx + S(106), hy + S(72)], 180, 360, fill=(40, 40, 48))
    d.polygon([(hx - S(106), hy - S(25)), (hx - S(106), hy - S(70)), (hx - S(30), hy - S(110)), (hx - S(40), hy - S(55))], fill=(40, 40, 48))
    d.line([(hx - S(30), hy - S(108)), (hx - S(42), hy - S(55))], fill=(200, 200, 210), width=W_(4))
    SK = (241, 194, 150)
    d.rectangle([hx - S(70), hy - S(20), hx + S(70), hy + S(95)], fill=SK)
    if shades:
        for sx in (-1, 1): d.rounded_rectangle([hx + sx * S(40) - S(36), hy - S(14), hx + sx * S(40) + S(36), hy + S(28)], int(S(8)), fill=(25, 25, 30), outline=BLK, width=W_(3))
        d.line([(hx - S(6), hy), (hx + S(6), hy)], fill=BLK, width=W_(5))
    else:
        for sx in (-1, 1):
            ex, ey = hx + sx * S(38), hy + S(5)
            if mood == "wink" and sx > 0: d.line([(ex - S(20), ey), (ex + S(20), ey)], fill=BLK, width=W_(7)); continue
            d.ellipse([ex - S(26), ey - S(26), ex + S(26), ey + S(26)], fill=WHITE, outline=BLK, width=W_(4))
            d.ellipse([ex - S(10), ey - S(10), ex + S(10), ey + S(10)], fill=BLK)
    my = hy + S(55)
    if mood in ("smile", "wink"):
        d.rectangle([hx - S(40), my - S(10), hx + S(40), my + S(16)], fill=WHITE, outline=BLK, width=W_(4))
        for k in range(1, 4): d.line([(hx - S(40) + k * S(20), my - S(10)), (hx - S(40) + k * S(20), my + S(16))], fill=BLK, width=W_(2))
    else: d.line([(hx - S(30), my), (hx + S(30), my)], fill=BLK, width=W_(6))
    if oil:
        for k, dx in enumerate((-105, 100)):
            yy = hy - S(20) + S((t * 70 + k * 30) % 60)
            d.polygon([(hx + S(dx), yy - S(22)), (hx + S(dx) - S(11), yy), (hx + S(dx) + S(11), yy)], fill=(40, 40, 45))
            d.ellipse([hx + S(dx) - S(11), yy - S(10), hx + S(dx) + S(11), yy + S(12)], fill=(40, 40, 45))

def st_nicholas(d, x, y, s=1.0, t=0.0, mood="calm", arms="down"):
    """San Nicolás (caricatura): obispo con mitra blanca y dorada, barba blanca, capa roja y báculo dorado. y = pies.
    mood: calm | stern. arms: down | stop (mano al frente para frenar)."""
    from .core import WHITE
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    RED, GOLD, SK = (190, 35, 45), (235, 190, 60), (241, 194, 150)
    d.ellipse([x - S(130), y - S(16), x + S(130), y + S(16)], fill=(60, 60, 65))
    robe = [(x - S(80), y - S(420)), (x + S(80), y - S(420)), (x + S(130), y), (x - S(130), y)]
    d.polygon(robe, fill=WHITE, outline=BLK); d.line(robe + [robe[0]], fill=BLK, width=W_(4))
    cape = [(x - S(95), y - S(420)), (x + S(95), y - S(420)), (x + S(150), y - S(20)), (x + S(70), y - S(20)), (x + S(40), y - S(380)), (x - S(40), y - S(380)), (x - S(70), y - S(20)), (x - S(150), y - S(20))]
    d.polygon(cape, fill=RED, outline=BLK); d.line(cape + [cape[0]], fill=BLK, width=W_(4))
    d.rectangle([x - S(14), y - S(380), x + S(14), y - S(20)], fill=GOLD)
    sx_ = x + S(170)
    d.line([(sx_, y), (sx_, y - S(620))], fill=BLK, width=W_(16)); d.line([(sx_, y), (sx_, y - S(620))], fill=GOLD, width=W_(10))
    d.arc([sx_ - S(70), y - S(700), sx_ + S(10), y - S(600)], 180, 360, fill=GOLD, width=W_(14)); d.arc([sx_ - S(70), y - S(700), sx_ - S(10), y - S(640)], 0, 180, fill=GOLD, width=W_(14))
    d.line([(x + S(80), y - S(380)), (sx_ - S(8), y - S(330))], fill=RED, width=W_(40)); d.ellipse([sx_ - S(22), y - S(352), sx_ + S(18), y - S(312)], fill=SK, outline=BLK, width=W_(3))
    if arms == "stop":
        d.line([(x - S(80), y - S(380)), (x - S(200), y - S(450))], fill=RED, width=W_(40)); d.ellipse([x - S(230), y - S(480), x - S(180), y - S(420)], fill=SK, outline=BLK, width=W_(3))
    else:
        d.line([(x - S(80), y - S(380)), (x - S(120), y - S(220))], fill=RED, width=W_(40)); d.ellipse([x - S(140), y - S(240), x - S(100), y - S(200)], fill=SK, outline=BLK, width=W_(3))
    hx, hy = x, y - S(500)
    d.ellipse([hx - S(70), hy - S(75), hx + S(70), hy + S(70)], fill=SK, outline=BLK, width=W_(4))
    d.polygon([(hx - S(75), hy + S(5)), (hx + S(75), hy + S(5)), (hx + S(55), hy + S(110)), (hx, hy + S(150)), (hx - S(55), hy + S(110))], fill=WHITE, outline=BLK)
    d.chord([hx - S(40), hy + S(10), hx + S(40), hy + S(40)], 0, 180, fill=WHITE, outline=BLK)
    mit = [(hx - S(70), hy - S(45)), (hx + S(70), hy - S(45)), (hx + S(55), hy - S(170)), (hx, hy - S(215)), (hx - S(55), hy - S(170))]
    d.polygon(mit, fill=WHITE, outline=BLK); d.line(mit + [mit[0]], fill=BLK, width=W_(4))
    d.rectangle([hx - S(70), hy - S(70), hx + S(70), hy - S(45)], fill=GOLD, outline=BLK, width=W_(3))
    d.rectangle([hx - S(12), hy - S(200), hx + S(12), hy - S(70)], fill=GOLD)
    d.line([(hx - S(10), hy - S(150)), (hx + S(10), hy - S(150))], fill=RED, width=W_(6)); d.line([(hx, hy - S(162)), (hx, hy - S(138))], fill=RED, width=W_(6))
    for sx in (-1, 1):
        ex, ey = hx + sx * S(26), hy - S(12)
        d.ellipse([ex - S(8), ey - S(8), ex + S(8), ey + S(8)], fill=BLK)
        d.line([(ex - S(16), ey - S(20) - (sx * S(4) if mood == "stern" else 0)), (ex + S(16), ey - S(20) + (sx * S(4) if mood == "stern" else 0))], fill=(200, 200, 200), width=W_(6))


def stamp_point(x, y, s, ang, p, cx=None, cy=None):
    """Dónde queda un punto p=(px, py) de un personaje dibujado con stamp_guy(img, x, y, s, ang) después de girarlo.
    p se da como si el personaje estuviera derecho con sus pies en (x, y + 300s) (usa anchors(x, y + 300 * s, s))."""
    import math as _m
    a = _m.radians(ang); dx, dy = p[0] - x, p[1] - y
    return (x + dx * _m.cos(a) + dy * _m.sin(a), y - dx * _m.sin(a) + dy * _m.cos(a))
