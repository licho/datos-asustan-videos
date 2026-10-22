"""Cómo sobrevivir a Krampus esta noche (5 de diciembre, Noche de Krampus). Caricatura con cámara."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.core import say
from lib.motion import tw, yoyo, layer, shake, back_out, cubic_out, radial_bg
from lib.personajes import guy, krampus, st_nicholas, anchors
from lib.props import bells, scroll, phone_chat, mug, chair, document, house, tree, snowflake, arrow, sign_board
from reels_engine.camera import Shot, film, path, pan, zoom_in, ken_burns, whip, impact, handheld

NAME = "2026-12-05_krampus"
END = 4.5
LINES = [
 ("whispers", "Hoy, cinco de diciembre, es la Noche de Krampus. Y si te portaste mal este año… esto te interesa.", "Hoy, 5 de diciembre, es *la Noche de Krampus*. ¿Te portaste mal?"),
 ("serious", "Krampus es el compañero oscuro de San Nicolás en los Alpes: cuernos, lengua larguísima, una pezuña de cabra… y un pie humano. Nadie es perfecto.", "El compañero oscuro de San Nicolás: *una pezuña… y un pie humano*"),
 ("dramatically", "Su nombre viene de “krampen”, garra en alemán. Trae cadenas, cascabeles, un manojo de varas… y un costal para llevarse a los que se portaron mal.", "*“Krampen” = garra*. Cadenas, cascabeles, varas… *y un costal*"),
 ("confident", "Así sobrevives. Paso uno: confiesa tus pecados del año. Sí, el “visto” que le dejaste a tu tía también cuenta.", "*Paso 1:* confiesa tus pecados. *El “visto” a tu tía cuenta*"),
 ("sarcastic", "Paso dos: si a medianoche oyes cascabeles… no es el carrito de los elotes. Escóndete.", "*Paso 2:* si oyes cascabeles a medianoche… *no son los elotes*"),
 ("mischievously", "Paso tres: no le dejes galletas, él no es Santa. Mejor ofrécele una silla y un café: lleva siglos haciendo turno nocturno.", "*Paso 3:* no le dejes galletas. *Ofrécele un café*"),
 ("serious", "Paso cuatro: si te encuentra, finge que te portaste bien. Enséñale una boleta de puros dieces… de tu primo.", "*Paso 4:* enséñale una boleta de puros dieces… *de tu primo*"),
 ("excited", "Paso cinco: corre hacia San Nicolás. Es el único que lo controla… porque es su jefe.", "*Paso 5:* corre hacia San Nicolás… *es su jefe*"),
 ("whispers", "Dato real: en pueblos de Austria y Alemania, cada diciembre, la gente se disfraza de Krampus y sale a correr por las calles persiguiendo a los demás. Se llama Krampuslauf… y sí, a veces dan varazos.", "Dato real: en Austria y Alemania hacen el *Krampuslauf*… *y a veces dan varazos*"),
 ("sarcastic", "¿Te portaste bien este año? Dime la verdad en los comentarios… Krampus está leyendo.", "¿Te portaste bien? *Krampus está leyendo*"),
]
NIGHT = ((0, (55, 65, 120)), (.6, (25, 30, 70)), (1, (10, 12, 35)))

def snow_fall(d, t, n=18, seed=5, box=(0, 0, W, 1300)):
    r = random.Random(seed)
    for k in range(n):
        x0, sp, sz = r.uniform(box[0], box[2]), r.uniform(60, 130), r.uniform(10, 20)
        y = box[1] + (t * sp + r.uniform(0, box[3])) % (box[3] - box[1]); x = x0 + math.sin(t * 2 + k) * 25
        snowflake(d, x, y, sz, col=WHITE, width=4)

def village(t, w=W, h=H, lights=True):
    """Pueblo alpino nevado de noche (mundo para la cámara)."""
    img = radial_bg(NIGHT, cy=600).resize((w, h)); d = ImageDraw.Draw(img)
    for k, (x0, top, x1) in enumerate(((-200, 520, 520), (300, 440, 1050), (750, 560, 1400))):
        d.polygon([(x0, 1000), ((x0 + x1) / 2, top), (x1, 1000)], fill=(70, 80, 120))
        d.polygon([((x0 + x1) / 2 - 90, top + 100), ((x0 + x1) / 2, top), ((x0 + x1) / 2 + 90, top + 100)], fill=(235, 240, 250))
    d.rectangle([0, 1000, w, h], fill=(225, 232, 245)); d.line([(0, 1000), (w, 1000)], fill=(180, 190, 210), width=6)
    for k, x in enumerate((120, 420, 760, 1000)):
        if x < w: house(d, x, 1250, .9 + .1 * (k % 2), wall=(230, 200, 160), roof=(120, 60, 50), lights=lights)
    tree(d, 290, 1260, .9, kind="pine", col=(40, 100, 70)); tree(d, 900, 1250, .8, kind="pine", col=(40, 100, 70))
    d.rectangle([0, 1250, w, 1380], fill=(240, 244, 252))
    return img, d

def tag(img, text, x, y, k, rot=-10, bg=RED, size=56):
    def fn(dd, cx, cy):
        f = F(size); ww = dd.textlength(text, font=f) + 70
        dd.rounded_rectangle([cx - ww / 2, cy - size * .8, cx + ww / 2, cy + size * .8], 30, fill=bg, outline=BLK, width=6)
        dd.text((cx, cy), text, font=f, fill=WHITE, anchor="mm")
    return layer(img, fn, x, y, 1000, sx=k, sy=k, rot=rot)

# ------------------------------------------------------------------ escenas
def hook(c):
    world, d = village(c.t)
    d.rectangle([700, 1060, 800, 1150], fill=(255, 220, 120))
    if c.lt > 1.2: krampus(d, 960, 1250, .32, c.t, mood="grin", rods=False)              # ronda el pueblo
    d.rectangle([700, 1060, 800, 1150], outline=BLK, width=6); d.line([(750, 1060), (750, 1150)], fill=BLK, width=5)
    snow_fall(d, c.t)
    img = Image.new("RGB", (W, H)); film(img, world, handheld(path(c.lt, [(0, Shot(540, 960, 1.0)), (c.dur, Shot(860, 1050, 1.7))]), c.t, 5))
    d = ImageDraw.Draw(img)
    chip(d, "5 DE DICIEMBRE", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def who(c):
    world = radial_bg(((0, (90, 60, 80)), (1, (30, 18, 30))), cy=800); d = ImageDraw.Draw(world)
    d.rectangle([0, 1250, W, 1380], fill=(60, 40, 50))
    krampus(d, 540, 1290, 1.05, c.t, mood="grin")
    f = c.lt / c.dur
    img = Image.new("RGB", (W, H)); film(img, world, path(c.lt, [(0, Shot(540, 700, 2.0)), (c.dur * .45, Shot(540, 960, 1.0))]))
    d = ImageDraw.Draw(img)
    if f > .5:
        arrow(d, 250, 1100, 420, 1250, col=YEL, w=12); d.text((230, 1070), "PEZUÑA", font=F(44), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)
    if f > .65:
        arrow(d, 860, 1080, 680, 1240, col=YEL, w=12); d.text((880, 1050), "PIE HUMANO", font=F(44), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)
    chip(d, "¿QUIÉN ES KRAMPUS?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def gear(c):
    img = radial_bg(((0, (70, 50, 60)), (1, (25, 18, 25))), cy=800); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    bigtext(d, "KRAMPEN = GARRA", 540, 520, 70, fill=YEL)
    items = ["cadenas", "cascabeles", "varas", "costal"]
    for i, it in enumerate(items):
        if f < .15 + i * .18: continue
        x, y = 160 + (i % 2) * 520, 700 + (i // 2) * 320
        d.rounded_rectangle([x - 20, y - 20, x + 380, y + 260], 24, fill=(45, 32, 40), outline=(200, 180, 150), width=5)
        cx, cy = x + 180, y + 110
        if it == "cadenas":
            for k in range(6): d.ellipse([cx - 150 + k * 50, cy - 20, cx - 100 + k * 50, cy + 20], outline=(170, 170, 180), width=10)
        elif it == "cascabeles": bells(d, cx, cy - 40, 1.6, c.t)
        elif it == "varas":
            for k in range(6): d.line([(cx - 20 + k * 6, cy - 70), (cx - 90 + k * 30, cy + 90)], fill=(150, 115, 70), width=8)
            d.rectangle([cx - 30, cy - 85, cx + 30, cy - 50], fill=RED, outline=BLK, width=4)
        else:
            wob = math.sin(c.t * 8) * 10
            d.ellipse([cx - 90 + wob, cy - 80, cx + 90 + wob, cy + 90], fill=(150, 120, 80), outline=BLK, width=6)
            d.line([(cx - 20 + wob, cy - 80), (cx + 20 + wob, cy - 80)], fill=(110, 85, 55), width=14)
        d.text((x + 180, y + 225), it.upper(), font=F(40), fill=WHITE, anchor="mm")
    chip(d, "SU EQUIPO", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def step1(c):
    world, d = village(c.t)
    img, d = canvas(((235, 225, 210), (205, 190, 170))); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(150, 120, 95))
    scroll(d, 70, 470, 440, 760, "MIS PECADOS 2026", ["· Robé wifi", "· Dije “ya voy”", "· Comí del refri", "· Dejé en visto", "  a mi tía" if f > .35 else ""], size=36)
    phone_chat(d, 580, 480, 420, 600, "TÍA", [("l", "¿Vienes a la cena?", "12:10"), ("r", "Visto 14:32", "")], shown=1 + int(f > .4), size=30)
    guy(d, 790, 1290, .5, mood="scared", t=c.t)
    chip(d, "PASO 1", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def step2(c):
    world, d = village(c.t, lights=False); lt = c.lt; f = lt / c.dur
    d.rectangle([860, 700, W, 1250], fill=(150, 120, 100), outline=BLK, width=6)
    for y in range(740, 1240, 60): d.line([(860, y), (W, y)], fill=(120, 95, 80), width=3)
    if f > .45:
        kx = tw(lt, c.dur * .45, .5, 1200, 990, back_out)
        krampus(d, kx, 1290, .8, c.t, mood="grin")
        d.rectangle([860, 700, 905, 1250], fill=(150, 120, 100), outline=BLK, width=6)
    bells(d, 960, 640, 1.2, c.t)
    guy(d, 420, 1290, .75, mood="scared" if f > .55 else "neutral", arms="up" if f > .55 else "down", t=c.t)
    img = Image.new("RGB", (W, H)); film(img, world, impact(Shot(540, 960, 1.0), lt, c.dur * .55, .4, 14))
    d = ImageDraw.Draw(img)
    if f < .5:
        a = anchors(420, 1290, .75); say(d, "¡Elotes!", a["mouth"], head=a["head_r"], size=50, maxw=320)
    chip(d, "PASO 2", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def step3(c):
    img = radial_bg(((0, (250, 220, 180)), (1, (190, 140, 110))), cy=800); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(140, 100, 70))
    d.rectangle([80, 520, 360, 760], fill=(40, 30, 50), outline=BLK, width=8); snow_fall(d, c.t, 6, box=(90, 530, 350, 750))
    chair(d, 640, 1290, 1.3, kind="chair", facing=-1)
    krampus(d, 600, 1290, .78, c.t, mood="tired" if f > .45 else "grin", arms="hold", rods=False)
    if f > .35: mug(d, 600, 1290 - .78 * 330 + 10, .45, c.t)
    if f > .6: d = tag(img, "TURNO NOCTURNO", 300, 1140, tw(lt, c.dur * .6, .4, 0, 1, back_out), bg=BLUE, size=48)
    chip(d, "PASO 3", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def step4(c):
    world, d = village(c.t); lt = c.lt; f = lt / c.dur
    krampus(d, 760, 1290, .85, c.t, mood="suspicious" if f > .45 else "grin")
    guy(d, 260, 1290, .7, mood="scared", arms="up", t=c.t)
    a = anchors(260, 1290, .7)
    document(d, a["hand_r_up"][0] - 20, a["hand_r_up"][1] - 180, 240, 300, "BOLETA", ["Mate: 10", "Español: 10", "Ciencias: 10", "", "Alumno: Primo" if f > .5 else ""], size=24)
    img = Image.new("RGB", (W, H)); film(img, world, path(lt, [(0, Shot(540, 960, 1.0)), (c.dur * .5, Shot(560, 900, 1.15))]))
    chip(ImageDraw.Draw(img), "PASO 4", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def step5(c):
    lt = c.lt; f = lt / c.dur
    world, d = village(c.t)
    world = world.resize((2000, H)); d = ImageDraw.Draw(world)
    d.rectangle([0, 1250, 2000, 1380], fill=(240, 244, 252))
    krampus(d, 380, 1290, .8, c.t, mood="stop" if f > .55 else "grin", arms="stop" if f > .55 else "down", flip=False)
    gx = tw(lt, 0, c.dur * .5, 700, 1380, cubic_out)
    guy(d, gx, 1290, .62, mood="scared", arms="up", t=c.t)
    st_nicholas(d, 1600, 1290, .85, c.t, mood="stern", arms="stop" if f > .5 else "down")
    img = Image.new("RGB", (W, H))
    film(img, world, whip(lt, c.dur * .25, .5, Shot(560, 960, 1.0), Shot(1440, 960, 1.0)))
    d = ImageDraw.Draw(img)
    if f > .6: d = tag(img, "ES SU JEFE", 540, 560, tw(lt, c.dur * .6, .4, 0, 1, back_out), bg=RED)
    chip(d, "PASO 5", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def parade(c):
    lt = c.lt
    world, d = village(c.t)
    world = world.resize((2200, H)); d = ImageDraw.Draw(world)
    d.rectangle([0, 1250, 2200, 1380], fill=(240, 244, 252))
    for k in range(4):
        kx = 500 + k * 380 + lt * 60
        krampus(d, kx, 1290, .62, c.t + k, mood="grin", mask=True, torch=True, rods=k % 2 == 0)
    for k in range(3):
        gx = 1900 + k * 120 + lt * 140
        guy(d, gx, 1290, .45, mood="scared", arms="up", t=c.t + k, hoodie=((90, 160, 220), (230, 120, 60), (120, 180, 90))[k])
    img = Image.new("RGB", (W, H))
    film(img, world, handheld(pan(lt, 0, c.dur, Shot(700, 960, 1.0), Shot(1600, 960, 1.0)), c.t, 6))
    d = ImageDraw.Draw(img)
    chip(d, "KRAMPUSLAUF", CHIP2 + 360, bg=GRAY, size=52, appear=(lt - .8) / .3)
    chip(d, "DATO REAL", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def ending(c):
    img = radial_bg(NIGHT, cy=800); d = ImageDraw.Draw(img); lt = c.lt
    world = Image.new("RGB", (W, H), (0, 0, 0)); wd = ImageDraw.Draw(world)
    world.paste(img, (0, 0)); krampus(wd, 900, 1290, 1.1, c.t, mood="suspicious", rods=False)
    film(img, world, path(lt, [(0, Shot(540, 960, 1.0)), (1.5, Shot(560, 960, 1.08))]))
    d = ImageDraw.Draw(img)
    bigtext(d, "¿TE PORTASTE", 400, 520, 76, fill=WHITE); bigtext(d, "BIEN?", 400, 620, 86, fill=YEL)
    follow_btn(d, lt, y=1240, delay=c.dur * .5)
    return img

SCENES = [(0, hook), (1, who), (2, gear), (3, step1), (4, step2), (5, step3), (6, step4), (7, step5), (8, parade), (9, ending)]
SFX = [(0, 1.6, "sting", {}), (1, .2, "whoosh", {}), (2, .5, "pop", {}), (2, 1.3, "pop", {}), (2, 2.1, "pop", {}), (2, 2.9, "thud", {}),
       (3, 1.5, "ding", {}), (4, 2.0, "thud", {}), (5, 2.5, "pop", {}), (6, 2.5, "boing", {}), (7, 1.2, "whoosh", {}), (7, 2.8, "buzzer", {}),
       (8, .3, "rumble", {}), (9, 2.0, "jingle", {})]
MUSIC = ("navidad_oscura", [(8, 9)], 9)
