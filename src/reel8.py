import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy, zombie, freezer,
                  STORE, GLASS, draw_lights, glass_overlay, W, H, YEL, RED, WHITE, BLK, SKIN, FEET)

FPS = 30

def outside_day(w, h):
    img = Image.new("RGB", (w, h)); d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lc((150, 200, 240), (220, 235, 245), y / h))
    d.rectangle([0, int(h * 0.62), w, h], fill=(120, 120, 125))
    return img
OUT_DAY = outside_day(GLASS[2] - GLASS[0], GLASS[3] - GLASS[1])

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img
BG_BODEGA = grad((90, 75, 60), (40, 32, 25))
BG_DARK = grad((10, 10, 14), (0, 0, 0))
BG_LAB = grad((235, 238, 242), (190, 198, 208))

def store_day(t, zombies_at_door=True):
    img = STORE.copy(); d = ImageDraw.Draw(img)
    draw_lights(d, 1.0)
    layer = OUT_DAY.copy(); ld = ImageDraw.Draw(layer)
    if zombies_at_door:
        for i, zx in enumerate([70, 190]):
            zombie(ld, zx, 590, 0.42, t + i, face=-1, shade=0.8)
    img.paste(layer, (GLASS[0], GLASS[1]))
    d = ImageDraw.Draw(img); glass_overlay(d, GLASS)
    return img, d

def fridge_empty(d, x0, y0, w, h, open_=1.0):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(225, 235, 245), outline=BLK, width=6)
    for k in range(1, 4):
        d.line([(x0 + 10, y0 + k * h / 4), (x0 + w - 10, y0 + k * h / 4)], fill=(170, 180, 190), width=8)
    d.polygon([(x0 + w, y0), (x0 + w + 160 * open_, y0 - 30), (x0 + w + 160 * open_, y0 + h + 30), (x0 + w, y0 + h)], fill=(200, 215, 230), outline=BLK)

def bottle(d, x, y, s=1.0):
    d.rounded_rectangle([x - 22 * s, y - 70 * s, x + 22 * s, y + 70 * s], int(12 * s), fill=(150, 205, 245), outline=BLK, width=3)
    d.rectangle([x - 10 * s, y - 90 * s, x + 10 * s, y - 70 * s], fill=(40, 90, 200))

def can(d, x, y, s=1.0, col=(240, 200, 60)):
    d.rounded_rectangle([x - 40 * s, y - 60 * s, x + 40 * s, y + 60 * s], int(10 * s), fill=col, outline=BLK, width=4)
    d.ellipse([x - 40 * s, y - 72 * s, x + 40 * s, y - 48 * s], fill=(200, 200, 205), outline=BLK, width=3)

def ice(d, x, y, s=1.0):
    for (a, b) in [(-30, 0), (30, -10), (0, 30)]:
        d.rounded_rectangle([x + a * s - 28 * s, y + b * s - 28 * s, x + a * s + 28 * s, y + b * s + 28 * s], int(8 * s), fill=(200, 235, 255), outline=(90, 150, 200), width=4)

def heater(d, x, y, s=1.0):
    d.rounded_rectangle([x - 70 * s, y - 150 * s, x + 70 * s, y + 150 * s], int(40 * s), fill=(235, 235, 230), outline=BLK, width=5)
    d.rectangle([x - 20 * s, y + 90 * s, x + 20 * s, y + 120 * s], fill=(200, 60, 50))
    d.line([(x - 40 * s, y - 150 * s), (x - 40 * s, y - 210 * s)], fill=(150, 150, 155), width=int(12 * s))
    d.line([(x + 40 * s, y - 150 * s), (x + 40 * s, y - 210 * s)], fill=(150, 150, 155), width=int(12 * s))

def card(d, cx, cy, sc, label):
    S = lambda v: v * sc
    d.rounded_rectangle([cx - S(150) + 8, cy - S(170) + 10, cx + S(150) + 8, cy + S(170) + 10], int(S(30)), fill=BLK)
    d.rounded_rectangle([cx - S(150), cy - S(170), cx + S(150), cy + S(170)], int(S(30)), fill=(250, 248, 240), outline=BLK, width=6)
    d.text((cx, cy + S(130)), label, font=F(S(36)), fill=(40, 40, 40), anchor="mm")

def truck(d, x, y, s=1.0):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(180), y - S(120), x + S(80), y + S(40)], int(S(14)), fill=(70, 140, 220), outline=BLK, width=5)
    d.rounded_rectangle([x + S(80), y - S(80), x + S(180), y + S(40)], int(S(14)), fill=(240, 240, 245), outline=BLK, width=5)
    for wx in (x - S(110), x + S(120)):
        d.ellipse([wx - S(36), y + S(10), wx + S(36), y + S(82)], fill=(40, 40, 40))
    d.text((x - S(50), y - S(40)), "AGUA", font=F(S(46)), fill=WHITE, anchor="mm")

def pot(d, x, y, s, t):
    S = lambda v: v * s
    d.rectangle([x - S(150), y + S(60), x + S(150), y + S(90)], fill=(60, 60, 65))
    for k in range(5):
        fx = x - S(110) + k * S(55)
        h = S(30) + S(10) * math.sin(t * 15 + k)
        d.polygon([(fx - S(18), y + S(60)), (fx, y + S(60) - h), (fx + S(18), y + S(60))], fill=(255, 150, 40))
    d.rounded_rectangle([x - S(130), y - S(110), x + S(130), y + S(60)], int(S(20)), fill=(170, 175, 185), outline=BLK, width=5)
    for k in range(6):
        bx = x - S(90) + k * S(36); by = y - S(110) - ((t * 90 + k * 25) % S(60))
        d.ellipse([bx - S(10), by - S(10), bx + S(10), by + S(10)], outline=(200, 230, 255), width=3)

def coffee_machine(d, x, y, s, t):
    S = lambda v: v * s
    for k in range(6):
        r = S(260 + k * 18 + 10 * math.sin(t * 3 + k))
        d.ellipse([x - r, y - r * 1.3, x + r, y + r * 1.3], outline=(120 + k * 10, 40, 160), width=4)
    d.rounded_rectangle([x - S(150), y - S(240), x + S(150), y + S(240)], int(S(20)), fill=(60, 50, 55), outline=BLK, width=6)
    d.rectangle([x - S(110), y - S(200), x + S(110), y - S(80)], fill=(20, 20, 25))
    for sx in (-1, 1):
        d.ellipse([x + sx * S(45) - S(22), y - S(160), x + sx * S(45) + S(22), y - S(120)], fill=(255, 40, 40))
    d.rectangle([x - S(70), y + S(40), x + S(70), y + S(150)], fill=(30, 25, 25))
    d.rounded_rectangle([x - S(40), y + S(90), x + S(40), y + S(150)], int(S(8)), fill=WHITE, outline=BLK, width=3)
    d.text((x, y + S(200)), "CAFÉ", font=F(S(48)), fill=WHITE, anchor="mm")

def ice_machine(d, x, y, s, t, glow=1.0):
    S = lambda v: v * s
    for k in range(8):
        a = -math.pi / 2 + (k - 3.5) * 0.12
        d.line([(x, y - S(900)), (x + math.cos(a) * S(1200), y - S(900) + math.sin(a + math.pi) * -S(1200))], fill=lc((10, 10, 14), (255, 250, 200), 0.25 * glow), width=int(S(30)))
    d.rounded_rectangle([x - S(200), y - S(380), x + S(200), y + S(200)], int(S(24)), fill=(230, 240, 250), outline=BLK, width=6)
    d.rectangle([x - S(160), y - S(330), x + S(160), y - S(230)], fill=(40, 120, 210))
    d.text((x, y - S(280)), "HIELO", font=F(S(70)), fill=WHITE, anchor="mm")
    ice(d, x, y - S(60), 1.4 * s)
    for k in range(4):
        sx, sy = x - S(220) + k * S(150), y - S(420) + (k % 2) * S(60); L = S(26) * (0.6 + 0.4 * math.sin(t * 6 + k))
        d.polygon([(sx, sy - L), (sx + L * 0.25, sy), (sx, sy + L), (sx - L * 0.25, sy)], fill=YEL)
        d.polygon([(sx - L, sy), (sx, sy - L * 0.25), (sx + L, sy), (sx, sy + L * 0.25)], fill=YEL)

def employee(d, x, y, s, t):
    guy(d, x, y, s, mood="scared", arms="down", look=-1, t=t * 2, hoodie=(90, 160, 90))
    S = lambda v: v * s
    hx, hy = x, y - S(505)
    for k in range(7):
        a = math.pi + k * 0.45
        d.line([(hx + math.cos(a) * S(90), hy - S(60) + math.sin(a) * S(60)), (hx + math.cos(a) * S(140), hy - S(80) + math.sin(a) * S(100))], fill=(55, 38, 28), width=int(S(10)))
    d.rounded_rectangle([x + S(110), y - S(330), x + S(200), y - S(220)], int(S(8)), fill=(230, 230, 230), outline=BLK, width=4)
    d.text((x + S(155), y - S(275)), "0", font=F(S(50)), fill=RED, anchor="mm")

CAPS = [
    (0.0, 3.5, "*Día 2* del apocalipsis zombi. Se acabó el agua"),
    (3.5, 8.0, "El peor error: confiar en que llegaría *el camión del agua*"),
    (8.0, 12.0, "*Regla 1:* no entres en pánico. *Revisa la bodega*"),
    (12.0, 17.0, "Si encuentras al repartidor zombi… *tienes un problema laboral*"),
    (17.0, 20.0, "*Regla 2:* busca *líquidos sellados*"),
    (20.0, 26.0, "Agua escondida: *hielo, el juguito de las latas* y el *tanque del calentador*"),
    (26.0, 33.0, "No te tomes nada del piso: *infección intestinal* + apocalipsis"),
    (33.0, 37.0, "*Regla 3:* si sales, *planea una ruta* y evita enfrentamientos"),
    (37.0, 41.0, "¿Agua dudosa? *Hiérvela 1 minuto completo*"),
    (41.0, 46.0, "Y el café de la máquina… *¿máquina o entidad del inframundo?*"),
    (46.0, 50.0, "Pero entonces… *escuchas algo detrás de ti*"),
    (50.0, 56.0, "Es el empleado… y *se acabaron los cigarros*"),
    (56.0, 61.0, "Los zombis no quieren entrar al minisúper…"),
    (61.0, 66.0, "Quieren llegar… *a la máquina de hielo*"),
]

def s1(t):
    if t < 3.5:
        img, d = store_day(t)
        fridge_empty(d, 120, 560, 420, 560, open_=ease(t / 0.8))
        guy(d, 700, FEET, 0.95, mood="scared", look=-1, t=t)
        d.text((330, 900), "VACÍO", font=F(70), fill=RED, anchor="mm", stroke_width=6, stroke_fill=WHITE)
        chip(d, "DÍA 2", 300, bg=RED, size=80, appear=t / 0.4)
        return img, 1.0, 1.0 + 0.04 * t / 3.5
    lt = t - 3.5
    img = outside_day(W, H); d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, W, 1350], fill=(90, 90, 95))
    for x in range(0, W, 160): d.rectangle([x, 1240, x + 80, 1255], fill=(240, 220, 80))
    truck(d, 540, 900, 1.3)
    d.text((540, 600), "?", font=F(200), fill=WHITE, anchor="mm", stroke_width=10, stroke_fill=BLK)
    if lt > 1.8:
        sc = pop((lt - 1.8) / 0.3)
        d.rounded_rectangle([540 - 330 * sc, 1110 - 90 * sc, 540 + 330 * sc, 1110 + 90 * sc], int(20 * sc), outline=RED, width=int(14 * sc) + 1)
        d.text((540, 1110), "NUNCA LLEGÓ", font=F(max(8, 80 * sc)), fill=RED, anchor="mm")
    return img, 1.0, 1.0, (1.8 < lt < 2.1)

def s2(t):
    lt = t - 8
    img = BG_BODEGA.copy(); d = ImageDraw.Draw(img)
    for yy in (700, 1000):
        d.rectangle([60, yy, 1020, yy + 24], fill=(150, 110, 70))
    chip(d, "REGLA 1: NO ENTRES EN PÁNICO", 300, bg=(30, 110, 210), size=50, appear=lt / 0.4)
    if lt < 4.0:
        for i in range(6):
            bottle(d, 200 + i * 130, 620, pop((lt - 0.4 - i * 0.1) / 0.3))
        guy(d, 300, 1350, 0.8, mood="neutral", t=t)
        if lt > 1.8: bigtext(d, "+ PROVISIONES", 640, 1150, int(70 * pop((lt - 1.8) / 0.3)), fill=YEL)
        return img, 1.0, 1.0
    zombie(d, 640, 1350, 1.0, t, face=-1)
    d.chord([560, 790, 740, 900], 180, 360, fill=(220, 50, 50))
    d.rectangle([530, 880, 760, 895], fill=(220, 50, 50))
    d.rounded_rectangle([380, 1000, 520, 1110], 8, fill=(200, 160, 100), outline=BLK, width=4)
    guy(d, 220, 1350, 0.8, mood="scared", t=t)
    if lt > 1.5:
        bigtext(d, "PROBLEMA LABORAL", 540, 560, int(70 * pop((lt - 1.5) / 0.3)), fill=YEL)
    return img, 1.0, 1.0

def s3(t):
    lt = t - 17
    img = BG_LAB.copy(); d = ImageDraw.Draw(img)
    chip(d, "REGLA 2: LÍQUIDOS SELLADOS", 300, bg=(40, 140, 80), size=52, appear=lt / 0.4)
    if lt < 3.0:
        for i in range(4):
            sc = pop((lt - 0.2 - i * 0.15) / 0.3)
            if i % 2: can(d, 250 + i * 190, 850, 1.3 * sc, [(240, 200, 60), (200, 60, 60)][i % 2])
            else: bottle(d, 250 + i * 190, 850, 1.6 * sc)
            if lt > 1.2: check(d, 250 + i * 190 + 60, 700, pop((lt - 1.2 - i * 0.1) / 0.3))
        return img, 1.0, 1.0
    if lt < 9.0:
        items = [(3.2, "Hielo", ice), (4.6, "Latas", can), (6.2, "Calentador", heater)]
        for k, (st, lab, fn) in enumerate(items):
            if lt < st: continue
            sc = pop((lt - st) / 0.35)
            cx = 200 + k * 340
            card(d, cx, 850, sc, lab)
            if fn is heater: fn(d, cx, 820, 0.7 * sc)
            elif fn is can: fn(d, cx, 820, 1.2 * sc)
            else: fn(d, cx, 820, 1.2 * sc)
        bigtext(d, "AGUA ESCONDIDA", 540, 520, int(70 * pop((lt - 3.0) / 0.3)), fill=(30, 110, 210), stroke=WHITE)
        return img, 1.0, 1.0
    d.ellipse([200, 1180, 700, 1300], fill=(140, 120, 70))
    xmark(d, 450, 1240, 0.7 * pop((lt - 9.3) / 0.3))
    guy(d, 760, 1350, 0.9, mood="scared", t=t * 3)
    if lt > 10.5:
        bigtext(d, "GLUGLU…", 760, 650, int(60 * pop((lt - 10.5) / 0.3)), fill=(120, 170, 60))
    return img, 1.0, 1.0

def s4(t):
    lt = t - 33
    img = BG_LAB.copy(); d = ImageDraw.Draw(img)
    chip(d, "REGLA 3: SI TIENES QUE SALIR", 300, bg=(220, 120, 40), size=50, appear=lt / 0.4)
    if lt < 4.0:
        d.rounded_rectangle([90, 450, 990, 1300], 30, fill=(235, 225, 195), outline=BLK, width=6)
        for (x, y) in [(400, 650), (650, 900), (350, 1050)]:
            d.text((x, y), "Z", font=F(80), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
        pts = [(180, 1220), (250, 900), (500, 780), (820, 700), (880, 520)]
        p = ease(lt / 2.5); n = max(2, int(p * 30))
        path = []
        for i in range(n):
            u = i / 29 * (len(pts) - 1); k = min(int(u), len(pts) - 2); f = u - k
            path.append((lerp(pts[k][0], pts[k + 1][0], f), lerp(pts[k][1], pts[k + 1][1], f)))
        for i in range(0, len(path) - 1, 2):
            d.line([path[i], path[i + 1]], fill=(30, 110, 210), width=12)
        d.text((880, 480), "AGUA", font=F(50), fill=(30, 110, 210), anchor="mm")
        return img, 1.0, 1.0
    if lt < 8.0:
        pot(d, 540, 900, 1.6, t)
        sec = min(60, int((lt - 4.0) / 3.5 * 60))
        d.rounded_rectangle([340, 470, 740, 600], 30, fill=BLK)
        d.text((540, 535), f"0:{sec:02d} / 1:00", font=F(64), fill=(90, 255, 140), anchor="mm")
        return img, 1.0, 1.0
    img = BG_DARK.copy(); d = ImageDraw.Draw(img)
    coffee_machine(d, 540, 880, 1.3, t)
    if lt > 9.5:
        bigtext(d, "¿?", 860, 520, int(120 * pop((lt - 9.5) / 0.3)), fill=(200, 120, 255))
    return img, 1.0, 1.0

def s5(t):
    lt = t - 46
    if lt < 4.0:
        img = BG_DARK.copy(); d = ImageDraw.Draw(img)
        guy(d, 380, 1350, 0.95, mood="scared", look=1, t=t)
        if lt > 1.5:
            for sx in (-1, 1):
                d.ellipse([820 + sx * 40 - 18, 760 - 18, 820 + sx * 40 + 18, 760 + 18], fill=(255, 240, 150))
        return img, 0.75, 1.0 + 0.05 * lt / 4
    img, d = store_day(t, zombies_at_door=True)
    employee(d, 760, FEET + 20, 0.95, t)
    guy(d, 300, FEET, 0.9, mood="neutral", look=1, t=t)
    if lt > 5.0:
        bigtext(d, "SIN CIGARROS", 760, 470, int(70 * pop((lt - 5.0) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0, (4.0 < lt < 4.3)

def s6(t):
    lt = t - 56
    img = BG_DARK.copy(); d = ImageDraw.Draw(img)
    if lt < 5.0:
        img, d = store_day(t, zombies_at_door=False)
        for i in range(3):
            zx = lerp(-150 - i * 170, 1250, ease((lt - i * 0.3) / 4.5))
            zombie(d, zx, FEET, 0.8, t + i, face=1)
        d.text((540, 520), "→", font=F(160), fill=YEL, anchor="mm", stroke_width=8, stroke_fill=BLK)
        return img, 1.0, 1.0
    l2 = lt - 5.0
    ice_machine(d, 540, 1000, 1.2, t, glow=ease(l2 / 1.0))
    for i in range(3):
        zombie(d, 140 + i * 400, 1380, 0.6, t + i, face=1 if i == 0 else -1, shade=0.6)
    if l2 > 2.2:
        sc = pop((l2 - 2.2) / 0.35)
        d.rounded_rectangle([540 - 470 * sc, 300 - 110 * sc, 540 + 470 * sc, 300 + 110 * sc], int(24 * sc), fill=RED, outline=WHITE, width=6)
        d.text((540, 265), "PARTE 3:", font=F(max(8, 50 * sc)), fill=WHITE, anchor="mm")
        d.text((540, 335), "¿QUIÉN CONTROLA EL HIELO?", font=F(max(8, 52 * sc)), fill=YEL, anchor="mm")
    return img, 1.0, 1.0, (0.0 < l2 < 0.35)

SCENES = [(0, 8, s1), (8, 17, s2), (17, 33, s3), (33, 46, s4), (46, 56, s5), (56, 70, s6)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img, b, z = r[0], r[1], r[2]
    shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce:
            rich_caption(d, txt, appear=(t - cs) / 0.25)
    if z > 1.001:
        cw, ch = W / z, H / z
        img = img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = b * (0.3 + 0.7 * fi)
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
        sheet.save("sheet_r8.png"); sys.exit()
    from warp8 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(69.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
