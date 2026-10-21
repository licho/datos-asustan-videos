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
