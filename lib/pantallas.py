"""Pantallas propias del canal. Las comunes (documentos, chat, gráficas, people_grid, monitor, …) viven en el motor (reels_engine.pantallas)."""
from reels_engine.pantallas import *
from .core import BLK, dk

def codex(d, x0, y0, x1, y1, unroll=1.0, seed=2):
    """Códice tipo biombo (páginas dobladas con glifos de colores). unroll 0..1 = cuánto se ha abierto."""
    import random; r = random.Random(seed)
    PAPER, COLS = (240, 225, 185), ((200, 60, 50), (40, 110, 170), (230, 170, 40), (60, 140, 80), (30, 30, 30))
    xe = x0 + (x1 - x0) * max(.12, unroll); n = 5; pw = (x1 - x0) / n
    k = 0; xx = x0
    while xx < xe - 1:
        w = min(pw, xe - xx)
        d.rectangle([xx, y0, xx + w, y1], fill=PAPER if k % 2 == 0 else dk(PAPER, .93), outline=BLK, width=4)
        for g in range(3):
            gx, gy = xx + w * .2 + r.uniform(0, w * .4), y0 + 30 + g * (y1 - y0 - 60) / 3
            c = COLS[r.randrange(len(COLS))]; sz = r.uniform(.5, .8) * min(w, (y1 - y0) / 3) * .5
            if r.random() < .5: d.ellipse([gx, gy, gx + sz, gy + sz], fill=c, outline=BLK, width=3)
            else: d.rectangle([gx, gy, gx + sz, gy + sz * .8], fill=c, outline=BLK, width=3)
        xx += pw; k += 1
    d.rectangle([x0, y0, xe, y0 + 14], fill=(200, 60, 50)); d.rectangle([x0, y1 - 14, xe, y1], fill=(200, 60, 50))
