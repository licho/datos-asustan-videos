import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from pixel import P, rect, text, FONT, FONTB, LW, LH, SC
from alien import popup, dialog, FONTM, lerp, cl

FPS = 30

# ---------- objetos (12x12 lógicos) ----------
def obj(d, kind, x, y, big=2, t=0.0):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "agua":
        R(3, 2, 6, 10, "lgray"); R(4, 4, 4, 7, "blue"); R(4, 3, 4, 1, "white"); R(5, 5, 1, 4, "white")
    elif kind == "velas":
        R(4, 4, 4, 8, "white"); R(4, 11, 4, 1, "lgray"); R(6, 3, 1, 1, "black")
        fl = int(t * 8) % 2
        R(5 - fl, 0, 3, 3, "yellow"); R(6 - fl, 1, 1, 2, "orange")
    elif kind == "cempasuchil":
        R(4, 8, 5, 4, "brown"); R(4, 8, 5, 1, "orange")
        R(5, 4, 1, 4, "dgreen"); R(7, 4, 1, 4, "dgreen")
        for a, b in [(1, 2), (5, 0), (8, 2)]:
            R(a, b, 4, 4, "orange"); R(a + 1, b + 1, 2, 2, "yellow")
    elif kind == "sal":
        R(4, 1, 4, 3, "lgray"); R(5, 0, 1, 1, "dgray"); R(3, 4, 6, 8, "white"); R(4, 6, 4, 4, "lgray")
    elif kind == "copal":
        R(1, 8, 10, 4, "brown"); R(2, 7, 8, 1, "orange"); R(4, 6, 4, 1, "red")
    elif kind == "papel":
        R(0, 0, 12, 1, "lgray"); R(1, 1, 10, 10, "pink"); R(3, 3, 2, 2, "black"); R(7, 3, 2, 2, "black"); R(5, 6, 2, 2, "black")
        for k in range(5): R(1 + k * 2, 11, 1, 1, "pink")
    elif kind == "foto":
        R(1, 0, 10, 12, "brown"); R(2, 1, 8, 10, "lav"); R(4, 3, 4, 4, "peach"); R(4, 2, 4, 2, "white")
        R(4, 4, 1, 1, "black"); R(7, 4, 1, 1, "black"); R(4, 6, 4, 1, "white"); R(3, 8, 6, 3, "navy")
    elif kind == "comida":
        R(0, 9, 12, 3, "white"); R(1, 6, 10, 3, "brown"); R(2, 5, 6, 1, "brown"); R(3, 6, 1, 1, "white"); R(7, 7, 1, 1, "white"); R(9, 6, 1, 1, "white")
    elif kind == "pan":
        R(3, 4, 6, 1, "orange"); R(2, 5, 8, 2, "orange"); R(1, 7, 10, 5, "orange")
        R(5, 2, 2, 2, "brown"); R(2, 6, 2, 1, "brown"); R(4, 7, 1, 1, "brown"); R(7, 7, 1, 1, "brown"); R(8, 6, 2, 1, "brown")
        R(3, 9, 1, 1, "white"); R(6, 10, 1, 1, "white"); R(9, 9, 1, 1, "white"); R(1, 11, 10, 1, "brown")
    elif kind == "energetica":
        R(4, 0, 4, 1, "lgray"); R(3, 1, 6, 11, "green"); R(3, 4, 6, 5, "black"); R(6, 4, 2, 2, "yellow"); R(5, 6, 2, 2, "yellow")
    elif kind == "gps":
        R(3, 0, 6, 12, "black"); R(4, 1, 4, 9, "green"); R(4, 4, 4, 1, "white"); R(6, 6, 1, 3, "white"); R(5, 2, 2, 2, "red")
    elif kind == "ensalada":
        R(1, 7, 10, 4, "white"); R(2, 11, 8, 1, "lgray"); R(2, 4, 8, 3, "green"); R(3, 3, 3, 2, "dgreen"); R(7, 4, 2, 2, "red"); R(5, 5, 2, 1, "orange")
    elif kind == "wifi":
        R(0, 0, 12, 12, "white"); R(1, 1, 10, 10, "lgray")
        R(2, 3, 8, 1, "blue"); R(3, 5, 6, 1, "blue"); R(4, 7, 4, 1, "blue"); R(5, 9, 2, 2, "blue")

def soul(d, x, y, t, s=1.0):
    y = y + math.sin(t * 3) * 2 * s
    r = 8 * s
    d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=P["lav"])
    d.ellipse([x - r, y - r, x + r, y + r], fill=P["white"])
    if s >= 0.8:
        rect(d, x - 10, y - 8, 20, 2, "yellow"); rect(d, x - 5, y - 13, 10, 5, "yellow"); rect(d, x - 5, y - 10, 10, 1, "red")
        rect(d, x - 4, y - 2, 2, 3, "black"); rect(d, x + 2, y - 2, 2, 3, "black"); rect(d, x - 2, y + 3, 4, 1, "black")
        for k in range(3):
            rect(d, x - 3 + k * 2, y + r + 1 + (k + int(t * 6)) % 3, 2, 2, "lav")

# ---------- catálogo (v_mostrar, v_decidir, tipo, nombre, aceptado, etiqueta) ----------
CAT = [
    (10.0, 12.0, "agua", "AGUA", True, "QUITA LA SED"),
    (15.0, 17.0, "energetica", "BEBIDA ENERGÉTICA", False, "NO ES CARRERA"),
    (20.0, 21.0, "velas", "VELAS", True, "LUZ DEL CAMINO"),
    (22.5, 23.5, "cempasuchil", "CEMPASÚCHIL", True, "GPS ACTIVADO"),
    (26.0, 27.0, "gps", "GPS DE VERDAD", False, "YA SE PERDIÓ UNA VEZ"),
    (31.0, 32.0, "sal", "SAL", True, "PURIFICA"),
    (33.5, 34.5, "copal", "COPAL", True, "LIMPIA EL LUGAR"),
    (36.0, 37.0, "papel", "PAPEL PICADO", True, "VIENTO + FIESTA"),
    (40.0, 41.0, "foto", "SU FOTO", True, "ES PARA ÉL"),
    (42.5, 43.3, "comida", "SU COMIDA FAVORITA", True, "MOLE ✓"),
    (44.5, 45.2, "pan", "PAN DE MUERTO", True, "ESENCIAL"),
    (46.0, 47.0, "ensalada", "ENSALADA", False, "NI EN VIDA"),
    (51.0, 52.0, "wifi", "CONTRASEÑA WIFI", False, "VIENE A VISITARTE"),
]
OKS = [c for c in CAT if c[4]]
POS = {"agua": [(36, 161)], "comida": [(62, 161)], "pan": [(94, 161)], "sal": [(124, 161)],
       "foto": [(78, 126)], "velas": [(50, 126), (106, 126)], "cempasuchil": [(44, 196), (112, 196)], "copal": [(14, 196)]}

def accepted(v): return [c for c in OKS if c[1] <= v]

def room(d, t):
    for y in range(16, 250, 4):
        rect(d, 0, y, LW, 4, "navy" if (y // 4) % 2 else "black")
    rect(d, 0, 250, LW, 12, "brown")
    for x in range(0, LW, 10): rect(d, x, 250, 1, 12, "black")

def altar(d):
    for (x0, x1, y0, y1) in [(50, 130, 150, 185), (32, 148, 185, 220), (14, 166, 220, 250)]:
        rect(d, x0, y0, x1 - x0, y1 - y0, "purple"); rect(d, x0, y0, x1 - x0, 2, "white")
        for x in range(x0 + 2, x1 - 2, 6): rect(d, x, y0 + 2, 3, 2, "pink")
        rect(d, x0, y0, 1, y1 - y0, "black"); rect(d, x1 - 1, y0, 1, y1 - y0, "black")

def altar_items(d, v, t):
    acc = accepted(v)
    kinds = [c[2] for c in acc]
    for c in acc:
        k = c[2]
        if k == "papel":
            rect(d, 0, 114, LW, 1, "lgray")
            cols = ["pink", "orange", "green", "yellow", "blue", "red"]
            for i, x in enumerate(range(4, LW - 10, 20)):
                sway = int(math.sin(t * 3 + i) * 1.5)
                rect(d, x + sway, 115, 14, 10, cols[i % 6]); rect(d, x + 4 + sway, 117, 2, 2, "black"); rect(d, x + 8 + sway, 117, 2, 2, "black"); rect(d, x + 6 + sway, 120, 2, 2, "black")
            continue
        pop = cl((v - c[1]) / 0.3)
        for (x, y) in POS[k]:
            obj(d, k, x, y - int((1 - pop) * 8), 2, t)
        if k == "copal":
            for j in range(6):
                ph = (t * 0.6 + j / 6) % 1
                rect(d, 24 - ph * 14 + math.sin(ph * 9 + j) * 2, 194 - ph * 50, 3, 3, "lgray" if j % 2 else "dgray")
    if "cempasuchil" in kinds:
        for x in range(72, 110, 5): rect(d, x, 216 + (x // 5) % 2 * 2, 3, 2, "orange")
        for x in range(150, LW, 5): rect(d, x, 252 + (x // 5) % 3 * 3, 3, 2, "orange")
        for x in range(0, 14, 4): pass

def panel(d, v, t):
    rect(d, 6, 20, 168, 92, "black")
    for (a, b, w, h) in [(6, 20, 168, 1), (6, 111, 168, 1), (6, 20, 1, 92), (173, 20, 1, 92)]: rect(d, a, b, w, h, "lav")
    rect(d, 6, 20, 168, 12, "purple"); text(d, LW / 2, 22, "CATÁLOGO DE OFRENDA", "yellow", FONTM)
    cur = [c for c in CAT if c[0] <= v]
    if not cur:
        text(d, LW / 2, 46, "ELIGE BIEN:", "white", FONTM)
        text(d, LW / 2, 60, "CADA OBJETO TIENE", "white", FONTM)
        text(d, LW / 2, 72, "UNA MISIÓN", "green", FONTM)
        if int(t * 3) % 2 == 0: text(d, LW / 2, 86, "▶ PRESIONA START", "pink", FONT)
        return
    vs, vd, k, name, ok, tag = cur[-1]
    if int(t * 3) % 2 == 0: text(d, 22, 50, "<", "pink", FONTB); text(d, 158, 50, ">", "pink", FONTB)
    rect(d, 70, 34, 40, 40, "navy")
    obj(d, k, 72, 36, 3, t)
    text(d, LW / 2, 76, name, "white", FONTM)
    if v >= vd:
        if ok:
            text(d, LW / 2, 92, "✓ " + tag, "green", FONTM)
        else:
            for j in range(36):
                rect(d, 72 + j, 36 + j, 2, 2, "red"); rect(d, 106 - j, 36 + j, 2, 2, "red")
            rect(d, 44, 88, 92, 12, "red"); text(d, LW / 2, 89, "RECHAZADO", "white", FONTM)
            text(d, LW / 2, 100, tag, "yellow", FONTM)
    else:
        text(d, LW / 2, 92, "COSTO: CARIÑO", "lav", FONT)

def hud(d, v):
    n = len(accepted(v)); pct = round(100 * n / len(OKS))
    rect(d, 0, 0, LW, 16, "black"); rect(d, 0, 15, LW, 1, "lgray")
    text(d, 5, 4, "MISIÓN ESPECIAL", "orange", FONTM, center=False)
    s = f"BRILLO {pct}%"; w = d.textlength(s, font=FONTM)
    text(d, LW - 5 - w, 4, s, "green" if pct == 100 else "yellow", FONTM, center=False)

CAPS = [
    (0.0, 5.0, "Misión especial: Día de Muertos. Tu abuelito viene de visita… y la ofrenda está vacía."),
    (5.0, 10.0, "Abre el catálogo. Elige bien: cada objeto tiene una misión."),
    (10.0, 15.0, "Primero: agua. Viene de un viaje larguísimo y llega con sed."),
    (15.0, 20.0, "¿Bebida energética para que llegue más rápido? RECHAZADO."),
    (20.0, 26.0, "Velas: su luz. Cempasúchil: su color y aroma lo guían. Es su GPS."),
    (26.0, 31.0, "¿Un GPS de verdad? RECHAZADO. Ya se perdió una vez en vida por usarlo."),
    (31.0, 36.0, "Sal, para purificar. Copal, para limpiar el lugar con su humo."),
    (36.0, 40.0, "Papel picado: representa el viento y le pone fiesta."),
    (40.0, 46.0, "Su foto, para que sepa que es para él. Su comida favorita… y su pan de muerto."),
    (46.0, 51.0, "¿Ensalada? RECHAZADO. Si en vida no la comía, ahora menos."),
    (51.0, 55.0, "¿La contraseña del WiFi? RECHAZADO. Viene a visitarte, no a ver videos."),
    (55.0, 61.0, "Ofrenda completa. El alma llega, huele el pan… y sonríe."),
    (61.0, 70.0, "¿Qué le pondrías tú a la ofrenda de alguien que extrañas?"),
]

def frame(v, T=None, Tof=None):
    t = T if T is not None else v
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    room(d, t); altar(d); altar_items(d, v, t)
    if v < 5.0:
        rect(d, 122, 24, 50, 56, "brown"); rect(d, 125, 27, 44, 50, "navy")
        rng = random.Random(3)
        for i in range(14): d.point((rng.randint(126, 167), rng.randint(28, 75)), fill=P["white"])
        soul(d, lerp(160, 140, v / 5), 60, t, 0.35)
        rect(d, 146, 27, 2, 50, "brown"); rect(d, 125, 51, 44, 2, "brown")
        popup(d, "VISITA EN CAMINO", 84, "yellow", "purple")
        if v > 2.0: popup(d, "OFRENDA: VACÍA", 104, "white", "red")
    elif v < 55.0:
        panel(d, v, t)
    else:
        lt = v - 55.0
        if lt < 2.5:
            sx, sy = lerp(200, 160, cl(lt / 2.5)), 238
        else:
            k = cl((lt - 2.5) / 1.5); sx, sy = 160, lerp(238, 148, k)
        if lt > 2.8:
            for j in range(5):
                ph = (t * 0.8 + j / 5) % 1
                rect(d, lerp(106, sx - 6, ph), lerp(158, sy, ph) + math.sin(ph * 8 + j) * 3, 2, 2, "peach")
        soul(d, sx, sy, t)
        if lt > 4.0:
            for j in range(4):
                ph = (t * 0.7 + j / 4) % 1
                hx, hy = sx - 14 + j * 9, sy - 18 - ph * 40
                rect(d, hx, hy, 2, 2, "red"); rect(d, hx + 3, hy, 2, 2, "red"); rect(d, hx, hy + 2, 5, 2, "red"); rect(d, hx + 1, hy + 4, 3, 1, "red")
        if v < 61.0:
            popup(d, "OFRENDA COMPLETA", 26, "yellow", "purple", FONTM)
            if lt > 0.6: popup(d, "BRILLO 100%", 46, "green", "black")
        else:
            rect(d, 6, 20, 168, 64, "black")
            for (a, b, w, h) in [(6, 20, 168, 1), (6, 83, 168, 1), (6, 20, 1, 64), (173, 20, 1, 64)]: rect(d, a, b, w, h, "lav")
            text(d, LW / 2, 24, "¿QUÉ LE PONDRÍAS TÚ?", "yellow", FONTM)
            if int(t * 2) % 2 == 0: text(d, LW / 2, 42, "COMENTA ↓", "pink", FONTB)
            text(d, LW / 2, 66, "SÍGUEME: DATOS QUE ASUSTAN", "white", FONT)
    hud(d, v)
    for cs, ce, s in CAPS:
        if cs <= v < ce:
            dialog(d, s, Tof(cs) if Tof else cs, t)
    big = img.resize((LW * SC, LH * SC), Image.NEAREST)
    arr = np.asarray(big).copy()
    arr[::SC, :, :] = (arr[::SC, :, :] * 0.82).astype(np.uint8)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        ims = [Image.fromarray(frame(float(x))).resize((270, 480), Image.NEAREST) for x in sys.argv[2:]]
        cols = min(6, len(ims)); rows = (len(ims) + 5) // 6
        sh = Image.new("RGB", (270 * cols, 480 * rows))
        for i, im in enumerate(ims): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sh.save("ofr_prev.png"); sys.exit()
    from warp21 import v_of_T, T_of_v, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(v_of_T(i / FPS), i / FPS, T_of_v).tobytes())
    p.stdin.close(); p.wait()
