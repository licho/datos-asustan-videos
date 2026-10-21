import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)
from reel2 import germ, phone, bottle, toilet_seat, person, GERMS

FPS = 30

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def make_bath():
    img = grad((210, 230, 235), (170, 195, 205)); d = ImageDraw.Draw(img)
    for y in range(240, 1300, 90):
        for x in range(0 if (y // 90) % 2 else -45, W, 90):
            d.rectangle([x, y, x + 86, y + 86], outline=(185, 205, 212), width=3)
    d.rectangle([0, 1300, W, H], fill=(150, 160, 170))
    return img
BATH = make_bath()
BG_ROOM = grad((28, 30, 42), (10, 10, 16))
BG_GERM = grad((20, 50, 30), (5, 18, 10))
BG_LAB = grad((235, 238, 242), (190, 198, 208))
BG_DARK = grad((12, 12, 18), (0, 0, 0))

def big_toilet(d, cx, base, s=1.0):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(150), base - S(620), cx + S(150), base - S(380)], int(S(30)), fill=(245, 247, 250), outline=BLK, width=6)
    d.rounded_rectangle([cx - S(60), base - S(600), cx + S(60), base - S(570)], int(S(10)), fill=(200, 205, 210))
    d.ellipse([cx - S(200), base - S(420), cx + S(200), base - S(240)], fill=(245, 247, 250), outline=BLK, width=6)
    d.ellipse([cx - S(140), base - S(395), cx + S(140), base - S(270)], fill=(150, 200, 230), outline=BLK, width=4)
    d.polygon([(cx - S(120), base - S(300)), (cx + S(120), base - S(300)), (cx + S(80), base), (cx - S(80), base)], fill=(240, 242, 245), outline=BLK)

def poop(d, cx, cy, s):
    S = lambda v: v * s
    for k, (w, h) in enumerate([(120, 50), (90, 45), (60, 40)]):
        y = cy - k * S(38)
        d.ellipse([cx - S(w), y - S(h), cx + S(w), y + S(h)], fill=(130, 85, 50), outline=BLK, width=4)
    d.polygon([(cx - S(15), cy - S(110)), (cx + S(10), cy - S(150)), (cx + S(20), cy - S(105))], fill=(130, 85, 50), outline=BLK)
    for sx in (-1, 1):
        d.ellipse([cx + sx * S(35) - S(18), cy - S(20) - S(20), cx + sx * S(35) + S(18), cy - S(20) + S(20)], fill=WHITE, outline=BLK, width=3)
        d.ellipse([cx + sx * S(35) - S(7), cy - S(22), cx + sx * S(35) + S(7), cy - S(8)], fill=BLK)
    d.arc([cx - S(30), cy - S(5), cx + S(30), cy + S(30)], 20, 160, fill=BLK, width=5)

def case_shape(d, cx, cy, s, col=(240, 110, 120), lift=0.0):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(175) + lift * S(60), cy - S(335) - lift * S(80), cx + S(175) + lift * S(60), cy + S(335) - lift * S(80)],
                        int(S(60)), outline=BLK, width=8, fill=None)
    d.rounded_rectangle([cx - S(172) + lift * S(60), cy - S(332) - lift * S(80), cx + S(172) + lift * S(60), cy + S(332) - lift * S(80)],
                        int(S(58)), outline=col, width=int(S(26)))

def port_zoom(img, cx, cy, R, t, clean=0.0, pick=None):
    lens = Image.new("RGB", (2 * R, 2 * R), (70, 72, 80)); ld = ImageDraw.Draw(lens)
    ld.rounded_rectangle([R * 0.25, R * 0.75, R * 1.75, R * 1.25], int(R * 0.25), fill=(20, 20, 24), outline=(150, 150, 160), width=10)
    ld.rounded_rectangle([R * 0.5, R * 0.93, R * 1.5, R * 1.07], int(R * 0.06), fill=(200, 170, 70))
    rng = random.Random(9)
    n = int(26 * (1 - clean))
    for i in range(n):
        x = rng.uniform(R * 0.35, R * 1.65); y = rng.uniform(R * 0.8, R * 1.2)
        r = rng.uniform(10, 26)
        ld.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=rng.choice([(200, 200, 205), (170, 160, 150), (120, 140, 190)]))
    if pick is not None:
        px = R * 0.3 + pick * R * 1.4
        ld.polygon([(px - 90, R * 0.83), (px + 40, R * 0.8), (px + 40, R * 0.86)], fill=(220, 180, 120), outline=BLK)
    mask = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(mask).ellipse([0, 0, 2 * R, 2 * R], fill=255)
    img.paste(lens, (int(cx - R), int(cy - R)), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14], outline=(60, 60, 70), width=28)

def badge(d, n, sc):
    d.ellipse([140 - 80 * sc, 470 - 80 * sc, 140 + 80 * sc, 470 + 80 * sc], fill=YEL, outline=BLK, width=8)
    d.text((140, 470), str(n), font=F(max(8, 100 * sc)), fill=BLK, anchor="mm")

CAPS = [
    (0.0, 2.5, "¿Me estás viendo *desde el baño*?"),
    (2.5, 5.0, "No te juzgo: *3 de cada 4* personas lo usan ahí"),
    (5.0, 8.5, "Al jalar, el agua lanza gérmenes que *aterrizan en tu pantalla*"),
    (8.5, 11.5, "*1 de cada 6* celulares tenía *E. coli*"),
    (11.5, 13.0, "Sí… *de la popó*"),
    (13.0, 17.0, "Bajo la funda: *sudor, grasa y migas*"),
    (17.0, 20.0, "Y en el puerto: *pelusa* que no te deja cargar"),
    (20.0, 23.0, "Así lo limpias. *1:* apágalo y desconéctalo"),
    (23.0, 27.0, "*2:* quita la funda y límpiala *por dentro y por fuera*"),
    (27.0, 31.0, "*3:* paño con *alcohol isopropílico al 70%*. Nada de cloro"),
    (31.0, 35.0, "Pásalo *3 veces*: una sola pasada *deja la mayoría*"),
    (35.0, 41.0, "*4:* el puerto, *en seco*: palillo de madera, suave y por los lados"),
    (41.0, 47.0, "*5:* deja de llevarlo al baño"),
    (47.0, 52.0, "¿Lo vas a limpiar hoy… *o sigues en el baño*? Comenta"),
]
STEPS = [20.5, 23.0, 27.0, 35.0, 41.0]

def s1(t):
    img = BATH.copy(); d = ImageDraw.Draw(img)
    if t < 2.5:
        big_toilet(d, 540, 1330, 1.0)
        phone(d, 760, 900, 0.75, glow=1.0)
        d.ellipse([835, 640, 865, 670], fill=RED if int(t * 2) % 2 else (120, 20, 20))
    else:
        for i in range(4):
            x = 210 + i * 220
            person(d, x, 900, 1.6 * pop((t - 2.5 - i * 0.1) / 0.3), (90, 140, 220) if i < 3 else (160, 165, 175))
            if i < 3 and t > 3.0:
                d.rounded_rectangle([x + 40, 780, x + 80, 850], 8, fill=(30, 30, 35))
        bigtext(d, "3 de cada 4", 540, 1130, int(100 * pop((t - 2.8) / 0.3)), fill=YEL)
    chip(d, "● EN VIVO DESDE EL BAÑO", 300, bg=RED, size=50, appear=t / 0.4)
    return img, 1.0, 1.0

def s2(t):
    lt = t - 5
    if lt < 3.5:
        img = BATH.copy(); d = ImageDraw.Draw(img)
        big_toilet(d, 330, 1330, 0.9)
        phone(d, 840, 820, 0.6, glow=1.0)
        rng = random.Random(2)
        for i in range(24):
            st = rng.uniform(0, 1.6)
            p = cl((lt - st) / 1.6)
            if p <= 0: continue
            x = lerp(330 + rng.uniform(-80, 80), 840 + rng.uniform(-80, 80), p)
            y = lerp(1000, 820 + rng.uniform(-150, 150), p) - math.sin(p * math.pi) * 350
            if p < 1: d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(110, 170, 230))
            else: germ(d, x, y, 22, GERMS[i % 3], t, i)
        bigtext(d, "SLOW MO", 900, 470, 44, fill=WHITE, stroke=BLK)
        return img, 1.0, 1.0
    img = BG_LAB.copy(); d = ImageDraw.Draw(img)
    if lt < 6.5:
        for i in range(6):
            r_, c_ = divmod(i, 3)
            cx, cy = 260 + c_ * 280, 650 + r_ * 450
            sc = pop((lt - 3.5 - i * 0.08) / 0.3)
            phone(d, cx, cy, 0.5 * sc, glow=1.0)
            if i == 4 and lt > 4.5:
                d.rounded_rectangle([cx - 100, cy - 190, cx + 100, cy + 190], 30, outline=RED, width=10)
                germ(d, cx, cy, 55, "ecoli", t)
        bigtext(d, "1 de cada 6", 540, 420, int(100 * pop((lt - 3.6) / 0.3)), fill=RED, stroke=WHITE, sw=10)
    else:
        poop(d, 540, 950, 1.8 * pop((lt - 6.5) / 0.35))
        bigtext(d, "¡ASCO!", 540, 520, int(120 * pop((lt - 6.8) / 0.3)), fill=YEL)
    return img, 1.0, 1.0, (6.5 < lt < 6.9)

def s3(t):
    lt = t - 13
    if lt < 4.0:
        img = BG_ROOM.copy(); d = ImageDraw.Draw(img)
        lift = ease((lt - 0.5) / 0.8)
        phone(d, 540, 880, 1.1, glow=0.6)
        if lift > 0.3:
            rng = random.Random(6)
            for i in range(12):
                x, y = rng.uniform(380, 700), rng.uniform(560, 1200)
                germ(d, x, y, rng.uniform(28, 40), GERMS[i % 3], t * 2, i)
            for i in range(30):
                x, y = 540 + rng.uniform(-300, 300), 880 + rng.uniform(-420, 420) + (t * 120 + i * 30) % 80
                d.rectangle([x, y, x + 12, y + 18], fill=rng.choice([YEL, RED, (90, 200, 240), (120, 220, 120)]))
        case_shape(d, 540, 880, 1.1, lift=lift)
        if lt > 1.5:
            bigtext(d, "FIESTA BAJO LA FUNDA", 540, 420, int(60 * pop((lt - 1.5) / 0.3)), fill=YEL)
        return img, 1.0, 1.0
    img = BG_ROOM.copy(); d = ImageDraw.Draw(img)
    phone(d, 300, 1000, 0.7, glow=0.5)
    port_zoom(img, 650, 760, 280, t)
    d = ImageDraw.Draw(img)
    d.line([(300, 1225), (480, 960)], fill=(90, 90, 100), width=8)
    bigtext(d, "PUERTO DE CARGA", 650, 380, 56, fill=WHITE)
    return img, 1.0, 1.0

def s4(t):
    lt = t - 20
    step = sum(1 for s in STEPS if t >= s)
    ls = t - STEPS[step - 1] if step else lt
    img = BG_DARK.copy() if step <= 1 else BG_LAB.copy()
    d = ImageDraw.Draw(img)
    if step <= 1:
        off = ease((ls - 0.6) / 0.5)
        phone(d, 540, 880, 1.1, glow=1 - off)
        sep = ease((ls - 1.2) / 0.5) * 140
        d.line([(540, 1250 + sep), (540, 1380)], fill=(220, 220, 225), width=26)
        d.rounded_rectangle([510, 1240 + sep, 570, 1300 + sep], 10, fill=(220, 220, 225), outline=BLK, width=4)
        if off > 0.5:
            d.ellipse([480, 820, 600, 940], outline=WHITE, width=10)
            d.line([(540, 800), (540, 870)], fill=WHITE, width=10)
    elif step == 2:
        case_shape(d, 380, 900, 0.9, col=(240, 110, 120))
        sx = 380 + math.sin(ls * 6) * 120
        d.rounded_rectangle([sx - 90, 820, sx + 90, 940], 30, fill=(250, 220, 80), outline=BLK, width=5)
        rng = random.Random(3)
        for i in range(14):
            age = (ls * 0.8 + rng.random()) % 1.0
            bx = 380 + rng.uniform(-220, 220); by = lerp(1150, 600, age); r = rng.uniform(14, 30)
            d.ellipse([bx - r, by - r, bx + r, by + r], outline=(160, 210, 255), width=4)
        phone(d, 840, 880, 0.55, glow=0.3)
        d.text((840, 1150), "aparte", font=F(46), fill=(40, 40, 40), anchor="mm")
    elif step == 3:
        phone(d, 430, 880, 0.95, glow=0.25)
        wipes = min(3, int(ls / 1.3) + 1)
        wx = lerp(300, 560, (math.sin(ls * 4.8) + 1) / 2)
        d.rounded_rectangle([wx - 110, 760, wx + 110, 900], 30, fill=(250, 250, 255), outline=BLK, width=5)
        bottle(d, 880, 640, 0.9)
        rng = random.Random(5)
        left = [12, 7, 2][wipes - 1]
        for i in range(left):
            germ(d, 330 + rng.uniform(0, 200), 650 + rng.uniform(0, 460), 22, GERMS[i % 3], t, i)
        d.text((880, 900), f"x{wipes}", font=F(90), fill=YEL, anchor="mm", stroke_width=8, stroke_fill=BLK)
        if ls > 4.0:
            sc = pop((ls - 4.0) / 0.3)
            d.rounded_rectangle([700, 1010, 1060, 1150], 30, fill=(40, 170, 80), outline=BLK, width=5)
            d.text((880, 1080), "-88%", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
        if 1.5 < ls < 4.0:
            d.rounded_rectangle([700, 1010, 1060, 1150], 30, fill=(255, 235, 235), outline=RED, width=5)
            d.text((880, 1080), "NO cloro", font=F(56), fill=RED, anchor="mm")
    elif step == 4:
        p = (math.sin(ls * 2.2) + 1) / 2
        port_zoom(img, 540, 820, 360, t, clean=ease(ls / 5.0), pick=p)
        d = ImageDraw.Draw(img)
        if ls > 2.5:
            for i, lab in enumerate(["NO metal", "NO líquidos"]):
                x = 300 + i * 480
                d.rounded_rectangle([x - 190, 1230, x + 190, 1330], 26, fill=(255, 235, 235), outline=RED, width=5)
                d.text((x, 1280), lab, font=F(50), fill=RED, anchor="mm")
    else:
        big_toilet(d, 540, 1330, 1.0)
        phone(d, 820, 780, 0.55, glow=1.0)
        if ls > 0.5:
            sc = pop((ls - 0.5) / 0.35)
            d.ellipse([540 - 330 * sc, 900 - 330 * sc, 540 + 330 * sc, 900 + 330 * sc], outline=RED, width=int(40 * sc) + 1)
            d.line([(540 - 230 * sc, 900 - 230 * sc), (540 + 230 * sc, 900 + 230 * sc)], fill=RED, width=int(40 * sc) + 1)
        if ls > 2.5:
            bigtext(d, "JAJAJA", 540, 500, int(90 * pop((ls - 2.5) / 0.3)), fill=YEL)
    if step >= 1:
        badge(d, step, pop(ls / 0.3))
    chip(d, "LÍMPIALO BIEN", 300, bg=(30, 110, 210), appear=lt / 0.4)
    return img, 1.0, 1.0

def s5(t):
    lt = t - 47
    img = Image.new("RGB", (W, H), (8, 8, 10)); d = ImageDraw.Draw(img)
    sc = pop(lt / 0.4)
    bigtext(d, "¿Lo limpias hoy…", 540, 650, int(80 * sc), fill=WHITE)
    bigtext(d, "o sigues", 540, 780, int(90 * sc), fill=WHITE)
    bigtext(d, "EN EL BAÑO?", 540, 900, int(110 * sc), fill=YEL)
    ay = 1060 + 25 * math.sin(lt * 8)
    d.polygon([(470, ay), (610, ay), (540, ay + 90)], fill=RED, outline=WHITE)
    d.rectangle([512, ay - 90, 568, ay], fill=RED)
    if lt > 1.0:
        bigtext(d, "PARTE 2 de: tu teclado", 540, 380, int(44 * pop((lt - 1.0) / 0.3)), fill=(170, 170, 170), sw=4)
    return img, ease(lt / 0.3), 1.0

SCENES = [(0, 5, s1), (5, 13, s2), (13, 20, s3), (20, 47, s4), (47, 52, s5)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img, b, z = r[0], r[1], r[2]
    shake = r[3] if len(r) > 3 else False
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce and fn is not s5:
            rich_caption(d, txt, appear=(t - cs) / 0.25)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    if fn is not s5: b = b * (0.3 + 0.7 * fi)
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
        sheet.save("sheet_r7.png"); sys.exit()
    from warp7 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(51.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
