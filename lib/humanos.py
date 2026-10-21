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
        "head": (x, y - S(520)), "head_top": (x, y - S(640)), "eyes": (x, y - S(530)), "mouth": (x, y - S(470)),
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
