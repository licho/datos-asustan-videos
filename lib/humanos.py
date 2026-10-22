"""Personajes humanos recurrentes construidos sobre 'guy'."""
from ._lazy import SRC
from reel import guy, BLK
from .core import dk

def don_tono(d, x, y, s=1.0, mood="neutral", arms="down", t=0.0):
    """Don Toño: señor de bigote y gorra (cliente eterno del minisúper)."""
    guy(d, x, y, s, mood=mood, arms=arms, t=t, hoodie=(110, 150, 90))
    S = lambda v: v * s; hy = y - S(520)
    d.polygon([(x - S(70), hy + S(30)), (x + S(70), hy + S(30)), (x + S(55), hy + S(55)), (x, hy + S(42)), (x - S(55), hy + S(55))], fill=(90, 70, 60), outline=BLK)
    d.chord([x - S(95), hy - S(115), x + S(95), hy + S(20)], 180, 360, fill=(200, 60, 50), outline=BLK, width=4)
    d.rectangle([x - S(10), hy - S(60), x + S(150), hy - S(40)], fill=(170, 50, 40), outline=BLK, width=3)

def anchors(x, y, s=1.0):
    """Puntos del cuerpo de 'guy' (y de don_tono) para poner objetos encima sin que floten.
    Uso: a = anchors(540, 1290, .7); medal(d, *a['chest'], ...)"""
    S = lambda v: v * s
    return {
        "head": (x, y - S(520)), "head_r": S(125), "box": (x - S(150), y - S(660), x + S(150), y), "head_top": (x, y - S(640)), "eyes": (x, y - S(530)), "mouth": (x, y - S(470)),
        "neck": (x, y - S(415)), "chest": (x - S(30), y - S(320)), "belly": (x, y - S(230)), "feet": (x, y),
        "hand_r_down": (x + S(135), y - S(205)), "hand_l_down": (x - S(135), y - S(205)),
        "hand_r_up": (x + S(185), y - S(560)), "hand_l_up": (x - S(185), y - S(560)),
        "hand_r_push": (x + S(200), y - S(285)), "hand_l_push": (x + S(150), y - S(300)),
    }

def medal(d, x, y, s=1.0, text="1º", ribbon=(40, 120, 220), neck=None):
    """Medalla colgada; (x, y) = centro de la medalla. neck=(x, y) dibuja el listón desde el cuello."""
    from .core import F, YEL, BLK
    S = lambda v: v * s
    if neck:
        d.line([(neck[0] - S(30), neck[1]), (x, y - S(30))], fill=ribbon, width=int(S(16))); d.line([(neck[0] + S(30), neck[1]), (x, y - S(30))], fill=ribbon, width=int(S(16)))
    d.ellipse([x - S(40), y - S(40), x + S(40), y + S(40)], fill=YEL, outline=BLK, width=4)
    d.text((x, y), text, font=F(S(34)), fill=BLK, anchor="mm")

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
