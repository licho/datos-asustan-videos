import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK)

FPS = 30
CG = (70, 140, 95)      # cthulhu green
CGD = (40, 90, 60)
GLOW = (255, 230, 60)
SEA_Y = 1050

def grad(top, bot, h=H):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / h))
    return img

def make_sea():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(SEA_Y):
        d.line([(0, y), (W, y)], fill=lc((10, 12, 35), (40, 45, 80), y / SEA_Y))
    rng = random.Random(1)
    for i in range(80):
        x, y, s = rng.uniform(0, W), rng.uniform(0, SEA_Y * 0.7), rng.uniform(1, 3.5)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(200, 200, 230))
    d.ellipse([760, 260, 940, 440], fill=(240, 235, 200))
    d.ellipse([800, 280, 960, 430], fill=lc((10, 12, 35), (40, 45, 80), 0.3))
    for y in range(SEA_Y, H):
        d.line([(0, y), (W, y)], fill=lc((20, 40, 70), (5, 12, 25), (y - SEA_Y) / (H - SEA_Y)))
    return img
SEA = make_sea()
BG_DARK = grad((12, 10, 20), (0, 0, 0))
BG_DEEP = grad((10, 40, 60), (2, 8, 15))

def waves(d, t, y=SEA_Y, col=(60, 90, 140)):
    for k in range(3):
        pts = [(x, y + k * 40 + math.sin(x / 70 + t * 2 + k) * 10) for x in range(0, W + 20, 20)]
        d.line(pts, fill=dk(col, 1 - k * 0.25), width=6)

def boat(d, x, y, s=1.0, t=0.0, with_guy=True, mood="neutral", tilt=0.0):
    bob = math.sin(t * 2.2) * 8 * s
    y = y + bob
    if with_guy:
        guy(d, x - 40 * s, y - 70 * s, 0.42 * s, mood=mood, t=t)
    d.line([(x + 60 * s, y - 70 * s), (x + 60 * s, y - 330 * s)], fill=(90, 60, 35), width=int(12 * s))
    d.polygon([(x + 66 * s, y - 320 * s), (x + 66 * s, y - 120 * s), (x + 200 * s, y - 130 * s)], fill=(235, 230, 215), outline=BLK)
    d.polygon([(x - 190 * s, y - 80 * s), (x + 200 * s, y - 80 * s), (x + 150 * s, y + 10 * s), (x - 150 * s, y + 10 * s)],
              fill=(160, 70, 45), outline=BLK)
    d.line([(x - 180 * s, y - 60 * s), (x + 190 * s, y - 60 * s)], fill=(235, 220, 190), width=int(8 * s))

def tentacle(d, x0, y0, length, ang, t, w0, col, phase=0.0, curl=1.0):
    pts = []; x, y = x0, y0; a = ang
    n = 14
    for i in range(n):
        pts.append((x, y))
        a += math.sin(t * 2.5 + phase + i * 0.45) * 0.12 * curl + 0.03 * curl
        x += math.cos(a) * length / n; y += math.sin(a) * length / n
    for i in range(n - 1):
        w = w0 * (1 - i / n) + 3
        d.line([pts[i], pts[i + 1]], fill=col, width=int(w))
        d.ellipse([pts[i][0] - w / 2, pts[i][1] - w / 2, pts[i][0] + w / 2, pts[i][1] + w / 2], fill=col)
    return pts

def cthulhu(d, x, y, s=1.0, t=0.0, eyes=1.0, wings=True, sleep=False, shade=1.0):
    C = lambda c: dk(c, shade)
    sway = math.sin(t * 1.2) * 12 * s
    x = x + sway
    if wings:
        for sx in (-1, 1):
            base = (x + sx * 150 * s, y + 40 * s)
            tip = (x + sx * 520 * s, y - 330 * s)
            pts = [base, tip]
            for k in range(4):
                pts.append((lerp(tip[0], x + sx * 230 * s, (k + 1) / 4) + sx * 20 * s * math.sin(k),
                            lerp(tip[1], y + 160 * s, (k + 1) / 4) - (0 if k % 2 else 60 * s)))
            d.polygon(pts, fill=C((30, 60, 45)), outline=BLK)
            d.line([base, tip], fill=C((20, 40, 30)), width=int(14 * s))
    # body
    d.rounded_rectangle([x - 190 * s, y + 60 * s, x + 190 * s, y + 520 * s], int(120 * s), fill=C(CGD), outline=BLK, width=max(3, int(8 * s)))
    # head
    d.ellipse([x - 230 * s, y - 330 * s, x + 230 * s, y + 140 * s], fill=C(CG), outline=BLK, width=max(3, int(8 * s)))
    for (a, b, r) in [(-120, -200, 30), (90, -240, 22), (140, -120, 18), (-60, -270, 16)]:
        d.ellipse([x + a * s - r * s, y + b * s - r * s, x + a * s + r * s, y + b * s + r * s], fill=C((90, 165, 115)))
    # face tentacles
    for i in range(7):
        ox = x + (-150 + i * 50) * s
        ang = math.pi / 2 + (i - 3) * 0.12
        tentacle(d, ox, y + 70 * s, 360 * s, ang, t, 46 * s, C((55, 120, 80)), phase=i * 0.8)
    # eyes
    for sx in (-1, 1):
        ex, ey = x + sx * 95 * s, y - 60 * s
        if sleep or eyes < 0.05:
            d.arc([ex - 50 * s, ey - 25 * s, ex + 50 * s, ey + 35 * s], 200, 340, fill=BLK, width=max(3, int(9 * s)))
        else:
            h = 42 * s * eyes
            d.ellipse([ex - 55 * s, ey - h, ex + 55 * s, ey + h], fill=GLOW, outline=BLK, width=max(3, int(6 * s)))
            d.ellipse([ex - 12 * s, ey - h * 0.85, ex + 12 * s, ey + h * 0.85], fill=BLK)
        d.line([(ex - 60 * s, ey - 70 * s - sx * 15 * s), (ex + 60 * s, ey - 70 * s + sx * 15 * s)], fill=BLK, width=max(3, int(12 * s)))

def bubbles(d, t, x0, x1, ybot, n=25, seed=3):
    rng = random.Random(seed)
    for i in range(n):
        age = (t * 0.8 + rng.random()) % 1.0
        bx = rng.uniform(x0, x1) + math.sin(t * 4 + i) * 10
        by = lerp(ybot, ybot - 260, age)
        r = rng.uniform(8, 22)
        d.ellipse([bx - r, by - r, bx + r, by + r], outline=(180, 220, 255), width=4)

def city(d, cx, base, s, t, col=(60, 75, 80)):
    rng = random.Random(6)
    for i in range(7):
        x = cx + (-330 + i * 110) * s
        h = rng.uniform(250, 520) * s; w = rng.uniform(70, 120) * s
        skew = rng.uniform(-70, 70) * s
        pts = [(x - w / 2, base), (x + w / 2, base), (x + w / 2 + skew, base - h), (x - w / 2 + skew * 0.3, base - h * 1.15)]
        d.polygon(pts, fill=col, outline=BLK)
        for k in range(3):
            wy = base - h * (0.3 + k * 0.22)
            d.polygon([(x - 12 * s + skew * (0.3 + k * 0.2), wy), (x + 18 * s + skew * (0.3 + k * 0.2), wy - 14 * s),
                       (x + 10 * s + skew * (0.3 + k * 0.2), wy + 26 * s)], fill=(140, 230, 160))

def book(d, cx, cy, s):
    d.polygon([(cx - 260 * s, cy - 150 * s), (cx, cy - 120 * s), (cx, cy + 180 * s), (cx - 260 * s, cy + 150 * s)], fill=(235, 225, 195), outline=BLK)
    d.polygon([(cx + 260 * s, cy - 150 * s), (cx, cy - 120 * s), (cx, cy + 180 * s), (cx + 260 * s, cy + 150 * s)], fill=(225, 215, 185), outline=BLK)
    d.text((cx - 130 * s, cy - 40 * s), "fhtagn", font=F(52 * s), fill=(120, 20, 20), anchor="mm")
    rng = random.Random(2)
    for side in (-1, 1):
        for k in range(5):
            y = cy + (20 + k * 26) * s
            x0 = cx + side * 40 * s; x1 = cx + side * 230 * s
            pts = [(lerp(x0, x1, j / 10), y + rng.uniform(-6, 6) * s) for j in range(11)]
            d.line(pts, fill=(90, 70, 60), width=max(2, int(5 * s)))

def eye_icon(d, cx, cy, s):
    d.ellipse([cx - 120 * s, cy - 60 * s, cx + 120 * s, cy + 60 * s], fill=WHITE, outline=BLK, width=8)
    d.ellipse([cx - 45 * s, cy - 45 * s, cx + 45 * s, cy + 45 * s], fill=(40, 120, 80))
    d.ellipse([cx - 18 * s, cy - 18 * s, cx + 18 * s, cy + 18 * s], fill=BLK)

def badge(d, n, sc):
    d.ellipse([140 - 80 * sc, 470 - 80 * sc, 140 + 80 * sc, 470 + 80 * sc], fill=YEL, outline=BLK, width=8)
    d.text((140, 470), str(n), font=F(max(8, 100 * sc)), fill=BLK, anchor="mm")

CAPS = [
    (0.0, 3.0, "Estás en un barco en medio del *Pacífico*…"),
    (3.0, 6.0, "…y el agua empieza a *burbujear*"),
    (6.0, 9.0, "Felicidades: acabas de encontrar a *Cthulhu*"),
    (9.0, 13.0, "Según Lovecraft, duerme en *R'lyeh*, una ciudad hundida"),
    (13.0, 16.0, "…y cuando sueña, la gente tiene *pesadillas*"),
    (16.0, 20.5, "Así sobrevives. *1:* no lo mires directo"),
    (20.5, 24.5, "*2:* no leas en voz alta nada que diga *“fhtagn”*"),
    (24.5, 28.5, "*3:* ¿ángulos que no deberían existir? *No entres*"),
    (28.5, 32.0, "*4:* embístelo con el barco"),
    (32.0, 35.5, "Funciona… *por un rato*"),
    (35.5, 41.0, "*5:* huye… y *no le cuentes a nadie*"),
    (41.0, 44.0, "Ah… y una cosa más: *no está muerto*"),
    (44.0, 47.0, "Solo está *soñando*"),
    (47.0, 52.0, "Y tú… acabas de aparecer *en su sueño*"),
]
STEPS = [16.5, 20.5, 24.5, 28.5, 35.5]

def s1(t):
    img = SEA.copy(); d = ImageDraw.Draw(img)
    rise = ease((t - 3.8) / 2.0)
    if t > 3.6:
        cthulhu(d, 560, lerp(SEA_Y + 450, SEA_Y + 60, rise), 1.0, t, eyes=rise, wings=False, shade=0.35)
        img.paste(SEA.crop((0, SEA_Y, W, H)), (0, SEA_Y)); d = ImageDraw.Draw(img)
        for i in range(3):
            tentacle(d, 120 + i * 420, SEA_Y + 40, 260 * rise, -math.pi / 2 + (i - 1) * 0.3, t, 40, (45, 100, 70), phase=i)
    waves(d, t)
    boat(d, 300, SEA_Y + 10, 1.0, t, mood="scared" if t > 3 else "neutral")
    if t > 2.6: bubbles(d, t, 450, 1000, SEA_Y + 20, n=int(cl((t - 2.6) / 1.5) * 30))
    return img, 1.0, 1.0 + 0.05 * t / 6, (4.5 < t < 5.2)

def s2(t):
    lt = t - 6
    img = SEA.copy(); d = ImageDraw.Draw(img)
    cthulhu(d, 540, 640, 1.15, t, eyes=1.0)
    img.paste(SEA.crop((0, SEA_Y + 60, W, H)), (0, SEA_Y + 60)); d = ImageDraw.Draw(img)
    waves(d, t, SEA_Y + 60)
    boat(d, 180, SEA_Y + 90, 0.6, t, mood="scared")
    chip(d, "CTHULHU", 300, bg=(40, 140, 80), size=72, appear=lt / 0.4)
    return img, 1.0, 1.0 + 0.08 * ease(lt / 3), (0.2 < lt < 0.6)

def s3(t):
    lt = t - 9
    img = BG_DEEP.copy(); d = ImageDraw.Draw(img)
    city(d, 540, 1200, 1.2, t)
    d.rectangle([0, 1200, W, H], fill=(10, 25, 35))
    cthulhu(d, 540, 760, 0.55, t, sleep=True, wings=False, shade=0.8)
    for k in range(3):
        zy = 560 - ((t * 60 + k * 60) % 180)
        d.text((660 + k * 40, zy), "Z", font=F(60 - k * 10), fill=WHITE, anchor="mm")
    d.rounded_rectangle([200, 380, 880, 460], 30, fill=BLK, outline=(140, 230, 160), width=5)
    d.text((540, 420), "R'LYEH · PACÍFICO SUR", font=F(40), fill=(140, 230, 160), anchor="mm")
    if lt > 4.0:
        sc = pop((lt - 4.0) / 0.4)
        for i, (bx, by) in enumerate([(230, 1310), (850, 1290)]):
            d.ellipse([bx - 110 * sc, by - 70 * sc, bx + 110 * sc, by + 70 * sc], fill=(60, 40, 90), outline=WHITE, width=4)
            d.text((bx, by), "!!", font=F(max(8, 60 * sc)), fill=RED, anchor="mm")
    return img, 1.0, 1.0 + 0.04 * lt / 7

def s4(t):
    lt = t - 16
    step = sum(1 for s in STEPS if t >= s)
    ls = t - STEPS[step - 1] if step else lt
    img = SEA.copy() if step in (0, 1, 4, 5) else BG_DARK.copy()
    d = ImageDraw.Draw(img)
    if step <= 1:
        cthulhu(d, 760, 620, 0.8, t, shade=0.5)
        img.paste(SEA.crop((0, SEA_Y, W, H)), (0, SEA_Y)); d = ImageDraw.Draw(img)
        waves(d, t)
        guy(d, 330, 1330, 1.0, mood="scared", arms="up" if int(t * 2) % 2 else "down", t=t)
        d.rounded_rectangle([230, 780, 430, 850], 20, fill=BLK)
        if ls > 0.6:
            sc = pop((ls - 0.6) / 0.3)
            eye_icon(d, 760, 1150, 0.8 * sc); xmark(d, 760, 1150, 0.55 * sc)
    elif step == 2:
        book(d, 540, 820, 1.4)
        if ls > 1.0: xmark(d, 540, 820, pop((ls - 1.0) / 0.25) * 1.3)
        if ls > 1.8: bigtext(d, "¡SHHH!", 540, 1180, int(110 * pop((ls - 1.8) / 0.3)), fill=YEL)
    elif step == 3:
        city(d, 540, 1250, 1.5, t, col=(70, 70, 85))
        if ls > 1.0:
            sc = pop((ls - 1.0) / 0.3)
            d.rounded_rectangle([540 - 300 * sc, 540 - 80 * sc, 540 + 300 * sc, 540 + 80 * sc], int(30 * sc), fill=RED, outline=WHITE, width=8)
            d.text((540, 540), "NO ENTRES", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
    elif step == 4:
        hit = 2.0
        if ls < hit + 0.1:
            cthulhu(d, 760, 640, 0.8, t, shade=0.9)
        else:
            rec = ease((ls - 3.6) / 2.5)
            rng = random.Random(4)
            for i in range(14):
                ang = rng.uniform(0, 2 * math.pi); dist = rng.uniform(80, 380) * (1 - rec)
                bx = 760 + math.cos(ang) * dist; by = 640 + math.sin(ang) * dist * 0.7
                r = rng.uniform(40, 90) * (1 - rec * 0.6)
                d.ellipse([bx - r, by - r, bx + r, by + r], fill=CG, outline=BLK, width=5)
            if rec > 0.3:
                cthulhu(d, 760, 640, 0.8 * rec, t, eyes=rec, shade=0.9)
        img.paste(SEA.crop((0, SEA_Y, W, H)), (0, SEA_Y)); d = ImageDraw.Draw(img)
        waves(d, t)
        bx = lerp(150, 620, ease(ls / hit)) if ls < hit else 620 - (ls - hit) * 40
        boat(d, bx, SEA_Y + 10, 1.0, t * 3, mood="scared")
        if hit < ls < hit + 0.8:
            bigtext(d, "¡SPLASH!", 640, 540, int(110 * pop((ls - hit) / 0.25)), fill=YEL)
        if ls > 4.0:
            bigtext(d, "…por un rato", 620, 1180, int(70 * pop((ls - 4.0) / 0.3)), fill=(150, 240, 170))
    else:
        cthulhu(d, 830, 600, 0.5, t, shade=0.5)
        img.paste(SEA.crop((0, SEA_Y, W, H)), (0, SEA_Y)); d = ImageDraw.Draw(img)
        waves(d, t)
        bx = lerp(600, 220, ease(ls / 1.5))
        boat(d, bx, SEA_Y + 10, 1.0, t * 4, mood="scared")
        for k in range(5):
            d.line([(bx + 200 + k * 40, SEA_Y - 20 + k * 8), (bx + 280 + k * 50, SEA_Y - 20 + k * 8)], fill=WHITE, width=5)
        if ls > 1.8:
            bigtext(d, "¡HUYE!", 540, 1200, int(130 * pop((ls - 1.8) / 0.3)), fill=RED, stroke=WHITE, sw=10)
    if step >= 1:
        badge(d, step, pop(ls / 0.3))
    chip(d, "TUTORIAL DE SUPERVIVENCIA", 300, bg=(40, 140, 80), appear=lt / 0.4)
    shake = step == 4 and 2.0 < ls < 2.4
    return img, 1.0, 1.0, shake

def s5(t):
    lt = t - 41
    img = BG_DARK.copy(); d = ImageDraw.Draw(img)
    open_ = ease((lt - 6.2) / 0.35)
    cthulhu(d, 540, 720, 1.2, t * 0.5, eyes=open_, sleep=open_ < 0.05, shade=0.55 + 0.4 * open_)
    if lt > 3.0 and lt < 6.2:
        for k in range(3):
            zy = 330 - ((t * 60 + k * 60) % 180)
            d.text((780 + k * 50, zy), "Z", font=F(80 - k * 12), fill=WHITE, anchor="mm")
    if lt > 5.0:
        sc = pop((lt - 5.0) / 0.4)
        for (bx, by, r) in [(330, 470, 22), (270, 400, 34)]:
            d.ellipse([bx - r * sc, by - r * sc, bx + r * sc, by + r * sc], fill=(230, 220, 255), outline=BLK, width=4)
        d.ellipse([60 - 0, 80, 60 + 400 * sc, 80 + 300 * sc], fill=(230, 220, 255), outline=BLK, width=6)
        if sc > 0.9:
            guy(d, 260, 340, 0.4, mood="scared", t=t)
    b = 0.9 if lt < 6.2 else 1.0
    shake = 6.2 < lt < 7.0
    fade = 1.0 - ease((lt - 10.4) / 0.6)
    return img, b * fade, 1.0 + (0.12 * ease((lt - 6.2) / 0.5) if lt > 6.2 else 0.03 * lt / 6), shake

def s6(t):
    lt = t - 52
    img = Image.new("RGB", (W, H), (8, 8, 10)); d = ImageDraw.Draw(img)
    sc = pop(lt / 0.4)
    bigtext(d, "¿Qué harías", 540, 650, int(90 * sc), fill=WHITE)
    bigtext(d, "TÚ?", 540, 790, int(150 * sc), fill=YEL)
    ay = 990 + 25 * math.sin(lt * 8)
    d.polygon([(470, ay), (610, ay), (540, ay + 90)], fill=RED, outline=WHITE)
    d.rectangle([512, ay - 90, 568, ay], fill=RED)
    if lt > 0.6:
        bigtext(d, "Comenta… si todavía puedes", 540, 1230, int(52 * pop((lt - 0.6) / 0.3)), fill=WHITE)
    if lt > 1.2:
        tentacle(d, -40, 1900, 520 * ease((lt - 1.2) / 1.5), -1.1, t, 70, (55, 120, 80), curl=1.4)
        tentacle(d, 1120, 1900, 520 * ease((lt - 1.4) / 1.5), -2.0, t, 70, (55, 120, 80), phase=2, curl=-1.4)
    return img, ease(lt / 0.3), 1.0

SCENES = [(0, 6, s1), (6, 9, s2), (9, 16, s3), (16, 41, s4), (41, 52, s5), (52, 60, s6)]

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
    if fn is not s6: b = b * (0.3 + 0.7 * fi)
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    if shake:
        k = int(t * FPS)
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1)
        arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r3.png"); sys.exit()
    from warp3 import v_of_T, DUR
    out = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(56.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
