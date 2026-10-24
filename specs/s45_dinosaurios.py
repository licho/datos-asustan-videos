"""¿Qué pasaría si los dinosaurios siguieran existiendo? (serie ¿Qué pasaría si…?). Caricatura con cámara y humor negro."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, layer, shake, back_out, cubic_out, radial_bg
from lib.personajes import stamp_point, guy, anchors, tyranno, raptor, pigeon, shrew, elephant, stamp_guy
from lib.props import (place_setting, candle, asteroid, picture, window, document, sneaker, table, sofa, tombstone, torta, soup_bowl,
                       snack_plate, pet_collar, tree)
from lib.fondos import living_room, city_street
from lib.efectos import tag, rubber_stamp
from reels_engine.camera import Shot, film, path, pan, zoom_in, impact, handheld

NAME = "2026-12-18_dinosaurios"
END = 4.5
LINES = [
 ("mischievously", "Los dinosaurios nunca se extinguieron… y uno te acaba de robar la torta.", "Los dinosaurios *nunca se extinguieron*… y uno *te robó la torta*"),
 ("serious", "¿Y si los grandes siguieran aquí? La mala noticia: tú probablemente no existirías. La buena: tu ex tampoco.", "¿Y si los grandes siguieran aquí? *Tú no existirías*… *tu ex tampoco*"),
 ("serious", "Hace sesenta y seis millones de años, un asteroide acabó con casi el setenta por ciento de las especies. Mientras los dinosaurios mandaban, el mamífero más grande pesaba unos diez kilos. Básicamente, éramos botana.", "Hace 66 millones de años: *adiós al 70% de las especies*. Los mamíferos pesaban *10 kilos*: *éramos botana*"),
 ("sarcastic", "Pero digamos que sí naces. El tiranosaurio muerde con hasta cincuenta y siete mil newtons: como si un elefante se te sentara encima. Y tu seguro de gastos médicos… «eso no lo cubre la póliza».", "Mordida: *57,000 newtons*. Como *un elefante encima*… y el seguro *no lo cubre*"),
 ("mischievously", "La buena noticia: un estudio dice que no podía correr; iba a unos dieciocho kilómetros por hora. Si te alcanza, en tu velorio dirán: «Al menos murió haciendo cardio».", "No podía correr: *18 km/h*. Si te alcanza… *al menos hiciste cardio*"),
 ("dramatically", "¿Y el velocirraptor de las películas? Era del tamaño de un pavo… y tenía plumas. En Navidad no sabrías si cenártelo… o si él te cena a ti.", "El velocirraptor real: *tamaño pavo y con plumas*. ¿Quién cena a quién?"),
 ("whispers", "¿Lo de la torta? No era broma: las aves son dinosaurios, del mismo grupo que el tiranosaurio. Hay unas once mil especies… y te están viendo.", "*Las aves SON dinosaurios*: unas *11,000 especies*… y te están viendo"),
 ("sarcastic", "Así que sí: la paloma de la torta es dinosaurio. Y el pollo de tu caldo también: te estás comiendo a los primos del tiranosaurio. Venganza servida… con limón.", "El pollo de tu caldo también es dinosaurio: *venganza con limón*"),
 ("", "¿Qué dinosaurio tendrías de mascota? Si dices tiranosaurio, deja tu testamento en los comentarios.", "¿Qué dinosaurio tendrías de mascota? Si es T. rex… *deja tu testamento*"),
]
JUNGLE = ((0, (190, 225, 170)), (1, (110, 165, 110)))
NIGHT = ((0, (60, 50, 90)), (1, (20, 18, 40)))

def jungle(w=W, h=H, seed=2):
    img = radial_bg(JUNGLE, cy=800).resize((w, h)); d = ImageDraw.Draw(img); r = random.Random(seed)
    for k in range(int(6 * w / W)): tree(d, r.uniform(0, w), 1100 + r.uniform(0, 60), r.uniform(.9, 1.4), kind=r.choice(("palm", "round")), col=(60, 140, 70))
    d.rectangle([0, 1290, w, 1380], fill=(120, 95, 65)); d.line([(0, 1290), (w, 1290)], fill=(90, 70, 45), width=6)
    return img, d

def blend(a, b, k):
    return Image.blend(a, b, cl(k))

# ------------------------------------------------------------------ escenas
def hook(c):
    f = c.lt / c.dur
    def room(person, ex):
        img, d = living_room()
        window(d, 90, 560, 430, 900, kind="day")
        if ex: picture(d, 690, 560, 960, 880, kind="portrait", label="MI EX")
        else: picture(d, 690, 560, 960, 880, kind="blank", label="MI EX")
        if person: guy(d, 540, 1290, .95, mood="scared" if f > .2 else "neutral", t=c.t)
        return img, d
    full, d = room(True, True)
    if f > .12:                                             # el T. rex se asoma por la ventana
        peek = Image.new("RGB", (W, H)); pk = radial_bg(((0, (150, 205, 240)), (1, (120, 180, 230))), cy=700); pd = ImageDraw.Draw(pk)
        tyranno(pd, tw(c.lt, c.dur * .12, c.dur * .3, -350, 10), 1250, 1.05, c.t, mood="grin", mouth=.25)
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle([102, 572, 418, 888], fill=255)
        full.paste(pk, (0, 0), mask); d = ImageDraw.Draw(full)
    img = full
    if f > .45:
        nop, _ = room(False, True)
        if f > .12: nop.paste(pk, (0, 0), mask)
        img = blend(full, nop, (f - .45) / .15)
    if f > .75:
        noex, _ = room(False, False)
        if f > .12: noex.paste(pk, (0, 0), mask)
        img = blend(img, noex, (f - .75) / .12)
    d = ImageDraw.Draw(img)
    chip(d, "¿QUÉ PASARÍA SI…?", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f > .45: bigtext(d, "TÚ: NO EXISTES", 540, 500, 62, fill=WHITE)
    if f > .75: tag(img, "TU EX: TAMPOCO", 820, 1000, cl((f - .75) / .1), rot=8, bg=RED, size=52)
    return img

def asteroid_snack(c):
    f = c.lt / c.dur
    if f < .38:
        img = radial_bg(((0, (250, 170, 90)), (1, (140, 60, 50))), cy=700); d = ImageDraw.Draw(img)
        d.rectangle([0, 1150, W, 1380], fill=(110, 70, 50))
        for k, x in enumerate((180, 520, 860)): tyranno(d, x, 1180, .3, c.t + k, mood="grin", mouth=0)
        k = cl(f / .3)
        asteroid(d, lerp(1000, 520, k), lerp(450, 1050, k), 120, c.t, face="angry", fire=1.0)
        if f > .3:
            fl = Image.new("RGB", (W, H), (255, 250, 230)); img = blend(img, fl, 1 - (f - .3) / .08); d = ImageDraw.Draw(img)
        chip(d, "HACE 66 MILLONES DE AÑOS", CHIP1, bg=RED, appear=c.lt / .3)
        if f > .3: bigtext(d, "ADIÓS AL 70% DE LAS ESPECIES", 540, 560, 56, fill=WHITE)
        return img
    img, d = jungle()
    d.rectangle([690, 1060, 930, 1290], fill=(150, 110, 70), outline=BLK, width=5)
    d.ellipse([690, 1040, 930, 1080], fill=(190, 150, 100), outline=BLK, width=5)
    snack_plate(d, 810, 1050, .75)
    shrew(d, 790, 1035, .85, c.t, mood="scared")
    tyranno(d, 300, 1290, .85, c.t, mood="grin", mouth=.3 + .2 * math.sin(c.t * 4), napkin=True)
    chip(d, "10 KILOS DE BOTANA", CHIP1, bg=ORANGE, appear=(f - .38) / .05)
    if f > .45: bigtext(d, "MAMÍFERO MÁS GRANDE: ~10 KG", 540, 560, 54, fill=WHITE)
    return img

_BITE = None
def bite(c):
    global _BITE
    f = c.lt / c.dur
    if f < .4:
        world, d = jungle(seed=5)
        tyranno(d, 380, 1290, 1.35, c.t, mood="angry", mouth=.2 + .8 * cl(c.lt / 1.2))
        img = Image.new("RGB", (W, H))
        film(img, world, path(c.lt, [(0, Shot(540, 960, 1.0)), (c.dur * .3, Shot(380 + 300 * 1.35, 1290 - 430 * 1.35, 1.9))]))
        d = ImageDraw.Draw(img)
        chip(d, "MORDIDA", CHIP1, bg=RED, appear=c.lt / .3)
        n = int(lerp(0, 57000, cl((f - .05) / .25)))
        bigtext(d, f"{n:,} NEWTONS", 540, 560, 72, fill=YEL)
        return img
    if f < .7:
        img, d = living_room()
        sh = (random.Random(int(c.t * 20)).randint(-6, 6) if f < .48 else 0)
        d.rectangle([180, 1236, 900, 1290], fill=(160, 60, 60), outline=BLK, width=5)               # sillón aplastado
        for x in (200, 860): d.rectangle([x, 1270, x + 20, 1290], fill=(90, 60, 40))
        drop = cl((f - .4) / .06)
        elephant(d, 560 + sh, lerp(450, 1250, back_out(drop) if drop < 1 else 1), 1.45, c.t, sit=True)
        chip(d, "MORDIDA", CHIP1, bg=RED)
        bigtext(d, "= UN ELEFANTE ENCIMA", 540, 560, 64, fill=YEL)
        return img
    img = radial_bg(((0, (225, 230, 240)), (1, (170, 180, 200))), cy=900); d = ImageDraw.Draw(img)
    document(d, 290, 620, 500, 640, title="PÓLIZA", lines=("Gastos médicos mayores", "Cubre: gripa", "Cubre: esguince", "NO cubre: mordida", "de tiranosaurio", "NO cubre: nada más"), size=30)
    if f > .78: rubber_stamp(img, "NO LO CUBRE", 540, 960, cl((f - .78) / .06), col=RED, size=90, rot=-12)
    d = ImageDraw.Draw(img)
    chip(d, "TU SEGURO", CHIP1, bg=BLUE)
    return img

def chase(c):
    f = c.lt / c.dur
    if f < .6:
        world, d = city_street(c.t, w=2160, seed=8)
        k = cl(c.lt / (c.dur * .6))
        gx = lerp(820, 1850, k); rx = gx - lerp(520, 700, k)
        tyranno(d, rx, 1300, 1.15, c.t, mood="tired", mouth=.5, run=True)
        stamp_guy(world, gx, 1300 - 330 + abs(math.sin(c.t * 12)) * -18, 1.0, -12, mood="scared", arms="up", t=c.t)
        img = Image.new("RGB", (W, H)); film(img, world, Shot((rx - 150 + gx + 230) / 2, 1000, 1.0))
        d = ImageDraw.Draw(img)
        chip(d, "TOPE: 18 KM/H", CHIP1, bg=BLUE, appear=c.lt / .3)
        if f > .25: bigtext(d, "NO PODÍA CORRER", 540, 560, 62, fill=WHITE)
        return img
    img = radial_bg(((0, (190, 190, 205)), (1, (120, 120, 140))), cy=900); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(90, 140, 70))
    tombstone(d, 540, 1290, 1.8, text="R.I.P.")
    for k, cx in enumerate((470, 610)): sneaker(img, cx, 1290 - 170 * 1.8 + 4, w=130, color=(230, 70, 60), seed=k + 1)
    d = ImageDraw.Draw(img)
    for x in (300, 780):
        d.line([(x, 1290), (x, 1200)], fill=(60, 120, 60), width=6); d.ellipse([x - 22, 1178, x + 22, 1222], fill=(250, 210, 60), outline=BLK, width=3)
    chip(d, "EN TU VELORIO", CHIP1, bg=PURPLE)
    if f > .7: tag(img, "AL MENOS HIZO CARDIO", 540, 620, cl((f - .7) / .08), rot=-6, bg=GREEN, size=54)
    return img

def raptors(c):
    f = c.lt / c.dur
    img, d = jungle(seed=9)
    if f < .62:
        if f < .4:
            s = 2.1
            raptor(d, 420, 1290, s, c.t, feathers=False, mood="angry")
            chip(d, "EN LAS PELÍCULAS", CHIP1, bg=GRAY, appear=c.lt / .3)
        else:
            s = lerp(2.1, 1.35, cl((f - .4) / .08))
            raptor(d, 470, 1290, s, c.t, feathers=True, mood="sly")
            chip(d, "EN LA VIDA REAL", CHIP1, bg=GREEN)
            if f > .46: bigtext(d, "TAMAÑO PAVO… Y CON PLUMAS", 540, 560, 56, fill=YEL)
        return img
    top = table(d, 540, 1290, 1.0, w=460, cloth=WHITE)
    d.line([(540 - 240, 1290 - 222), (540 + 260, 1290 - 222)], fill=RED, width=10)
    candle(d, 540, top, 1.0, c.t)
    place_setting(d, 400, top, .8); place_setting(d, 680, top, .8, food="pavo")
    a = anchors(220, 1290, .85)
    guy(d, 220, 1290, .85, mood="scared", t=c.t)
    nx, ny = a["neck"]; d.polygon([(nx - 45, ny - 5), (nx + 45, ny - 5), (nx, ny + 70)], fill=WHITE, outline=BLK)
    raptor(d, 880, 1290, 1.2, c.t, feathers=True, mood="sly", napkin=True, flip=True)
    chip(d, "CENA NAVIDEÑA", CHIP1, bg=RED)
    bigtext(d, "¿QUIÉN CENA A QUIÉN?", 540, 560, 64, fill=WHITE)
    return img

def birds(c):
    f = c.lt / c.dur
    img = radial_bg(NIGHT, cy=900); d = ImageDraw.Draw(img)
    if f < .6:
        a = img.copy(); da = ImageDraw.Draw(a); tyranno(da, 420, 1290, 1.0, c.t, mood="grin", mouth=.1)
        b = img.copy(); db = ImageDraw.Draw(b); pigeon(db, 520, 1290, 3.2, c.t, mood="sly")
        img = blend(a, b, (f - .15) / .2); d = ImageDraw.Draw(img)
        chip(d, "LAS AVES SON DINOSAURIOS", CHIP1, bg=PURPLE, appear=c.lt / .3)
        if f > .38:
            n = int(lerp(0, 11000, cl((f - .38) / .15)))
            bigtext(d, f"{n:,} ESPECIES", 540, 560, 72, fill=YEL)
        return img
    for wy in (820, 1160):
        d.line([(0, wy - 20), (W, wy + 20)], fill=(30, 30, 35), width=6)
        for k in range(7):
            x = 70 + k * 155
            pigeon(d, x, wy - 20 + 40 * x / W, .8, c.t + k, flip=k % 2 == 1, look=f > .78)
    chip(d, "LAS AVES SON DINOSAURIOS", CHIP1, bg=PURPLE)
    if f > .78: bigtext(d, "…Y TE ESTÁN VIENDO", 540, 560, 66, fill=WHITE)
    return img

def steal(c):
    """Gancho: desde el cuadro 0, una paloma (dinosaurio) le roba la torta al chavo."""
    f = c.lt / c.dur
    img = radial_bg(((0, (200, 230, 250)), (1, (150, 200, 230))), cy=700); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, 1380], fill=(110, 170, 90))
    for x in (120, 960): tree(d, x, 1210, 1.2, kind="round")
    a = anchors(380, 1290, .95); hx, hy = a["hand_r_down"]
    guy(d, 380, 1290, .95, mood="scared" if f > .3 else "neutral", t=c.t)
    k = cl(f / .2); k2 = cl((f - .25) / .3)
    px, py = (lerp(900, hx + 40, k), lerp(760, hy - 60, k)) if k2 == 0 else (lerp(hx + 40, 1000, k2), lerp(hy - 60, 560, k2))
    if k2 == 0: torta(d, hx + 30, hy, .7)
    else: torta(d, px, py + 70, .6)
    pigeon(d, px, py, 1.0, c.t, flip=k2 == 0, fly=True, mood="sly")
    if f > .35: rubber_stamp(img, "DINOSAURIO", 700, 820, cl((f - .35) / .08), col=RED, size=80, rot=-10)
    d = ImageDraw.Draw(img)
    chip(d, "LADRONA JURÁSICA", CHIP1, bg=PURPLE)
    return img

def revenge(c):
    f = c.lt / c.dur
    img, d = living_room()
    window(d, 620, 560, 1000, 900, kind="day")
    pk = radial_bg(((0, (150, 205, 240)), (1, (120, 180, 230))), cy=700); pd = ImageDraw.Draw(pk)
    tyranno(pd, 630, 1150, .75, c.t, mood="sad", mouth=0)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle([632, 572, 988, 888], fill=255)
    img.paste(pk, (0, 0), mask); d = ImageDraw.Draw(img)
    top = table(d, 400, 1290, 1.0, w=560, cloth=(240, 240, 235))
    soup_bowl(d, 380, top - 5, .95, c.t)
    chip(d, "VENGANZA CON LIMÓN", CHIP1, bg=GREEN)
    if f > .55: bigtext(d, "PRIMOS DEL T. REX", 540, 500, 62, fill=YEL)
    return img

def ending(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (200, 230, 250)), (1, (150, 200, 230))), cy=700); d = ImageDraw.Draw(img)
    d.rectangle([0, 1200, W, 1380], fill=(110, 170, 90))
    rx = lerp(560, 640, cl(f))
    tyranno(d, rx, 1290, .72, c.t, mood="grin", mouth=.3, run=True, collar=(220, 50, 60))
    cx, cy = rx + 175 * .72, 1290 - 405 * .72
    gx, gy, gs, ga = 200 + 30 * math.sin(c.t * 4), 1290 - 270, .9, -28
    stamp_guy(img, gx, gy, gs, ga, mood="scared", arms="up", t=c.t)
    d = ImageDraw.Draw(img)
    hx, hy = stamp_point(gx, gy, gs, ga, anchors(gx, gy + 300 * gs, gs)["hand_r_up"])
    d.line([(cx, cy), (hx, hy)], fill=(200, 40, 50), width=9)
    d.ellipse([hx - 24, hy - 24, hx + 24, hy + 24], fill=SKIN, outline=BLK, width=3)          # la mano agarra la correa
    pigeon(d, 940, 1290, .9, c.t, flip=True, mood="sly")
    pet_collar(d, 940 - 70 * .9, 1290 - 70 * .9 - 30 * .9 + 35, w=46)
    chip(d, "¿CUÁL TENDRÍAS DE MASCOTA?", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f > .45: chip(d, "T. REX = DEJA TESTAMENTO", CHIP2, bg=RED, appear=(f - .45) / .1)
    return img

SCENES = [(0, steal), (1, hook), (2, asteroid_snack), (3, bite), (4, chase), (5, raptors), (6, birds), (7, revenge), (8, ending)]
SFX = [(0, .1, "whoosh", {}), (0, 1.3, "pop", {}), (0, 1.6, "thud", {}), (1, .2, "sting", {}), (1, 1.2, "rumble", {}), (1, 3.5, "whoosh", {}), (2, .3, "whoosh", {}), (2, 3.4, "thud", {}), (2, 5.0, "pop", {}),
       (3, .5, "rumble", {}), (3, 4.2, "thud", {}), (3, 8.0, "buzzer", {}), (4, .2, "skid", {}), (4, 6.8, "sadtrom", {}),
       (5, .2, "sting", {}), (5, 4.0, "boing", {}), (6, .3, "whoosh", {}), (6, 8.5, "sting", {}), (7, 1.5, "whoosh", {}), (7, 2.8, "pop", {}),
       (7, 5.8, "ding", {}), (8, .2, "boing", {})]
MUSIC = ("bass", [(6, 7)], 7)
