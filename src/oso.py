import math, random, subprocess, sys, textwrap
import numpy as np
from PIL import Image, ImageDraw
from pixel import P, rect, text, FONT, FONTB, hero, LW, LH, SC

FPS = 30
from PIL import ImageFont
FONTM = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 10)
GROUND = 240

def forest(d, t):
    for y in range(0, GROUND, 4):
        rect(d, 0, y, LW, 4, "blue" if y < 90 else "lav" if y < 150 else "dgreen")
    rect(d, 120, 40, 18, 18, "yellow")
    rng = random.Random(3)
    for i in range(9):
        x = rng.randint(-10, LW); h = rng.randint(50, 90); base = GROUND
        rect(d, x + 7, base - 14, 4, 14, "brown")
        for k in range(5):
            w = 18 - k * 3
            rect(d, x + 9 - w // 2, base - 14 - (k + 1) * h // 6, w, h // 6 + 2, "dgreen" if k % 2 else "green")
    rect(d, 0, GROUND, LW, LH - GROUND, "dgreen")
    for x in range(0, LW, 10): rect(d, x, GROUND, 5, 2, "green")

def bear(d, x, y, big=2, kind="brown", frame=0, mood="normal"):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    body = "brown" if kind == "brown" else "black"
    dark = "dgray" if kind == "black" else "purple"
    snout = "peach" if kind == "brown" else "brown"
    R(0, 8, 22, 12, body)
    if kind == "brown": R(3, 5, 7, 4, body)
    off = frame % 2
    R(1, 20, 4, 5 - off, dark); R(8, 20, 4, 5, dark); R(13, 20, 4, 5 - (1 - off), dark); R(18, 20, 4, 5, dark)
    R(18, 2, 11, 10, body)
    R(19, 0 if kind == "black" else 1, 3, 3, body); R(25, 0 if kind == "black" else 1, 3, 3, body)
    R(26, 6, 5, 4, snout); R(30, 6, 2, 2, "black")
    R(23, 4, 2, 2, "white" if mood == "angry" else "black")
    if mood == "angry": R(23, 4, 1, 1, "red")
    if mood == "eat": R(27, 10, 4, 2, "red")

def sandwich(d, x, y, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    R(0, 0, 10, 2, "orange"); R(0, 2, 10, 1, "green"); R(0, 3, 10, 1, "red"); R(0, 4, 10, 2, "orange")

def heart(d, x, y, full=True):
    c = "red" if full else "dgray"
    rect(d, x, y + 1, 2, 2, c); rect(d, x + 3, y + 1, 2, 2, c); rect(d, x + 1, y, 1, 1, c); rect(d, x + 4, y, 1, 1, c)
    rect(d, x + 1, y + 3, 3, 1, c); rect(d, x + 2, y + 4, 1, 1, c)

def hud(d, lives, score):
    rect(d, 0, 0, LW, 16, "black")
    for i in range(3): heart(d, 6 + i * 8, 5, i < lives)
    text(d, LW - 4, 4, f"PTS {score:04d}", "yellow", center=False) if False else text(d, 140, 4, f"PTS {score:04d}", "yellow")

def dialog(d, s, t0, t, cps=26):
    rect(d, 6, 262, 168, 52, "black"); rect(d, 6, 262, 168, 1, "white"); rect(d, 6, 313, 168, 1, "white")
    rect(d, 6, 262, 1, 52, "white"); rect(d, 173, 262, 1, 52, "white")
    n = max(0, int((t - t0) * cps)); shown = s[:n]
    for i, line in enumerate(textwrap.wrap(shown, 26)[:4]):
        text(d, 11, 266 + i * 12, line, "white", font=FONTM, center=False)

def popup(d, s, y, c="yellow", bg="purple"):
    w = d.textlength(s, font=FONTB) + 12
    rect(d, LW / 2 - w / 2, y, w, 22, bg); rect(d, LW / 2 - w / 2, y, w, 1, "white"); rect(d, LW / 2 - w / 2, y + 21, w, 1, "white")
    text(d, LW / 2, y + 4, s, c, FONTB)

CAPS = [
    (0.0, 4.0, "¡NIVEL DESBLOQUEADO: OSO SALVAJE!"),
    (4.0, 7.0, "Vas de excursión, sacas tu sándwich... y ¡zas! Un oso."),
    (7.0, 9.5, "Tranquilo, así se pasa este nivel."),
    (9.5, 13.0, "1: NO corras. El oso es más rápido que tú..."),
    (13.0, 16.0, "...cuesta arriba, cuesta abajo... y cuando hay pizza."),
    (16.0, 22.0, "2: háblale con calma, mueve los brazos despacio y hazte grande."),
    (22.0, 28.0, "3: aléjate despacio y de lado. Nunca entre mamá osa y sus oseznos."),
    (28.0, 33.0, "4: no te subas a un árbol. Los osos trepan... mejor que tú."),
    (33.0, 37.0, "5: si ataca, depende del oso. ¿Pardo o grizzly? Hazte el muerto."),
    (37.0, 41.0, "¿Oso negro? NO te hagas el muerto: defiéndete y pégale en la cara."),
    (41.0, 45.0, "Ojo, el color engaña: el pardo tiene joroba en los hombros."),
    (45.0, 52.0, "Y lo más importante... no le des tu sándwich."),
    (52.0, 60.0, "Comenta: ¿corres, te haces el muerto... o le das el sándwich?"),
]
STEPS = [9.5, 16.0, 22.0, 28.0, 33.0]

def lives_score(t):
    lives, score = 3, 0
    if t > 11.5: lives = 2
    if t > 12.5: lives = 3
    for s in STEPS:
        if t > s + 2.0: score += 100
    if t > 30.5: lives = 2
    if t > 32.0: lives = 3
    return lives, score

def frame(t, T=None, Tof=None):
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    shake = (0, 0)
    step = sum(1 for s in STEPS if t >= s)
    if t < 9.5:
        forest(d, t)
        hx = int(20 + min(t, 4.0) * 12)
        hero(d, hx, 190, scared=t > 4.6, frame=int(t * 6) % 2)
        sandwich(d, hx + 26, 206)
        if t > 4.2:
            bx = int(lerp(200, 100, min(1, (t - 4.2) / 0.8)))
            bear(d, bx, 186, 2, "brown", int(t * 5), "angry")
            if t < 6.0: text(d, hx + 12, 170, "!", "red", FONTB)
        if t < 4.0:
            popup(d, "NIVEL 1", 60, "white", "navy"); popup(d, "OSO SALVAJE", 86, "yellow", "red")
            if t < 0.4: shake = (random.randint(-2, 2), random.randint(-2, 2))
    elif step == 1:
        ls = t - STEPS[0]
        forest(d, t)
        if ls < 2.5:
            hx = int(60 + ls * 25); hero(d, hx, 190, True, int(t * 10) % 2)
            bx = int(-40 + ls * 70); bear(d, bx, 186, 2, "brown", int(t * 10), "angry")
            if ls > 1.6: popup(d, "-1 VIDA", 70, "white", "red")
        else:
            hero(d, 80, 190, True, int(t * 6) % 2)
            popup(d, "NO CORRER", 70, "yellow", "red")
            if t > 13.0:
                rect(d, 120, 110, 30, 30, "orange"); rect(d, 123, 113, 24, 24, "yellow")
                for (a, b) in [(128, 118), (138, 126), (130, 130)]: rect(d, a, b, 4, 4, "red")
                text(d, 135, 145, "PIZZA", "white")
    elif step == 2:
        ls = t - STEPS[1]
        forest(d, t)
        rect(d, 50, 214, 50, 26, "dgray"); rect(d, 50, 214, 50, 3, "lgray")
        big = 2 if ls < 3.0 else 3
        hero(d, 62 if big == 2 else 56, 166 if big == 2 else 145, scared=False, frame=int(t * 4) % 2, big=big)
        if int(t * 4) % 2: rect(d, 52, 150 if big == 2 else 120, 6, 6, "peach"); rect(d, 92, 150 if big == 2 else 120, 6, 6, "peach")
        bear(d, 110, 186, 2, "brown", 0, "normal")
        rect(d, 10, 110, 100, 22, "white"); text(d, 60, 116, "HOLA, SOY HUMANO", "black", shadow=None)
        if ls > 3.0: popup(d, "+100 HAZTE GRANDE", 60, "yellow", "dgreen")
    elif step == 3:
        ls = t - STEPS[2]
        forest(d, t)
        hx = int(30 + ls * 6)
        hero(d, hx, 190, False, int(t * 3) % 2)
        text(d, hx + 12, 176, "→ de lado", "white")
        bear(d, 110, 192, 2, "brown", 0, "normal")
        bear(d, 140, 222, 1, "brown", int(t * 4), "normal")
        if ls > 2.5:
            rect(d, 100, 150, 70, 20, "red"); text(d, 135, 155, "¡NO ENTRES!", "white")
    elif step == 4:
        ls = t - STEPS[3]
        forest(d, t)
        rect(d, 70, 90, 12, 150, "brown")
        for k in range(4): rect(d, 46 - k * 2, 90 + k * 18, 60 + k * 4, 16, "dgreen" if k % 2 else "green")
        climb = min(1, ls / 1.2)
        hero(d, 62, int(200 - climb * 80), True, int(t * 8) % 2)
        if ls > 1.2:
            by = int(lerp(200, 140, min(1, (ls - 1.2) / 0.8)))
            bear(d, 60, by, 2, "black", int(t * 8), "angry")
        if 2.2 < ls < 3.8: popup(d, "-1 VIDA", 40, "white", "red")
        if ls > 3.8: popup(d, "NO AL ÁRBOL", 40, "yellow", "red")
    elif t < 45.0:
        forest(d, t)
        rect(d, 89, 20, 2, 220, "white")
        bear(d, 6, 150, 2, "brown", 0, "angry")
        text(d, 45, 40, "PARDO", "orange", FONTB)
        bear(d, 96, 150, 2, "black", 0, "angry")
        text(d, 135, 40, "NEGRO", "lgray", FONTB)
        if t > 34.5:
            rect(d, 14, 214, 30, 10, "orange"); rect(d, 40, 212, 8, 8, "peach")
            text(d, 45, 70, "HAZTE EL", "white"); text(d, 45, 82, "MUERTO", "yellow")
        if t > 37.5:
            hero(d, 140, 196, False, int(t * 10) % 2)
            text(d, 135, 70, "¡DEFIÉNDETE!", "yellow")
            if int(t * 6) % 2: text(d, 128, 175, "POW", "red", FONTB)
        if t > 41.0:
            text(d, 20, 120, "JOROBA ↓", "yellow")
            rect(d, 10, 150 + 2, 18, 2, "yellow")
    elif t < 52.0:
        lt = t - 45.0
        forest(d, t)
        hero(d, 30, 190, False, 0)
        bear(d, 90, 186, 2, "brown", 0, "eat" if lt > 2.5 else "normal")
        sandwich(d, 70, 150, 3)
        if int(t * 3) % 2: text(d, 85, 135, "♥", "red", FONTB)
        if lt > 2.5: popup(d, "NO LE DES TU SÁNDWICH", 60, "yellow", "red")
    else:
        lt = t - 52.0
        rect(d, 0, 0, LW, LH, "navy")
        popup(d, "¿QUÉ HACES?", 50, "white", "purple")
        opts = ["CORRER", "HACERSE EL MUERTO", "DAR EL SÁNDWICH"]
        sel = int(lt * 1.5) % 3
        for i, o in enumerate(opts):
            y = 100 + i * 30
            rect(d, 20, y, 140, 22, "black"); rect(d, 20, y, 140, 1, "white"); rect(d, 20, y + 21, 140, 1, "white")
            text(d, 95, y + 7, o, "yellow" if i == sel else "white")
            if i == sel and int(lt * 4) % 2: text(d, 28, y + 7, "▶", "pink", center=False)
        text(d, LW / 2, 210, "COMENTA ↓", "pink", FONTB)
    if t < 52.0:
        lives, score = lives_score(t)
        hud(d, lives, score)
        if step >= 1 and t < 45.0:
            rect(d, 4, 22, 22, 22, "yellow"); text(d, 15, 26, str(step), "black", FONTB, shadow=None)
    for cs, ce, s in CAPS:
        if cs <= t < ce:
            if T is not None: dialog(d, s, Tof(cs), T, cps=24)
            else: dialog(d, s, cs, t)
    big = img.resize((LW * SC, LH * SC), Image.NEAREST)
    arr = np.asarray(big).copy()
    if shake != (0, 0):
        arr = np.roll(arr, shake[0] * SC, axis=1); arr = np.roll(arr, shake[1] * SC, axis=0)
    arr[::SC, :, :] = (arr[::SC, :, :] * 0.82).astype(np.uint8)
    return arr

def lerp(a, b, t): return a + (b - a) * t

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        ims = [Image.fromarray(frame(float(x))).resize((270, 480), Image.NEAREST) for x in sys.argv[2:]]
        cols = min(6, len(ims)); rows = (len(ims) + 5) // 6
        sh = Image.new("RGB", (270 * cols, 480 * rows))
        for i, im in enumerate(ims): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sh.save("oso_prev.png"); sys.exit()
    from warp6 import v_of_T, T_of_v, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(min(59.99, v_of_T(i / FPS)), i / FPS, T_of_v).tobytes())
    p.stdin.close(); p.wait()
