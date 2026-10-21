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

def inv_grid_px(d, c, INV, item_fn, y0=44, bottom=None):
    rect(d, 0, 16, LW, 246, "navy")
    for y in range(20, 260, 8): rect(d, 0, y, LW, 1, "black")
    text(d, LW / 2, y0 - 18, "MOCHILA  6 ESPACIOS", "white", FONTM)
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
    backpack(d, 60, 202, 2, len(got))
    if bottom: bottom(d)
    return len(got)

def end_screen(d, c, INV, item_fn, next_name):
    rect(d, 0, 16, LW, 246, "navy")
    text(d, LW / 2, 26, "MOCHILA  6/6", "white", FONTB)
    for i in range(6):
        x, y = 16 + (i % 3) * 52, 50 + (i // 3) * 52
        rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, "lgray"); rect(d, x, y + 43, 44, 1, "lgray"); rect(d, x, y, 1, 44, "lgray"); rect(d, x + 43, y, 1, 44, "lgray")
        item_fn(d, INV[i][1], x + 10, y + 10, 2)
    text(d, LW / 2, 166, "¿QUÉ CAMBIARÍAS?", "yellow", FONTB)
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
