import math, random, subprocess, sys, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pixel import P, rect, text, FONT, FONTB, hero, LW, LH, SC

FPS = 30
FONTM = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 10)
GROUND = 236

def lerp(a, b, t): return a + (b - a) * t
def cl(x): return max(0.0, min(1.0, x))

# ---------- backgrounds ----------
def city(d, t, alarm=True):
    red = alarm and int(t * 3) % 2 == 0
    for y in range(16, GROUND, 4):
        rect(d, 0, y, LW, 4, ("purple" if red else "navy") if y < 140 else ("red" if red and y > 190 else "purple"))
    rng = random.Random(4)
    for i in range(30):
        d.point((rng.randint(0, LW - 1), rng.randint(18, 110)), fill=P["white"])
    for x0, w, h in [(0, 30, 70), (28, 26, 100), (52, 34, 60), (84, 24, 120), (106, 34, 80), (138, 42, 95)]:
        rect(d, x0, GROUND - h, w, h, "black")
        for wy in range(GROUND - h + 6, GROUND - 6, 10):
            for wx in range(x0 + 4, x0 + w - 4, 7):
                if rng.random() < 0.4: rect(d, wx, wy, 3, 4, "yellow" if rng.random() < 0.8 else "orange")
    rect(d, 0, GROUND, LW, LH - GROUND, "dgray")
    for x in range(0, LW, 16): rect(d, x, GROUND + 14, 8, 2, "yellow")

def ufo(d, x, y, big=1, t=0, beam=False, beam_h=120):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if beam:
        for k in range(beam_h):
            w = 8 + k * 0.35
            if (k + int(t * 20)) % 6 < 4:
                rect(d, x + 14 * big - w / 2, y + 10 * big + k, w, 1, "green")
    R(9, 0, 10, 5, "blue"); R(11, 1, 3, 2, "white")
    R(2, 5, 24, 4, "lgray"); R(0, 7, 28, 3, "dgray")
    for k in range(5):
        on = (k + int(t * 8)) % 5 == 0
        R(2 + k * 5, 8, 2, 1, "yellow" if on else "orange")

def alien(d, x, y, big=2, t=0):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    R(2, 0, 8, 7, "green"); R(3, 2, 2, 3, "black"); R(7, 2, 2, 3, "black")
    R(5, -3, 1, 3, "green"); R(5, -4, 1, 1, "yellow")
    R(4, 7, 4, 6, "green"); R(1, 8, 3, 1, "green"); R(8, 8, 3, 1, "green")
    R(4, 13, 1, 4, "green"); R(7, 13, 1, 4, "green")

def backpack(d, x, y, big=2, fill=0, closed=False):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    R(1, 2, 12, 14, "dgreen"); R(3, 0, 8, 3, "dgreen"); R(4, 1, 6, 1, "black")
    R(3, 8, 8, 6, "green")
    if not closed:
        R(1, 2, 12, 2, "black")
        for k in range(min(fill, 5)):
            R(2 + k * 2, 1 - (k % 2), 2, 2, ["blue", "orange", "red", "yellow", "white"][k])
    else:
        R(1, 2, 12, 1, "yellow")

# ---------- item icons (12x12 logical) ----------
def icon(d, kind, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    if kind == "agua":
        R(5, 0, 2, 2, "blue"); R(4, 2, 4, 1, "white"); R(3, 3, 6, 9, "blue"); R(4, 4, 1, 6, "white"); R(3, 6, 6, 2, "white")
    elif kind == "comida":
        R(2, 2, 8, 9, "lgray"); R(2, 2, 8, 1, "white"); R(2, 5, 8, 4, "red"); R(4, 6, 4, 2, "yellow")
    elif kind == "linterna":
        R(1, 4, 7, 4, "dgray"); R(8, 3, 3, 6, "lgray"); R(11, 2, 1, 8, "yellow"); R(3, 5, 2, 1, "red")
    elif kind == "baterias":
        for k in (0, 6): R(1 + k, 2, 4, 9, "orange"); R(1 + k, 2, 4, 3, "black"); R(2 + k, 1, 2, 1, "lgray")
    elif kind == "botiquin":
        R(1, 3, 10, 8, "white"); R(4, 1, 4, 2, "lgray"); R(5, 4, 2, 6, "red"); R(3, 6, 6, 2, "red")
    elif kind == "medicinas":
        R(3, 1, 6, 2, "white"); R(3, 3, 6, 9, "orange"); R(4, 6, 4, 3, "white")
    elif kind == "radio":
        R(1, 4, 10, 7, "dgray"); R(2, 6, 4, 4, "black"); R(7, 6, 3, 1, "yellow"); R(7, 8, 3, 1, "lgray"); R(9, 0, 1, 4, "lgray")
    elif kind == "documentos":
        R(1, 1, 10, 11, "lav"); R(2, 2, 8, 9, "white"); R(3, 4, 6, 1, "dgray"); R(3, 6, 6, 1, "dgray"); R(3, 8, 4, 1, "dgray")
    elif kind == "efectivo":
        R(0, 3, 12, 7, "dgreen"); R(1, 4, 10, 5, "green"); R(5, 5, 2, 3, "dgreen")
    elif kind == "cargador":
        R(2, 1, 8, 11, "black"); R(3, 2, 6, 8, "dgray"); R(4, 4, 4, 1, "green"); R(4, 6, 4, 1, "green"); R(5, 10, 2, 1, "lgray")
    elif kind == "celular":
        R(3, 0, 6, 12, "black"); R(4, 1, 4, 10, "navy")
    elif kind == "arma":
        R(1, 4, 9, 3, "lav"); R(10, 5, 2, 1, "green"); R(2, 7, 3, 4, "purple"); R(4, 3, 2, 1, "green")
    elif kind == "detector":
        R(3, 0, 6, 8, "lgray"); R(4, 1, 4, 4, "green"); R(5, 8, 2, 4, "dgray"); R(5, 2, 1, 1, "red")
    elif kind == "sombrero":
        d.polygon([(x + 6 * big, y), (x, y + 10 * big), (x + 12 * big, y + 10 * big)], fill=P["lgray"])
        R(5, 3, 1, 5, "white"); R(0, 10, 12, 2, "white")
    elif kind == "figuras":
        R(3, 0, 6, 6, "peach"); R(4, 2, 1, 1, "black"); R(7, 2, 1, 1, "black"); R(4, 6, 4, 6, "blue"); R(2, 11, 8, 1, "lgray")

def slot(d, x, y, kind=None, sel=False, cross=False, sz=30):
    rect(d, x, y, sz, sz, "black"); rect(d, x, y, sz, 1, "pink" if sel else "lgray"); rect(d, x, y + sz - 1, sz, 1, "pink" if sel else "lgray")
    rect(d, x, y, 1, sz, "pink" if sel else "lgray"); rect(d, x + sz - 1, y, 1, sz, "pink" if sel else "lgray")
    if kind: icon(d, kind, x + 3, y + 3, 2)
    if cross:
        for k in range(sz - 4):
            rect(d, x + 2 + k, y + 2 + k, 2, 2, "red"); rect(d, x + sz - 4 - k, y + 2 + k, 2, 2, "red")

def popup(d, s, y, c="yellow", bg="purple", font=FONTM):
    w = d.textlength(s, font=font) + 10
    rect(d, LW / 2 - w / 2, y, w, 16, bg); rect(d, LW / 2 - w / 2, y, w, 1, "white"); rect(d, LW / 2 - w / 2, y + 15, w, 1, "white")
    text(d, LW / 2, y + 3, s, c, font)

def dialog(d, s, t0, t, cps=24):
    rect(d, 6, 262, 168, 52, "black"); rect(d, 6, 262, 168, 1, "white"); rect(d, 6, 313, 168, 1, "white")
    rect(d, 6, 262, 1, 52, "white"); rect(d, 173, 262, 1, 52, "white")
    n = max(0, int((t - t0) * cps)); shown = s[:n]
    for i, line in enumerate(textwrap.wrap(shown, 26)[:4]):
        text(d, 11, 266 + i * 12, line, "white", font=FONTM, center=False)

def hud(d, secs, items):
    rect(d, 0, 0, LW, 16, "black"); rect(d, 0, 15, LW, 1, "lgray")
    c = "red" if secs <= 10 and int(secs * 4) % 2 == 0 else "yellow"
    text(d, 6, 4, f"TIEMPO {max(0, int(math.ceil(secs))):02d}", c, FONTM, center=False)
    text(d, 110, 4, f"ITEMS {items:02d}", "green", FONTM, center=False)

CAPS = [
    (0.0, 2.5, "¡Los extraterrestres acaban de invadir la Tierra!"),
    (2.5, 5.0, "Tienes 60 segundos para preparar tu mochila."),
    (5.0, 8.0, "Y no, tu colección de figuritas no cuenta como provisiones."),
    (8.0, 11.0, "Primero: agua potable. Después: comida no perecedera."),
    (11.0, 15.0, "El mejor plan de escape... pero la deshidratación no negocia."),
    (15.0, 20.0, "Linterna, baterías, botiquín, tus medicamentos y una radio portátil."),
    (20.0, 24.0, "Sin luz, tu celular será un espejo muy caro."),
    (24.0, 29.0, "Documentos en bolsa impermeable, efectivo y cargador portátil."),
    (29.0, 33.0, "No dependas de una sola tecnología."),
    (33.0, 37.0, "¿Arma alienígena? No tienes. ¿Detector de aliens? Tampoco."),
    (37.0, 43.0, "¿Sombrero de aluminio? Felicidades: te vas a cocinar la cabeza."),
    (43.0, 48.0, "Si las autoridades indican evacuar, no grabes el platillo volador."),
    (48.0, 54.0, "Tu canal puede esperar. Tu sistema circulatorio, no."),
    (54.0, 62.0, "¿Qué objeto meterías tú? Escribe tu elección antes de que se cierre el inventario."),
]

# item appearance times (nominal)
ITEMS = [(9.0, "agua", "AGUA +20 SUPERVIVENCIA"), (10.3, "comida", "COMIDA +15 ENERGÍA"),
         (15.2, "linterna", "LINTERNA +5 VISIÓN"), (16.0, "baterias", "BATERÍAS +5"), (16.8, "botiquin", "BOTIQUÍN +10 SALUD"),
         (17.6, "medicinas", "MEDICINAS +10 SALUD"), (18.6, "radio", "RADIO + INFORMACIÓN"),
         (24.5, "documentos", "DOCUMENTOS (A PRUEBA DE AGUA)"), (26.0, "efectivo", "EFECTIVO +5"), (27.3, "cargador", "CARGADOR +BATERÍA")]

def inventory(d, t, upto):
    rect(d, 0, 16, LW, GROUND - 16 + 20, "navy")
    for y in range(20, 250, 8): rect(d, 0, y, LW, 1, "black")
    text(d, LW / 2, 22, "INVENTARIO", "white", FONTB)
    got = [it for it in ITEMS if it[0] <= t]
    for i in range(12):
        cx, cy = 12 + (i % 4) * 40, 46 + (i // 4) * 40
        kind = ITEMS[i][1] if i < len(got) else None
        slot(d, cx, cy, kind, sel=(i == len(got) - 1 and t - got[-1][0] < 0.8) if got else False)
    if got and t - got[-1][0] < 1.2:
        popup(d, got[-1][2], 172, "yellow", "dgreen")
    return len(got)

def frame(t, T=None, Tof=None):
    if T is None: T = t
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    shake = (0, 0); items = len([1 for it in ITEMS if it[0] <= t])
    if t < 8.0:
        city(d, t)
        ufo(d, int(20 + math.sin(t * 1.3) * 10), 34, 2, t)
        ufo(d, int(120 + math.sin(t * 1.7 + 1) * 8), 70, 1, t)
        ufo(d, int(70 + math.sin(t * 2 + 2) * 6), 100, 1, t)
        hero(d, 50, GROUND - 46, scared=True, frame=int(t * 6) % 2)
        backpack(d, 100, GROUND - 32, 2, 0)
        if t < 5.0:
            if int(t * 3) % 2 == 0: popup(d, "ALERTA: INVASIÓN", 120, "white", "red", FONTB)
            if t > 2.5: popup(d, "TIEMPO PARA PREPARARTE: 60 s", 150, "yellow", "black")
        else:
            lt = t - 5.0
            icon(d, "figuras", 96, GROUND - 76, 3)
            if lt > 1.0:
                for k in range(36): rect(d, 96 + k, GROUND - 76 + k, 2, 2, "red"); rect(d, 130 - k, GROUND - 76 + k, 2, 2, "red")
                popup(d, "NO SON PROVISIONES", 130, "white", "red")
        if t < 0.5: shake = (random.randint(-2, 2), random.randint(-2, 2))
    elif t < 15.0 and not (11.0 <= t < 15.0):
        inventory(d, t, 2)
        hero(d, 30, 196, frame=0); backpack(d, 120, 206, 2, items)
    elif t < 15.0:
        lt = t - 11.0
        for y in range(16, GROUND, 4): rect(d, 0, y, LW, 4, "orange" if y < 120 else "yellow")
        rect(d, 140, 70, 22, 22, "white"); rect(d, 0, GROUND, LW, LH - GROUND, "brown")
        for x in (20, 140):
            rect(d, x, GROUND - 40, 8, 40, "dgreen"); rect(d, x - 8, GROUND - 28, 8, 4, "dgreen"); rect(d, x - 8, GROUND - 36, 4, 10, "dgreen")
        hero(d, 76, GROUND - 46, scared=True, frame=int(t * 4) % 2)
        for k in range(3):
            yy = GROUND - 60 - ((lt * 20 + k * 12) % 36)
            rect(d, 70 + k * 14, yy, 2, 4, "white")
        hp = max(0.05, 1 - lt / 3)
        text(d, LW / 2, 40, "HIDRATACIÓN", "white", FONTM)
        rect(d, 40, 54, 100, 8, "black"); rect(d, 41, 55, int(98 * hp), 6, "red" if hp < 0.4 else "green")
        if lt > 2.0: popup(d, "NO NEGOCIA", 90, "white", "red", FONTB)
    elif t < 24.0:
        if t < 20.0:
            inventory(d, t, 7)
            hero(d, 30, 196); backpack(d, 120, 206, 2, items)
        else:
            lt = t - 20.0
            city(d, t, alarm=False)
            for y in range(16, GROUND): pass
            rect(d, 30, 30, 120, 200, "black"); rect(d, 36, 40, 108, 176, "navy")
            for k in range(6): rect(d, 40 + k * 18, 44 + k * 26, 30, 2, "lav")
            hero(d, 66, 120, scared=True, frame=0, big=2)
            text(d, 90, 52, "SIN SEÑAL", "red", FONTM)
            if lt > 1.5: popup(d, "ESPEJO DE $$$$", 190, "yellow", "purple", FONTB)
    elif t < 33.0:
        if t < 29.0:
            inventory(d, t, 10)
            hero(d, 30, 196); backpack(d, 120, 206, 2, items)
        else:
            lt = t - 29.0
            city(d, t, alarm=False)
            icon(d, "radio", 66, 120, 4)
            for k in range(3):
                r = 10 + ((lt * 30 + k * 14) % 42)
                d.arc([110 - r, 120 - r, 110 + r, 120 + r], 280, 350, fill=P["green"], width=2)
            hero(d, 20, GROUND - 46)
            popup(d, "INFO +100", 60, "green", "black", FONTB)
    elif t < 43.0:
        lt = t - 33.0
        city(d, t, alarm=False)
        hero(d, 80, GROUND - 46, scared=lt > 6.5, frame=0)
        if lt < 4.0:
            slot(d, 30, 60, "arma", cross=lt > 1.2, sz=40); slot(d, 110, 60, "detector", cross=lt > 3.0, sz=40)
            if lt > 1.2: text(d, 50, 106, "NO TIENES", "red", FONTM)
            if lt > 3.0: text(d, 130, 106, "TAMPOCO", "red", FONTM)
        else:
            icon(d, "sombrero", 80, GROUND - 46 - 22, 2)
            if lt < 6.0: popup(d, "OBJETO EQUIPADO:", 70, "white", "black"); popup(d, "CERO BENEFICIOS", 88, "red", "black")
            else:
                ufo(d, 60, 24, 2, t, beam=True, beam_h=GROUND - 50 - 20)
                for k in range(3):
                    yy = GROUND - 80 - ((lt * 25 + k * 8) % 24)
                    rect(d, 84 + k * 8, yy, 2, 4, "lgray")
                popup(d, "ESCANEANDO...", 110, "green", "black")
                if lt > 7.5: popup(d, "CABEZA AL PUNTO", 130, "orange", "black")
                if 6.0 < lt < 6.4: shake = (random.randint(-2, 2), 0)
    elif t < 54.0:
        lt = t - 43.0
        city(d, t)
        ufo(d, int(60 + math.sin(t) * 20), 34, 2, t)
        if lt < 5.0:
            hero(d, 70, GROUND - 46, frame=0)
            icon(d, "celular", 96, GROUND - 40, 2)
            if int(t * 2) % 2: rect(d, 104, GROUND - 38, 3, 3, "red")
            text(d, 110, GROUND - 52, "REC", "red", FONTM)
            if lt > 2.0:
                for k in range(26): rect(d, 90 + k, GROUND - 60 + k, 2, 2, "red"); rect(d, 116 - k, GROUND - 60 + k, 2, 2, "red")
                popup(d, "¡EVACÚA!", 110, "white", "red", FONTB)
        else:
            lt2 = lt - 5.0
            rect(d, 130, GROUND - 40, 46, 40, "lgray"); rect(d, 126, GROUND - 46, 54, 8, "dgray"); rect(d, 146, GROUND - 26, 14, 26, "black")
            text(d, 153, GROUND - 58, "REFUGIO", "green", FONTM)
            hx = int(lerp(10, 132, cl(lt2 / 4.0)))
            if hx < 132:
                hero(d, hx, GROUND - 46, frame=int(t * 8) % 2); backpack(d, hx - 18, GROUND - 40, 1, 0, closed=True)
            popup(d, "OBJETIVO: LLEGAR A UN", 60, "white", "black"); popup(d, "LUGAR SEGURO", 76, "yellow", "black")
            if lt2 > 2.0: popup(d, "BONUS: NO MORIR POR UN SELFIE", 100, "pink", "purple")
            if lt2 > 4.2: popup(d, "MISIÓN CUMPLIDA", 130, "green", "black", FONTB)
    else:
        lt = t - 54.0
        rect(d, 0, 16, LW, 246, "navy")
        text(d, LW / 2, 26, "INVENTARIO", "white", FONTB)
        for i in range(12):
            cx, cy = 12 + (i % 4) * 40, 50 + (i // 4) * 40
            if i < 11: slot(d, cx, cy, ITEMS[i][1] if i < 10 else None)
            else:
                slot(d, cx, cy, None, sel=int(t * 3) % 2 == 0)
                text(d, cx + 15, cy + 8, "?", "pink", FONTB)
        text(d, LW / 2, 180, "¿QUÉ METERÍAS TÚ?", "yellow", FONTB)
        if int(t * 2) % 2 == 0: text(d, LW / 2, 204, "COMENTA ↓", "pink", FONTB)
        text(d, LW / 2, 230, "SÍGUEME: DATOS QUE ASUSTAN", "green", FONTM)
    secs = 60.0 * (1 - T / DUR_REAL) if DUR_REAL else 60.0
    if t >= 54.0: secs = max(0.0, 6 * (1 - (t - 54.0) / 7.0))
    hud(d, secs, min(items, 10))
    for cs, ce, s in CAPS:
        if cs <= t < ce:
            dialog(d, s, Tof(cs) if Tof else cs, T)
    big = img.resize((LW * SC, LH * SC), Image.NEAREST)
    arr = np.asarray(big).copy()
    if shake != (0, 0):
        arr = np.roll(arr, shake[0] * SC, axis=1); arr = np.roll(arr, shake[1] * SC, axis=0)
    arr[::SC, :, :] = (arr[::SC, :, :] * 0.82).astype(np.uint8)
    return arr

DUR_REAL = 62.0

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        ims = [Image.fromarray(frame(float(x))).resize((270, 480), Image.NEAREST) for x in sys.argv[2:]]
        cols = min(6, len(ims)); rows = (len(ims) + 5) // 6
        sh = Image.new("RGB", (270 * cols, 480 * rows))
        for i, im in enumerate(ims): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sh.save("alien_prev.png"); sys.exit()
    from warp10 import v_of_T, T_of_v, DUR
    DUR_REAL = DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(min(61.99, v_of_T(i / FPS)), i / FPS, T_of_v).tobytes())
    p.stdin.close(); p.wait()
