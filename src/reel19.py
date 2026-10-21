import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, check, xmark, guy, zombie,
                  W, H, YEL, RED, WHITE, BLK, SKIN, FEET)
from reel8 import store_day, employee, ice_machine, ice, fridge_empty
from reel17 import paste_stamp

FPS = 30

def grad(top, bot):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0, y), (W, y)], fill=lc(top, bot, y / H))
    return img

def thermo(d, x, y, s, frac, label="45 °C"):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(28), y - S(260), x + S(28), y + S(20)], int(S(28)), fill=WHITE, outline=BLK, width=5)
    d.ellipse([x - S(55), y - S(10), x + S(55), y + S(100)], fill=RED, outline=BLK, width=5)
    h = S(250) * frac
    d.rectangle([x - S(14), y + S(10) - h, x + S(14), y + S(20)], fill=RED)
    d.text((x + S(80), y - S(150)), label, font=F(max(8, int(S(60)))), fill=RED, anchor="lm", stroke_width=5, stroke_fill=WHITE)

def key_on_neck(d, x, y, s):
    S = lambda v: v * s
    hx, hy = x, y - S(505)
    d.line([(hx - S(60), hy + S(100)), (hx, hy + S(220)), (hx + S(60), hy + S(100))], fill=(150, 150, 160), width=max(2, int(S(6))))
    d.ellipse([hx - S(22), hy + S(205), hx + S(22), hy + S(249)], outline=(230, 190, 40), width=max(3, int(S(10))))
    d.rectangle([hx - S(6), hy + S(245), hx + S(6), hy + S(320)], fill=(230, 190, 40))
    d.rectangle([hx + S(6), hy + S(290), hx + S(26), hy + S(302)], fill=(230, 190, 40))

def bags(d, x, y, s):
    S = lambda v: v * s
    hx, hy = x, y - S(505)
    for sx in (-1, 1):
        d.arc([hx + sx * S(35) - S(26), hy + S(10), hx + sx * S(35) + S(26), hy + S(40)], 0, 180, fill=(120, 90, 110), width=max(2, int(S(6))))

def milk(d, x, y, s, label="CADUCA HOY"):
    S = lambda v: v * s
    d.rectangle([x - S(70), y - S(150), x + S(70), y + S(100)], fill=WHITE, outline=BLK, width=5)
    d.polygon([(x - S(70), y - S(150)), (x, y - S(220)), (x + S(70), y - S(150))], fill=(220, 230, 240), outline=BLK)
    d.rectangle([x - S(70), y - S(80), x + S(70), y - S(20)], fill=(60, 120, 210))
    d.text((x, y - S(50)), "LECHE", font=F(max(8, int(S(32)))), fill=WHITE, anchor="mm")
    d.text((x, y + S(45)), label, font=F(max(8, int(S(24)))), fill=RED, anchor="mm")

def sun_desert(t):
    img = grad((255, 190, 80), (255, 230, 150)); d = ImageDraw.Draw(img)
    d.ellipse([720, 160, 980, 420], fill=(255, 250, 200))
    for k in range(12):
        a = k / 12 * 2 * math.pi + t * 0.4
        d.line([(850 + math.cos(a) * 150, 290 + math.sin(a) * 150), (850 + math.cos(a) * 220, 290 + math.sin(a) * 220)], fill=(255, 240, 160), width=12)
    d.rectangle([0, 1150, W, H], fill=(215, 170, 100))
    for k in range(5):
        y = 1050 + k * 30
        pts = [(x, y + math.sin(x / 60 + t * 4 + k) * 8) for x in range(0, W + 40, 40)]
        d.line(pts, fill=(255, 230, 170), width=3)
    for x in (80, 990):
        d.rounded_rectangle([x - 22, 820, x + 22, 1150], 20, fill=(70, 140, 70), outline=BLK, width=4)
        d.rounded_rectangle([x - 70, 900, x - 30, 1010], 18, fill=(70, 140, 70), outline=BLK, width=4)
        d.rounded_rectangle([x + 30, 940, x + 70, 1040], 18, fill=(70, 140, 70), outline=BLK, width=4)
    return img

def ticket(d, cx, cy, sc):
    d.rectangle([cx - 160 * sc, cy - 170 * sc, cx + 160 * sc, cy + 170 * sc], fill=WHITE, outline=BLK, width=4)
    for i, (a, b) in enumerate([("HIELO 5 kg", "$25.00"), ("IVA", "$4.00"), ("TOTAL", "$29.00")]):
        y = cy - 110 * sc + i * 80 * sc
        d.text((cx - 140 * sc, y), a, font=F(max(8, int(30 * sc))), fill=(30, 30, 30), anchor="lm")
        d.text((cx + 140 * sc, y), b, font=F(max(8, int(30 * sc))), fill=RED if a == "IVA" else (30, 30, 30), anchor="rm")
    d.text((cx, cy + 130 * sc), "GRACIAS POR SU COMPRA", font=F(max(8, int(20 * sc))), fill=(90, 90, 90), anchor="mm")

CAPS = [
    (0.0, 4.0, "*Día 3* del apocalipsis zombi. *En pleno verano de Sonora*"),
    (4.0, 7.0, "*100 zombis* afuera, *2 humanos* adentro… y *una máquina de hielo*"),
    (7.0, 11.0, "¿Quién la controla? *El empleado.* Sin dormir, *cero cigarros*… y *la única llave*"),
    (11.0, 15.0, "Los zombis llevan 3 días *a 45 grados*… *se echan a perder* más rápido que la leche"),
    (15.0, 17.0, "Ya les revisé *la fecha de caducidad*… *a los dos*"),
    (17.0, 23.0, "Sin luz: refri cerrado *4 horas*. Congelador lleno *48*, medio vacío *24*"),
    (23.0, 25.0, "*El gerente aguantó menos*"),
    (25.0, 29.0, "*Regla 1:* nadie abre el refri *\"a ver si sigue frío\"*"),
    (29.0, 33.0, "*Regla 2:* el hielo es para la comida… *ni para el dedo de Don Toño*"),
    (33.0, 37.0, "*Regla 3:* +4 horas sin luz: *carne, pollo, huevos y sobras a la basura*"),
    (37.0, 39.0, "*Sin excepciones.* Ni para los que *se quedaron afuera*"),
    (39.0, 45.0, "El empleado abre *otra caja*… y les vende el hielo *con todo e IVA*"),
    (45.0, 49.0, "En Sonora el hielo no es un lujo… *es infraestructura*"),
    (49.0, 58.0, "¿De qué lado estás: *empleado, zombis o hielo*? *Comenta*"),
]

def s_hook(t):
    img, d = store_day(t)
    ice_machine(d, 300, 1180, 0.75, t, glow=0.5)
    guy(d, 620, FEET, 0.75, mood="scared", look=-1, t=t)
    employee(d, 860, FEET, 0.75, t)
    key_on_neck(d, 860, FEET, 0.75)
    chip(d, "DÍA 3 · SONORA", 230, bg=RED, size=64, appear=t / 0.3)
    if t < 4.0:
        thermo(d, 140, 640, 1.0, cl(t / 2.0) * 0.95)
    else:
        lt = t - 4.0
        for i, (st, txt, c) in enumerate([(0.0, "100 ZOMBIS", RED), (1.0, "2 HUMANOS", (30, 110, 210)), (2.0, "1 MÁQUINA DE HIELO", (40, 150, 200))]):
            if lt > st: chip(d, txt, 350 + i * 95, bg=c, size=46, appear=(lt - st) / 0.25)
    return img, 1.0, 1.0

def s_employee(t):
    lt = t - 7.0
    img, d = store_day(t)
    ice_machine(d, 280, 1180, 0.75, t, glow=0.8)
    employee(d, 700, FEET + 60, 1.05, t)
    bags(d, 700, FEET + 60, 1.05)
    key_on_neck(d, 700, FEET + 60, 1.05)
    if lt > 1.5:
        sc = pop((lt - 1.5) / 0.3)
        d.text((640, 600), "EL QUE TIENE LA LLAVE", font=F(max(8, int(50 * sc))), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)
        d.text((640, 670), "TIENE EL HIELO", font=F(max(8, int(50 * sc))), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)
    chip(d, "EL EMPLEADO", 230, bg=(90, 160, 90), size=56, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_heat(t):
    lt = t - 11.0
    img = sun_desert(t); d = ImageDraw.Draw(img)
    for i, zx in enumerate((220, 520, 820)):
        zombie(d, zx, FEET, 0.6, t + i, face=-1, shade=1.0)
        for k in range(3):
            yy = FEET - 420 + ((lt * 120 + k * 50 + i * 30) % 150)
            d.ellipse([zx - 60 + k * 50, yy, zx - 46 + k * 50, yy + 22], fill=(140, 200, 240))
    thermo(d, 120, 600, 0.8, 0.98, "45 °C")
    if lt > 2.5:
        milk(d, 110, 1240, 0.75)
    if lt > 4.0:
        for zx in (220, 520, 820):
            sc = pop((lt - 4.0) / 0.3)
            d.rounded_rectangle([zx - 90 * sc, FEET - 620 - 30 * sc, zx + 90 * sc, FEET - 620 + 30 * sc], 8, fill=WHITE, outline=RED, width=4)
            d.text((zx, FEET - 620), "VENCIDO", font=F(max(8, int(30 * sc))), fill=RED, anchor="mm")
    chip(d, "AFUERA: 45 °C", 230, bg=(230, 120, 30), size=56, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_data(t):
    lt = t - 17.0
    img = grad((40, 45, 60), (20, 22, 30)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, H], fill=(50, 50, 60))
    fridge_empty(d, 90, 520, 380, 620, open_=0.0)
    d.text((280, 470), "REFRI", font=F(48), fill=WHITE, anchor="mm")
    sc = pop((lt - 0.4) / 0.3)
    d.ellipse([280 - 110 * sc, 830 - 110 * sc, 280 + 110 * sc, 830 + 110 * sc], fill=WHITE, outline=BLK, width=6)
    d.text((280, 830), "4 h", font=F(max(8, int(70 * sc))), fill=RED, anchor="mm")
    d.rectangle([560, 520, 990, 1140], fill=(215, 230, 245), outline=BLK, width=6)
    d.text((775, 470), "CONGELADOR", font=F(44), fill=WHITE, anchor="mm")
    for i, (st, lab, frac, col) in enumerate([(1.8, "LLENO: 48 h", 1.0, (40, 150, 200)), (3.4, "MEDIO: 24 h", 0.5, (230, 150, 40))]):
        if lt < st: continue
        y = 640 + i * 220
        d.rectangle([600, y, 950, y + 70], fill=(255, 255, 255), outline=BLK, width=4)
        d.rectangle([600, y, 600 + 350 * frac * cl((lt - st) / 0.6), y + 70], fill=col)
        d.text((775, y + 115), lab, font=F(42), fill=(30, 30, 30), anchor="mm")
    chip(d, "SE FUE LA LUZ", 230, bg=(30, 30, 40), fg=YEL, size=56, appear=lt / 0.3)
    if lt > 6.0:
        lt2 = lt - 6.0
        d.rectangle([0, 0, W, H], fill=None)
        d.rounded_rectangle([340, 300, 740, 420], 14, fill=WHITE, outline=BLK, width=5)
        d.text((540, 340), "GERENTE", font=F(46), fill=(40, 40, 40), anchor="mm")
        d.text((540, 395), "aguantó: 3 h 59 min", font=F(30), fill=RED, anchor="mm")
    return img, 1.0, 1.0

RULES = [(25.3, "1. No abrir el refri"), (29.3, "2. Hielo solo para comida"), (33.3, "3. +4 h sin luz: a la basura")]

def s_rules(t):
    lt = t - 25.0
    img, d = store_day(t)
    ice_machine(d, 760, 1180, 0.7, t, glow=0.5)
    employee(d, 330, FEET, 0.8, t)
    key_on_neck(d, 330, FEET, 0.8)
    d.rounded_rectangle([80, 300, 1000, 640], 24, fill=(252, 250, 240), outline=BLK, width=7)
    d.text((540, 350), "REGLAS DEL HIELO", font=F(52), fill=(40, 40, 40), anchor="mm")
    for i, (st, txt) in enumerate(RULES):
        if t < st: continue
        d.text((120, 430 + i * 70), txt, font=F(int(42 * cl((t - st) / 0.25)) + 1), fill=(30, 30, 30), anchor="lm")
    if 29.8 < t < 33.0:
        sc = pop((t - 29.8) / 0.3)
        bx, by = 560, 760
        d.rounded_rectangle([bx - 120 * sc, by - 90 * sc, bx + 120 * sc, by + 90 * sc], int(30 * sc), fill=(210, 235, 250), outline=BLK, width=4)
        d.rounded_rectangle([bx - 45 * sc, by - 20 * sc, bx + 45 * sc, by + 10 * sc], int(15 * sc), fill=SKIN, outline=BLK, width=3)
        d.ellipse([bx + 25 * sc, by - 18 * sc, bx + 43 * sc, by + 6 * sc], fill=(250, 230, 220))
        d.rectangle([bx - 110 * sc, by + 40 * sc, bx + 110 * sc, by + 80 * sc], fill=WHITE, outline=BLK, width=2)
        d.text((bx, by + 60 * sc), "DON TOÑO - NO TIRAR", font=F(max(8, int(22 * sc))), fill=RED, anchor="mm")
    if 33.3 < t < 37.0:
        sc = pop((t - 33.6) / 0.3)
        d.rounded_rectangle([660, 960 - 0, 900, 1200], 16, fill=(70, 80, 90), outline=BLK, width=5)
        d.rectangle([640, 930, 920, 970], fill=(90, 100, 110), outline=BLK, width=4)
        for k, c in enumerate([(200, 80, 80), (250, 240, 220), (230, 190, 120)]):
            d.ellipse([690 + k * 70, 900 - 40 * sc, 740 + k * 70, 950 - 40 * sc], fill=c, outline=BLK, width=3)
    if t > 37.0:
        chip(d, "LOS DE AFUERA: SIN EXCEPCIÓN", 720, bg=RED, size=46, appear=(t - 37.0) / 0.3)
    return img, 1.0, 1.0

def s_sale(t):
    lt = t - 39.0
    img, d = store_day(t, zombies_at_door=False)
    d.rectangle([60, 1000, 1020, 1200], fill=(150, 110, 75), outline=BLK, width=6)
    employee(d, 760, FEET - 200, 0.6, t)
    d.rectangle([60, 1000, 1020, 1200], fill=(150, 110, 75), outline=BLK, width=6)
    d.rounded_rectangle([600, 860, 760, 1000], 10, fill=(60, 60, 70), outline=BLK, width=4)
    d.text((680, 900), "CAJA 2", font=F(30), fill=(100, 255, 150), anchor="mm")
    for i in range(int(cl(lt / 1.5) * 4)):
        zombie(d, 420 - i * 120, FEET, 0.55, t + i, face=1, shade=1.0)
        ice(d, 420 - i * 120 + 70, FEET - 230, 0.6)
    if lt > 2.5:
        ticket(d, 260, 560, pop((lt - 2.5) / 0.3))
    chip(d, "SE ABRE LA CAJA 2", 230, bg=(40, 150, 80), size=56, appear=lt / 0.3)
    return img, 1.0, 1.0

def s_infra(t):
    lt = t - 45.0
    img = sun_desert(t); d = ImageDraw.Draw(img)
    ice(d, 540, 900, 3.0)
    sc = pop(lt / 0.35)
    d.rounded_rectangle([540 - 380 * sc, 400 - 70 * sc, 540 + 380 * sc, 400 + 70 * sc], int(20 * sc), fill=(40, 120, 210), outline=WHITE, width=6)
    d.text((540, 400), "HIELO = INFRAESTRUCTURA", font=F(max(8, int(46 * sc))), fill=WHITE, anchor="mm")
    return img, 1.0, 1.0

def s_end(t):
    lt = t - 49.0
    img, d = store_day(t)
    for i, (txt, c) in enumerate([("EL EMPLEADO", (90, 160, 90)), ("LOS ZOMBIS", (200, 40, 50)), ("EL HIELO", (40, 120, 210))]):
        if lt < 0.2 + i * 0.6: continue
        sc = pop((lt - 0.2 - i * 0.6) / 0.3)
        y = 420 + i * 150
        d.rounded_rectangle([540 - 330 * sc, y - 60 * sc, 540 + 330 * sc, y + 60 * sc], int(22 * sc), fill=c, outline=WHITE, width=6)
        d.text((540, y), txt, font=F(max(8, int(54 * sc))), fill=WHITE, anchor="mm")
    chip(d, "¿DE QUÉ LADO ESTÁS? COMENTA", 230, bg=(30, 30, 40), fg=YEL, size=48, appear=lt / 0.3)
    return img, 1.0, 1.0

SCENES = [(0, 7, s_hook), (7, 11, s_employee), (11, 17, s_heat), (17, 25, s_data), (25, 39, s_rules), (39, 45, s_sale),
          (45, 49, s_infra), (49, 99, s_end)]

def render(t):
    for st, en, fn in SCENES:
        if st <= t < en: break
    r = fn(t)
    img = r[0]
    d = ImageDraw.Draw(img)
    for cs, ce, txt in CAPS:
        if cs <= t < ce: rich_caption(d, txt, appear=(t - cs) / 0.25)
    fi = cl((t - st) / 0.12) if st > 0 else 1.0
    b = 0.3 + 0.7 * fi
    arr = np.asarray(img)
    if b < 0.999: arr = (arr.astype(np.float32) * b).astype(np.uint8)
    return arr

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r19.png"); sys.exit()
    from warp19 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(min(57.99, v_of_T(i / FPS))).tobytes())
    p.stdin.close(); p.wait()
