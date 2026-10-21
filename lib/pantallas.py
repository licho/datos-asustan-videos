"""Documentos, pantallas e íconos: listas con palomitas, currículum, chat, monitores, gráficas, gente."""
import math
from .core import F, fit_font, BLK, WHITE, RED, YEL, dk, lc, cl, pop, check

def checklist(d, x, y, w, title, items, done=None, size=36, appear=1.0):
    """Tarjeta con lista. (x, y) = esquina sup. izq. done = cuántos ya tienen palomita (None = todos)."""
    n = len(items); h = 110 + n * (size + 26)
    d.rounded_rectangle([x, y, x + w, y + h], 24, fill=WHITE, outline=BLK, width=6)
    d.text((x + w / 2, y + 55), title, font=F(size + 8), fill=BLK, anchor="mm")
    for i, it in enumerate(items):
        if i >= n * cl(appear) + .001: break
        yy = y + 115 + i * (size + 26)
        ok = done is None or i < done
        d.rounded_rectangle([x + 30, yy - 18, x + 66, yy + 18], 8, fill=(40, 170, 80) if ok else WHITE, outline=BLK, width=3)
        if ok: d.line([(x + 38, yy), (x + 46, yy + 9), (x + 60, yy - 10)], fill=WHITE, width=5)
        d.text((x + 86, yy), it, font=F(size), fill=BLK, anchor="lm")
    return h

def document(d, x, y, w, h, title="CURRÍCULUM", lines=(), size=30, stamp=None):
    """Hoja tipo documento (CV, contrato). stamp=('RECHAZADO', color) sello rotado encima (dibújalo con lib.core.stamp si quieres rotar)."""
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BLK, width=6)
    d.text((x + w / 2, y + 55), title, font=F(size + 12), fill=BLK, anchor="mm")
    yy = y + 110
    for ln in lines:
        d.text((x + 30, yy), ln, font=F(size), fill=(60, 60, 60), anchor="lm"); yy += size + 20
    while yy < y + h - 40:
        d.line([(x + 30, yy), (x + w - 30, yy)], fill=(210, 210, 210), width=6); yy += 44
    if stamp:
        txt, col = stamp
        d.rounded_rectangle([x + w * .15, y + h * .55, x + w * .85, y + h * .55 + size * 2.4], 10, outline=col, width=8)
        d.text((x + w / 2, y + h * .55 + size * 1.2), txt, font=fit_font(d, txt, w * .62, int(size * 1.4)), fill=col, anchor="mm")

def phone_chat(d, x, y, w, h, title, msgs, shown=None, size=32):
    """Celular con chat. msgs = [(lado 'l'|'r', texto, hora)]. shown = cuántos mensajes se ven."""
    d.rounded_rectangle([x, y, x + w, y + h], 40, fill=(30, 30, 35), outline=BLK, width=6)
    d.rounded_rectangle([x + 16, y + 16, x + w - 16, y + h - 16], 28, fill=(240, 242, 245))
    d.rectangle([x + 16, y + 40, x + w - 16, y + 110], fill=(90, 80, 160)); d.text((x + 40, y + 75), title, font=F(size), fill=WHITE, anchor="lm")
    yy = y + 140
    for i, (side, txt, hora) in enumerate(msgs[: (len(msgs) if shown is None else shown)]):
        tw = d.textlength(txt, font=F(size)) + 40
        bx = x + 36 if side == "l" else x + w - 36 - tw
        d.rounded_rectangle([bx, yy, bx + tw, yy + size + 30], 18, fill=WHITE if side == "l" else (200, 230, 255), outline=(180, 180, 190), width=2)
        d.text((bx + 20, yy + (size + 30) / 2), txt, font=F(size), fill=BLK, anchor="lm")
        if hora: d.text((bx + tw - 6, yy + size + 40), hora, font=F(size * .6), fill=(120, 120, 130), anchor="rm")
        yy += size + 70

def monitor(d, x0, y0, x1, y1, content="chart", t=0.0, trend=1.0, col=(80, 220, 120), stand=True):
    """Monitor/pantalla. content: chart (gráfica; trend>0 sube) | wave (onda) | blank | text:<texto>."""
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(20, 25, 30), outline=BLK, width=6)
    i0, j0, i1, j1 = x0 + 20, y0 + 20, x1 - 20, y1 - 20
    if content == "chart":
        pts = []
        for k in range(25):
            u = k / 24; v = .5 - trend * (u - .5) * .8 + .08 * math.sin(k * 1.7 + t)
            pts.append((i0 + u * (i1 - i0), j0 + cl(v) * (j1 - j0)))
        d.line(pts, fill=col, width=7)
    elif content == "wave":
        mid = (j0 + j1) / 2
        d.line([(i0 + k * (i1 - i0) / 80, mid + math.sin(k * .9 + t * 8) * (j1 - j0) * .35 * abs(math.sin(k * .21 + t))) for k in range(81)], fill=col, width=5)
    elif content.startswith("text:"):
        d.text(((i0 + i1) / 2, (j0 + j1) / 2), content[5:], font=fit_font(d, content[5:], i1 - i0 - 20, 60), fill=col, anchor="mm")
    if stand:
        cx = (x0 + x1) / 2
        d.rectangle([cx - 15, y1, cx + 15, y1 + 50], fill=(60, 60, 65)); d.rectangle([cx - 80, y1 + 45, cx + 80, y1 + 60], fill=(60, 60, 65), outline=BLK, width=3)

def people_grid(d, x, y, n=10, cols=5, highlight=(), gap=95, size=1.0, col=(150, 155, 165), hcol=RED):
    """Íconos de personas ('1 de cada 10'). (x, y) = centro de la cuadrícula."""
    rows = math.ceil(n / cols)
    for i in range(n):
        cx = x + (i % cols - (cols - 1) / 2) * gap * size; cy = y + (i // cols - (rows - 1) / 2) * gap * 1.4 * size
        c = hcol if i in highlight else col
        d.ellipse([cx - 22 * size, cy - 60 * size, cx + 22 * size, cy - 16 * size], fill=c)
        d.rounded_rectangle([cx - 34 * size, cy - 10 * size, cx + 34 * size, cy + 60 * size], int(18 * size), fill=c)

def thought(d, x, y, w, h, tail_to=None, fill=WHITE):
    """Nube de pensamiento (x, y = centro) con bolitas hacia tail_to. Devuelve caja interior."""
    for k in range(10):
        a = k / 10 * 2 * math.pi
        cx, cy = x + math.cos(a) * w * .42, y + math.sin(a) * h * .38
        d.ellipse([cx - w * .17, cy - h * .2, cx + w * .17, cy + h * .2], fill=fill, outline=BLK, width=4)
    d.ellipse([x - w * .45, y - h * .4, x + w * .45, y + h * .4], fill=fill)
    if tail_to:
        tx, ty = tail_to
        for k, r in enumerate((22, 15, 9)):
            u = .55 + k * .17; px, py = x + (tx - x) * u, y + h * .4 + (ty - y - h * .4) * u
            d.ellipse([px - r, py - r, px + r, py + r], fill=fill, outline=BLK, width=3)
    return (x - w * .35, y - h * .3, x + w * .35, y + h * .3)

def sign_board(d, x, y, text, size=48, bg=(110, 70, 40), fg=WHITE, post=True, post_h=260):
    """Letrero de madera con poste; (x, y) = base del poste (piso)."""
    tw = d.textlength(text, font=F(size)) + 60; top = y - post_h - size * 2
    if post: d.rectangle([x - 14, top + size, x + 14, y], fill=dk(bg, .85), outline=BLK, width=4)
    d.rounded_rectangle([x - tw / 2, top, x + tw / 2, top + size * 1.8], 12, fill=bg, outline=BLK, width=5)
    d.text((x, top + size * .9), text, font=F(size), fill=fg, anchor="mm")

def heart(d, x, y, r=40, col=RED):
    d.ellipse([x - r, y - r * .6, x, y + r * .3], fill=col); d.ellipse([x, y - r * .6, x + r, y + r * .3], fill=col)
    d.polygon([(x - r * .97, y), (x + r * .97, y), (x, y + r)], fill=col)

def arrow(d, x0, y0, x1, y1, col=RED, w=14):
    d.line([(x0, y0), (x1, y1)], fill=col, width=w)
    a = math.atan2(y1 - y0, x1 - x0); L = w * 2.6
    d.polygon([(x1 + math.cos(a) * L * .5, y1 + math.sin(a) * L * .5), (x1 + math.cos(a + 2.5) * L, y1 + math.sin(a + 2.5) * L), (x1 + math.cos(a - 2.5) * L, y1 + math.sin(a - 2.5) * L)], fill=col)
