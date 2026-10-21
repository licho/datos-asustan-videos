import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)
from reel2 import germ

FPS = 30
KINDS = ["ecoli", "coli", "staph"]

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def kitchen():
    img = grad((235, 240, 230), (205, 215, 200)); d = ImageDraw.Draw(img)
    for y in range(300, 1150, 90):
        for x in range(0 if (y // 90) % 2 else -45, W, 90):
            d.rectangle([x, y, x + 88, y + 88], outline=(215, 222, 212), width=3)
    d.rectangle([0, 1150, W, 1230], fill=(170, 150, 130), outline=BLK, width=5)
    d.rectangle([0, 1230, W, H], fill=(225, 220, 210))
    d.rounded_rectangle([250, 1150, 830, 1210], 20, fill=(150, 160, 170), outline=BLK, width=5)
    d.rectangle([800, 980, 840, 1150], fill=(180, 185, 195), outline=BLK, width=4)
    d.rounded_rectangle([640, 960, 840, 1000], 18, fill=(180, 185, 195), outline=BLK, width=4)
    return img
KITCHEN = kitchen()

def sponge(d, cx, cy, s, t=0.0, mood="smug", dirt=0.0, wet=0.0, sparkle=False):
    S = lambda v: v * s
    body = lc((250, 215, 70), (170, 150, 70), dirt)
    d.rounded_rectangle([cx - S(220), cy - S(70), cx + S(220), cy + S(140)], int(S(40)), fill=body, outline=BLK, width=max(3, int(S(7))))
    d.rounded_rectangle([cx - S(220), cy - S(140), cx + S(220), cy - S(40)], int(S(30)), fill=lc((70, 160, 80), (60, 90, 60), dirt), outline=BLK, width=max(3, int(S(7))))
    rng = random.Random(3)
    for i in range(40):
        px, py = cx + rng.uniform(-190, 190) * s, cy + rng.uniform(-40, 120) * s
        r = rng.uniform(5, 12) * s
        d.ellipse([px - r, py - r, px + r, py + r], fill=dk(body, 0.8))
    for i in range(int(dirt * 14)):
        px, py = cx + rng.uniform(-180, 180) * s, cy + rng.uniform(-30, 110) * s
        r = rng.uniform(10, 24) * s
        d.ellipse([px - r, py - r * 0.6, px + r, py + r * 0.6], fill=(120, 100, 60))
    if wet > 0:
        for k in range(4):
            dx = cx - S(150) + k * S(100); dy = cy + S(150) + ((t * 120 + k * 40) % 80) * s
            d.ellipse([dx - S(10), dy - S(14), dx + S(10), dy + S(14)], fill=(140, 200, 240))
    hx, hy = cx, cy + S(30)
    for sx in (-1, 1):
        ex = hx + sx * S(70)
        d.ellipse([ex - S(30), hy - S(30), ex + S(30), hy + S(30)], fill=WHITE, outline=BLK, width=max(2, int(S(5))))
        d.ellipse([ex - S(11), hy - S(8), ex + S(11), hy + S(14)], fill=BLK)
        if mood == "smug":
            d.line([(ex - S(32), hy - S(42) - sx * S(6)), (ex + S(32), hy - S(42) + sx * S(6))], fill=BLK, width=max(2, int(S(7))))
    if mood in ("smug", "happy"):
        d.arc([hx - S(55), hy + S(30), hx + S(55), hy + S(90)], 20, 160, fill=BLK, width=max(2, int(S(7))))
    else:
        d.ellipse([hx - S(20), hy + S(45), hx + S(20), hy + S(85)], fill=(60, 10, 20), outline=BLK, width=3)
    if sparkle:
        for k in range(3):
            a = t * 3 + k * 2.1
            sx, sy = cx + math.cos(a) * S(280), cy - S(60) + math.sin(a) * S(120)
            d.polygon([(sx, sy - 22), (sx + 7, sy - 7), (sx + 22, sy), (sx + 7, sy + 7), (sx, sy + 22), (sx - 7, sy + 7), (sx - 22, sy), (sx - 7, sy - 7)], fill=WHITE)

def swarm(d, cx, cy, rx, ry, n, t, size=34, seed=5, bad=-1):
    rng = random.Random(seed)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(0.2, 1.0)
        x = cx + math.cos(a + t * 0.3 * rng.choice([-1, 1])) * rx * rr
        y = cy + math.sin(a + t * 0.3) * ry * rr
        germ(d, x, y, size * rng.uniform(0.8, 1.2), KINDS[i % 3], t, phase=i)
        if i == bad:
            d.ellipse([x - size * 2, y - size * 2, x + size * 2, y + size * 2], outline=RED, width=8)

CAPS = [
    (0.0, 3.5, "Algo que usas para *limpiar*… podría ser un *paraíso para microorganismos*"),
    (3.5, 5.0, "Y sí, *probablemente lo usaste hoy*"),
    (5.0, 8.0, "*La esponja para lavar trastes*"),
    (8.0, 11.5, "*Restos de comida, grasa, humedad*… y horas sin secarse"),
    (11.5, 15.0, "Un *departamento amueblado* con *comida incluida*"),
    (15.0, 20.0, "*Miles de espacios* donde quedan atrapados *residuos y microorganismos*"),
    (20.0, 23.0, "Estudios han hallado *comunidades bacterianas muy diversas*"),
    (23.0, 27.0, "La mayoría no son peligrosas… pero *algunas pueden causar enfermedades*"),
    (27.0, 31.0, "*Enjuagarla rápido ≠ desinfectarla*"),
    (31.0, 37.0, "Húmeda junto al fregadero *por días*… *condiciones perfectas* para ellos"),
    (37.0, 45.0, "*Enjuágala, escúrrela y déjala secar.* Cámbiala *con regularidad*"),
    (45.0, 49.0, "¿Carne cruda? *No confíes en un simple enjuague*"),
    (49.0, 55.0, "No es para ser *el experimento científico más antiguo de tu cocina*"),
    (55.0, 62.0, "¿Cuándo fue la *última vez que cambiaste la tuya*?"),
]

def s_hook(t):
    img = KITCHEN.copy(); d = ImageDraw.Draw(img)
    sponge(d, 420, 1040, 0.8, t, mood="smug", sparkle=t < 2.0, dirt=cl((t - 2.0) / 2.0) * 0.5)
    if t > 2.0:
        for k in range(int(cl((t - 2.0) / 1.5) * 10)):
            germ(d, 240 + (k * 97) % 600, 700 + (k * 53) % 200, 30, KINDS[k % 3], t, phase=k)
    chip(d, "LO MÁS ASQUEROSO DE TU COCINA", 230, bg=RED, size=50, appear=t / 0.3)
    return img, 1.0, 1.0

def s_reveal(t):
    lt = t - 5.0
    img = grad((255, 235, 140), (250, 200, 80)); d = ImageDraw.Draw(img)
    for k in range(16):
        a = k / 16 * 2 * math.pi + t * 0.3
        d.polygon([(540, 900), (540 + math.cos(a) * 1400, 900 + math.sin(a) * 1400), (540 + math.cos(a + 0.18) * 1400, 900 + math.sin(a + 0.18) * 1400)], fill=(255, 245, 180))
    sponge(d, 540, 900, 1.6 * pop(lt / 0.4) + 0.01, t, mood="smug")
    bigtext(d, "LA ESPONJA", 540, 400, int(110 * pop((lt - 0.3) / 0.3)) + 1, fill=RED, stroke=WHITE, sw=10)
    return img, 1.0, 1.0, (lt < 0.3)

def s_apartment(t):
    lt = t - 8.0
    img = KITCHEN.copy(); d = ImageDraw.Draw(img)
    if lt < 3.5:
        sponge(d, 420, 1040, 0.8, t, mood="smug", dirt=0.5 + 0.3 * cl(lt / 3), wet=1)
        items = [(0.2, "COMIDA", (200, 120, 60)), (1.0, "GRASA", (230, 190, 60)), (1.8, "HUMEDAD", (90, 160, 230)), (2.6, "HORAS", (120, 120, 140))]
        for i, (st, txt, c) in enumerate(items):
            if lt < st: continue
            a = cl((lt - st) / 0.6)
            x = 200 + i * 230; y = lerp(380, 900, a)
            d.rounded_rectangle([x - 108, y - 45, x + 108, y + 45], 18, fill=c, outline=BLK, width=4)
            d.text((x, y), txt, font=F(32), fill=WHITE, anchor="mm")
    else:
        lt2 = lt - 3.5
        S = 1.0
        d.rounded_rectangle([240, 420, 840, 1150], 30, fill=(250, 215, 70), outline=BLK, width=8)
        d.rectangle([240, 420, 840, 520], fill=(70, 160, 80), outline=BLK, width=8)
        for r in range(4):
            for c in range(3):
                x0, y0 = 290 + c * 190, 560 + r * 140
                d.rectangle([x0, y0, x0 + 130, y0 + 100], fill=(255, 245, 200), outline=BLK, width=4)
                if (r * 3 + c) < int(cl(lt2 / 1.5) * 12):
                    germ(d, x0 + 65, y0 + 55, 32, KINDS[(r + c) % 3], t, phase=r + c)
        sc = pop((lt2 - 0.8) / 0.3)
        d.rounded_rectangle([540 - 330 * sc, 330 - 60 * sc, 540 + 330 * sc, 330 + 60 * sc], int(16 * sc), fill=WHITE, outline=BLK, width=5)
        d.text((540, 330), "SE RENTA · COMIDA INCLUIDA", font=F(max(8, int(34 * sc))), fill=RED, anchor="mm")
    return img, 1.0, 1.0

def s_micro(t):
    lt = t - 15.0
    img = grad((25, 30, 45), (45, 50, 70)); d = ImageDraw.Draw(img)
    cx, cy, R = 540, 850, 430
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(240, 205, 90), outline=(200, 200, 210), width=24)
    rng = random.Random(7)
    for i in range(30):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(0, R - 60)
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        r = rng.uniform(25, 60)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(205, 165, 60))
    n = int(cl(lt / 4.0) * 22)
    bad = 3 if lt > 8.0 else -1
    swarm(d, cx, cy, R - 90, R - 90, n, t, 34, 11, bad=bad)
    chip(d, "ZOOM: DENTRO DE LA ESPONJA", 230, bg=(30, 110, 210), size=50, appear=lt / 0.3)
    if lt > 5.0 and lt < 8.0: chip(d, "COMUNIDADES MUY DIVERSAS", 330, bg=(40, 140, 80), size=50, appear=(lt - 5.0) / 0.3)
    if lt > 8.0: chip(d, "ALGUNAS PUEDEN ENFERMARTE", 330, bg=RED, size=50, appear=(lt - 8.0) / 0.3)
    return img, 1.0, 1.0

def s_rinse(t):
    lt = t - 27.0
    img = KITCHEN.copy(); d = ImageDraw.Draw(img)
    if lt < 4.0:
        for k in range(6):
            y = 1000 + ((t * 600 + k * 30) % 100)
            d.line([(645 + k * 6, 1000), (645 + k * 6, y)], fill=(140, 200, 240), width=6)
        sponge(d, 660, 1090, 0.6, t, mood="happy", dirt=0.6, wet=1)
        for k in range(5):
            gx = 480 + k * 70 + math.sin(t * 4 + k) * 10
            germ(d, gx, 1010 - (k % 2) * 40, 28, KINDS[k % 3], t, phase=k)
        sc = pop((lt - 0.5) / 0.3)
        d.rounded_rectangle([540 - 380 * sc, 420 - 70 * sc, 540 + 380 * sc, 420 + 70 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=6)
        d.text((540, 420), "ENJUAGAR ≠ DESINFECTAR", font=F(max(8, int(46 * sc))), fill=RED, anchor="mm")
    else:
        lt2 = lt - 4.0
        day = 1 + min(4, int(lt2 / 1.2))
        sponge(d, 400, 1090, 0.6, t, mood="o", dirt=0.6 + 0.08 * day, wet=1)
        d.rectangle([700, 400, 960, 640], fill=WHITE, outline=BLK, width=6)
        d.rectangle([700, 400, 960, 470], fill=RED)
        d.text((830, 435), "DÍA", font=F(44), fill=WHITE, anchor="mm")
        d.text((830, 560), str(day), font=F(110), fill=(30, 30, 30), anchor="mm")
        swarm(d, 400, 900, 280, 160, 3 + day * 4, t, 28, 13)
    return img, 1.0, 1.0

TIPS = [(37.3, "Enjuágala bien"), (38.6, "Escúrrela"), (39.8, "Déjala secar"), (41.5, "Cámbiala seguido"), (43.0, "¿Huele mal? Reemplázala"), (45.2, "Carne cruda: ¡enjuagar no basta!")]

def s_tips(t):
    lt = t - 37.0
    img = grad((225, 240, 230), (195, 220, 205)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([80, 300, 1000, 1180], 40, fill=(252, 250, 240), outline=BLK, width=8)
    d.text((540, 380), "MANUAL DE LA ESPONJA", font=F(62), fill=(40, 40, 40), anchor="mm")
    for i, (st, txt) in enumerate(TIPS):
        if t < st: continue
        a = cl((t - st) / 0.25)
        y = 500 + i * 115
        d.rounded_rectangle([130, y - 40, 210, y + 40], 16, outline=BLK, width=6, fill=WHITE)
        if t > st + 0.3:
            check(d, 170, y, 0.7) if i < 5 else xmark(d, 170, y, 0.35)
        d.text((235, y), txt, font=F(int((34 if i == 5 else 40) * a) + 1), fill=RED if i == 5 else (30, 30, 30), anchor="lm")
    return img, 1.0, 1.0

def s_lab(t):
    lt = t - 49.0
    img = grad((210, 225, 240), (180, 200, 220)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, W, H], fill=(150, 160, 175))
    d.rectangle([180, 380, 900, 1150], fill=(235, 245, 250), outline=BLK, width=8)
    d.rectangle([180, 380, 900, 460], fill=(60, 80, 120))
    d.text((540, 420), "LABORATORIO", font=F(52), fill=WHITE, anchor="mm")
    sponge(d, 540, 820, 0.9, t, mood="smug", dirt=1.0)
    swarm(d, 540, 700, 300, 120, 10, t, 28, 17)
    sc = pop((lt - 1.0) / 0.3)
    d.rounded_rectangle([300, 1020 - 50 * sc, 780, 1020 + 50 * sc], 12, fill=WHITE, outline=BLK, width=4)
    d.text((540, 1020), "MUESTRA #1 · AÑO ???", font=F(max(8, int(32 * sc))), fill=(30, 30, 30), anchor="mm")
    chip(d, "EXPERIMENTO MÁS ANTIGUO", 230, bg=(150, 60, 200), size=52, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 55.0
    img = KITCHEN.copy(); d = ImageDraw.Draw(img)
    sponge(d, 240, 1060, 0.55, t, mood="o", dirt=0.9)
    sponge(d, 580, 1060, 0.55, t, mood="happy", sparkle=True)
    d.text((240, 910), "VIEJA", font=F(44), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    d.text((580, 910), "NUEVA", font=F(44), fill=(40, 150, 80), anchor="mm", stroke_width=5, stroke_fill=WHITE)
    sc = pop(lt / 0.35)
    d.rounded_rectangle([540 - 400 * sc, 400 - 90 * sc, 540 + 400 * sc, 400 + 90 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
    d.text((540, 370), "¿CUÁNDO CAMBIASTE", font=F(max(8, int(52 * sc))), fill=WHITE, anchor="mm")
    d.text((540, 435), "LA TUYA?", font=F(max(8, int(52 * sc))), fill=YEL, anchor="mm")
    if lt > 1.5: chip(d, "COMENTA  ·  SÍGUEME", 230, bg=(30, 30, 40), fg=YEL, size=50, appear=(lt - 1.5) / 0.3)
    return img, 1.0, 1.0

SCENES = [(0, 5, s_hook), (5, 8, s_reveal), (8, 15, s_apartment), (15, 27, s_micro), (27, 37, s_rinse),
          (37, 49, s_tips), (49, 55, s_lab), (55, 99, s_end)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img = r[0]; shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce: rich_caption(d, txt, appear=(t - cs) / 0.25)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = 0.3 + 0.7 * fi
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    if shake:
        k = int(t * FPS)
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1); arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r16.png"); sys.exit()
    from warp16 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(61.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
