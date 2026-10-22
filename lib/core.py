import math
"""Núcleo compartido: dibujo, texto, zonas seguras y utilidades.
Importa los helpers probados de src/reel.py para no duplicar código."""
import os, sys, math, random
from functools import lru_cache
_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
if _SRC not in sys.path: sys.path.insert(0, _SRC)
from PIL import Image, ImageDraw
from reel import F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, W, H, YEL, RED, WHITE, BLK, SKIN

# ---------------- zonas seguras (1080x1920) ----------------
CHIP1, CHIP2 = 300, 420        # letreros arriba
ACTION_TOP, ACTION_BOT = 480, 1320   # zona de acción
FLOOR = 1300                   # piso por defecto (pies de personajes)
CAP_Y = 1500                   # subtítulos (no poner nada importante entre 1380 y 1640)
GREEN, BLUE, GRAY, ORANGE, PURPLE = (30, 140, 80), (40, 120, 220), (90, 90, 100), (230, 130, 30), (140, 60, 170)

@lru_cache(maxsize=64)
def _grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def grad(top, bot):
    """Fondo degradado (cacheado). Devuelve copia lista para dibujar."""
    return _grad(tuple(top), tuple(bot)).copy()

def canvas(bg):
    """bg puede ser Image (se copia) o tupla de 2 colores (degradado)."""
    img = bg.copy() if isinstance(bg, Image.Image) else grad(*bg)
    return img, ImageDraw.Draw(img)

def _bubble_layout(d, text, size, maxw):
    f = F(size); words = text.split(); lines = []; cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = test
    lines.append(cur)
    lw = max(d.textlength(l, font=f) for l in lines); lh = size * 1.2
    return f, lines, lh, lw + size * 1.2, lh * len(lines) + size * 0.8

def bubble(d, x, y, text, size=52, tail=None, maxw=760, fill=WHITE, fg=BLK, max_tail=None):
    """Globo de diálogo centrado en (x,y). tail=(x,y) = boca de quien habla.
    La punta es corta y ancha (máx. ~2.2× el tamaño de letra): si quien habla está lejos, apunta hacia él sin estirarse.
    Mejor usa say(), que acomoda el globo solo junto a quien habla."""
    f, lines, lh, bw, bh = _bubble_layout(d, text, size, maxw)
    x0, y0, x1, y1 = x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2
    r = int(size * 0.6); ow = max(4, int(size * .1))
    tri = None
    if tail:
        tx, ty = tail
        if ty > y1 or ty < y0:                                   # punta arriba o abajo
            ex = min(max(tx, x0 + r + 30), x1 - r - 30); ey = y1 - 2 if ty > y1 else y0 + 2
        else:                                                    # punta de lado
            ey = min(max(ty, y0 + r + 20), y1 - r - 20); ex = x1 - 2 if tx > x1 else x0 + 2
        dx, dy = tx - ex, ty - ey; L = math.hypot(dx, dy) or 1
        mt = max_tail or size * 2.2; Lc = min(L, mt)
        tipx, tipy = ex + dx / L * Lc, ey + dy / L * Lc
        hw = min(size * .55, max(size * .35, Lc * .35))         # base ancha y proporcional
        px, py = -dy / L, dx / L                                  # perpendicular
        if abs(dy) >= abs(dx) or (ty > y1 or ty < y0): b1, b2 = (ex - hw, ey), (ex + hw, ey)
        else: b1, b2 = (ex, ey - hw), (ex, ey + hw)
        bend = Lc * .18                                           # punta ligeramente curva (estilo cómic)
        mid1 = ((b1[0] + tipx) / 2 + px * bend, (b1[1] + tipy) / 2 + py * bend)
        tri = [b1, mid1, (tipx, tipy), b2]
        d.polygon(tri, fill=fill, outline=BLK, width=ow)
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=BLK, width=ow)
    if tri:                                                       # tapa la costura entre globo y punta
        cx_, cy_ = (tri[0][0] + tri[3][0]) / 2, (tri[0][1] + tri[3][1]) / 2
        shrink = lambda p: (cx_ + (p[0] - cx_) * .78, cy_ + (p[1] - cy_) * .78)
        d.polygon([shrink(tri[0]), shrink(tri[1]), (cx_ + (tri[2][0] - cx_) * .5, cy_ + (tri[2][1] - cy_) * .5), shrink(tri[3])], fill=fill)
    for i, l in enumerate(lines):
        d.text((x, y0 + size * 0.4 + lh * i + lh / 2), l, font=f, fill=fg, anchor="mm")
    return (x0, y0, x1, y1)

def say(d, text, mouth, head=110, size=52, maxw=520, fill=WHITE, fg=BLK, side=None):
    """Globo que se acomoda SOLO junto a quien habla, sin tapar su cabeza.
    mouth = (x, y) de la boca; head = radio aproximado de la cabeza en px (guy: anchors(...)['head_r']).
    Va arriba y hacia el centro de la pantalla; si no cabe, de lado. La punta llega al costado de la cara.
    Nunca sale de la pantalla ni baja a los subtítulos. Devuelve la caja del globo."""
    _, _, _, bw, bh = _bubble_layout(d, text, size, maxw)
    mx, my = mouth; toward = side or (1 if mx < W / 2 else -1)
    tip = (mx + toward * head * .8, my - head * .15)
    bx = mx + toward * (head * .7 + bw * .3); by = my - head * 1.8 - bh / 2          # por encima de la coronilla (y gorra)
    if side or by - bh / 2 < 380:                                   # no cabe arriba: de lado
        bx = mx + toward * (head + 50 + bw / 2); by = my - head * .5
    bx = min(max(bx, bw / 2 + 30), W - bw / 2 - 30)
    by = min(max(by, 380 + bh / 2), 1330 - bh / 2)
    return bubble(d, bx, by, text, size, tail=tip, maxw=maxw, fill=fill, fg=fg, max_tail=max(size * 1.4, head * 1.1))

def calendar(d, cx, cy, day, label="DÍA", col=(240, 150, 40), sc=0.7):
    S = lambda v: v * sc
    d.rounded_rectangle([cx - S(190), cy - S(170), cx + S(190), cy + S(170)], int(S(26)), fill=WHITE, outline=BLK, width=6)
    d.rounded_rectangle([cx - S(190), cy - S(170), cx + S(190), cy - S(70)], int(S(26)), fill=col, outline=BLK, width=6)
    d.text((cx, cy - S(120)), label, font=fit_font(d, label, S(340), int(S(52))), fill=WHITE, anchor="mm")
    d.text((cx, cy + S(50)), str(day), font=fit_font(d, str(day), S(330), int(S(150))), fill=BLK, anchor="mm")   # se ajusta al ancho

def gauge(d, cx, cy, r, val, vmax, label, fg=WHITE):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(30, 30, 40), outline=WHITE, width=6)
    for k in range(11):
        a = math.pi + k / 10 * math.pi
        d.line([(cx + math.cos(a) * r * .85, cy + math.sin(a) * r * .85), (cx + math.cos(a) * r * .97, cy + math.sin(a) * r * .97)], fill=WHITE, width=5)
    a = math.pi + cl(val / vmax) * math.pi
    d.line([(cx, cy), (cx + math.cos(a) * r * .8, cy + math.sin(a) * r * .8)], fill=RED, width=12)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=RED)
    d.text((cx, cy + 50), label, font=F(56), fill=fg, anchor="mm", stroke_width=5, stroke_fill=BLK)

def confetti(d, t, n=60, seed=7):
    rng = random.Random(seed)
    for i in range(n):
        x = rng.uniform(0, W); sp = rng.uniform(200, 400); y = (rng.uniform(-H, 0) + t * sp) % H
        c = rng.choice([(255, 214, 0), (225, 35, 45), (60, 160, 230), (60, 180, 90), (240, 120, 200)])
        d.rectangle([x, y, x + 14, y + 24], fill=c)

def speedlines(d, t, n=26, col=WHITE, y0=250, y1=1350, seed=2):
    rng = random.Random(seed)
    for i in range(n):
        y = rng.uniform(y0, y1); ln = rng.uniform(80, 260); sp = rng.uniform(1600, 2600)
        x = (rng.uniform(0, W) + t * sp) % (W + 400) - 300
        d.line([(x, y), (x + ln, y)], fill=col, width=5)

def sparkles(d, t, n=24, box=(80, 300, 1000, 1250), col=YEL, seed=3):
    rng = random.Random(seed)
    for i in range(n):
        x, y = rng.uniform(box[0], box[2]), rng.uniform(box[1], box[3])
        if (int(t * 4) + i) % 3 == 0:
            d.polygon([(x, y - 18), (x + 6, y), (x, y + 18), (x - 6, y)], fill=col)
            d.polygon([(x - 18, y), (x, y - 6), (x + 18, y), (x, y + 6)], fill=col)

def follow_btn(d, lt, y=1250, delay=1.5, text="SÍGUEME"):
    """Botón SÍGUEME que aparece con rebote."""
    if lt <= delay: return
    sc = pop((lt - delay) / 0.35)
    d.rounded_rectangle([540 - 330 * sc, y - 80 * sc, 540 + 330 * sc, y + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
    d.text((540, y), text, font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")

def stamp(img, draw_fn, x, y, size=900, angle=0.0, flip=False, **kw):
    """Dibuja cualquier personaje en una capa aparte y la pega rotada/volteada.
    draw_fn(d, cx, cy, **kw) se llama con el centro de la capa (size/2, size/2)."""
    tmp = Image.new("RGBA", (size, size), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    draw_fn(td, size / 2, size / 2, **kw)
    if flip: tmp = tmp.transpose(Image.FLIP_LEFT_RIGHT)
    if angle: tmp = tmp.rotate(angle, resample=Image.BICUBIC)
    img.paste(tmp, (int(x - size / 2), int(y - size / 2)), tmp)
    return ImageDraw.Draw(img)

def shake_arr(arr, t, amp):
    import numpy as np
    return np.roll(arr, int(math.sin(t * 60) * amp), axis=1) if amp else arr


def fit_font(d, text, maxw, size):
    """Fuente del tamaño más grande (<= size) para que 'text' quepa en maxw px."""
    while size > 10 and d.textlength(text, font=F(size)) > maxw: size -= 2
    return F(size)
