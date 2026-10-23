"""Efectos y gráficos sobrepuestos reutilizables del canal: sellos, etiquetas giradas, nieve, ondas de sonido."""
import math, random
from reels_engine.motion import layer
from .core import F, W, BLK, WHITE, RED

def tag(img, text, x, y, k, rot=-10, bg=RED, size=56):
    """Etiqueta redondeada y girada que entra con escala k (0..1); úsala con k = tw(lt, t0, .4, 0, 1, back_out).
    Devuelve el nuevo ImageDraw (la pega en una capa)."""
    def fn(dd, cx, cy):
        f = F(size); w = dd.textlength(text, font=f) + 70
        dd.rounded_rectangle([cx - w / 2, cy - size * .8, cx + w / 2, cy + size * .8], 30, fill=bg, outline=BLK, width=6)
        dd.text((cx, cy), text, font=f, fill=WHITE, anchor="mm")
    return layer(img, fn, x, y, 1000, sx=k, sy=k, rot=rot)

def rubber_stamp(img, text, x, y, k, col=RED, size=78, rot=-10):
    """Sello de goma (solo contorno y letras) girado; k = escala de entrada."""
    def fn(dd, cx, cy):
        f = F(size); w = dd.textlength(text, font=f) + 60
        dd.rounded_rectangle([cx - w / 2, cy - size * .85, cx + w / 2, cy + size * .85], 18, outline=col, width=12)
        dd.text((cx, cy), text, font=f, fill=col, anchor="mm")
    return layer(img, fn, x, y, 1000, sx=k, sy=k, rot=rot)

def snow_fall(d, t, n=18, seed=5, box=(0, 480, W, 1300), size=(12, 22), speed=(60, 130), col=WHITE, wobble=25):
    """Copos de nieve cayendo dentro de box=(x0, y0, x1, y1). Determinista (depende de t y seed)."""
    from .objetos import snowflake
    r = random.Random(seed); span = box[3] - box[1]
    for k in range(n):
        x0, sp, sz = r.uniform(box[0], box[2]), r.uniform(*speed), r.uniform(*size)
        y = box[1] + (t * sp + r.uniform(0, span)) % span; x = x0 + math.sin(t * 2 + k) * wobble
        snowflake(d, x, y, sz, col=col, width=4)

def sound_waves(d, x, y, t, n=3, col=(200, 220, 255), width=7):
    """Ondas de sonido saliendo a los lados de (x, y) (llanto, grito, alarma)."""
    for k in range(n):
        r = 60 + ((t * 140 + k * 60) % 180)
        for sx in (-1, 1):
            a0, a1 = (300, 60) if sx > 0 else (120, 240)
            d.arc([x - r, y - r, x + r, y + r], a0, a1, fill=col, width=width)
