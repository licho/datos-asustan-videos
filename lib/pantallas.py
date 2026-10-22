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

def captcha(d, x, y, w, t=0.0, picked=(), grid=True, checked=False, size=34):
    """Prueba genérica de 'No soy un robot' (sin logos). (x, y) = esquina sup. izq. picked = casillas (0..8) marcadas."""
    from .core import F, WHITE
    h0 = 110
    d.rounded_rectangle([x, y, x + w, y + h0], 14, fill=(248, 248, 250), outline=BLK, width=4)
    d.rectangle([x + 28, y + 30, x + 78, y + 80], fill=WHITE, outline=(90, 90, 100), width=4)
    if checked: d.line([(x + 36, y + 55), (x + 50, y + 70), (x + 72, y + 38)], fill=(40, 160, 80), width=8)
    d.text((x + 100, y + h0 / 2), "No soy un robot", font=F(size), fill=BLK, anchor="lm")
    if not grid: return y + h0
    gy = y + h0 + 20; cw = (w - 40) / 3
    d.rounded_rectangle([x, gy, x + w, gy + 3 * cw + 110], 14, fill=WHITE, outline=BLK, width=4)
    d.rectangle([x + 12, gy + 12, x + w - 12, gy + 80], fill=(60, 120, 220))
    d.text((x + 30, gy + 46), "Elige todos los SEMÁFOROS", font=F(int(size * .8)), fill=WHITE, anchor="lm")
    for k in range(9):
        cx0 = x + 20 + (k % 3) * cw; cy0 = gy + 95 + (k // 3) * cw
        d.rectangle([cx0, cy0, cx0 + cw - 8, cy0 + cw - 8], fill=(170, 200, 220) if k % 2 else (150, 175, 150), outline=WHITE, width=3)
        if k in (1, 3, 5, 7):
            px = cx0 + cw / 2 - 4
            d.rounded_rectangle([px - 16, cy0 + 18, px + 16, cy0 + cw - 34], 6, fill=(40, 40, 45))
            for j, c in enumerate(((230, 60, 50), (240, 200, 40), (60, 190, 90))):
                yy = cy0 + 30 + j * (cw - 70) / 3; d.ellipse([px - 10, yy, px + 10, yy + 20], fill=c)
        if k in picked:
            d.rectangle([cx0, cy0, cx0 + cw - 8, cy0 + cw - 8], outline=(60, 120, 220), width=8)
            d.ellipse([cx0 + 6, cy0 + 6, cx0 + 40, cy0 + 40], fill=(60, 120, 220)); d.line([(cx0 + 14, cy0 + 24), (cx0 + 22, cy0 + 32), (cx0 + 33, cy0 + 15)], fill=WHITE, width=5)
    return gy + 3 * cw + 110
