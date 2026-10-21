import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, guy, W, H, YEL, RED, WHITE, BLK, SKIN, FEET)

FPS = 30
DUR = 42.0
FLOOR = 1240

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def make_kitchen():
    img = grad((240, 225, 200), (225, 205, 175)); d = ImageDraw.Draw(img)
    for y in range(0, FLOOR - 80, 110):
        for x in range((y // 110) % 2 * 55, W, 110): d.rectangle([x, y, x + 106, y + 106], outline=(215, 195, 165), width=3)
    d.rectangle([0, FLOOR - 80, W, FLOOR], fill=(150, 110, 80))
    d.rectangle([0, FLOOR, W, H], fill=(205, 190, 170))
    for x in range(0, W, 150):
        d.line([(x, FLOOR), (x - 200, H)], fill=(185, 170, 150), width=4)
    return img
KITCHEN = make_kitchen()

BODY = (120, 60, 30); SHIELD = (170, 100, 50); LEG = (70, 35, 15)

def roach(d, cx, cy, s, t, head=True, walk=True, wings=0.0, face="neutral", flip=False):
    S = lambda v: v * s
    dirx = -1 if flip else 1
    ph = t * 14 if walk else 0
    # patas
    for i, lx in enumerate((-70, 0, 70)):
        for side in (-1, 1):
            sw = math.sin(ph + i * 2.1 + (0 if side > 0 else math.pi)) * 22
            kx = cx + dirx * S(lx + sw); ky = cy + side * S(70)
            fx = cx + dirx * S(lx + sw * 1.6 - 20); fy = cy + side * S(120)
            d.line([(cx + dirx * S(lx), cy + side * S(25)), (kx, ky), (fx, fy)], fill=LEG, width=max(3, int(S(12))), joint="curve")
    if wings > 0:
        for side in (-1, 1):
            a = side * (0.4 + 0.5 * wings * abs(math.sin(t * 40)))
            wx = cx - dirx * S(30); wy = cy
            pts = [(wx, wy), (wx - dirx * S(200) * math.cos(a), wy + S(200) * math.sin(a) * 1.4), (wx - dirx * S(140), wy + side * S(30))]
            d.polygon(pts, fill=(230, 210, 160), outline=BLK)
    d.ellipse([cx - S(150), cy - S(70), cx + S(130), cy + S(70)], fill=BODY, outline=BLK, width=max(3, int(S(6))))
    for k in range(4):
        x = cx - dirx * S(120 - k * 40)
        d.arc([x - S(30), cy - S(68), x + S(30), cy + S(68)], -60 if dirx > 0 else 120, 60 if dirx > 0 else 240, fill=dk(BODY, 0.7), width=max(2, int(S(5))))
    sx = cx + dirx * S(110)
    d.ellipse([sx - S(55), cy - S(62), sx + S(55), cy + S(62)], fill=SHIELD, outline=BLK, width=max(3, int(S(5))))
    if head:
        hx = cx + dirx * S(175)
        for side in (-1, 1):
            pts = []
            for k in range(12):
                u = k / 11
                pts.append((hx + dirx * S(30 + u * 230), cy + side * S(20) + side * S(u * 120) + math.sin(t * 5 + u * 4 + side) * S(18) * u))
            d.line(pts, fill=LEG, width=max(2, int(S(6))))
        d.ellipse([hx - S(42), cy - S(40), hx + S(42), cy + S(40)], fill=BODY, outline=BLK, width=max(3, int(S(5))))
        for side in (-1, 1):
            ex, ey = hx + dirx * S(12), cy + side * S(18)
            d.ellipse([ex - S(14), ey - S(14), ex + S(14), ey + S(14)], fill=WHITE, outline=BLK, width=2)
            d.ellipse([ex + dirx * S(3) - S(6), ey - S(6), ex + dirx * S(3) + S(6), ey + S(6)], fill=BLK)
    else:
        hx = cx + dirx * S(165)
        d.ellipse([hx - S(24), cy - S(30), hx + S(24), cy + S(30)], fill=(250, 245, 230), outline=BLK, width=max(2, int(S(4))))

def roach_head(d, x, y, s, t, blink=True):
    S = lambda v: v * s
    for side in (-1, 1):
        pts = []
        for k in range(12):
            u = k / 11
            pts.append((x + S(30 + u * 230), y + side * S(20) + side * S(u * 110) + math.sin(t * 6 + u * 4 + side) * S(28) * u))
        d.line(pts, fill=LEG, width=max(2, int(S(7))))
    d.ellipse([x - S(50), y - S(48), x + S(50), y + S(48)], fill=BODY, outline=BLK, width=max(3, int(S(6))))
    closed = blink and int(t * 1.3) % 4 == 0
    for side in (-1, 1):
        ex, ey = x + S(14), y + side * S(20)
        if closed:
            d.line([(ex - S(14), ey), (ex + S(14), ey)], fill=BLK, width=4)
        else:
            d.ellipse([ex - S(16), ey - S(16), ex + S(16), ey + S(16)], fill=WHITE, outline=BLK, width=2)
            d.ellipse([ex - S(6), ey - S(6), ex + S(6), ey + S(6)], fill=BLK)

def calendar(d, cx, cy, day, label="DÍA", col=(240, 150, 40), sc=0.7):
    S = lambda v: v * sc
    d.rounded_rectangle([cx - S(190), cy - S(170), cx + S(190), cy + S(170)], int(S(26)), fill=WHITE, outline=BLK, width=6)
    d.rounded_rectangle([cx - S(190), cy - S(170), cx + S(190), cy - S(70)], int(S(26)), fill=col, outline=BLK, width=6)
    d.text((cx, cy - S(120)), label, font=F(S(52)), fill=WHITE, anchor="mm")
    d.text((cx, cy + S(50)), str(day), font=F(S(150)), fill=BLK, anchor="mm")

def sandal(d, cx, cy, s, ang=0.0):
    S = lambda v: v * s
    tmp = Image.new("RGBA", (int(S(700)), int(S(700))), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    o = S(350)
    td.rounded_rectangle([o - S(140), o - S(300), o + S(140), o + S(300)], int(S(130)), fill=(60, 140, 220, 255), outline=(0, 0, 0, 255), width=8)
    td.rounded_rectangle([o - S(110), o - S(270), o + S(110), o + S(270)], int(S(110)), fill=(90, 170, 240, 255))
    td.line([(o - S(110), o - S(120)), (o, o - S(200)), (o + S(110), o - S(120))], fill=(40, 40, 40, 255), width=int(S(26)))
    return tmp.rotate(ang, expand=False, resample=Image.BICUBIC)

def glass(d, cx, ybot):
    d.polygon([(cx - 80, ybot - 220), (cx + 80, ybot - 220), (cx + 65, ybot), (cx - 65, ybot)], fill=(210, 235, 250), outline=BLK)
    d.polygon([(cx - 74, ybot - 140), (cx + 74, ybot - 140), (cx + 65, ybot - 4), (cx - 65, ybot - 4)], fill=(120, 190, 240))

CAPS = [
    (0.0, 3.2, "¿Sabías que una cucaracha puede vivir… *sin cabeza*?"),
    (3.2, 4.6, "*Hasta una semana.*"),
    (4.6, 10.2, "No respira por la boca: respira por unos agujeritos llamados *espiráculos*"),
    (10.2, 16.5, "Y no se desangra: su sangre circula *a baja presión* y la herida *se sella rápido*"),
    (16.5, 21.0, "¿De qué muere? *De sed.* Sin boca, no puede tomar agua"),
    (21.0, 26.2, "Y la cabeza, por su lado, *puede seguir moviendo las antenas durante horas*"),
    (26.2, 31.8, "La próxima vez que le des un chanclazo… *asegúrate de que sea definitivo*"),
    (31.8, 60.0, "¿A qué le tienes más miedo: a la cucaracha… *o a la cucaracha voladora*?"),
]

def render(v, t=None):
    if t is None: t = v
    shake = 0
    img = KITCHEN.copy(); d = ImageDraw.Draw(img)
    if v < 4.6:
        x = lerp(-200, 480, ease(v / 2.2))
        popped = v >= 2.4
        roach(d, x, 1170, 1.1, t, head=not popped)
        if popped:
            k = ease((v - 2.4) / 0.6)
            hx = lerp(x + 190, 860, k); hy = 1200 - 30 * k - math.sin(k * math.pi) * 420
            roach_head(d, hx, hy, 1.0, t)
            if v < 3.2: bigtext(d, "¡POP!", 700, 600, 120, fill=YEL); shake = 6
        chip(d, "¿SIN CABEZA?", 300, bg=RED, appear=v / 0.3)
        if v >= 3.2:
            calendar(d, 540, 560, int(lerp(1, 7, cl((v - 3.2) / 1.2))))
    elif v < 10.2:
        lt = v - 4.6
        img = grad((250, 240, 225), (230, 215, 195)); d = ImageDraw.Draw(img)
        roach(d, 500, 900, 2.2, t, head=False, walk=False)
        for i in range(5):
            px = 500 - 2.2 * 120 + i * 2.2 * 55; py = 900 - 2.2 * 40
            d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(250, 240, 220), outline=BLK, width=3)
            ph = (t * 1.2 + i * 0.2) % 1
            d.ellipse([px - 8 - ph * 30, py - 40 - ph * 120, px + 8 + ph * 30, py - 24 - ph * 120], outline=(150, 190, 230), width=4)
        chip(d, "ESPIRÁCULOS", 360, bg=(60, 120, 200), appear=lt / 0.3)
        if lt > 1.5:
            bigtext(d, "BOCA: ✗", 540, 480, 70, fill=RED)
    elif v < 16.5:
        lt = v - 10.2
        img = grad((250, 240, 225), (230, 215, 195)); d = ImageDraw.Draw(img)
        roach(d, 440, 950, 2.0, t, head=False, walk=False)
        nx = 440 + 2.0 * 165
        k = ease(lt / 3.0)
        d.rounded_rectangle([nx - 40, 950 - 70, nx + 40, 950 + 70], 20, fill=(240, 220, 180), outline=BLK, width=4)
        d.line([(nx - 30, 950 - 40), (nx + 30, 950 + 40)], fill=(200, 170, 130), width=6); d.line([(nx - 30, 950 + 40), (nx + 30, 950 - 40)], fill=(200, 170, 130), width=6)
        cx, cy, r = 540, 520, 170
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(30, 30, 40), outline=WHITE, width=6)
        a = math.pi + 0.25 * math.pi + 0.05 * math.sin(t * 3)
        d.line([(cx, cy), (cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8)], fill=(80, 220, 120), width=10)
        d.text((cx, cy + 50), "PRESIÓN: BAJA", font=F(44), fill=BLK, anchor="mm")
        chip(d, "NO SE DESANGRA", 280, bg=(30, 140, 80), appear=(lt - 0.5) / 0.3)
    elif v < 21.0:
        lt = v - 16.5
        roach(d, lerp(250, 520, ease(lt / 2.0)), 1180, 1.0, t, head=False, walk=lt < 2.0)
        glass(d, 820, 1220)
        calendar(d, 540, 560, 7)
        if lt > 1.5:
            bigtext(d, "...", 690, 1000, 90, fill=BLK)
            chip(d, "MUERE DE SED", 300, bg=(200, 120, 40), appear=(lt - 1.5) / 0.3)
    elif v < 26.2:
        lt = v - 21.0
        roach_head(d, 420, 1220, 1.8, t)
        chip(d, "LA CABEZA SIGUE", 300, bg=(90, 90, 100), appear=lt / 0.3)
        if lt > 1.2: chip(d, "MOVIENDO LAS ANTENAS… HORAS", 420, bg=RED, size=44, appear=(lt - 1.2) / 0.3)
    elif v < 31.8:
        lt = v - 26.2
        hit = (lt % 1.4) < 0.25 and lt > 0.6
        roach(d, 600 + math.sin(t * 3) * 120, 1180, 1.0, t)
        sy = 960 if hit else 960 - 380 * abs(math.sin(lt / 1.4 * math.pi))
        d.line([(640, -40), (600, sy - 60)], fill=(220, 175, 140), width=70)
        sn = sandal(d, 0, 0, 1.0, 90)
        img.paste(sn, (int(560 - 350), int(sy - 350)), sn); d = ImageDraw.Draw(img)
        d.ellipse([545, sy - 120, 655, sy - 20], fill=(241, 194, 150), outline=BLK, width=4)
        if hit:
            bigtext(d, "¡PAS!", 540, 560, 140, fill=YEL); shake = 10
        if lt > 2.0: chip(d, "ASEGÚRATE", 300, bg=RED, appear=(lt - 2.0) / 0.3)
    else:
        lt = v - 31.8
        img = grad((40, 30, 40), (90, 60, 50)); d = ImageDraw.Draw(img)
        if lt < 3.0:
            roach(d, 360, 1150, 0.9, t)
            bigtext(d, "¿CUCARACHA…", 540, 380, 90, fill=WHITE)
        else:
            s = lerp(0.8, 2.0, ease((lt - 3.0) / 2.0))
            roach(d, 540, lerp(1100, 760, ease((lt - 3.0) / 2.0)), s, t, wings=1.0, walk=False)
            bigtext(d, "¿…O VOLADORA?", 540, 380, 90, fill=RED)
            if lt > 5.5:
                sc = pop((lt - 5.5) / 0.35)
                d.rounded_rectangle([540 - 330 * sc, 1220 - 80 * sc, 540 + 330 * sc, 1220 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
                d.text((540, 1220), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
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
        sheet.save("sheet_r27.png"); sys.exit()
    try:
        from warp27 import v_of_T, DUR as D2
    except ImportError:
        v_of_T = lambda T: T; D2 = DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(D2 * FPS)):
        p.stdin.write(render(v_of_T(i / FPS), i / FPS).tobytes())
    p.stdin.close(); p.wait()
