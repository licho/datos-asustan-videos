import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy,
                  W, H, YEL, RED, WHITE, BLK, SKIN)
from reel15 import office, desk, TT, bubble
from reel17 import paste_stamp

FPS = 30
FEET = 1380
ZS = (150, 185, 140)
ZD = (110, 140, 100)

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def zomb(d, x, y, s=1.0, t=0.0, mood="blank", arms="out", outfit="office", hat=None, arm_off=False):
    S = lambda v: v * s
    sway = math.sin(t * 2.2) * S(8)
    d.ellipse([x - S(120), y - S(16), x + S(120), y + S(16)], fill=(70, 72, 75))
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx * S(10) - (S(55) if sx < 0 else 0), y - S(190), x + sx * S(10) + (S(55) if sx > 0 else 0), y - S(10)], int(S(18)), fill=(70, 75, 95))
        d.ellipse([x + sx * S(45) - S(45), y - S(40), x + sx * S(45) + S(45), y + S(4)], fill=(40, 35, 30))
    shirt = {"office": (225, 225, 215), "call": (90, 140, 200), "movie": (150, 120, 100), "suit": (60, 60, 75)}[outfit]
    x2 = x + sway
    def arm(sx, hx, hy):
        d.line([(x2 + sx * S(95), y - S(395)), (hx, hy)], fill=dk(shirt, 0.85), width=int(S(42)), joint="curve")
        d.ellipse([hx - S(26), hy - S(26), hx + S(26), hy + S(26)], fill=ZS)
    d.rounded_rectangle([x2 - S(105), y - S(425), x2 + S(105), y - S(170)], int(S(40)), fill=shirt, outline=BLK, width=4)
    for k in range(3):
        d.polygon([(x2 - S(105) + k * S(70), y - S(175)), (x2 - S(80) + k * S(70), y - S(150)), (x2 - S(55) + k * S(70), y - S(175))], fill=shirt)
    d.ellipse([x2 + S(20), y - S(330), x2 + S(60), y - S(300)], fill=(120, 140, 90))
    if outfit in ("office", "suit"):
        d.polygon([(x2 - S(12), y - S(420)), (x2 + S(12), y - S(420)), (x2 + S(40), y - S(290)), (x2 + S(22), y - S(270)), (x2 + S(10), y - S(290))], fill=(170, 40, 50))
    if arms == "out":
        arm(-1, x2 + S(160), y - S(400)) if not arm_off else None
        arm(1, x2 + S(200), y - S(380))
    elif arms == "down":
        arm(-1, x2 - S(130), y - S(200)) if not arm_off else None
        arm(1, x2 + S(130), y - S(200))
    elif arms == "desk":
        arm(-1, x2 - S(80), y - S(250)) if not arm_off else None
        arm(1, x2 + S(80), y - S(250))
    elif arms == "shrug":
        arm(-1, x2 - S(190), y - S(470)) if not arm_off else None
        arm(1, x2 + S(190), y - S(470))
    hx, hy = x2 + S(10), y - S(520)
    d.ellipse([hx - S(100), hy - S(105), hx + S(100), hy + S(100)], fill=ZS, outline=BLK, width=3)
    for (a, b, w, h) in [(-50, -60, 20, 50), (30, -75, 15, 40), (55, 20, 25, 18)]:
        d.ellipse([hx + S(a), hy + S(b), hx + S(a + w), hy + S(b + h)], fill=ZD)
    for k in range(5):
        d.line([(hx - S(80) + k * S(35), hy - S(90)), (hx - S(70) + k * S(35), hy - S(125) - (k % 2) * S(12))], fill=(60, 50, 40), width=max(2, int(S(8))))
    for sx, sz in ((-1, 26), (1, 18)):
        ex, ey = hx + sx * S(40), hy - S(5)
        d.ellipse([ex - S(sz), ey - S(sz), ex + S(sz), ey + S(sz)], fill=(245, 245, 220), outline=BLK, width=3)
        d.ellipse([ex - S(5), ey - S(5) + S(4), ex + S(5), ey + S(5) + S(4)], fill=BLK)
    my = hy + S(55)
    if mood == "groan":
        d.ellipse([hx - S(28), my - S(14), hx + S(28), my + S(28)], fill=(60, 30, 30), outline=BLK, width=3)
    elif mood == "smile":
        d.arc([hx - S(40), my - S(20), hx + S(40), my + S(20)], 20, 160, fill=BLK, width=max(2, int(S(6))))
    else:
        d.line([(hx - S(35), my), (hx + S(35), my + S(8))], fill=BLK, width=max(2, int(S(6))))
    for k in (-1, 1): d.rectangle([hx + k * S(12) - S(6), my, hx + k * S(12) + S(6), my + S(12)], fill=WHITE)
    if hat == "headset":
        d.arc([hx - S(110), hy - S(125), hx + S(110), hy + S(60)], 190, 350, fill=(40, 40, 40), width=max(3, int(S(12))))
        d.ellipse([hx - S(125), hy - S(25), hx - S(90), hy + S(25)], fill=(40, 40, 40))
        d.line([(hx - S(105), hy + S(20)), (hx - S(40), hy + S(70))], fill=(40, 40, 40), width=max(2, int(S(6))))

def loose_arm(d, x, y, s, rot=0.0, shirt=(225, 225, 215)):
    S = lambda v: v * s
    ca, sa = math.cos(rot), math.sin(rot)
    P = lambda a, b: (x + a * ca - b * sa, y + a * sa + b * ca)
    d.line([P(-S(90), 0), P(S(70), 0)], fill=dk(shirt, 0.85), width=int(S(42)))
    ex, ey = P(S(95), 0)
    d.ellipse([ex - S(28), ey - S(28), ex + S(28), ey + S(28)], fill=ZS)

CAPS = [
    (0.0, 3.0, "Si fueras *zombi en 2026*… ¿de qué trabajarías *para pagar la renta*?"),
    (3.0, 8.0, "Tu vocabulario: *\"cerebrooos\"*… y *tu última referencia laboral te la comiste*"),
    (8.0, 12.5, "*Trabajo #1:* oficinista *un lunes a las 8 a.m.*"),
    (12.5, 16.0, "Nadie nota que *estás muerto*… *empleado del mes*"),
    (16.0, 21.0, "*Trabajo #2:* atención a clientes. El cliente grita… tú: *\"mmmh\"*"),
    (21.0, 24.0, "*Calificación de empatía: perfecta*"),
    (24.0, 27.0, "*Trabajo #3:* extra en películas de zombis. *El papel de tu vida*"),
    (27.0, 31.0, "Pero el director dice que tu actuación *\"no es creíble\"*"),
    (31.0, 37.0, "*Trabajo #4:* reclutador. Solo buscas una cosa: *cerebros*"),
    (37.0, 42.0, "El problema no es que *se te caiga un brazo en plena junta*…"),
    (42.0, 49.0, "*Sin descanso, sin quejas, sin vacaciones*… y *te falta actitud*"),
    (49.0, 58.0, "¿De qué pondrías a trabajar *a un zombi*? *Comenta*"),
]

def s_hook(t):
    img = office(); d = ImageDraw.Draw(img)
    zomb(d, 540, FEET, 0.85, t, mood="groan", arms="desk")
    desk(d, 150, 930)
    d.rectangle([250, TT - 45, 470, TT], fill=WHITE, outline=BLK, width=3)
    d.text((360, TT - 22), "RENTA", font=F(34), fill=RED, anchor="mm")
    chip(d, "GUÍA LABORAL DE LOS MONSTRUOS", 230, bg=(150, 20, 40), size=50, appear=t / 0.3)
    chip(d, "EPISODIO 3", 330, bg=(30, 30, 40), fg=YEL, size=44, appear=(t - 0.4) / 0.3)
    return img, 1.0, 1.0

def s_intro(t):
    lt = t - 3.0
    img = office(); d = ImageDraw.Draw(img)
    zomb(d, 330, FEET, 0.8, t, mood="groan", arms="out")
    bubble(d, 330, 520, 520, 130, ["CEREBROOOS"], 64, a=(lt - 0.2) / 0.3)
    if lt > 2.3:
        sc = pop((lt - 2.3) / 0.3)
        d.rounded_rectangle([600, 760 - 230 * sc, 1000, 760 + 230 * sc], 12, fill=(250, 248, 238), outline=BLK, width=5)
        if sc > 0.9:
            d.text((800, 580), "CARTA DE", font=F(40), fill=(40, 40, 40), anchor="mm")
            d.text((800, 630), "RECOMENDACIÓN", font=F(36), fill=(40, 40, 40), anchor="mm")
            for k in range(4): d.line([(640, 700 + k * 40), (960, 700 + k * 40)], fill=(170, 170, 170), width=4)
            d.chord([880, 880, 1080, 1060], 90, 270, fill=(210, 205, 195))
            for k in range(5): d.polygon([(905 + 0, 900 + k * 32), (925, 912 + k * 32), (905, 924 + k * 32)], fill=(250, 248, 238))
    return img, 1.0, 1.0

def s_office(t):
    lt = t - 8.0
    img = office(); d = ImageDraw.Draw(img)
    if lt < 4.5:
        d.rounded_rectangle([640, 330, 1010, 470], 16, fill=WHITE, outline=BLK, width=5)
        d.text((825, 400), "LUNES 8:00", font=F(46), fill=RED, anchor="mm")
        guy(d, 200, FEET, 0.6, mood="neutral", look=0, t=t, hoodie=(150, 150, 160))
        zomb(d, 520, FEET, 0.65, t, mood="groan", arms="desk")
        guy(d, 850, FEET, 0.6, mood="neutral", look=0, t=t, hoodie=(150, 150, 160))
        desk(d, 60, 1020)
        for x in (200, 520, 850):
            d.rectangle([x - 40, TT - 70, x + 30, TT], fill=WHITE, outline=BLK, width=3)
            d.arc([x + 20, TT - 55, x + 50, TT - 20], 270, 90, fill=BLK, width=5)
        for k in range(3):
            d.text((200 + k * 325, 700), "zzz" if k != 1 else "grr", font=F(48), fill=(90, 90, 110), anchor="mm")
    else:
        lt2 = lt - 4.5
        d.rounded_rectangle([290, 520, 790, 1170], 20, fill=(140, 95, 50), outline=BLK, width=8)
        win = (330, 560, 750, 1020)
        tmp = Image.new("RGB", (W, H), (200, 220, 235)); td = ImageDraw.Draw(tmp)
        zomb(td, 530, 1400, 1.0, t, mood="smile", arms="down")
        img.paste(tmp.crop(win), win[:2]); d = ImageDraw.Draw(img)
        d.text((540, 1090), "EMPLEADO DEL MES", font=F(42), fill=YEL, anchor="mm")
        if lt2 > 0.5: bigtext(d, "¡FELICIDADES!", 540, 430, int(70 * pop((lt2 - 0.5) / 0.3)), fill=(40, 150, 80), stroke=WHITE, sw=8)
    chip(d, "TRABAJO #1: OFICINISTA", 230, bg=(30, 110, 210), size=52, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_call(t):
    lt = t - 16.0
    img = office(); d = ImageDraw.Draw(img)
    zomb(d, 330, FEET, 0.8, t, mood="groan" if int(t * 2) % 2 else "blank", outfit="call", hat="headset", arms="desk")
    desk(d, 80, 1000)
    d.rectangle([620, TT - 220, 940, TT - 20], fill=(30, 30, 40), outline=BLK, width=5)
    d.rectangle([640, TT - 200, 920, TT - 40], fill=(60, 90, 150))
    if lt < 5.0:
        for i, (st, txt) in enumerate([(0.3, "¡ESTO ES INACEPTABLE!"), (1.5, "¡VOY A CANCELAR!"), (2.7, "¡QUIERO A SU SUPERVISOR!")]):
            if lt > st: bubble(d, 640, 420 + i * 120, 700, 90, [txt], 40, col=(255, 225, 225), a=(lt - st) / 0.25)
        if lt > 3.8: bubble(d, 300, 760, 260, 110, ["mmmh"], 56, a=(lt - 3.8) / 0.3)
    else:
        lt2 = lt - 5.0
        d.text((540, 480), "★★★★★", font=F(110), fill=(250, 190, 30), anchor="mm", stroke_width=6, stroke_fill=BLK)
        bigtext(d, "EMPATÍA: 100%", 540, 640, int(70 * pop(lt2 / 0.3)), fill=(40, 150, 80), stroke=WHITE, sw=8)
    chip(d, "TRABAJO #2: ATENCIÓN A CLIENTES", 230, bg=(90, 140, 200), size=48, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_movie(t):
    lt = t - 24.0
    img = grad((40, 40, 55), (80, 70, 90)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(60, 55, 60))
    d.polygon([(380, 0), (700, 0), (900, 1200), (180, 1200)], fill=(90, 85, 100))
    zomb(d, 540, FEET, 0.8, t, mood="groan" if lt < 3 else "blank", outfit="movie", arms="out" if lt < 3 else "shrug")
    cx, cy = 180, 700
    d.rectangle([cx - 120, cy - 20, cx + 120, cy + 140], fill=(30, 30, 30), outline=WHITE, width=4)
    d.text((cx, cy + 60), "TOMA 47", font=F(40), fill=WHITE, anchor="mm")
    ang = -0.4 if int(t * 3) % 6 == 0 else 0
    d.polygon([(cx - 120, cy - 20), (cx + 120, cy - 20 + ang * 100), (cx + 120, cy - 70 + ang * 100), (cx - 120, cy - 70)], fill=(30, 30, 30), outline=WHITE)
    for k in range(6): d.line([(cx - 100 + k * 40, cy - 70), (cx - 80 + k * 40, cy - 20)], fill=WHITE, width=6)
    if lt > 3.0:
        bubble(d, 760, 520, 520, 150, ["¡NO ES", "CREÍBLE!"], 52, col=(255, 230, 200), a=(lt - 3.0) / 0.3)
        d.polygon([(920, 640), (1000, 600), (1000, 700)], fill=(240, 200, 40), outline=BLK)
    chip(d, "TRABAJO #3: EXTRA DE PELÍCULA", 230, bg=(150, 120, 100), size=48, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_recruit(t):
    lt = t - 31.0
    img = office(); d = ImageDraw.Draw(img)
    zomb(d, 300, FEET, 0.8, t, mood="blank", outfit="suit", arms="desk")
    desk(d, 60, 1020)
    for k in range(int(cl(lt / 2.0) * 8)):
        d.rectangle([600 + (k % 2) * 30, TT - 20 - k * 22, 900 + (k % 2) * 30, TT - k * 22], fill=(250, 248, 238), outline=BLK, width=3)
    if lt > 2.5:
        sc = pop((lt - 2.5) / 0.3)
        d.rounded_rectangle([540 - 330 * sc, 520 - 90 * sc, 540 + 330 * sc, 520 + 90 * sc], int(20 * sc), fill=WHITE, outline=BLK, width=6)
        d.text((540, 490), "SE BUSCA:", font=F(max(8, int(44 * sc))), fill=(40, 40, 40), anchor="mm")
        d.text((540, 555), "CEREBROS", font=F(max(8, int(66 * sc))), fill=RED, anchor="mm")
    chip(d, "TRABAJO #4: RECLUTADOR", 230, bg=(60, 60, 75), size=52, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_arm(t):
    lt = t - 37.0
    img = office(); d = ImageDraw.Draw(img)
    off = lt > 2.5
    guy(d, 180, FEET, 0.65, mood="scared" if off else "neutral", look=1, t=t, hoodie=(90, 130, 200))
    zomb(d, 540, FEET, 0.7, t, mood="blank", arms="desk", arm_off=off)
    guy(d, 880, FEET, 0.65, mood="scared" if off else "neutral", look=-1, t=t)
    desk(d, 40, 1040)
    if off:
        fall = ease((lt - 2.5) / 0.4)
        loose_arm(d, 400, lerp(TT - 260, TT - 20, fall), 0.7, rot=lerp(-1.2, 0.1, fall))
        if lt > 3.0: bigtext(d, "¡PLOP!", 400, TT - 200, int(70 * pop((lt - 3.0) / 0.25)), fill=RED, stroke=WHITE, sw=8)
    chip(d, "JUNTA SEMANAL", 230, bg=(30, 30, 40), fg=YEL, size=52, appear=lt / 0.3)
    return img, 1.0, 1.0, (2.9 < lt < 3.2)

def s_boss(t):
    lt = t - 42.0
    img = office(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([110, 330, 970, 1050], 30, fill=(252, 250, 240), outline=BLK, width=8)
    d.text((540, 410), "EVALUACIÓN ANUAL", font=F(58), fill=(40, 40, 40), anchor="mm")
    for i, (st, txt) in enumerate([(0.4, "Sin descanso"), (1.2, "Sin quejas"), (2.0, "Sin vacaciones")]):
        if lt < st: continue
        y = 540 + i * 120
        d.rounded_rectangle([170, y - 40, 250, y + 40], 16, outline=BLK, width=6, fill=WHITE)
        check(d, 210, y, 0.7)
        d.text((290, y), txt, font=F(48), fill=(30, 30, 30), anchor="lm")
    if lt > 3.4:
        paste_stamp(img, 540, 1000, "TE FALTA ACTITUD", (200, 30, 30), (lt - 3.4) / 0.3)
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 49.0
    img = office(); d = ImageDraw.Draw(img)
    zomb(d, 540, FEET + 40, 0.9, t, mood="groan", arms="out")
    sc = pop(lt / 0.35)
    d.rounded_rectangle([540 - 380 * sc, 330 - 90 * sc, 540 + 380 * sc, 330 + 90 * sc], int(26 * sc), fill=(150, 20, 40), outline=WHITE, width=6)
    d.text((540, 300), "¿DE QUÉ LO PONDRÍAS", font=F(max(8, int(48 * sc))), fill=WHITE, anchor="mm")
    d.text((540, 365), "A TRABAJAR?", font=F(max(8, int(48 * sc))), fill=YEL, anchor="mm")
    if lt > 1.5: chip(d, "COMENTA  ·  SÍGUEME", 500, bg=(30, 30, 40), fg=WHITE, size=48, appear=(lt - 1.5) / 0.3)
    return img, 1.0, 1.0

SCENES = [(0, 3, s_hook), (3, 8, s_intro), (8, 16, s_office), (16, 24, s_call), (24, 31, s_movie), (31, 37, s_recruit),
          (37, 42, s_arm), (42, 49, s_boss), (49, 99, s_end)]

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
        sheet.save("sheet_r18.png"); sys.exit()
    from warp18 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(57.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
