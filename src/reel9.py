import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN, FEET)

FPS = 30

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def make_street():
    img = grad((15, 18, 40), (30, 32, 55)); d = ImageDraw.Draw(img)
    rng = random.Random(2)
    for i in range(60):
        x, y, s = rng.uniform(0, W), rng.uniform(0, 700), rng.uniform(1, 3)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(200, 200, 230))
    for x0, h in [(-40, 520), (220, 640), (520, 480), (760, 600)]:
        d.rectangle([x0, 1150 - h, x0 + 260, 1150], fill=(25, 28, 45))
        for wy in range(1150 - h + 40, 1120, 90):
            for wx in range(x0 + 30, x0 + 230, 70):
                if rng.random() < 0.3: d.rectangle([wx, wy, wx + 34, wy + 44], fill=(240, 210, 120))
    d.rectangle([0, 1150, W, H], fill=(55, 55, 65))
    return img
STREET = make_street()

def make_room(dark=False):
    img = grad((205, 185, 160), (165, 145, 125)) if not dark else grad((45, 40, 55), (20, 18, 28))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, W, H], fill=(120, 85, 60) if not dark else (40, 30, 25))
    d.rectangle([680, 380, 960, 700], fill=(25, 30, 60), outline=(240, 235, 225), width=14)
    d.line([(820, 380), (820, 700)], fill=(240, 235, 225), width=10)
    d.ellipse([860, 410, 920, 470], fill=(235, 235, 210))
    d.line([(150, 1150), (150, 700)], fill=(60, 50, 40), width=10)
    d.polygon([(90, 700), (210, 700), (180, 600), (120, 600)], fill=(250, 220, 150) if not dark else (90, 80, 60))
    return img
ROOM = make_room(); ROOM_DARK = make_room(True)
BG_LAB = grad((235, 238, 242), (190, 198, 208))
BG_DARK = grad((10, 10, 14), (0, 0, 0))

def sofa(d, cx, y, s=1.0):
    S = lambda v: v * s
    d.rounded_rectangle([cx - S(330), y - S(330), cx + S(330), y - S(130)], int(S(50)), fill=(110, 60, 80), outline=BLK, width=6)
    d.rounded_rectangle([cx - S(380), y - S(200), cx + S(380), y - S(40)], int(S(50)), fill=(130, 70, 95), outline=BLK, width=6)
    for sx in (-1, 1):
        d.rectangle([cx + sx * S(330) - S(20), y - S(40), cx + sx * S(330) + S(20), y], fill=(60, 40, 30))

def doppel(d, x, y, s, t, mood="smile", glow=1.0, point=False):
    guy(d, x, y, s, mood="neutral", arms="up" if point else "down", look=0, t=t)
    S = lambda v: v * s
    hx, hy = x, y - S(505)
    for sx in (-1, 1):
        ex, ey = hx + sx * S(38), hy + S(5)
        d.ellipse([ex - S(27), ey - S(27), ex + S(27), ey + S(27)], fill=WHITE, outline=BLK, width=max(2, int(S(4))))
        r = S(5)
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=lc((0, 0, 0), (230, 40, 40), glow))
    d.rectangle([hx - S(45), hy + S(28), hx + S(45), hy + S(70)], fill=SKIN)
    d.chord([hx - S(55), hy + S(20), hx + S(55), hy + S(80)], 0, 180, fill=WHITE, outline=BLK, width=max(2, int(S(4))))
    for k in range(1, 6):
        tx = hx - S(55) + k * S(18.3)
        d.line([(tx, hy + S(50)), (tx, hy + S(78))], fill=(180, 180, 180), width=2)
    d.line([(hx - S(40), hy - S(35)), (hx - S(12), hy - S(48))], fill=(55, 38, 28), width=max(2, int(S(7))))
    d.line([(hx + S(12), hy - S(48)), (hx + S(40), hy - S(35))], fill=(55, 38, 28), width=max(2, int(S(7))))

def scar(d, x, y, s):
    d.line([(x - 18 * s, y - 14 * s), (x + 18 * s, y + 14 * s)], fill=(190, 90, 80), width=max(2, int(6 * s)))
    for k in (-1, 0, 1):
        cx, cy = x + k * 10 * s, y + k * 8 * s
        d.line([(cx - 8 * s, cy + 6 * s), (cx + 8 * s, cy - 6 * s)], fill=(190, 90, 80), width=max(1, int(4 * s)))

def dna(d, x, y, h, t, col1=(90, 160, 240), col2=(240, 120, 160)):
    for i in range(24):
        yy = y - h / 2 + i * h / 23
        a = t * 2 + i * 0.5
        x1, x2 = x + math.sin(a) * 70, x - math.sin(a) * 70
        d.line([(x1, yy), (x2, yy)], fill=(200, 200, 210), width=4)
        d.ellipse([x1 - 10, yy - 10, x1 + 10, yy + 10], fill=col1)
        d.ellipse([x2 - 10, yy - 10, x2 + 10, yy + 10], fill=col2)

def phone_small(d, x, y, s, glow=1.0, content=None):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(80), y - S(150), x + S(80), y + S(150)], int(S(22)), fill=(20, 20, 24), outline=(90, 90, 100), width=5)
    d.rounded_rectangle([x - S(68), y - S(134), x + S(68), y + S(134)], int(S(14)), fill=lc((10, 10, 20), (60, 120, 200), glow))
    if content == "video":
        d.text((x, y - S(60)), "DATOS QUE", font=F(S(22)), fill=WHITE, anchor="mm")
        d.text((x, y - S(30)), "ASUSTAN", font=F(S(26)), fill=YEL, anchor="mm")
        d.ellipse([x - S(30), y + S(10), x + S(30), y + S(70)], fill=(240, 120, 40))

CAPS = [
    (0.0, 3.0, "Si ves a alguien *idéntico a ti*… *no le preguntes quién es*"),
    (3.0, 6.0, "Podría estar esperando *que tú se lo digas*"),
    (6.0, 10.0, "Llegas a tu casa… *y ahí estás tú*"),
    (10.0, 14.0, "Misma cara, misma voz… *hasta tu cicatriz*"),
    (14.0, 18.0, "Pero hay un problema: *tú nunca habías estado ahí*"),
    (18.0, 25.0, "Estudio de 2022: *9 parejas de \"dobles\"* sin parentesco compartían *miles de variantes genéticas*"),
    (25.0, 30.0, "*Regla 1:* no te acerques. *Mantén la distancia*"),
    (30.0, 35.0, "Aunque diga que es tu *gemelo perdido*…"),
    (35.0, 40.0, "Tu mamá *no tuvo presupuesto para dos*"),
    (40.0, 46.0, "*Regla 2:* no le reveles *información personal*"),
    (46.0, 48.0, "Podría saberlo *de alguna forma*…"),
    (48.0, 51.0, "…o es una criatura *muy comprometida con su papel*"),
    (51.0, 55.0, "Y eso es *todavía más preocupante*"),
    (55.0, 58.0, "*Regla 3:* aléjate y *pide ayuda*"),
    (58.0, 61.0, "No investigues si *respira* o si *sangra*"),
    (61.0, 68.0, "No eres detective. *No te pagan lo suficiente*"),
    (68.0, 76.0, "Si dice que *TÚ eres el impostor*… *no te quedes a discutir*"),
    (76.0, 84.0, "Si alguien idéntico a ti *está viendo este video*…"),
    (84.0, 88.0, "…al menos *uno de los dos* ya sabe qué hacer"),
    (88.0, 95.0, "Sígueme para más *manuales de supervivencia*"),
]

def s1(t):
    img = STREET.copy(); d = ImageDraw.Draw(img)
    lamp = (880, 520)
    d.line([(lamp[0], 1150), (lamp[0], lamp[1])], fill=(70, 70, 80), width=14)
    d.polygon([(lamp[0] - 260, 1180), (lamp[0] + 220, 1180), (lamp[0] + 30, lamp[1] + 20), (lamp[0] - 30, lamp[1] + 20)], fill=(60, 58, 50))
    d.ellipse([lamp[0] - 40, lamp[1] - 20, lamp[0] + 40, lamp[1] + 30], fill=(255, 230, 150))
    guy(d, 260, FEET, 0.9, mood="scared" if t > 1.0 else "neutral", look=1, t=t)
    doppel(d, 820, FEET, 0.9, t, glow=ease((t - 2.5) / 1.0))
    return img, 1.0, 1.0 + 0.05 * t / 6

def s2(t):
    lt = t - 6
    img = ROOM.copy(); d = ImageDraw.Draw(img)
    sofa(d, 640, 1180, 0.9)
    doppel(d, 640, FEET + 40, 0.85, t, glow=0.3)
    if lt < 9.5:
        guy(d, 170, FEET + 40, 0.85, mood="scared" if lt > 1.0 else "neutral", look=1, t=t)
    if 5.5 < lt < 9.5:
        sc = pop((lt - 5.5) / 0.35)
        for (cx, cy) in [(240, 610), (720, 590)]:
            d.ellipse([cx - 110 * sc, cy - 110 * sc, cx + 110 * sc, cy + 110 * sc], fill=SKIN, outline=YEL, width=8)
            scar(d, cx, cy, 2.6 * sc)
        bigtext(d, "=", 480, 600, int(110 * sc), fill=YEL)
    if lt > 9.5:
        bigtext(d, "TÚ NUNCA ESTUVISTE AQUÍ", 540, 460, int(58 * pop((lt - 9.5) / 0.3)), fill=RED, stroke=WHITE, sw=8)
    return img, 1.0, 1.0, (9.5 < lt < 9.9)

def s3(t):
    lt = t - 18
    img = BG_LAB.copy(); d = ImageDraw.Draw(img)
    for i, cx in enumerate((300, 780)):
        d.ellipse([cx - 150, 420, cx + 150, 720], fill=SKIN, outline=BLK, width=6)
        d.chord([cx - 155, 405, cx + 155, 640], 180, 360, fill=(55, 38, 28))
        for sx in (-1, 1): d.ellipse([cx + sx * 55 - 18, 560 - 18, cx + sx * 55 + 18, 560 + 18], fill=BLK)
        sy = 420 + ((lt * 260 + i * 80) % 300)
        d.line([(cx - 160, sy), (cx + 160, sy)], fill=(40, 200, 120), width=6)
    if lt > 1.0:
        bigtext(d, "MATCH", 540, 790, int(80 * pop((lt - 1.0) / 0.3)), fill=(40, 200, 120))
    dna(d, 300, 990, 260, t); dna(d, 780, 990, 260, t)
    if lt > 2.5:
        sc = pop((lt - 2.5) / 0.3)
        d.rounded_rectangle([540 - 240 * sc, 1200 - 60 * sc, 540 + 240 * sc, 1200 + 60 * sc], int(24 * sc), fill=YEL, outline=BLK, width=6)
        d.text((540, 1200), "9 PAREJAS", font=F(max(8, 66 * sc)), fill=BLK, anchor="mm")
    chip(d, "ESTUDIO REAL · 2022", 300, bg=(40, 140, 80), appear=lt / 0.4)
    return img, 1.0, 1.0

def s4(t):
    lt = t - 25
    img = ROOM.copy(); d = ImageDraw.Draw(img)
    gx = lerp(420, 170, ease(lt / 2.0))
    guy(d, gx, FEET + 40, 0.8, mood="scared", look=1, t=t)
    doppel(d, 820, FEET + 40, 0.8, t, glow=0.2, point=(lt > 5 and int(t * 2) % 2 == 0))
    y = 760 if lt < 10.0 else 10000
    d.line([(gx + 120, y), (700, y)], fill=YEL, width=10)
    d.polygon([(gx + 120, y), (gx + 150, y - 22), (gx + 150, y + 22)], fill=YEL)
    d.polygon([(700, y), (670, y - 22), (670, y + 22)], fill=YEL)
    bigtext(d, "DISTANCIA", (gx + 820) / 2, y - 70, 50, fill=WHITE)
    if lt > 5.0 and lt < 10.0:
        d.rounded_rectangle([600, 420, 1040, 540], 30, fill=WHITE, outline=BLK, width=5)
        d.text((820, 480), "¡Soy tu gemelo!", font=F(46), fill=(30, 30, 30), anchor="mm")
    if lt > 10.0:
        sc = pop((lt - 10.0) / 0.35)
        cx, cy = 540, 560
        for lx in (-80, -30, 30, 80):
            d.rectangle([cx + lx * sc - 18 * sc, cy + 80 * sc, cx + lx * sc + 18 * sc, cy + 140 * sc], fill=(225, 130, 150), outline=BLK, width=5)
        d.ellipse([cx - 170 * sc, cy - 120 * sc, cx + 170 * sc, cy + 120 * sc], fill=(240, 150, 170), outline=BLK, width=6)
        d.polygon([(cx - 90 * sc, cy - 100 * sc), (cx - 50 * sc, cy - 170 * sc), (cx - 30 * sc, cy - 110 * sc)], fill=(240, 150, 170), outline=BLK)
        d.ellipse([cx + 140 * sc, cy - 40 * sc, cx + 210 * sc, cy + 40 * sc], fill=(225, 120, 145), outline=BLK, width=5)
        for ny in (-14, 14): d.ellipse([cx + 168 * sc, cy + ny * sc - 8 * sc, cx + 184 * sc, cy + ny * sc + 8 * sc], fill=BLK)
        d.ellipse([cx + 70 * sc, cy - 50 * sc, cx + 96 * sc, cy - 24 * sc], fill=BLK)
        d.rectangle([cx - 50 * sc, cy - 112 * sc, cx + 50 * sc, cy - 98 * sc], fill=BLK)
        d.text((cx - 20, cy + 10), "$1", font=F(max(8, 60 * sc)), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
        d.text((540, 790), "PRESUPUESTO: 1 HIJO", font=F(max(8, 48 * sc)), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    chip(d, "REGLA 1: NO TE ACERQUES", 300, bg=(30, 110, 210), appear=lt / 0.4)
    return img, 1.0, 1.0

def s5(t):
    lt = t - 40
    img = ROOM.copy(); d = ImageDraw.Draw(img)
    doppel(d, 760, FEET + 40, 0.85, t, glow=0.4)
    d.ellipse([480, 380, 1030, 700], fill=WHITE, outline=BLK, width=6)
    for (bx, by, r) in [(640, 730, 26), (690, 790, 18)]:
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=WHITE, outline=BLK, width=4)
    d.rectangle([600, 430, 910, 640], fill=(240, 230, 210), outline=BLK, width=4)
    guy(d, 755, 640, 0.32, mood="neutral", t=0)
    guy(d, 230, FEET + 40, 0.85, mood="neutral", look=1, t=t)
    hx, hy = 230, FEET + 40 - 505 * 0.85
    d.rectangle([hx - 40, hy + 40, hx + 40, hy + 56], fill=(120, 120, 130))
    for k in range(6): d.line([(hx - 36 + k * 15, hy + 36), (hx - 36 + k * 15, hy + 60)], fill=(80, 80, 90), width=3)
    if lt > 8.0:
        sc = pop((lt - 8.0) / 0.35)
        cx, cy = 760, FEET + 40 - 505 * 0.85
        d.ellipse([cx - 90 * sc, cy - 110 * sc, cx + 90 * sc, cy + 110 * sc], fill=(250, 250, 250), outline=BLK, width=6)
        for sx in (-1, 1): d.ellipse([cx + sx * 35 - 15 * sc, cy - 30 * sc - 15 * sc, cx + sx * 35 + 15 * sc, cy - 30 * sc + 15 * sc], fill=BLK)
        d.arc([cx - 45 * sc, cy + 10 * sc, cx + 45 * sc, cy + 60 * sc], 20, 160, fill=BLK, width=6)
        d.text((cx, cy - 170), "MODO ACTOR", font=F(max(8, 40 * sc)), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    chip(d, "REGLA 2: CERO INFO PERSONAL", 300, bg=(150, 60, 200), appear=lt / 0.4)
    return img, 1.0, 1.0

def s6(t):
    lt = t - 55
    img = STREET.copy(); d = ImageDraw.Draw(img)
    if lt < 6.0:
        gx = lerp(540, 200, ease(lt / 2.0))
        guy(d, gx, FEET, 0.9, mood="scared", look=-1, t=t * 2)
        phone_small(d, gx + 170, FEET - 330, 0.7)
        if lt > 2.0:
            d.rounded_rectangle([600, 500, 1020, 620], 30, fill=WHITE, outline=BLK, width=5)
            d.text((810, 560), "¡AYUDA!", font=F(60), fill=RED, anchor="mm")
        return img, 1.0, 1.0
    img = BG_LAB.copy(); d = ImageDraw.Draw(img)
    d.ellipse([340, 560, 640, 860], outline=(60, 60, 70), width=28)
    d.line([(600, 820), (760, 980)], fill=(90, 55, 30), width=40)
    d.polygon([(380, 520), (700, 520), (640, 440), (440, 440)], fill=(150, 120, 80), outline=BLK)
    d.rectangle([330, 510, 750, 540], fill=(150, 120, 80), outline=BLK)
    xmark(d, 540, 700, 1.1 * pop((lt - 6.3) / 0.3))
    if lt > 8.0:
        bigtext(d, "NO TE PAGAN LO SUFICIENTE", 540, 1150, int(52 * pop((lt - 8.0) / 0.3)), fill=YEL)
    chip(d, "REGLA 3: ALÉJATE Y PIDE AYUDA", 300, bg=(220, 120, 40), size=50, appear=lt / 0.4)
    return img, 1.0, 1.0

def s7(t):
    lt = t - 68
    img = ROOM_DARK.copy(); d = ImageDraw.Draw(img)
    doppel(d, 760, FEET + 40, 0.9, t, glow=1.0, point=True)
    if lt > 1.0:
        d.rounded_rectangle([420, 380, 1050, 500], 30, fill=WHITE, outline=BLK, width=5)
        d.text((735, 440), "¡ÉL es el impostor!", font=F(52), fill=RED, anchor="mm")
    gx = lerp(300, -200, ease((lt - 4.0) / 2.0)) if lt > 4.0 else 300
    guy(d, gx, FEET + 40, 0.85, mood="scared", look=-1, t=t * 3)
    if lt > 4.0:
        for k in range(4): d.line([(gx + 120 + k * 40, 900 + k * 60), (gx + 220 + k * 50, 900 + k * 60)], fill=WHITE, width=6)
    return img, 1.0, 1.0, (1.0 < lt < 1.4)

def s8(t):
    lt = t - 76
    img = ROOM_DARK.copy(); d = ImageDraw.Draw(img)
    sofa(d, 540, 1180, 0.9)
    doppel(d, 540, FEET + 40, 0.85, t, glow=0.7)
    phone_small(d, 700, 760, 0.8, glow=1.0, content="video")
    d.polygon([(620, 640), (1000, 200), (1080, 200), (780, 640)], fill=(40, 60, 100))
    if lt > 12.0:
        sc = pop((lt - 12.0) / 0.35)
        d.rounded_rectangle([540 - 330 * sc, 340 - 80 * sc, 540 + 330 * sc, 340 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
        d.text((540, 340), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
        d.text((540, 470), "más manuales de supervivencia", font=F(max(8, 42 * sc)), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    return img, 0.9, 1.0 + 0.04 * ease(lt / 8)

SCENES = [(0, 6, s1), (6, 18, s2), (18, 25, s3), (25, 40, s4), (40, 55, s5), (55, 68, s6), (68, 76, s7), (76, 95, s8)]

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
        sheet.save("sheet_r9.png"); sys.exit()
    from warp9 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(94.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
