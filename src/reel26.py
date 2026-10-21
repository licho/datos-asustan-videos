import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, guy, W, H, YEL, RED, WHITE, BLK, SKIN, FEET)

FPS = 30
DUR = 67.0
SH1, SH2 = 760, 1180  # repisas del refri (parte de arriba)

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def make_fridge(tint=(225, 238, 248)):
    img = grad(tint, dk(tint, 0.86)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 60, H], fill=dk(tint, 0.8)); d.rectangle([W - 60, 0, W, H], fill=dk(tint, 0.8))
    d.ellipse([340, 60, 740, 200], fill=(255, 255, 230))
    for y in (SH1, SH2):
        d.rectangle([60, y, W - 60, y + 22], fill=(200, 225, 240), outline=(150, 170, 190), width=3)
    d.rectangle([60, 1380, W - 60, H], fill=dk(tint, 0.75))
    return img
FRIDGE = make_fridge()
FRIDGE_DARK = make_fridge((150, 165, 150))
KITCHEN = grad((250, 235, 210), (235, 210, 180))

def taper(d, x, y, w=360, h=170, lid=(60, 140, 220), food=(150, 80, 40), label=None):
    d.rounded_rectangle([x, y + 25, x + w, y + h], 18, fill=(235, 245, 250), outline=BLK, width=5)
    d.rounded_rectangle([x + 10, y + 45, x + w - 10, y + h - 10], 12, fill=food)
    for k in range(5): d.ellipse([x + 30 + k * 50, y + 60 + (k % 2) * 25, x + 60 + k * 50, y + 85 + (k % 2) * 25], fill=dk(food, 1.25))
    d.rounded_rectangle([x - 8, y, x + w + 8, y + 32], 12, fill=lid, outline=BLK, width=5)
    if label:
        d.rounded_rectangle([x + w / 2 - 170, y + 70, x + w / 2 + 170, y + 135], 10, fill=WHITE, outline=BLK, width=3)
        d.text((x + w / 2, y + 102), label, font=F(42), fill=RED, anchor="mm")

def jar(d, x, ybot, text="MOSTAZA"):
    d.rounded_rectangle([x, ybot - 230, x + 140, ybot], 22, fill=(240, 200, 30), outline=BLK, width=5)
    d.rounded_rectangle([x + 10, ybot - 270, x + 130, ybot - 225], 10, fill=(200, 60, 40), outline=BLK, width=4)
    d.rectangle([x + 8, ybot - 160, x + 132, ybot - 90], fill=WHITE, outline=BLK, width=3)
    d.text((x + 70, ybot - 125), text, font=F(24), fill=BLK, anchor="mm")

def milk(d, x, ybot):
    d.rectangle([x, ybot - 260, x + 120, ybot], fill=WHITE, outline=BLK, width=5)
    d.polygon([(x, ybot - 260), (x + 60, ybot - 320), (x + 120, ybot - 260)], fill=(230, 230, 240), outline=BLK)
    d.rectangle([x + 10, ybot - 200, x + 110, ybot - 120], fill=(80, 150, 230))
    d.text((x + 60, ybot - 160), "LECHE", font=F(26), fill=WHITE, anchor="mm")

def lettuce(d, cx, ybot, melt=0.0):
    if melt < 1.0:
        s = 1 - melt * 0.7
        for k, (dx, r) in enumerate([(-50, 70), (40, 75), (0, 90)]):
            d.ellipse([cx + dx * s - r * s, ybot - 2 * r * s - 10, cx + dx * s + r * s, ybot], fill=lc((110, 200, 90), (90, 120, 60), melt), outline=BLK, width=4)
    if melt > 0.2:
        pw = 120 + 200 * melt
        d.ellipse([cx - pw, ybot - 30 * melt, cx + pw, ybot + 10], fill=(120, 150, 60), outline=BLK, width=3)

def bacteria(d, x, y, s, t, kind="green", suitcase=False, shades=False):
    col = {"green": (90, 200, 90), "blue": (110, 170, 240), "purple": (170, 110, 210)}[kind]
    bob = math.sin(t * 6 + x) * 6 * s
    y = y + bob
    d.ellipse([x - 45 * s, y - 40 * s, x + 45 * s, y + 40 * s], fill=col, outline=BLK, width=max(2, int(4 * s)))
    for k in range(6):
        a = k * 1.05
        d.line([(x + math.cos(a) * 45 * s, y + math.sin(a) * 40 * s), (x + math.cos(a) * 62 * s, y + math.sin(a) * 55 * s)], fill=BLK, width=max(2, int(3 * s)))
    if shades:
        d.rectangle([x - 32 * s, y - 15 * s, x + 32 * s, y + 2 * s], fill=BLK)
    else:
        for sx in (-1, 1):
            d.ellipse([x + sx * 16 * s - 10 * s, y - 16 * s, x + sx * 16 * s + 10 * s, y + 4 * s], fill=WHITE, outline=BLK, width=2)
            d.ellipse([x + sx * 16 * s - 4 * s, y - 9 * s, x + sx * 16 * s + 4 * s, y - 1 * s], fill=BLK)
    d.arc([x - 18 * s, y + 2 * s, x + 18 * s, y + 24 * s], 20, 160, fill=BLK, width=max(2, int(4 * s)))
    if suitcase:
        d.rounded_rectangle([x + 40 * s, y + 5 * s, x + 90 * s, y + 45 * s], 6, fill=(150, 90, 40), outline=BLK, width=3)
        d.line([(x + 55 * s, y + 5 * s), (x + 55 * s, y - 5 * s), (x + 75 * s, y - 5 * s), (x + 75 * s, y + 5 * s)], fill=BLK, width=3)

def listeria(d, x, y, s, t):
    bacteria(d, x, y, s, t, "blue")
    S = lambda v: v * s
    d.chord([x - S(48), y - S(75), x + S(48), y - S(10)], 180, 360, fill=(220, 50, 60), outline=BLK, width=3)
    d.ellipse([x - S(14), y - S(95), x + S(14), y - S(67)], fill=WHITE, outline=BLK, width=2)
    d.rounded_rectangle([x - S(50), y + S(18), x + S(50), y + S(34)], S(8), fill=(240, 200, 40), outline=BLK, width=2)

def mold(d, cx, cy, r, k, t, seed=1):
    rng = random.Random(seed)
    for i in range(int(30 * k)):
        a = rng.uniform(0, 6.28); rr = rng.uniform(0, r)
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.4
        s = rng.uniform(14, 34) * min(1, k * 1.5)
        c = rng.choice([(120, 170, 110), (160, 170, 160), (90, 140, 90), (200, 210, 200)])
        d.ellipse([x - s, y - s, x + s, y + s], fill=c, outline=dk(c, 0.7), width=2)

def calendar(d, cx, cy, day, label="DÍA", col=(240, 150, 40), sc=0.6):
    S = lambda v: v * sc
    d.rounded_rectangle([cx - S(190), cy - S(170), cx + S(190), cy + S(170)], int(S(26)), fill=WHITE, outline=BLK, width=6)
    d.rounded_rectangle([cx - S(190), cy - S(170), cx + S(190), cy - S(70)], int(S(26)), fill=col, outline=BLK, width=6)
    d.text((cx, cy - S(120)), label, font=F(S(52)), fill=WHITE, anchor="mm")
    d.text((cx, cy + S(50)), str(day), font=F(S(150)), fill=BLK, anchor="mm")

def cloud(d, cx, cy, t):
    for (dx, dy, r) in [(-90, 0, 70), (0, -30, 90), (90, 0, 70)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(150, 160, 175), outline=BLK, width=3)
    for i in range(10):
        x = cx - 140 + i * 30; y = cy + 70 + ((t * 300 + i * 47) % 300)
        d.line([(x, y), (x - 6, y + 26)], fill=(90, 150, 230), width=6)

CAPS = [
    (0.0, 4.0, "¿Qué pasa si olvidas comida en el refri *durante un mes*?"),
    (4.0, 6.8, "Día 1: guardas el guisado. Todo bien."),
    (6.8, 11.3, "Regla de oro: las sobras se comen en *3 o 4 días*"),
    (11.3, 14.8, "Pero lo olvidaste *detrás del frasco de mostaza*…"),
    (14.8, 19.3, "Día 5: se ve igual, huele igual… *pero ya no es igual*"),
    (19.3, 25.0, "Lo que asusta: las bacterias que te intoxican *no cambian el olor, el sabor ni el aspecto*"),
    (25.0, 29.5, "*La prueba de olerlo… no sirve.*"),
    (29.5, 33.6, "Y algunas, como la *listeria*, crecen aunque el refri *esté frío*"),
    (33.6, 38.5, "Semana 2: aparece *el moho*. Pelusa verde, gris…"),
    (38.5, 43.5, "Y no basta con quitar la parte mala: en comida blanda, *sus raíces ya llegaron adentro*"),
    (43.5, 48.8, "Semana 3: la lechuga *se volvió sopa*. El refri tiene *su propio clima*"),
    (48.8, 54.1, "Mes 1: un ecosistema completo. Hay un táper que *nadie se atreve a abrir*"),
    (54.1, 59.0, "Y lo peor… el táper *era de tu mamá*. Ahora sí estás en peligro."),
    (59.0, 90.0, "¿Qué es lo más viejo que has encontrado en tu refri? *Te leo en los comentarios*"),
]

def render(v, t=None):
    if t is None: t = v
    shake = 0
    if v < 14.8:
        img = FRIDGE.copy(); d = ImageDraw.Draw(img)
        milk(d, 120, SH1); jar(d, 820, SH1, "SALSA")
        tx = 380
        if v >= 4.0:
            tx = lerp(-400, 360, ease((v - 4.0) / 1.2))
            taper(d, tx, SH2 - 170)
        if v >= 11.3:
            jx = lerp(1200, 460, ease((v - 11.3) / 1.0))
            jar(d, jx, SH2 + 22 - 22)
        if v < 4.0:
            chip(d, "¿QUÉ PASA SI…?", 380, bg=RED, appear=v / 0.3)
            day = 1
        else:
            day = int(lerp(1, 4, cl((v - 6.8) / 4.0)))
        calendar(d, 880, 260, day)
        if 6.8 <= v < 11.3: chip(d, "SOBRAS: 3–4 DÍAS", 1290, bg=(30, 140, 80), appear=(v - 6.8) / 0.3)
        if v >= 11.8: chip(d, "OLVIDADO", 1290, bg=(120, 120, 130), appear=(v - 11.8) / 0.3)
    elif v < 19.3:
        lt = v - 14.8
        img = FRIDGE.copy(); d = ImageDraw.Draw(img)
        milk(d, 120, SH1); jar(d, 820, SH1, "SALSA")
        taper(d, 360, SH2 - 170)
        jar(d, lerp(460, 760, ease(lt / 0.8)), SH2)
        calendar(d, 880, 260, 5)
        for i in range(3):
            bx = lerp(-100 - i * 140, 430 + i * 90, ease((lt - 0.8 - i * 0.3) / 1.8))
            if bx > -80: bacteria(d, bx, SH2 - 200, 0.8, t + i, "green", suitcase=True)
        chip(d, "SE VE IGUAL · HUELE IGUAL", 380, bg=(90, 90, 100), size=48, appear=(lt - 0.5) / 0.3)
    elif v < 29.5:
        lt = v - 19.3
        img = KITCHEN.copy(); d = ImageDraw.Draw(img)
        for y in range(0, 1150, 120):
            for x in range((y // 120) % 2 * 60, W, 120): d.rectangle([x, y, x + 116, y + 116], outline=(225, 200, 170), width=3)
        d.rectangle([0, 1150, W, H], fill=(190, 160, 130))
        guy(d, 400, 1420, 0.85, mood="neutral", arms="push", t=t)
        tx, ty = 400 + 0.85 * 150 - 40, 1420 - 0.85 * 300 - 120
        taper(d, tx, ty, 260, 130)
        for k in range(3):
            y = ty - 30 - k * 40 - (t * 60) % 40
            d.arc([tx - 60, y, tx + 40, y + 40], 200, 340, fill=(120, 160, 90), width=6)
        for i in range(3): bacteria(d, tx + 50 + i * 80, ty - 40, 0.5, t + i, "green", shades=True)
        d.text((640, 520), "*snif snif*", font=F(54), fill=BLK, anchor="mm")
        if lt > 1.0: chip(d, "OLOR ✓  SABOR ✓  ASPECTO ✓", 300, bg=(30, 140, 80), size=44, appear=(lt - 1.0) / 0.3)
        if v >= 25.0:
            chip(d, "PRUEBA DE OLERLO: NO SIRVE", 420, bg=RED, size=48, appear=(v - 25.0) / 0.3)
    elif v < 33.6:
        lt = v - 29.5
        img = FRIDGE.copy(); d = ImageDraw.Draw(img)
        for i in range(30):
            x = (i * 97) % (W - 160) + 80; y = (i * 151) % 1200 + 120
            d.line([(x - 10, y), (x + 10, y)], fill=WHITE, width=3); d.line([(x, y - 10), (x, y + 10)], fill=WHITE, width=3)
        taper(d, 360, SH2 - 170)
        listeria(d, 540 + math.sin(t * 2) * 120, SH2 - 230, 1.3, t)
        d.rounded_rectangle([140, SH1 - 400, 220, SH1 - 80], 40, fill=WHITE, outline=BLK, width=5)
        d.ellipse([125, SH1 - 110, 235, SH1], fill=(80, 150, 230), outline=BLK, width=5)
        d.rectangle([170, SH1 - 280, 190, SH1 - 90], fill=(80, 150, 230))
        d.text((180, SH1 - 440), "4 °C", font=F(54), fill=BLK, anchor="mm")
        chip(d, "LISTERIA: CRECE EN EL FRÍO", 1290, bg=(60, 110, 200), size=48, appear=lt / 0.3)
    elif v < 43.5:
        lt = v - 33.6
        img = grad((70, 80, 70), (30, 35, 30)); d = ImageDraw.Draw(img)
        if v < 38.5:
            d.rounded_rectangle([140, 560, 940, 1000], 40, fill=(235, 245, 250), outline=BLK, width=8)
            d.rounded_rectangle([170, 600, 910, 970], 30, fill=(150, 80, 40))
            mold(d, 540, 640, 330, ease(lt / 3.0), t)
            chip(d, "SEMANA 2: MOHO", 380, bg=(90, 140, 90), appear=lt / 0.3)
        else:
            k = ease((v - 38.5) / 2.5)
            d.rectangle([160, 600, 920, 1180], fill=(150, 80, 40), outline=BLK, width=6)
            d.rectangle([160, 560, 920, 600], fill=(130, 170, 120))
            mold(d, 540, 570, 360, 1.0, t, 3)
            rng = random.Random(5)
            for i in range(14):
                x = 200 + i * 52
                pts = [(x, 600)]
                for j in range(1, 10):
                    pts.append((x + rng.uniform(-18, 18), 600 + j * 58 * k))
                d.line(pts, fill=(210, 230, 200), width=5)
            d.text((540, 500), "CORTE", font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
            chip(d, "SUS RAÍCES LLEGAN ADENTRO", 1290, bg=RED, size=48, appear=(v - 38.8) / 0.3)
    elif v < 48.8:
        lt = v - 43.5
        img = FRIDGE_DARK.copy(); d = ImageDraw.Draw(img)
        lettuce(d, 330, SH2, cl(lt / 2.5))
        taper(d, 600, SH2 - 170, food=(110, 120, 60))
        mold(d, 770, SH2 - 150, 120, 1.0, t, 7)
        cloud(d, 540, 330, t)
        chip(d, "SEMANA 3: CLIMA PROPIO", 1290, bg=(90, 100, 120), size=48, appear=(lt - 1.5) / 0.3)
    elif v < 54.1:
        lt = v - 48.8
        img = FRIDGE_DARK.copy(); d = ImageDraw.Draw(img)
        mold(d, 300, SH1 - 40, 220, 1.0, t, 11); mold(d, 800, SH1 - 40, 200, 1.0, t, 12)
        for i in range(6):
            x = 100 + i * 170
            d.line([(x, 0), (x + math.sin(t + i) * 30, 400 + i * 40)], fill=(70, 120, 60), width=12)
        bulge = 20 + 10 * math.sin(t * 5)
        taper(d, 360, SH2 - 170, lid=(60, 140, 220), food=(60, 70, 40))
        d.chord([352, SH2 - 170 - bulge * 2, 728, SH2 - 170 + 30], 180, 360, fill=(60, 140, 220), outline=BLK, width=5)
        for sx in (-1, 1):
            d.ellipse([540 + sx * 60 - 20, SH2 - 80 - 14, 540 + sx * 60 + 20, SH2 - 80 + 14], fill=(255, 240, 80))
        bacteria(d, 200, SH2 - 60, 0.8, t, "purple"); bacteria(d, 880, SH2 - 60, 0.7, t + 2, "green")
        chip(d, "MES 1: NADIE LO ABRE", 1290, bg=BLK, fg=YEL, size=50, appear=lt / 0.3)
        if int(t * 2) % 2 == 0: shake = 3
    elif v < 59.0:
        lt = v - 54.1
        img = FRIDGE_DARK.copy(); d = ImageDraw.Draw(img)
        taper(d, 300, SH2 - 200, 480, 200, lid=(220, 60, 120), food=(60, 70, 40), label="DE MAMÁ ♥")
        if lt > 1.0:
            yy = lerp(-200, 60, ease((lt - 1.0) / 0.4))
            d.rounded_rectangle([70, yy, 1010, yy + 210], 36, fill=(245, 245, 250), outline=(60, 60, 70), width=5)
            d.rounded_rectangle([100, yy + 40, 220, yy + 160], 28, fill=(60, 200, 110))
            d.text((160, yy + 100), "M", font=F(70), fill=WHITE, anchor="mm")
            d.text((250, yy + 60), "Mamá · ahora", font=F(40), fill=(90, 90, 100), anchor="lm")
            d.text((250, yy + 135), "¿Y mi táper?", font=F(60), fill=BLK, anchor="lm")
        if lt > 2.2:
            chip(d, "AHORA SÍ: PELIGRO", 1290, bg=RED, size=56, appear=(lt - 2.2) / 0.3)
            shake = 8 if lt < 3.0 else 0
    else:
        lt = v - 59.0
        img = FRIDGE.copy(); d = ImageDraw.Draw(img)
        taper(d, 300, SH2 - 200, 480, 200)
        bigtext(d, "¿LO MÁS VIEJO", 540, 330, 86, fill=WHITE)
        bigtext(d, "DE TU REFRI?", 540, 440, 86, fill=YEL)
        if lt > 1.5:
            sc = pop((lt - 1.5) / 0.35)
            d.rounded_rectangle([540 - 330 * sc, 620 - 80 * sc, 540 + 330 * sc, 620 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
            d.text((540, 620), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
    for cs, ce, txt in CAPS:
        if cs <= v < ce: rich_caption(d, txt, appear=(v - cs) / 0.25)
    arr = np.asarray(img)
    if shake:
        arr = np.roll(arr, int(math.sin(t * 60) * shake), axis=1)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r26.png"); sys.exit()
    try:
        from warp26 import v_of_T, DUR as D2
    except ImportError:
        v_of_T = lambda T: T; D2 = DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(D2 * FPS)):
        p.stdin.write(render(v_of_T(i / FPS), i / FPS).tobytes())
    p.stdin.close(); p.wait()
