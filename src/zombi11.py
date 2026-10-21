import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from pixel import P, rect, text, FONT, FONTB, hero, zombie, LW, LH, SC
from alien import icon, slot, popup, dialog, backpack, FONTM, GROUND, lerp, cl

FPS = 30

def street(d, t, red=False):
    flash = red and int(t * 3) % 2 == 0
    for y in range(16, GROUND, 4):
        rect(d, 0, y, LW, 4, ("purple" if flash else "navy") if y < 120 else ("dgray" if y < 180 else "lav"))
    d.ellipse([130, 30, 150, 50], fill=P["lgray"])
    rng = random.Random(7)
    for x0, w, h in [(0, 34, 90), (32, 30, 120), (60, 40, 80), (98, 30, 130), (126, 54, 100)]:
        rect(d, x0, GROUND - h, w, h, "black")
        for wy in range(GROUND - h + 6, GROUND - 6, 10):
            for wx in range(x0 + 4, x0 + w - 4, 7):
                r = rng.random()
                if r < 0.12: rect(d, wx, wy, 3, 4, "orange")
                elif r < 0.2: rect(d, wx, wy, 3, 4, "red")
    rect(d, 0, GROUND, LW, LH - GROUND, "dgray")
    for x in range(0, LW, 16): rect(d, x, GROUND + 14, 8, 2, "yellow")

def car(d, x, y, c="red"):
    rect(d, x + 6, y, 22, 7, c); rect(d, x, y + 6, 36, 9, c)
    rect(d, x + 8, y + 1, 8, 5, "blue"); rect(d, x + 18, y + 1, 8, 5, "black")
    rect(d, x + 4, y + 14, 7, 5, "black"); rect(d, x + 25, y + 14, 7, 5, "black")

def extra_icon(d, kind, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "consola":
        R(0, 4, 12, 6, "lgray"); R(2, 6, 2, 2, "dgray"); R(1, 7, 4, 0.5, "dgray"); R(8, 6, 1, 1, "red"); R(10, 7, 1, 1, "blue")
    elif kind == "katana":
        for k in range(10): R(1 + k, 10 - k, 1, 1, "white")
        R(1, 9, 3, 1, "yellow"); R(0, 10, 2, 2, "brown")
    elif kind == "telefono":
        R(1, 0, 5, 11, "black"); R(2, 1, 3, 8, "blue"); R(7, 6, 4, 6, "lav"); R(8, 7, 2, 1, "white"); R(8, 9, 2, 1, "white")
    else:
        icon(d, kind, x, y, big)

INV = [(6.0, "agua", "AGUA: EQUIPADA"), (8.0, "comida", "COMIDA: EQUIPADA"), (16.0, "linterna", "LINTERNA + BATERÍAS"),
       (19.0, "botiquin", "SALUD: PROTEGIDA"), (29.0, "radio", "RADIO: EQUIPADA"), (31.5, "telefono", "TEL + CARGADOR + DOCS")]

def n_items(t): return len([1 for it in INV if it[0] <= t])

def inv_grid(d, t, y0=40, hl=None):
    rect(d, 0, 16, LW, GROUND - 16 + 26, "navy")
    for y in range(20, 260, 8): rect(d, 0, y, LW, 1, "black")
    text(d, LW / 2, y0 - 16, "MOCHILA  6 ESPACIOS", "white", FONTM)
    got = [it for it in INV if it[0] <= t]
    for i in range(6):
        x, y = 16 + (i % 3) * 52, y0 + (i // 3) * 52
        sel = bool(got) and i == len(got) - 1 and t - got[-1][0] < 0.9
        rect(d, x, y, 44, 44, "black")
        col = "yellow" if sel else "lgray"
        rect(d, x, y, 44, 1, col); rect(d, x, y + 43, 44, 1, col); rect(d, x, y, 1, 44, col); rect(d, x + 43, y, 1, 44, col)
        text(d, x + 5, y + 2, str(i + 1), "lav", FONT, center=False, shadow=None)
        if i < len(got): extra_icon(d, got[i][1], x + 10, y + 10, 2)
    if got and t - got[-1][0] < 1.6:
        popup(d, got[-1][2], 150, "green", "black")
    return len(got)

def hud(d, items):
    rect(d, 0, 0, LW, 16, "black"); rect(d, 0, 15, LW, 1, "lgray")
    text(d, 6, 4, "MISIÓN 001", "red", FONTM, center=False)
    text(d, 120, 4, f"INV {items}/6", "green" if items == 6 else "yellow", FONTM, center=False)

def bar(d, x, y, label, frac, col):
    text(d, x, y, label, "white", FONTM, center=False)
    rect(d, x, y + 12, 100, 7, "black"); w = int(98 * max(0, frac))
    if w > 0: rect(d, x + 1, y + 13, w, 5, col)

CAPS = [
    (0.0, 2.5, "Acaba de comenzar el apocalipsis zombi."),
    (2.5, 3.5, "Tienes una mochila... y solo 6 objetos."),
    (3.5, 5.0, "Si metes tu consola, ya empezamos mal."),
    (5.0, 10.0, "1: agua potable. 2: comida no perecedera."),
    (10.0, 15.0, "Los zombis podrán comerse tu cerebro... pero la deshidratación se te adelanta."),
    (15.0, 21.0, "3: linterna con baterías extra. 4: botiquín con tus medicamentos."),
    (21.0, 28.0, "Sobrevivir a los muertos vivientes para morir por una ampolla... humillante."),
    (28.0, 34.0, "5: radio portátil. 6: teléfono, cargador y documentos protegidos."),
    (34.0, 40.0, "Información, comunicación y una forma de identificarte."),
    (40.0, 44.0, "¿Y las armas? ¿La katana que compraste por internet? Déjala."),
    (44.0, 51.0, "Tu personaje tiene cero experiencia... y tú te cansas subiendo escaleras."),
    (51.0, 55.0, "Evita multitudes, sigue las alertas oficiales y busca un lugar seguro."),
    (55.0, 60.0, "Misión: sobrevivir. Secundario: no ser el NPC más inútil del apocalipsis."),
    (60.0, 66.0, "¿Qué objeto añadirías tú?"),
]

def frame(t, T=None, Tof=None):
    if T is None: T = t
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    shake = (0, 0); items = n_items(t)
    if t < 5.0:
        street(d, t, red=True)
        car(d, 4, GROUND - 19, "red"); car(d, 120, GROUND - 19, "blue")
        zombie(d, int(60 + t * 3), GROUND - 48, int(t * 4), big=2)
        hero(d, 140, GROUND - 46 - 22, scared=True, frame=int(t * 6) % 2) if False else hero(d, 128, GROUND - 46, scared=True, frame=int(t * 6) % 2)
        backpack(d, 100, GROUND - 32, 2, 0)
        if t < 3.5:
            if int(t * 3) % 2 == 0: popup(d, "ALERTA: BROTE ZOMBI", 60, "white", "red", FONTB)
            if t > 2.0: popup(d, "INVENTARIO: 0/6", 90, "yellow", "black")
        else:
            extra_icon(d, "consola", 66, 100, 4)
            for k in range(48): rect(d, 66 + k, 96 + k, 2, 2, "red"); rect(d, 114 - k, 96 + k, 2, 2, "red")
            popup(d, "YA EMPEZAMOS MAL", 70, "white", "red")
        if t < 0.4: shake = (random.randint(-2, 2), random.randint(-2, 2))
    elif t < 10.0 or 15.0 <= t < 21.0 or 28.0 <= t < 34.0:
        inv_grid(d, t)
        hero(d, 24, 184); backpack(d, 128, 194, 2, items)
        if 16.0 <= t < 21.0:
            for k in range(30):
                w = 6 + k * 3
                if k % 2 == 0: rect(d, 90 - w / 2, 230 - k * 2, w, 1, "yellow")
    elif t < 15.0:
        lt = t - 10.0
        street(d, t)
        hero(d, 120, GROUND - 46, scared=lt > 2.5, frame=0)
        zx = int(10 + lt * 3)
        zombie(d, zx, GROUND - 48, int(t * 3), big=2)
        text(d, zx + 12, GROUND - 60, "LENTO...", "green", FONTM)
        bar(d, 40, 30, "HIDRATACIÓN", 1 - lt / 4.5, "blue")
        bar(d, 40, 56, "ZOMBI LLEGANDO", lt / 60, "green")
        if lt > 2.5: popup(d, "LA SED GANA", 100, "white", "red", FONTB)
        for k in range(3):
            yy = GROUND - 60 - ((lt * 20 + k * 12) % 30)
            rect(d, 124 + k * 6, yy, 2, 4, "white")
    elif t < 28.0:
        lt = t - 21.0
        street(d, t)
        hx = int(lerp(10, 80, cl(lt / 2.5)))
        icon(d, "comida", 92, GROUND - 14, 1)
        if lt < 2.5:
            hero(d, hx, GROUND - 46, frame=int(t * 8) % 2)
        else:
            # fallen hero
            rect(d, 70, GROUND - 14, 46, 14, "orange"); rect(d, 112, GROUND - 16, 16, 16, "peach"); rect(d, 112, GROUND - 16, 16, 6, "brown")
            rect(d, 50, GROUND - 10, 20, 8, "navy")
            for k in range(3):
                a = t * 5 + k * 2.1
                rect(d, 120 + math.cos(a) * 14, GROUND - 30 + math.sin(a) * 5, 3, 3, "yellow")
            if lt > 3.2: popup(d, "AMPOLLA: -1 HP", 70, "white", "red", FONTB)
            if lt > 4.6: popup(d, "MUERTE MÁS HUMILLANTE", 100, "yellow", "purple")
            if lt > 4.6: popup(d, "DEL APOCALIPSIS", 116, "yellow", "purple")
            if 2.5 < lt < 2.9: shake = (random.randint(-2, 2), random.randint(-2, 2))
    elif t < 40.0:
        lt = t - 34.0
        inv_grid(d, t)
        hero(d, 24, 184); backpack(d, 128, 194, 2, 6)
        popup(d, "INVENTARIO COMPLETO 6/6", 150, "green", "black")
        for i, (lab, t0, c) in enumerate([("INFORMACIÓN +", 0.3, "blue"), ("COMUNICACIÓN +", 1.6, "green"), ("IDENTIDAD +", 3.0, "orange")]):
            if lt > t0: text(d, 96, 186 + i * 14, lab, c, FONTM)
    elif t < 51.0:
        lt = t - 40.0
        if lt < 4.0:
            inv_grid(d, t)
            hero(d, 24, 184); backpack(d, 128, 194, 2, 6)
            kx = int(lerp(-30, 70, cl(lt / 1.2)))
            extra_icon(d, "katana", kx, 168, 3)
            if lt > 1.5:
                popup(d, "INVENTARIO LLENO", 150, "white", "red", FONTB)
                if 1.5 < lt < 1.9: shake = (random.randint(-2, 2), 0)
        else:
            lt2 = lt - 4.0
            for y in range(16, GROUND + 26, 4): rect(d, 0, y, LW, 4, "dgray" if (y // 4) % 2 else "lav")
            for k in range(8):
                rect(d, 20 + k * 18, GROUND - k * 22, 40, 6, "lgray"); rect(d, 20 + k * 18, GROUND - k * 22 + 6, 40, 2, "black")
            step = min(3, int(lt2 / 1.2))
            hero(d, 26 + step * 18, GROUND - 46 - step * 22, scared=True, frame=int(t * 6) % 2)
            for k in range(3):
                yy = GROUND - 60 - step * 22 - ((lt2 * 20 + k * 10) % 24)
                rect(d, 30 + step * 18 + k * 8, yy, 2, 4, "white")
            popup(d, "EXPERIENCIA DE COMBATE: 0", 40, "white", "red")
            bar(d, 40, 64, "ENERGÍA", max(0.03, 1 - lt2 / 4.0), "yellow")
            if lt2 > 3.5: popup(d, "ESCALÓN 3: AGOTADO", 100, "yellow", "black")
    elif t < 60.0:
        lt = t - 51.0
        street(d, t)
        rect(d, 132, GROUND - 40, 46, 40, "lgray"); rect(d, 128, GROUND - 46, 52, 8, "dgreen"); rect(d, 148, GROUND - 26, 14, 26, "black")
        text(d, 154, GROUND - 58, "REFUGIO", "green", FONTM)
        for k in range(4):
            zombie(d, int(-10 + k * 16 + lt * 3), GROUND - 48 + (k % 2) * 2, int(t * 4) + k, big=1 if k % 2 else 2)
        hx = int(lerp(70, 134, cl(lt / 7.0)))
        if hx < 134:
            hero(d, hx, GROUND - 46, frame=int(t * 6) % 2); backpack(d, hx - 18, GROUND - 40, 1, 0, closed=True)
        if lt < 4.0:
            popup(d, "EVITA MULTITUDES", 40, "white", "red")
            if lt > 1.3: popup(d, "SIGUE ALERTAS OFICIALES", 60, "white", "black")
            if lt > 2.6: popup(d, "BUSCA UN LUGAR SEGURO", 80, "green", "black")
        else:
            popup(d, "MISIÓN: EN CURSO", 40, "yellow", "black", FONTB)
            popup(d, "OBJETIVO: NO HACERSE EL HÉROE", 66, "white", "purple")
            if lt > 5.6: popup(d, "BONUS: NO SER EL NPC INÚTIL", 86, "pink", "black")
    else:
        lt = t - 60.0
        rect(d, 0, 16, LW, 246, "navy")
        text(d, LW / 2, 26, "MOCHILA  6/6", "white", FONTB)
        for i in range(6):
            x, y = 16 + (i % 3) * 52, 50 + (i // 3) * 52
            rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, "lgray"); rect(d, x, y + 43, 44, 1, "lgray")
            rect(d, x, y, 1, 44, "lgray"); rect(d, x + 43, y, 1, 44, "lgray")
            extra_icon(d, INV[i][1], x + 10, y + 10, 2)
        text(d, LW / 2, 166, "¿QUÉ CAMBIARÍAS?", "yellow", FONTB)
        if int(t * 2) % 2 == 0: text(d, LW / 2, 190, "COMENTA ↓", "pink", FONTB)
        text(d, LW / 2, 222, "MISIÓN 002: PRÓXIMAMENTE", "green", FONTM)
        text(d, LW / 2, 240, "SÍGUEME: DATOS QUE ASUSTAN", "white", FONTM)
    hud(d, items)
    for cs, ce, s in CAPS:
        if cs <= t < ce:
            dialog(d, s, Tof(cs) if Tof else cs, T)
    big = img.resize((LW * SC, LH * SC), Image.NEAREST)
    arr = np.asarray(big).copy()
    if shake != (0, 0):
        arr = np.roll(arr, shake[0] * SC, axis=1); arr = np.roll(arr, shake[1] * SC, axis=0)
    arr[::SC, :, :] = (arr[::SC, :, :] * 0.82).astype(np.uint8)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        ims = [Image.fromarray(frame(float(x))).resize((270, 480), Image.NEAREST) for x in sys.argv[2:]]
        cols = min(6, len(ims)); rows = (len(ims) + 5) // 6
        sh = Image.new("RGB", (270 * cols, 480 * rows))
        for i, im in enumerate(ims): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sh.save("z11_prev.png"); sys.exit()
    from warp11 import v_of_T, T_of_v, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(min(65.99, v_of_T(i / FPS)), i / FPS, T_of_v).tobytes())
    p.stdin.close(); p.wait()
