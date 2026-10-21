import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)

FPS = 30
MITE = (232, 215, 185)

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

BG_NIGHT = grad((25, 30, 60), (10, 12, 25))
BG_MICRO = grad((60, 50, 80), (25, 20, 35))
BG_ROOM = grad((235, 232, 245), (200, 195, 215))
BG_SKY = grad((120, 190, 240), (210, 235, 250))
BG_DARK = grad((15, 12, 20), (0, 0, 0))

def mite(d, x, y, s=1.0, t=0.0, phase=0.0, mood="grin", shade=1.0, dizzy=False):
    S = lambda v: v * s
    C = lambda c: dk(c, shade)
    for sx in (-1, 1):
        for k in range(4):
            a = math.radians(-50 + k * 33) if sx > 0 else math.radians(230 - k * 33)
            wig = math.sin(t * 12 + phase + k) * 0.18
            x1, y1 = x + math.cos(a) * S(55), y + math.sin(a) * S(45)
            x2, y2 = x1 + math.cos(a + wig + 0.6 * sx) * S(55), y1 + math.sin(a + wig + 0.6 * sx) * S(55)
            d.line([(x1, y1), (x2, y2)], fill=C((150, 120, 90)), width=max(2, int(S(9))), joint="curve")
    d.ellipse([x - S(70), y - S(60), x + S(70), y + S(70)], fill=C(MITE), outline=BLK, width=max(2, int(S(5))))
    for k in range(3):
        d.arc([x - S(55), y - S(30) + k * S(28), x + S(55), y + S(10) + k * S(28)], 20, 160, fill=C((200, 180, 150)), width=max(1, int(S(4))))
    hx, hy = x, y - S(65)
    d.ellipse([hx - S(32), hy - S(26), hx + S(32), hy + S(26)], fill=C((210, 185, 150)), outline=BLK, width=max(2, int(S(4))))
    for sx in (-1, 1):
        ex, ey = hx + sx * S(13), hy - S(4)
        if dizzy:
            d.text((ex, ey), "x", font=F(max(8, S(22))), fill=BLK, anchor="mm")
        else:
            d.ellipse([ex - S(9), ey - S(10), ex + S(9), ey + S(10)], fill=WHITE, outline=BLK, width=max(1, int(S(2))))
            d.ellipse([ex - S(4), ey - S(3), ex + S(4), ey + S(6)], fill=BLK)
    if mood == "grin":
        d.arc([hx - S(14), hy + S(4), hx + S(14), hy + S(18)], 20, 160, fill=BLK, width=max(1, int(S(4))))
    elif mood == "scared":
        d.ellipse([hx - S(7), hy + S(6), hx + S(7), hy + S(20)], fill=BLK)
    elif mood == "chew":
        k = int(t * 10) % 2
        d.ellipse([hx - S(8), hy + S(6), hx + S(8), hy + S(12 + 8 * k)], fill=(90, 30, 30))

def flake(d, x, y, s):
    pts = [(x + math.cos(a) * s * (0.7 + 0.3 * math.sin(a * 3)), y + math.sin(a) * s * 0.6 * (0.7 + 0.3 * math.cos(a * 2))) for a in np.linspace(0, 2 * math.pi, 9)]
    d.polygon(pts, fill=(245, 225, 205), outline=(190, 160, 130))

def pellet(d, x, y, s):
    d.ellipse([x - s, y - s * 0.7, x + s, y + s * 0.7], fill=(110, 80, 55), outline=BLK)

def bed(d, cx, cy, s, t, sleeping=True):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(420), cy - S(80), cx + S(420), cy + S(120)], int(S(30)), fill=(120, 80, 60), outline=BLK, width=6)
    d.rounded_rectangle([cx - S(400), cy - S(140), cx + S(400), cy + S(30)], int(S(40)), fill=(240, 240, 250), outline=BLK, width=5)
    d.rounded_rectangle([cx - S(380), cy - S(210), cx - S(120), cy - S(110)], int(S(40)), fill=(250, 250, 255), outline=BLK, width=5)
    d.rounded_rectangle([cx - S(200), cy - S(150), cx + S(400), cy + S(20)], int(S(40)), fill=(90, 120, 200), outline=BLK, width=5)
    if sleeping:
        hx, hy = cx - S(250), cy - S(175)
        d.ellipse([hx - S(70), hy - S(70), hx + S(70), hy + S(70)], fill=SKIN, outline=BLK, width=4)
        d.chord([hx - S(74), hy - S(80), hx + S(74), hy + S(30)], 180, 360, fill=(55, 38, 28))
        for sx in (-1, 1):
            d.arc([hx + sx * S(26) - S(16), hy, hx + sx * S(26) + S(16), hy + S(18)], 200, 340, fill=BLK, width=4)
        for k in range(3):
            zy = hy - S(90) - ((t * 50 + k * 45) % 135)
            d.text((hx + S(80) + k * S(25), zy), "z", font=F(max(8, S(50) - k * 8)), fill=WHITE, anchor="mm")

def microscope_circle(img, cx, cy, R, t, n):
    lens = Image.new("RGB", (2 * R, 2 * R), (245, 240, 250)); ld = ImageDraw.Draw(lens)
    for i in range(0, 2 * R, 60):
        ld.line([(i, 0), (i + 120, 2 * R)], fill=(230, 225, 240), width=26)
    rng = random.Random(7)
    for i in range(14):
        flake(ld, rng.uniform(40, 2 * R - 40), rng.uniform(40, 2 * R - 40), rng.uniform(16, 30))
    for i in range(n):
        mx, my = rng.uniform(R * 0.35, R * 1.65), rng.uniform(R * 0.4, R * 1.7)
        mite(ld, mx + math.sin(t * 2 + i) * 8, my, rng.uniform(0.45, 0.7), t, i)
    mask = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(mask).ellipse([0, 0, 2 * R, 2 * R], fill=255)
    img.paste(lens, (int(cx - R), int(cy - R)), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - R - 16, cy - R - 16, cx + R + 16, cy + R + 16], outline=(40, 40, 50), width=32)

def washer(d, cx, cy, s, t):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(260), cy - S(300), cx + S(260), cy + S(300)], int(S(30)), fill=(240, 242, 246), outline=BLK, width=6)
    d.rectangle([cx - S(260), cy - S(300), cx + S(260), cy - S(200)], fill=(210, 215, 225), outline=BLK, width=5)
    d.ellipse([cx - S(190), cy - S(150), cx + S(190), cy + S(230)], fill=(160, 170, 185), outline=BLK, width=6)
    d.ellipse([cx - S(150), cy - S(110), cx + S(150), cy + S(190)], fill=(140, 200, 240))
    for k in range(4):
        a = t * 8 + k * math.pi / 2
        mite(d, cx + math.cos(a) * S(80), cy + S(40) + math.sin(a) * S(80), 0.35 * s, t, k, dizzy=True)
    d.rounded_rectangle([cx + S(60), cy - S(285), cx + S(240), cy - S(215)], int(S(14)), fill=RED)
    d.text((cx + S(150), cy - S(250)), "55°C", font=F(S(48)), fill=WHITE, anchor="mm")

def covers(d, cx, cy, s, t, ls):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(380), cy - S(60), cx + S(380), cy + S(140)], int(S(30)), fill=(70, 130, 210), outline=BLK, width=6)
    d.rounded_rectangle([cx - S(300), cy - S(200), cx + S(60), cy - S(80)], int(S(40)), fill=(70, 130, 210), outline=BLK, width=6)
    d.line([(cx - S(370), cy + S(30)), (cx + S(370), cy + S(30))], fill=(220, 220, 230), width=int(S(8)))
    d.text((cx, cy + S(80)), "ANTIÁCAROS", font=F(S(52)), fill=WHITE, anchor="mm")
    for k in range(3):
        bx = cx + S(-200 + k * 200); by = cy - S(260) - abs(math.sin(t * 5 + k)) * S(140)
        mite(d, bx, by, 0.4 * s, t, k, mood="scared")

def dehumidifier(d, cx, cy, s, t, ls):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(170), cy - S(300), cx + S(170), cy + S(300)], int(S(30)), fill=(245, 245, 248), outline=BLK, width=6)
    d.rounded_rectangle([cx - S(120), cy - S(250), cx + S(120), cy - S(130)], int(S(16)), fill=(20, 40, 30))
    val = int(lerp(80, 45, ease(ls / 2.0)))
    d.text((cx, cy - S(190)), f"{val}%", font=F(S(70)), fill=(90, 255, 140), anchor="mm")
    for k in range(6):
        d.line([(cx - S(120), cy - S(80) + k * S(30)), (cx + S(120), cy - S(80) + k * S(30))], fill=(190, 195, 205), width=int(S(8)))
    d.rounded_rectangle([cx - S(140), cy + S(150), cx + S(140), cy + S(280)], int(S(16)), fill=(150, 200, 240), outline=BLK, width=4)
    if ls > 1.5:
        for k in range(3):
            mite(d, cx + S(330), cy - S(120) + k * S(170), 0.42 * s, t, k, mood="scared", shade=lerp(1, 0.6, ease((ls - 1.5) / 2)))

def vacuum(d, cx, cy, s, t, ls):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(160), cy - S(140), cx + S(160), cy + S(140)], int(S(60)), fill=(230, 60, 80), outline=BLK, width=6)
    d.ellipse([cx - S(150), cy + S(90), cx - S(70), cy + S(170)], fill=(40, 40, 40))
    d.ellipse([cx + S(70), cy + S(90), cx + S(150), cy + S(170)], fill=(40, 40, 40))
    d.rounded_rectangle([cx - S(90), cy - S(60), cx + S(90), cy + S(0)], int(S(12)), fill=WHITE)
    d.text((cx, cy - S(30)), "HEPA", font=F(S(42)), fill=(230, 60, 80), anchor="mm")
    hx = cx - S(170)
    d.line([(hx, cy), (hx - S(200), cy - S(160)), (hx - S(380), cy - S(160))], fill=(60, 60, 70), width=int(S(26)), joint="curve")
    nx, ny = hx - S(380), cy - S(160)
    d.rounded_rectangle([nx - S(40), ny - S(50), nx + S(10), ny + S(50)], int(S(10)), fill=(60, 60, 70))
    rng = random.Random(3)
    for k in range(6):
        age = (ls * 1.2 + rng.random()) % 1.0
        mx = lerp(nx - S(250), nx - S(30), age) + math.sin(age * 12 + k) * S(30) * (1 - age)
        my = ny + rng.uniform(-150, 150) * s * (1 - age)
        mite(d, mx, my, 0.3 * s * (1 - age * 0.6), t, k, mood="scared")

def sun_pillow(d, t, ls):
    d.ellipse([760, 380, 980, 600], fill=(255, 215, 60))
    for k in range(12):
        a = k * math.pi / 6 + t * 0.4
        d.line([(870 + math.cos(a) * 140, 490 + math.sin(a) * 140), (870 + math.cos(a) * 190, 490 + math.sin(a) * 190)], fill=(255, 215, 60), width=12)
    d.line([(60, 720), (1020, 760)], fill=(90, 90, 90), width=6)
    d.rounded_rectangle([300, 720, 700, 900], 60, fill=WHITE, outline=BLK, width=6)
    for x in (380, 620):
        d.rectangle([x - 12, 700, x + 12, 750], fill=(200, 120, 60), outline=BLK)
    if ls > 0.8:
        for k in range(4):
            p = ease((ls - 0.8 - k * 0.15) / 1.4)
            mx = lerp(400 + k * 70, -120 + k * 60, p); my = lerp(820, 1150, p)
            mite(d, mx, my, 0.45, t, k, mood="scared")
        bigtext(d, "¡AY!", 240, 1000, int(70 * pop((ls - 0.8) / 0.3)), fill=YEL)
    d.rectangle([0, 1250, W, H], fill=(110, 170, 80))

def badge(d, n, sc):
    d.ellipse([140 - 80 * sc, 470 - 80 * sc, 140 + 80 * sc, 470 + 80 * sc], fill=YEL, outline=BLK, width=8)
    d.text((140, 470), str(n), font=F(max(8, 100 * sc)), fill=BLK, anchor="mm")

CAPS = [
    (0.0, 2.5, "Esta noche *no vas a dormir solo*…"),
    (2.5, 5.0, "…vas a dormir con *miles de ácaros*"),
    (5.0, 8.0, "Tan pequeños que no los ves… y comen *tu piel muerta*"),
    (8.0, 11.0, "Lo peor es *su popó*: hasta *20 bolitas al día*"),
    (11.0, 14.0, "Eso te da *alergia, estornudos y hasta asma*"),
    (14.0, 16.0, "¿Su clima favorito? *Calor y humedad*"),
    (16.0, 19.0, "O sea… *tu cama después de una noche sudando*"),
    (19.0, 24.5, "Así los sacas. *1:* lava sábanas y fundas cada semana a *55 °C* o más"),
    (24.5, 29.0, "*2:* fundas antiácaros en colchón y almohadas"),
    (29.0, 33.5, "*3:* humedad del cuarto *menor al 50%*"),
    (33.5, 37.5, "*4:* aspira con filtro *HEPA*"),
    (37.5, 43.0, "*5:* saca tu almohada *al sol*"),
    (43.0, 46.5, "¿Hace cuánto *no lavas tu almohada*?"),
    (46.5, 50.0, "Te leo en los comentarios… *mientras ellos te leen a ti*"),
]
STEPS = [20.0, 24.5, 29.0, 33.5, 37.5]

def s1(t):
    img = BG_NIGHT.copy(); d = ImageDraw.Draw(img)
    d.ellipse([780, 330, 920, 470], fill=(235, 235, 210))
    bed(d, 540, 1150, 1.0, t)
    if t > 2.0:
        p = ease((t - 2.0) / 0.7)
        R = int(lerp(40, 330, p))
        microscope_circle(img, lerp(290, 540, p), lerp(975, 700, p), R, t, int(p * 9))
        d = ImageDraw.Draw(img)
    return img, 1.0, 1.0 + 0.03 * t / 5, False

def s2(t):
    lt = t - 5
    img = BG_MICRO.copy(); d = ImageDraw.Draw(img)
    rng = random.Random(11)
    for i in range(12):
        flake(d, rng.uniform(80, 1000), rng.uniform(420, 1300), rng.uniform(30, 60))
    if lt < 3.0:
        mite(d, 540, 820, 2.2 * pop(lt / 0.4), t, mood="chew")
        flake(d, 700, 760, 70)
    elif lt < 6.0:
        mite(d, 420, 760, 1.8, t)
        n = min(20, int((lt - 3.0) * 8))
        for i in range(n):
            pellet(d, 620 + (i % 5) * 70, 840 + (i // 5) * 70, 26)
        bigtext(d, "x20", 820, 640, int(110 * pop((lt - 3.2) / 0.3)), fill=YEL)
    else:
        guy(d, 540, 1350, 1.0, mood="scared", t=t)
        if lt > 6.4:
            bigtext(d, "¡ACHÚ!", 540, 560, int(130 * pop((lt - 6.4) / 0.25)), fill=WHITE, stroke=RED, sw=12)
    chip(d, "¿QUÉ SON?", 300, bg=(150, 80, 200), appear=lt / 0.4)
    return img, 1.0, 1.0, (lt > 6.4 and lt < 6.9)

def s3(t):
    lt = t - 14
    img = BG_MICRO.copy(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([140, 520, 940, 820], 40, fill=(20, 30, 25), outline=WHITE, width=6)
    d.text((540, 610), "HUMEDAD", font=F(52), fill=(150, 220, 170), anchor="mm")
    d.text((540, 720), f"{int(lerp(50, 80, ease(lt / 1.5)))}%  ·  25 °C", font=F(80), fill=(90, 255, 140), anchor="mm")
    for i in range(5):
        mite(d, 160 + i * 190, 1150 + math.sin(t * 6 + i) * 30, 0.75, t, i)
    if lt > 2.0:
        for k in range(6):
            dy = (t * 200 + k * 60) % 300
            x = 200 + k * 140
            d.polygon([(x, 900 + dy), (x - 14, 930 + dy), (x + 14, 930 + dy)], fill=(120, 190, 255))
            d.ellipse([x - 14, 918 + dy, x + 14, 946 + dy], fill=(120, 190, 255))
    chip(d, "SU CLIMA FAVORITO", 300, bg=(220, 120, 40), appear=lt / 0.4)
    return img, 1.0, 1.0

def s4(t):
    lt = t - 19
    step = sum(1 for s in STEPS if t >= s)
    ls = t - STEPS[step - 1] if step else lt
    img = BG_SKY.copy() if step == 5 else BG_ROOM.copy()
    d = ImageDraw.Draw(img)
    if step <= 1: washer(d, 540, 900, 1.2, t)
    elif step == 2: covers(d, 540, 950, 1.2, t, ls)
    elif step == 3: dehumidifier(d, 470, 900, 1.2, t, ls)
    elif step == 4: vacuum(d, 860, 900, 1.0, t, ls)
    else: sun_pillow(d, t, ls)
    if step >= 1: badge(d, step, pop(ls / 0.3))
    chip(d, "SÁCALOS DE TU CAMA", 300, bg=(40, 140, 80), appear=lt / 0.4)
    return img, 1.0, 1.0

def s5(t):
    lt = t - 43
    img = BG_DARK.copy(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([140, 700, 940, 1100], 120, fill=(60, 60, 75), outline=(110, 110, 130), width=6)
    rng = random.Random(4)
    n = int(cl((lt - 0.5) / 2.0) * 16)
    for i in range(n):
        x, y = rng.uniform(220, 860), rng.uniform(760, 1040)
        blink = (int(t * 3 + i) % 7) == 0
        for sx in (-1, 1):
            if blink:
                d.line([(x + sx * 14 - 8, y), (x + sx * 14 + 8, y)], fill=(255, 240, 150), width=3)
            else:
                d.ellipse([x + sx * 14 - 8, y - 8, x + sx * 14 + 8, y + 8], fill=(255, 240, 150))
    if lt > 3.5:
        bigtext(d, "👀" if False else "TE ESTÁN LEYENDO", 540, 560, int(70 * pop((lt - 3.5) / 0.3)), fill=YEL)
    fade = 1.0 - ease((lt - 6.4) / 0.5)
    return img, fade, 1.0 + 0.05 * ease(lt / 6)

SCENES = [(0, 5, s1), (5, 14, s2), (14, 19, s3), (19, 43, s4), (43, 50, s5)]

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
        arr = np.roll(arr, ((k * 37) % 31) - 15, axis=1)
        arr = np.roll(arr, ((k * 53) % 31) - 15, axis=0)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r5.png"); sys.exit()
    from warp5 import v_of_T, DUR
    out = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(49.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
