import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from pixel import P, rect, text, FONT, FONTB, LW, LH, SC
from alien import icon, popup, dialog, backpack, FONTM, GROUND, lerp, cl
from mision002 import hero, item as item2

FPS = 30

# ---------- escenario ----------
def garden(d, t):
    for y in range(16, 150, 4): rect(d, 0, y, LW, 4, "blue")
    d.ellipse([20, 30, 40, 50], fill=P["yellow"])
    for cx in (70, 120):
        d.ellipse([cx, 40, cx + 30, 52], fill=P["white"]); d.ellipse([cx + 10, 34, cx + 34, 50], fill=P["white"])
    rect(d, 0, 150, LW, GROUND - 150, "green")
    for x in range(0, LW, 8):
        for y in range(156, GROUND, 10): rect(d, x + (y // 10) % 2 * 4, y, 1, 2, "dgreen")
    rect(d, 0, GROUND, LW, LH - GROUND, "brown")
    for x in range(0, LW, 12): rect(d, x, GROUND + 6, 6, 2, "dgray")

def house(d):
    rect(d, 0, 140, 46, GROUND - 140, "peach"); d.polygon([(-4, 140), (23, 116), (50, 140)], fill=P["red"])
    rect(d, 14, GROUND - 30, 16, 30, "brown"); rect(d, 26, GROUND - 16, 2, 2, "yellow"); rect(d, 32, 154, 10, 10, "blue")

def tree(d):
    rect(d, 150, 140, 10, GROUND - 140, "brown")
    d.ellipse([124, 92, 180, 150], fill=P["dgreen"]); d.ellipse([132, 100, 172, 142], fill=P["green"])

def hive(d, x, y, t, shake=0.0):
    dx = int(math.sin(t * 30) * 2 * shake)
    rect(d, x + 7 + dx, y - 6, 2, 6, "brown")
    for k, w in enumerate([10, 14, 16, 14, 10]):
        rect(d, x + 8 - w // 2 + dx, y + k * 4, w, 4, "yellow" if k % 2 == 0 else "orange")
    rect(d, x + 6 + dx, y + 14, 4, 3, "black")

def car(d, x, y, t, inside=False, scared=False):
    rect(d, x + 10, y, 36, 14, "red"); rect(d, x + 14, y + 3, 12, 10, "blue"); rect(d, x + 30, y + 3, 13, 10, "blue")
    if inside:
        rect(d, x + 16, y + 5, 8, 8, "peach"); rect(d, x + 16, y + 5, 8, 2, "brown")
        rect(d, x + 18, y + 8, 1, 1 + scared, "black"); rect(d, x + 21, y + 8, 1, 1 + scared, "black")
    rect(d, x, y + 13, 60, 14, "red"); rect(d, x + 2, y + 16, 6, 3, "yellow"); rect(d, x + 28, y + 15, 1, 10, "black")
    rect(d, x + 6, y + 25, 10, 8, "black"); rect(d, x + 44, y + 25, 10, 8, "black")

def mower(d, x, y, hx, hy, t):
    rect(d, x, y + 4, 20, 9, "red"); rect(d, x + 4, y + 1, 12, 4, "lgray")
    rect(d, x + 1, y + 12, 5, 5, "black"); rect(d, x + 14, y + 12, 5, 5, "black")
    d.line([(x + 2, y + 4), (hx, hy)], fill=P["black"], width=2)
    if int(t * 10) % 2: rect(d, x + 20, y + 10, 4, 2, "dgreen"); rect(d, x + 22, y + 6, 3, 2, "green")

def bee(d, x, y, angry=False):
    rect(d, x, y, 5, 3, "yellow"); rect(d, x + 1, y, 1, 3, "black"); rect(d, x + 3, y, 1, 3, "black")
    rect(d, x + 1, y - 2, 3, 2, "white")
    if angry: rect(d, x + 4, y, 1, 1, "red")

def swarm(d, cx, cy, t, n=24, spread=14, angry=False, seed=7):
    rng = random.Random(seed)
    for i in range(n):
        a = rng.random() * 6.28 + t * (2 + rng.random() * 3) * (1 if i % 2 else -1)
        r = spread * (0.3 + rng.random() * 0.7)
        bee(d, cx + math.cos(a) * r, cy + math.sin(a) * r * 0.7, angry)

def bush(d, x, y, t, shake=0.0):
    dx = int(math.sin(t * 25) * 2 * shake)
    for (a, b, r) in [(10, 14, 14), (28, 8, 16), (46, 14, 14)]:
        d.ellipse([x + a - r + dx, y + b - r, x + a + r + dx, y + b + r], fill=P["dgreen"])
    for (a, b, r) in [(12, 12, 9), (30, 6, 10), (46, 12, 8)]:
        d.ellipse([x + a - r + dx, y + b - r, x + a + r + dx, y + b + r], fill=P["green"])

# ---------- objetos de la mochila ----------
def item(d, kind, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "tenis":
        R(1, 5, 6, 4, "white"); R(1, 8, 11, 2, "white"); R(1, 10, 11, 1, "red"); R(3, 6, 3, 1, "blue"); R(7, 7, 4, 1, "lgray")
    elif kind == "llaves":
        R(1, 1, 5, 5, "yellow"); R(2, 2, 3, 3, "black"); R(5, 3, 6, 2, "yellow"); R(8, 5, 1, 2, "yellow"); R(10, 5, 1, 2, "yellow")
        R(2, 7, 5, 4, "black"); R(3, 8, 3, 1, "red")
    elif kind == "sudadera":
        R(0, 3, 12, 3, "purple"); R(0, 6, 2, 6, "purple"); R(10, 6, 2, 6, "purple"); R(3, 5, 6, 7, "purple")
        R(0, 11, 2, 1, "pink"); R(10, 11, 2, 1, "pink"); R(2, 6, 1, 6, "black"); R(9, 6, 1, 6, "black")
        R(3, 0, 6, 4, "purple"); R(4, 1, 4, 3, "black")
        R(5, 4, 1, 2, "white"); R(7, 4, 1, 2, "white"); R(4, 9, 4, 2, "pink")
    elif kind == "clara":
        R(3, 1, 6, 10, "white"); R(0, 2, 3, 4, "white"); R(9, 2, 3, 4, "white"); R(5, 1, 2, 1, "lgray")
    elif kind == "tarjeta":
        R(0, 2, 12, 8, "lav"); R(0, 4, 12, 2, "black"); R(1, 7, 3, 2, "yellow"); R(6, 8, 5, 1, "white")
    elif kind == "celular":
        R(2, 0, 8, 12, "lgray"); R(3, 1, 6, 9, "black"); R(4, 2, 4, 7, "blue"); R(5, 0, 2, 1, "dgray"); R(5, 10, 2, 1, "dgray")
        R(4, 4, 1, 3, "green"); R(5, 6, 2, 1, "green"); R(4, 4, 2, 1, "green"); R(7, 6, 1, 1, "green")
    elif kind == "calavera":
        item2(d, "calavera", x, y, big)
    else:
        icon(d, kind, x, y, big)

INV = [(14.0, "tenis", "LÍNEA RECTA (NO ZIGZAG)"), (19.5, "llaves", "SIN LLAVES = VITRINA"), (24.5, "sudadera", "TAPA TU CARA"),
       (29.5, "clara", "MODO ANTI-METALERO"), (34.5, "tarjeta", "RASPAR, NO APRETAR"), (39.5, "celular", "EMERGENCIAS: 911")]

def n_items(v): return len([1 for it in INV if it[0] <= v])

def hud(d, items):
    rect(d, 0, 0, LW, 16, "black"); rect(d, 0, 15, LW, 1, "lgray")
    text(d, 6, 4, "MISIÓN 003", "orange", FONTM, center=False)
    s = f"INV {items}/6"; w = d.textlength(s, font=FONTM)
    text(d, LW - 6 - w, 4, s, "green" if items == 6 else "yellow", FONTM, center=False)

def inv_grid(d, v, t, y0=44):
    rect(d, 0, 16, LW, 246, "navy")
    for y in range(20, 260, 8): rect(d, 0, y, LW, 1, "black")
    text(d, LW / 2, y0 - 18, "MOCHILA  6 ESPACIOS", "white", FONTM)
    got = [it for it in INV if it[0] <= v]
    for i in range(6):
        x, y = 16 + (i % 3) * 52, y0 + (i // 3) * 52
        sel = bool(got) and i == len(got) - 1 and v - got[-1][0] < 0.9
        col = "yellow" if sel else "lgray"
        rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, col); rect(d, x, y + 43, 44, 1, col); rect(d, x, y, 1, 44, col); rect(d, x + 43, y, 1, 44, col)
        text(d, x + 5, y + 2, str(i + 1), "lav", FONT, center=False, shadow=None)
        if i < len(got): item(d, got[i][1], x + 10, y + 10, 2)
    if got and v - got[-1][0] < 2.5:
        popup(d, got[-1][2], 152, "green", "black")
    hero(d, 24, 190, scared=True, frame=int(t * 6) % 2)
    swarm(d, 120, 206, t, n=18, spread=16)
    backpack(d, 60, 202, 2, len(got))

CAPS = [
    (0.0, 6.0, "Misión 003: hoy decidiste cortar el pasto… y a 3 metros había un panal de abejas africanas."),
    (6.0, 10.0, "Para ellas, el ruido de la podadora es una declaración de guerra."),
    (10.0, 13.0, "Tienes una mochila con 6 espacios. ¡CORRE!"),
    (13.0, 19.0, "1: tenis. Corre en línea recta a un lugar cerrado. Nada de zigzag: no eres conejo."),
    (19.0, 24.0, "2: llaves del coche. Sin llaves, tu coche es una vitrina para verte sufrir."),
    (24.0, 29.0, "3: sudadera con capucha. Tápate la cara: ahí es donde más atacan."),
    (29.0, 34.0, "4: ropa clara. Lo oscuro les llama más la atención. Hoy no vas de metalero."),
    (34.0, 39.0, "5: tarjeta vieja. Raspa los aguijones rápido: siguen soltando veneno."),
    (39.0, 44.0, "6: celular. Muchas picaduras o te cuesta respirar: a emergencias, YA."),
    (44.0, 50.0, "¿Tirarte a la alberca? RECHAZADO: te esperan arriba y te pican al sacar la cabeza."),
    (50.0, 54.0, "¿Manotear como si bailaras? RECHAZADO. Solo las enojas más."),
    (54.0, 57.0, "¿Esconderte en los arbustos? GAME OVER."),
    (57.0, 62.0, "Dato que asusta: te pueden perseguir casi 400 metros."),
    (62.0, 68.0, "Misión: llegar al coche. Secundario: no volver a cortar el pasto sin revisar."),
    (68.0, 80.0, "¿Qué objeto cambiarías tú? Misión 004… próximamente."),
]

def frame(v, T=None, Tof=None):
    t = T if T is not None else v
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    shake = (0, 0); items = n_items(v)
    if v < 13.0:
        garden(d, t); house(d); tree(d)
        car(d, 50, GROUND - 33, t)
        if v < 10.0:
            hx = 112
            hero(d, hx, GROUND - 46, scared=v > 6.5, frame=int(t * 6) % 2)
            mower(d, hx + 26, GROUND - 17, hx + 22, GROUND - 28, t if v < 6.5 else 0)
            hive(d, 132, 146, t, shake=1.0 if v > 3.0 else 0.0)
            if v > 6.0:
                k = cl((v - 6.0) / 2.0)
                swarm(d, lerp(140, 128, k), lerp(160, 170, k), t, n=int(6 + 30 * k), spread=6 + 14 * k, angry=True)
            if 2.5 < v < 6.0 and int(t * 3) % 2 == 0: popup(d, "ALERTA: PANAL DETECTADO", 60, "white", "red")
            if v > 6.5: popup(d, "PELIGRO: ENJAMBRE", 60, "yellow", "black")
            if 6.0 < v < 6.4: shake = (random.randint(-2, 2), 0)
        else:
            k = cl((v - 10.0) / 3.0)
            hx = 112 - k * 40
            hive(d, 132, 146, t, 0.3)
            mower(d, 138, GROUND - 17, 160, GROUND - 14, 0)
            hero(d, hx, GROUND - 46, scared=True, frame=int(t * 8) % 2)
            swarm(d, hx + 44, GROUND - 40, t, n=36, spread=18, angry=True)
            popup(d, "¡CORRE!", 60, "white", "red", FONTB)
    elif v < 44.0:
        inv_grid(d, v, t)
    elif v < 50.0:
        lt = v - 44.0
        garden(d, t)
        rect(d, 8, 166, 164, 64, "white"); rect(d, 12, 170, 156, 56, "blue")
        for y in range(176, 224, 8):
            for x in range(16 + (y // 8) % 2 * 6, 164, 14): rect(d, x, y, 6, 1, "white")
        hy = 186 + int(math.sin(t * 2) * 3) if lt < 1.0 or int(t * 1.2) % 2 else 200
        if hy < 200:
            rect(d, 82, hy, 16, 14, "peach"); rect(d, 82, hy, 16, 4, "brown"); rect(d, 85, hy + 6, 2, 2, "black"); rect(d, 93, hy + 6, 2, 2, "black")
        else:
            for k in range(3): rect(d, 84 + k * 5, 198 - k % 2 * 2, 2, 2, "white")
        swarm(d, 90, 160, t, n=30, spread=24, angry=True)
        if lt > 1.2:
            popup(d, "RECHAZADO", 70, "white", "red", FONTB)
            popup(d, "TE ESPERAN ARRIBA", 96, "yellow", "black")
    elif v < 54.0:
        lt = v - 50.0
        garden(d, t); tree(d)
        hero(d, 70, GROUND - 46, scared=True, frame=int(t * 12) % 2)
        swarm(d, 82, GROUND - 40, t, n=26 + int(lt * 10), spread=22 + lt * 4, angry=True)
        if lt > 1.0:
            popup(d, "RECHAZADO", 70, "white", "red", FONTB)
            popup(d, "+100 ENOJO", 96, "yellow", "black")
    elif v < 57.0:
        lt = v - 54.0
        if lt < 1.4:
            garden(d, t); house(d)
            bush(d, 70, GROUND - 22, t, 1.0)
            rect(d, 84, GROUND - 6, 6, 6, "navy"); rect(d, 96, GROUND - 6, 6, 6, "navy")
            swarm(d, 98, GROUND - 40, t, n=30, spread=24, angry=True)
        else:
            rect(d, 0, 16, LW, 246, "black")
            item(d, "calavera", 66, 70, 4)
            text(d, LW / 2, 140, "GAME OVER", "red", FONTB)
            if int(t * 3) % 2 == 0: text(d, LW / 2, 170, "INSERTE ANTIALÉRGICO", "white", FONTM)
            if lt < 1.7: shake = (random.randint(-2, 2), 0)
    elif v < 62.0:
        lt = v - 57.0
        for y in range(16, 150, 4): rect(d, 0, y, LW, 4, "blue")
        rect(d, 0, 150, LW, GROUND - 150, "green")
        off = int(t * 90) % 24
        for x in range(-24, LW + 24, 24): rect(d, x + off, 190, 10, 30, "dgreen"); rect(d, x + off - 4, 182, 18, 10, "green")
        rect(d, 0, GROUND, LW, LH - GROUND, "dgray")
        for x in range(-16, LW + 16, 16): rect(d, x + off % 16, GROUND + 10, 8, 2, "yellow")
        hero(d, 50, GROUND - 46, scared=True, frame=int(t * 10) % 2)
        swarm(d, 104 + math.sin(t * 2) * 6, GROUND - 40, t, n=40, spread=24, angry=True)
        dist = int(400 * cl(lt / 4.0))
        rect(d, 30, 40, 120, 40, "black"); rect(d, 30, 40, 120, 1, "yellow"); rect(d, 30, 79, 120, 1, "yellow")
        text(d, LW / 2, 44, "DISTANCIA", "white", FONTM)
        text(d, LW / 2, 58, f"{dist} m", "yellow" if dist < 400 else "red", FONTB)
    elif v < 68.0:
        lt = v - 62.0
        garden(d, t); house(d); tree(d)
        if lt < 1.2:
            k = cl(lt / 1.2)
            car(d, 50, GROUND - 33, t)
            hero(d, lerp(120, 66, k), GROUND - 46, scared=True, frame=int(t * 10) % 2)
            swarm(d, lerp(160, 106, k), GROUND - 40, t, n=36, spread=20, angry=True)
        else:
            car(d, 50, GROUND - 33, t, inside=True, scared=False)
            rng = random.Random(5)
            for i in range(22):
                bx = 62 + rng.random() * 34 + math.sin(t * 9 + i) * 3
                by = GROUND - 30 + rng.random() * 12 + math.cos(t * 7 + i) * 2
                bee(d, bx, by, True)
            if lt < 1.5: shake = (random.randint(-1, 1), 0)
            popup(d, "MISIÓN CUMPLIDA", 50, "green", "black", FONTB)
            if lt > 2.0: popup(d, "OBJETIVO 2: REVISA", 82, "yellow", "black"); popup(d, "ANTES DE PODAR", 98, "yellow", "black")
    else:
        rect(d, 0, 16, LW, 246, "navy")
        text(d, LW / 2, 26, "MOCHILA  6/6", "white", FONTB)
        for i in range(6):
            x, y = 16 + (i % 3) * 52, 50 + (i // 3) * 52
            rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, "lgray"); rect(d, x, y + 43, 44, 1, "lgray"); rect(d, x, y, 1, 44, "lgray"); rect(d, x + 43, y, 1, 44, "lgray")
            item(d, INV[i][1], x + 10, y + 10, 2)
        text(d, LW / 2, 166, "¿QUÉ CAMBIARÍAS?", "yellow", FONTB)
        if int(t * 2) % 2 == 0: text(d, LW / 2, 190, "COMENTA ↓", "pink", FONTB)
        text(d, LW / 2, 222, "MISIÓN 004: PRÓXIMAMENTE", "green", FONTM)
        text(d, LW / 2, 240, "SÍGUEME: DATOS QUE ASUSTAN", "white", FONTM)
    hud(d, items)
    for cs, ce, s in CAPS:
        if cs <= v < ce:
            dialog(d, s, Tof(cs) if Tof else cs, t)
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
        sh.save("m003_prev.png"); sys.exit()
    from warp22 import v_of_T, T_of_v, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(v_of_T(i / FPS), i / FPS, T_of_v).tobytes())
    p.stdin.close(); p.wait()
