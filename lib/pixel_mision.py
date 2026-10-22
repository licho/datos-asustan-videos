"""Motor para las 'Misiones' en pixel art (180x320 escalado 6x): HUD, mochila, diálogo, ventanas y cierre.
Uso en un spec:  CAPTIONS = False  y cada escena termina con  return finish(c, img, "MISIÓN 004", INV)"""
import math, random, textwrap
import numpy as np
from PIL import Image, ImageDraw
from ._lazy import SRC  # asegura src en sys.path
from pixel import P, rect, text, FONT, FONTB, LW, LH, SC
from alien import icon, popup, backpack, FONTM, GROUND
from mision002 import hero, item as item2

def canvas_px(col="black"):
    img = Image.new("RGB", (LW, LH), P[col]); return img, ImageDraw.Draw(img)

def dialog_px(d, s, lt, cps=24):
    s = s.replace("*", "")
    rect(d, 6, 262, 168, 52, "black"); rect(d, 6, 262, 168, 1, "white"); rect(d, 6, 313, 168, 1, "white")
    rect(d, 6, 262, 1, 52, "white"); rect(d, 173, 262, 1, 52, "white")
    shown = s[:max(0, int(lt * cps))]
    for i, line in enumerate(textwrap.wrap(shown, 26)[:4]):
        text(d, 11, 266 + i * 12, line, "white", font=FONTM, center=False)

def hud_px(d, name, items, total=6):
    rect(d, 0, 0, LW, 16, "black"); rect(d, 0, 15, LW, 1, "lgray")
    text(d, 6, 4, name, "orange", FONTM, center=False)
    s = f"INV {items}/{total}"; w = d.textlength(s, font=FONTM)
    text(d, LW - 6 - w, 4, s, "green" if items == total else "yellow", FONTM, center=False)

def n_items(c, INV):
    """INV = [(índice_de_línea, tipo, letrero)]."""
    return len([1 for it in INV if it[0] <= c.line])

def inv_grid_px(d, c, INV, item_fn, y0=44, bottom=None, title="MOCHILA  6 ESPACIOS", carrier=None):
    rect(d, 0, 16, LW, 246, "navy")
    for y in range(20, 260, 8): rect(d, 0, y, LW, 1, "black")
    text(d, LW / 2, y0 - 18, title, "white", FONTM)
    got = [it for it in INV if it[0] <= c.line]
    for i in range(6):
        x, y = 16 + (i % 3) * 52, y0 + (i // 3) * 52
        sel = bool(got) and i == len(got) - 1 and c.cap_lt < 0.9
        col = "yellow" if sel else "lgray"
        rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, col); rect(d, x, y + 43, 44, 1, col); rect(d, x, y, 1, 44, col); rect(d, x + 43, y, 1, 44, col)
        text(d, x + 5, y + 2, str(i + 1), "lav", FONT, center=False, shadow=None)
        if i < len(got): item_fn(d, got[i][1], x + 10, y + 10, 2)
    if got and got[-1][0] == c.line and c.cap_lt < 3.0:
        popup(d, got[-1][2], 152, "green", "black")
    hero(d, 24, 190, scared=True, frame=int(c.t * 6) % 2)
    (carrier or (lambda dd, n: backpack(dd, 60, 202, 2, n)))(d, len(got))
    if bottom: bottom(d)
    return len(got)

def end_screen(d, c, INV, item_fn, next_name, title="MOCHILA  6/6", question="¿QUÉ CAMBIARÍAS?"):
    rect(d, 0, 16, LW, 246, "navy")
    text(d, LW / 2, 26, title, "white", FONTB)
    for i in range(6):
        x, y = 16 + (i % 3) * 52, 50 + (i // 3) * 52
        rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, "lgray"); rect(d, x, y + 43, 44, 1, "lgray"); rect(d, x, y, 1, 44, "lgray"); rect(d, x + 43, y, 1, 44, "lgray")
        item_fn(d, INV[i][1], x + 10, y + 10, 2)
    text(d, LW / 2, 166, question, "yellow", FONTB)
    if int(c.t * 2) % 2 == 0: text(d, LW / 2, 190, "COMENTA ↓", "pink", FONTB)
    text(d, LW / 2, 222, f"{next_name}: PRÓXIMAMENTE", "green", FONTM)
    text(d, LW / 2, 240, "SÍGUEME: DATOS QUE ASUSTAN", "white", FONTM)

def game_over(d, c, line2="", skull=True):
    rect(d, 0, 16, LW, 246, "black")
    if skull: item2(d, "calavera", 66, 70, 4)
    text(d, LW / 2, 140, "GAME OVER", "red", FONTB)
    if line2 and int(c.t * 3) % 2 == 0: text(d, LW / 2, 170, line2, "white", FONTM)

def finish(c, img, name, INV, items=None, shake=(0, 0)):
    """HUD + diálogo (subtítulo de la línea actual) + escala 6x con scanlines → imagen 1080x1920."""
    d = ImageDraw.Draw(img)
    hud_px(d, name, n_items(c, INV) if items is None else items)
    if c.cap: dialog_px(d, c.cap, c.cap_lt)
    big = img.resize((LW * SC, LH * SC), Image.NEAREST)
    arr = np.asarray(big).copy()
    if shake != (0, 0): arr = np.roll(arr, shake[0] * SC, axis=1); arr = np.roll(arr, shake[1] * SC, axis=0)
    arr[::SC, :, :] = (arr[::SC, :, :] * 0.82).astype(np.uint8)
    return Image.fromarray(arr)

# ---------- íconos pixel nuevos (12x12 lógicos) ----------
def item_px(d, kind, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "manivela":
        R(1, 4, 7, 4, "dgray"); R(8, 3, 3, 6, "lgray"); R(11, 2, 1, 8, "yellow"); R(3, 8, 1, 3, "orange"); R(2, 10, 3, 1, "orange")
    elif kind == "libreta":
        R(2, 0, 9, 12, "orange"); R(3, 1, 7, 10, "white"); R(1, 2, 2, 1, "dgray"); R(1, 5, 2, 1, "dgray"); R(1, 8, 2, 1, "dgray")
        R(4, 3, 5, 1, "navy"); R(4, 5, 4, 1, "navy"); R(4, 7, 5, 1, "navy")
    elif kind == "mapa":
        R(0, 1, 4, 10, "white"); R(4, 2, 4, 10, "lgray"); R(8, 1, 4, 10, "white"); R(2, 4, 7, 1, "red"); R(8, 4, 1, 4, "red"); R(9, 7, 2, 2, "red"); R(1, 8, 2, 2, "green")
    elif kind == "candado":
        R(3, 0, 6, 2, "lgray"); R(2, 1, 2, 5, "lgray"); R(8, 1, 2, 5, "lgray"); R(1, 5, 10, 7, "yellow"); R(5, 7, 2, 3, "black")
    elif kind == "reloj":
        R(4, 0, 4, 2, "dgray"); R(4, 10, 4, 2, "dgray"); R(2, 2, 8, 8, "black"); R(3, 3, 6, 6, "blue"); R(4, 5, 4, 1, "green"); R(5, 4, 1, 3, "green")
    elif kind == "aspiradora":
        d.ellipse([x, y + 3 * big, x + 12 * big, y + 12 * big], fill=P["dgray"]); R(3, 5, 6, 2, "black"); R(4, 5, 1, 1, "red"); R(7, 5, 1, 1, "red")
    else:
        try: item2(d, kind, x, y, big)
        except Exception: icon(d, kind, x, y, big)

def evil_eyes(d, x, y, w=10, t=0.0):
    """Ojos rojos de máquina malvada (x, y = centro)."""
    on = int(t * 3) % 7 != 0
    for dx in (-w // 2, w // 2 - 2):
        rect(d, x + dx, y, 3, 2 if on else 1, "red")
    rect(d, x - w // 2 - 1, y - 2, 4, 1, "black"); rect(d, x + w // 2 - 2, y - 2, 4, 1, "black")


# ---------- cámara pixel: mueve/acerca un "mundo" lógico y lo deja en 180x320 sin perder los pixeles ----------
def px_film(world, cx, cy, zoom=1.0):
    """Recorta el mundo (imagen lógica, cualquier tamaño) centrado en (cx, cy) con zoom (1 = tamaño de pantalla lógica,
    2 = el doble de cerca, 0.5 = ve el doble de área) y lo escala a LWxLH sin suavizar (pixel nítido).
    Para los movimientos usa reels_engine.camera (path, pan, whip, impact…): pasa shot.x, shot.y, shot.zoom."""
    w, h = LW / zoom, LH / zoom
    x0 = min(max(cx - w / 2, 0), max(0, world.width - w)); y0 = min(max(cy - h / 2, 0), max(0, world.height - h))
    box = tuple(int(round(v)) for v in (x0, y0, x0 + w, y0 + h))
    return world.crop(box).resize((LW, LH), Image.NEAREST)

# ---------- piezas navideñas pixel ----------
def night_sky_px(d, w, h, t, seed=3):
    for y in range(0, h, 4): rect(d, 0, y, w, 4, "navy" if y < h * .55 else "purple")
    r = random.Random(seed)
    for k in range(int(w * h / 900)):
        x, y = r.randint(0, w - 1), r.randint(0, int(h * .6))
        if (int(t * 4) + k) % 5: rect(d, x, y, 1, 1, "white")
    d.ellipse([w - 46, 20, w - 24, 42], fill=P["white"]); d.ellipse([w - 40, 18, w - 20, 38], fill=P["navy"])

def house_px(d, x, y, w=40, h=30, wall="peach", roof="red", lit=True, chimney=True):
    """Casa con techo nevado; (x, y) = esquina inf. izq."""
    rect(d, x, y - h, w, h, wall); rect(d, x, y - h, w, 1, "black")
    d.polygon([(x - 3, y - h), (x + w / 2, y - h - w * .45), (x + w + 3, y - h)], fill=P[roof])
    d.polygon([(x - 3, y - h), (x + w / 2, y - h - w * .45), (x + w + 3, y - h), (x + w / 2, y - h - w * .3)], fill=P["white"])
    if chimney: rect(d, x + w - 12, y - h - w * .42, 6, 10, "brown"); rect(d, x + w - 13, y - h - w * .42, 8, 2, "white")
    rect(d, x + 6, y - h + 8, 8, 8, "yellow" if lit else "dgray"); rect(d, x + w - 14, y - h + 8, 8, 8, "yellow" if lit else "dgray")
    rect(d, x + w / 2 - 4, y - 12, 8, 12, "brown")

def snow_ground_px(d, y, w, h):
    rect(d, 0, y, w, h - y, "white"); rect(d, 0, y, w, 1, "lgray")

def reindeer_px(d, x, y, t, k=0):
    fr = (int(t * 8) + k) % 2
    rect(d, x, y, 12, 5, "brown"); rect(d, x + 10, y - 4, 4, 5, "brown"); rect(d, x + 13, y - 3, 1, 1, "black")
    rect(d, x + 14, y - 2, 1, 1, "red" if k == 0 else "brown")
    rect(d, x + 10, y - 7, 1, 3, "orange"); rect(d, x + 9, y - 8, 3, 1, "orange")
    for lx in (1, 9): rect(d, x + lx + (fr if lx == 1 else -fr), y + 5, 1, 3, "brown")

def sleigh_px(d, x, y, t, sack=0, reindeer=2, rider=True):
    """Trineo con renos (vuela a la derecha); (x, y) = esquina sup. izq. del trineo."""
    for k in range(reindeer): reindeer_px(d, x + 34 + k * 18, y + 2 + (k % 2), t, k)
    rect(d, x + 26, y + 6, 10 + 18 * (reindeer - 1), 1, "lgray")
    rect(d, x, y + 4, 30, 10, "red"); rect(d, x, y + 4, 30, 1, "black"); rect(d, x + 24, y, 6, 6, "red")
    rect(d, x - 2, y + 15, 34, 1, "yellow"); rect(d, x + 31, y + 13, 2, 2, "yellow")
    if sack: d.ellipse([x + 2, y - 8 - min(sack, 6), x + 16, y + 6], fill=P["brown"]); rect(d, x + 7, y - 9 - min(sack, 6), 4, 2, "yellow")
    if rider: hero(d, x + 18, y - 14, frame=0, big=1)

def santa_bed_px(d, x, y, t):
    """Santa enfermo en cama (gripa): (x, y) = esquina inf. izq. de la cama."""
    rect(d, x, y - 10, 60, 10, "brown"); rect(d, x, y - 22, 6, 22, "brown")
    rect(d, x + 6, y - 16, 54, 7, "red"); rect(d, x + 6, y - 16, 54, 1, "white")
    rect(d, x + 7, y - 22, 12, 7, "white")
    rect(d, x + 9, y - 28, 10, 8, "peach"); rect(d, x + 9, y - 22, 10, 5, "white")
    rect(d, x + 8, y - 31, 12, 4, "red"); rect(d, x + 20, y - 33, 3, 3, "white")
    rect(d, x + 18, y - 25, 3, 2, "red")
    rect(d, x + 20, y - 24, 8, 1, "white"); rect(d, x + 27, y - 25, 2, 3, "red")
    if int(t * 2) % 2: text(d, x + 36, y - 40, "ACHÚ!", "white", FONTM)

def cookie_milk_px(d, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    R(0, 2, 5, 10, "white"); R(0, 2, 5, 1, "lgray"); d.ellipse([x + 6 * big, y + 5 * big, x + 12 * big, y + 11 * big], fill=P["orange"])
    R(8, 7, 1, 1, "brown"); R(10, 8, 1, 1, "brown"); R(8, 9, 1, 1, "brown")

def tamal_px(d, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    R(1, 3, 10, 7, "yellow"); R(0, 4, 2, 5, "lgray"); R(10, 4, 2, 5, "lgray"); R(3, 5, 6, 1, "orange"); R(4, 7, 4, 1, "orange")
    for k in range(3): R(3 + k * 3, 0 + (k % 2), 1, 2, "lgray")

def xmas_item_px(d, kind, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "lista":
        R(2, 0, 8, 12, "white"); R(1, 0, 10, 1, "orange"); R(1, 11, 10, 1, "orange")
        for k in range(4): R(3, 2 + k * 2, 1, 1, "green"); R(5, 2 + k * 2, 4, 1, "navy")
    elif kind == "zanahoria":
        d.polygon([(x + 3 * big, y + 3 * big), (x + 9 * big, y + 3 * big), (x + 6 * big, y + 12 * big)], fill=P["orange"]); R(4, 0, 1, 3, "green"); R(6, 0, 1, 3, "green"); R(8, 1, 1, 2, "green")
    elif kind == "calcetines":
        R(2, 0, 4, 8, "red"); R(2, 7, 7, 4, "red"); R(2, 0, 4, 2, "white"); R(2, 3, 4, 1, "white"); R(8, 8, 1, 3, "white")
    elif kind == "pantuflas":
        R(0, 6, 11, 5, "pink"); R(0, 6, 4, 2, "white"); R(8, 4, 2, 2, "white"); R(9, 3, 1, 1, "black"); R(7, 3, 1, 1, "black")
    elif kind == "llave":
        d.ellipse([x, y, x + 6 * big, y + 6 * big], outline=P["yellow"], width=2 * big); R(5, 3, 7, 1, "yellow"); R(9, 4, 1, 3, "yellow"); R(11, 4, 1, 2, "yellow")
    elif kind == "globo":
        d.ellipse([x + big, y + big, x + 11 * big, y + 11 * big], fill=P["blue"]); R(3, 3, 3, 2, "green"); R(6, 6, 3, 3, "green"); R(2, 7, 2, 2, "green"); R(1, 6, 10, 1, "white")
    elif kind == "galletas": cookie_milk_px(d, x, y, big)
    elif kind == "tamal": tamal_px(d, x, y, big)
    else: item_px(d, kind, x, y, big)
