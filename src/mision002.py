import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from pixel import P, rect, text, FONT, FONTB, hero, LW, LH, SC
from alien import icon, popup, dialog, backpack, FONTM, GROUND, lerp, cl

def hero(d, x, y, scared=False, frame=0, big=2):
    parts = [(2, 0, 8, 8, "peach"), (2, 0, 8, 3, "brown"), (1, 8, 10, 9, "blue"), (2, 17, 3, 6, "navy"), (7, 17, 3, 6, "navy")]
    if scared: parts += [(-2, 4 - frame, 3, 3, "peach"), (11, 4 - frame, 3, 3, "peach")]
    for a, b, w, h, c in parts:
        rect(d, x + a * big - 2, y + b * big - 2, w * big + 4, h * big + 4, "black")
    for a, b, w, h, c in parts:
        rect(d, x + a * big, y + b * big, w * big, h * big, c)
    rect(d, x + 2 * big, y + 2 * big, 8 * big, 1 * big, "white")   # cinta del sombrero/gorra
    rect(d, x + 4 * big, y + 4 * big, 1 * big, (1 + scared) * big, "black"); rect(d, x + 7 * big, y + 4 * big, 1 * big, (1 + scared) * big, "black")

FPS = 30

def desert(d, t, noon=False):
    for y in range(16, GROUND, 4):
        rect(d, 0, y, LW, 4, ("orange" if y < 120 else "yellow") if noon else ("blue" if y < 110 else "peach"))
    sx, sy = (120, 30) if noon else (140, 40)
    d.ellipse([sx, sy, sx + 26, sy + 26], fill=P["white" if noon else "yellow"])
    rect(d, 0, GROUND - 30, LW, 30, "orange")
    for x0, h in [(0, 22), (40, 34), (100, 18), (140, 28)]:
        d.polygon([(x0, GROUND - 30), (x0 + 20, GROUND - 30 - h), (x0 + 40, GROUND - 30)], fill=P["brown"])
    rect(d, 0, GROUND, LW, LH - GROUND, "peach")
    for k in range(4):
        y = GROUND + 6 + k * 6
        for x in range(0, LW, 6):
            if (x // 6 + k + int(t * 6)) % 5 == 0: d.point((x, y), fill=P["orange"])

def cactus(d, x, y, s=1):
    R = lambda a, b, w, h: rect(d, x + a * s, y + b * s, w * s, h * s, "dgreen")
    R(4, 0, 4, 24); R(0, 8, 4, 2); R(0, 4, 2, 6); R(8, 10, 4, 2); R(10, 6, 2, 6)

def car(d, x, y, t):
    rect(d, x + 6, y, 26, 8, "red"); rect(d, x, y + 7, 40, 10, "red")
    rect(d, x + 9, y + 2, 8, 5, "blue"); rect(d, x + 20, y + 2, 9, 5, "blue")
    rect(d, x + 4, y + 16, 8, 6, "black"); rect(d, x + 28, y + 16, 8, 6, "black")
    for k in range(4):
        ph = (t * 1.2 + k * 0.25) % 1
        r = 2 + ph * 6
        cx, cy = x + 36 + ph * 6, y + 4 - ph * 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=P["lgray" if k % 2 else "dgray"])

def heli(d, x, y, t):
    # va hacia la derecha: cabina adelante (derecha), cola atrás (izquierda)
    rect(d, x + 16, y, 22, 9, "dgreen"); rect(d, x + 28, y + 2, 7, 4, "blue"); rect(d, x, y + 3, 16, 3, "dgreen")
    rect(d, x - 1, y, 3, 8, "dgreen"); rect(d, x + 18, y + 10, 16, 2, "black")
    w = 16 if int(t * 12) % 2 else 10
    rect(d, x + 27 - w, y - 3, w * 2, 2, "black")

def item(d, kind, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "sombrero":
        R(0, 7, 12, 2, "brown"); R(3, 2, 6, 5, "brown"); R(3, 5, 6, 1, "red")
    elif kind == "camisa":
        R(3, 1, 6, 10, "blue"); R(0, 2, 3, 8, "blue"); R(9, 2, 3, 8, "blue"); R(5, 1, 2, 2, "white")
    elif kind == "espejo":
        R(2, 1, 8, 10, "lgray"); R(3, 2, 6, 8, "white"); R(4, 3, 2, 3, "blue")
    elif kind == "silbato":
        R(1, 4, 8, 5, "orange"); R(9, 5, 3, 2, "orange"); R(3, 5, 2, 2, "black"); R(0, 2, 2, 2, "lgray")
    elif kind == "orina":
        R(4, 0, 4, 2, "lgray"); R(3, 2, 6, 10, "yellow"); R(4, 4, 1, 6, "white")
    elif kind == "calavera":
        R(2, 1, 8, 7, "white"); R(3, 3, 2, 2, "black"); R(7, 3, 2, 2, "black"); R(4, 8, 4, 3, "white"); R(5, 9, 1, 2, "black")
    else:
        icon(d, kind, x, y, big)

INV = [(10.5, "agua", "AGUA: ¡TÓMALA!"), (13.5, "sombrero", "TU CABEZA ≠ COMAL"), (15.5, "camisa", "MODO ANTI-CHICHARRÓN"),
       (18.5, "espejo", "+SEÑALES (NO SELFIES)"), (21.5, "linterna", "CAMINA DE NOCHE"), (25.0, "silbato", "GRITAR CANSA")]

def n_items(t): return len([1 for it in INV if it[0] <= t])

def hud(d, items):
    rect(d, 0, 0, LW, 16, "black"); rect(d, 0, 15, LW, 1, "lgray")
    text(d, 6, 4, "MISIÓN 002", "orange", FONTM, center=False)
    text(d, 120, 4, f"INV {items}/6", "green" if items == 6 else "yellow", FONTM, center=False)

def inv_grid(d, t, y0=44):
    rect(d, 0, 16, LW, GROUND - 16 + 26, "navy")
    for y in range(20, 260, 8): rect(d, 0, y, LW, 1, "black")
    text(d, LW / 2, y0 - 18, "MOCHILA  6 ESPACIOS", "white", FONTM)
    got = [it for it in INV if it[0] <= t]
    for i in range(6):
        x, y = 16 + (i % 3) * 52, y0 + (i // 3) * 52
        sel = bool(got) and i == len(got) - 1 and t - got[-1][0] < 0.9
        col = "yellow" if sel else "lgray"
        rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, col); rect(d, x, y + 43, 44, 1, col); rect(d, x, y, 1, 44, col); rect(d, x + 43, y, 1, 44, col)
        text(d, x + 5, y + 2, str(i + 1), "lav", FONT, center=False, shadow=None)
        if i < len(got): item(d, got[i][1], x + 10, y + 10, 2)
        if i == 3 and i < len(got) and 18.5 < t < 21.5 and int(t * 6) % 2 == 0:
            for k in range(3): rect(d, x + 30 + k * 4, y + 6 - k * 3, 6, 2, "white")
    if got and t - got[-1][0] < 1.8:
        popup(d, got[-1][2], 152, "green", "black")
    hero(d, 24, 184); backpack(d, 128, 194, 2, len(got))

CAPS = [
    (0.0, 3.0, "Misión 002: tu coche se descompuso en medio del desierto."),
    (3.0, 5.0, "6 espacios, cero señal… y agua tibia que sabe a plástico."),
    (5.0, 7.5, "Regla de oro: NO te alejes del coche."),
    (7.5, 10.0, "Desde arriba, tú pareces un cactus con ansiedad."),
    (10.0, 13.0, "1: agua. Y tómatela. Racionarla hasta desmayarte es drama."),
    (13.0, 15.0, "2: sombrero. Tu cabeza no es un comal."),
    (15.0, 18.0, "3: manga larga, aunque haga 45 grados. Cero bronceado chicharrón."),
    (18.0, 21.0, "4: espejo para señales. Por fin sirve para algo más que selfies."),
    (21.0, 24.5, "5: linterna. Camina de noche o temprano, nunca al mediodía."),
    (24.5, 28.0, "6: silbato. Gritar cansa. El silbato no."),
    (28.0, 32.0, "¿Tomar tu orina? RECHAZADO: mito de película. Deshidrata más."),
    (32.0, 35.0, "¿Caminar al mediodía buscando \"un atajo\"? GAME OVER."),
    (35.0, 39.0, "Misión: sobrevivir. Secundario: no ser el ejemplo de lo que no hay que hacer."),
    (39.0, 46.0, "¿Qué objeto cambiarías tú? Misión 003… próximamente."),
]

def frame(t, T=None, Tof=None):
    if T is None: T = t
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    shake = (0, 0); items = n_items(t)
    if t < 5.0:
        desert(d, t)
        cactus(d, 10, GROUND - 24); cactus(d, 156, GROUND - 26)
        car(d, 92, GROUND - 22, t)
        hero(d, 30, GROUND - 46, scared=t > 1.0, frame=int(t * 6) % 2)
        if t < 3.0:
            if int(t * 3) % 2 == 0: popup(d, "ALERTA: COCHE DESCOMPUESTO", 60, "white", "red")
            popup(d, "PELIGRO: 45 °C", 82, "yellow", "black")
        else:
            popup(d, "SEÑAL: 0 BARRAS", 60, "white", "black")
            item(d, "agua", 64, GROUND - 24, 2)
            text(d, 78, GROUND - 36, "TIBIA", "orange", FONTM)
        if t < 0.4: shake = (random.randint(-2, 2), random.randint(-2, 2))
    elif t < 10.0:
        lt = t - 5.0
        desert(d, t)
        car(d, 30, GROUND - 22, t)
        hx = int(lerp(20, 145, cl((lt - 0.5) / 4.0)))
        heli(d, int(lerp(-40, 120, cl(lt / 5.0))), 40, t)
        if lt < 2.5:
            popup(d, "NO TE ALEJES DEL COCHE", 90, "white", "red")
            hero(d, 92, GROUND - 46, frame=0)
        else:
            cactus(d, 100, GROUND - 26); cactus(d, 152, GROUND - 24)
            hero(d, 124, GROUND - 46, scared=True, frame=int(t * 6) % 2)
            text(d, 50, 64, "COCHE: VISTO ✓", "green", FONTM)
            text(d, 134, GROUND - 64, "¿CACTUS?", "pink", FONTM)
    elif t < 28.0:
        inv_grid(d, t)
    elif t < 32.0:
        lt = t - 28.0
        rect(d, 0, 16, LW, 246, "navy")
        rect(d, 60, 70, 60, 60, "black"); rect(d, 60, 70, 60, 1, "red"); rect(d, 60, 129, 60, 1, "red"); rect(d, 60, 70, 1, 60, "red"); rect(d, 119, 70, 1, 60, "red")
        item(d, "orina", 72, 82, 3)
        if lt > 0.8:
            for k in range(54): rect(d, 63 + k, 73 + k, 3, 3, "red"); rect(d, 114 - k, 73 + k, 3, 3, "red")
            popup(d, "RECHAZADO", 150, "white", "red", FONTB)
            popup(d, "MITO DE PELÍCULA", 178, "yellow", "black")
    elif t < 35.0:
        lt = t - 32.0
        desert(d, t, noon=True)
        hx = int(lerp(20, 90, cl(lt / 1.5)))
        if lt < 1.5:
            hero(d, hx, GROUND - 46, scared=True, frame=int(t * 6) % 2)
            text(d, LW / 2, 70, "\"UN ATAJO\"", "black", FONTB, shadow=None)
        else:
            rect(d, 0, 16, LW, 246, "black")
            item(d, "calavera", 66, 80, 4)
            text(d, LW / 2, 150, "GAME OVER", "red", FONTB)
            if int(t * 3) % 2 == 0: text(d, LW / 2, 180, "INSERTE AGUA", "white", FONTM)
            if 1.5 < lt < 1.9: shake = (random.randint(-2, 2), 0)
    elif t < 39.0:
        lt = t - 35.0
        desert(d, t)
        car(d, 8, GROUND - 22, t)
        hero(d, 84, GROUND - 46); backpack(d, 108, GROUND - 32, 1, 6, closed=True)
        popup(d, "MISIÓN: SOBREVIVIR", 50, "green", "black", FONTB)
        if lt > 1.2: popup(d, "OBJETIVO 2: NO SER", 82, "yellow", "black"); popup(d, "EL MAL EJEMPLO", 98, "yellow", "black")
    else:
        rect(d, 0, 16, LW, 246, "navy")
        text(d, LW / 2, 26, "MOCHILA  6/6", "white", FONTB)
        for i in range(6):
            x, y = 16 + (i % 3) * 52, 50 + (i // 3) * 52
            rect(d, x, y, 44, 44, "black"); rect(d, x, y, 44, 1, "lgray"); rect(d, x, y + 43, 44, 1, "lgray"); rect(d, x, y, 1, 44, "lgray"); rect(d, x + 43, y, 1, 44, "lgray")
            item(d, INV[i][1], x + 10, y + 10, 2)
        text(d, LW / 2, 166, "¿QUÉ CAMBIARÍAS?", "yellow", FONTB)
        if int(t * 2) % 2 == 0: text(d, LW / 2, 190, "COMENTA ↓", "pink", FONTB)
        text(d, LW / 2, 222, "MISIÓN 003: PRÓXIMAMENTE", "green", FONTM)
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
        sh.save("m002_prev.png"); sys.exit()
    from warp20 import v_of_T, T_of_v, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(min(45.99, v_of_T(i / FPS)), i / FPS, T_of_v).tobytes())
    p.stdin.close(); p.wait()
