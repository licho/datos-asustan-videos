"""Criaturas nuevas (cartoon). Se dibujan sobre img (no sobre d) cuando necesitan transparencia."""
import math
from PIL import Image, ImageDraw, ImageFilter
from .core import BLK, WHITE, RED, dk

def ghost_draw(d, x, y, s=1.0, t=0.0, mood="happy", tie=None, headset=False, col=(245, 248, 255), arms="down"):
    """Fantasma de sábana. (x, y) = centro del cuerpo. Alto ~420·s. mood: happy | scared | sad | smug."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    top, bot, hw = y - S(210), y + S(170), S(140)
    pts = []
    for k in range(41):                                   # cúpula
        a = math.pi + k / 40 * math.pi
        pts.append((x + math.cos(a) * hw, top + S(140) + math.sin(a) * S(140)))
    n = 8
    for k in range(n + 1):                                # orilla ondulada (de derecha a izquierda)
        u = 1 - k / n; px = x - hw + u * 2 * hw
        py = bot + (S(28) if k % 2 == 0 else -S(8)) + math.sin(t * 5 + k) * S(10)
        pts.append((px + S(18) * math.sin(t * 2), py))
    d.polygon(pts, fill=col, outline=BLK, width=W_(5))
    for side in (-1, 1):                                  # bracitos
        if arms == "up" and side > 0:
            d.ellipse([x + side * hw - S(30), y - S(120), x + side * hw + S(30), y - S(60)], fill=col, outline=BLK, width=W_(4))
        elif arms == "wave" and side > 0:
            wy = y - S(90) + math.sin(t * 10) * S(25)
            d.ellipse([x + hw - S(10), wy - S(30), x + hw + S(50), wy + S(30)], fill=col, outline=BLK, width=W_(4))
        else:
            d.ellipse([x + side * hw - S(30), y - S(10), x + side * hw + S(30), y + S(50)], fill=col, outline=BLK, width=W_(4))
    ey = y - S(90)
    for side in (-1, 1):
        ex = x + side * S(48)
        if mood == "scared":
            d.ellipse([ex - S(26), ey - S(34), ex + S(26), ey + S(34)], fill=WHITE, outline=BLK, width=W_(4)); d.ellipse([ex - S(9), ey - S(9), ex + S(9), ey + S(9)], fill=BLK)
        elif mood == "smug":
            d.chord([ex - S(24), ey - S(30), ex + S(24), ey + S(30)], 0, 180, fill=BLK)
        else:
            d.ellipse([ex - S(20), ey - S(30), ex + S(20), ey + S(30)], fill=(40, 40, 60))
            d.ellipse([ex - S(9) + S(6), ey - S(20), ex + S(3) + S(6), ey - S(6)], fill=WHITE)
    my = y - S(10)
    if mood == "scared": d.ellipse([x - S(24), my - S(20), x + S(24), my + S(40)], fill=(40, 40, 60))
    elif mood == "sad": d.arc([x - S(40), my, x + S(40), my + S(50)], 200, 340, fill=BLK, width=W_(6))
    else: d.arc([x - S(45), my - S(40), x + S(45), my + S(20)], 20, 160, fill=BLK, width=W_(6))
    if tie:
        d.polygon([(x - S(18), y + S(20)), (x + S(18), y + S(20)), (x, y + S(45))], fill=tie, outline=BLK)
        d.polygon([(x - S(12), y + S(42)), (x + S(12), y + S(42)), (x + S(20), y + S(140)), (x, y + S(165)), (x - S(20), y + S(140))], fill=tie, outline=BLK)
    if headset:
        d.arc([x - hw * .9, top + S(10), x + hw * .9, y + S(20)], 200, 340, fill=(50, 50, 55), width=W_(12))
        d.ellipse([x - hw * .9 - S(22), y - S(110), x - hw * .9 + S(22), y - S(50)], fill=(50, 50, 55))
        d.line([(x - hw * .85, y - S(60)), (x - S(40), y + S(5))], fill=(50, 50, 55), width=W_(6))

def ghost(img, x, y, s=1.0, t=0.0, alpha=1.0, pixel=0, bob=True, **kw):
    """Pega un fantasma con transparencia (alpha 0..1) y opcionalmente pixelado (pixel = tamaño de bloque)."""
    if alpha <= 0.01: return ImageDraw.Draw(img)
    if bob: y += math.sin(t * 2.2) * 18 * s
    size = int(560 * s) + 40
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ghost_draw(ImageDraw.Draw(layer), size / 2, size / 2, s, t, **kw)
    if pixel > 1:
        small = layer.resize((max(1, size // pixel), max(1, size // pixel)), Image.NEAREST); layer = small.resize((size, size), Image.NEAREST)
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha)); layer.putalpha(a)
    img.paste(layer, (int(x - size / 2), int(y - size / 2)), layer)
    return ImageDraw.Draw(img)
