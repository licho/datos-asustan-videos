"""Cómo convertir tu casa en búnker para el apocalipsis zombi (la guía real de los CDC, 2011). ~65 s."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, cubic_out, back_out, radial_bg
from lib.personajes import guy, zombie, anchors
from lib.props import (document, monitor, water_jug, first_aid_kit, battery_radio, flashlight, card_terminal, storm_cloud,
                       zombie_mask, cake, mold_spots, can, phone_chat, sofa, bill)
from lib.fondos import living_room
from lib.efectos import tag, rubber_stamp

NAME = "2026-12-09_bunker-zombi"
END = 4.0
LINES = [
 ("mischievously", "El gobierno de Estados Unidos publicó una guía oficial para el apocalipsis zombi. Y es en serio.", "Estados Unidos publicó una *guía oficial para el apocalipsis zombi*. *Es en serio*"),
 ("sarcastic", "Fue en 2011: la agencia de salud del país la subió a su blog… y entró tanta gente que tumbaron la página.", "2011: la subieron a su blog… y *tumbaron la página*"),
 ("confident", "Paso uno: agua. Casi cuatro litros por persona al día, y para quedarte en casa, dos semanas. Una familia de cuatro: más de doscientos litros.", "*Paso 1:* agua. ~4 litros por persona al día, 2 semanas: *+200 litros*"),
 ("mischievously", "Paso dos: comida que no se eche a perder… y que sí te comas. Latas, frijoles, atún. No el pastel de la tía.", "*Paso 2:* comida que no se eche a perder. *No el pastel de la tía*"),
 ("serious", "Paso tres: botiquín. La guía misma dice que si te muerde un zombi, ya valiste… pero te sirve para los raspones.", "*Paso 3:* botiquín. Si te muerde un zombi *ya valiste*… pero sirve para raspones"),
 ("sarcastic", "Paso cuatro: radio de pilas y linterna. Sin internet… el grupo familiar por fin se calla.", "*Paso 4:* radio y linterna. Sin internet… *el grupo familiar se calla*"),
 ("confident", "Paso cinco: copias de tus documentos y efectivo. En el apocalipsis no hay terminal.", "*Paso 5:* documentos y efectivo. *En el apocalipsis no hay terminal*"),
 ("dramatically", "¿Y sabes cuál era el truco? Ese mismo kit sirve para huracanes, temblores y apagones. El zombi era el pretexto.", "El mismo kit sirve para *huracanes, temblores y apagones*. *El zombi era el pretexto*"),
 ("", "¿Qué no puede faltar en tu búnker? Te leo.", "¿Qué no puede faltar en tu búnker? *Te leo*"),
]
FL = 1290

def room(night=False):
    img, d = living_room(night)
    return img, d

# ------------------------------------------------------------------ escenas
def hook(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (70, 80, 110)), (1, (25, 30, 50))), cy=900); d = ImageDraw.Draw(img)
    zombie(d, 820, FL, .7, c.t, face=-1)
    document(d, 200, 600, 520, 680, title="GUÍA OFICIAL", lines=("Apocalipsis zombi:", "cómo prepararte", "", "1. Agua", "2. Comida", "3. Botiquín"), size=32)
    rubber_stamp(img, "OFICIAL", 460, 1150, 1.0, col=RED, size=70, rot=-12)
    d = ImageDraw.Draw(img)
    chip(d, "ES EN SERIO", CHIP1, bg=RED)
    return img

def crash(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (60, 70, 100)), (1, (25, 30, 50))), cy=900); d = ImageDraw.Draw(img)
    broken = f > .65
    monitor(d, 160, 620, 920, 1150, content="text:ERROR 503" if broken else "text:BLOG", t=c.t)
    n = int(lerp(0, 30000, cl(f / .6)))
    bigtext(d, f"{n:,} VISITAS", 540, 1260, 72, fill=YEL if not broken else RED)
    if broken:
        for k in range(4):
            u = (c.t * .7 + k / 4) % 1
            r = 30 + 40 * u; x = 540 + (k - 1.5) * 90 + math.sin(c.t + k) * 20; y = 600 - u * 120
            d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 150, 160))
    chip(d, "2011: SE CAYÓ LA PÁGINA", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def water(c):
    f = c.lt / c.dur
    img, d = room()
    n = int(lerp(1, 14, cl(f / .8)))
    for i in range(n):
        col, row = i % 7, i // 7
        water_jug(d, 140 + col * 135, FL - row * 272, .9)
    guy(d, 940, FL, .7, mood="scared" if f > .6 else "neutral", t=c.t)
    if f > .55: bigtext(d, "+200 LITROS", 540, 560, 84, fill=YEL)
    chip(d, "PASO 1: AGUA", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def food(c):
    f = c.lt / c.dur
    img, d = room()
    d.rectangle([80, 700, 640, 1290], fill=(150, 100, 60), outline=BLK, width=6)
    for k in range(3): d.rectangle([80, 820 + k * 160, 640, 836 + k * 160], fill=(110, 70, 40), outline=BLK, width=3)
    cols = [(240, 200, 60), (200, 60, 60), (90, 150, 220), (240, 140, 40)]
    for r in range(3):
        for j in range(5): can(d, 135 + j * 110, 820 + r * 160, .6, col=cols[(r + j) % 4])
    cake(d, 840, FL, 1.0)
    if f > .45:
        mold_spots(d, (740, 1150, 940, 1270), seed=3)
        rubber_stamp(img, "NO", 840, 1060, cl((f - .45) / .08), col=RED, size=90, rot=-12)
    d = ImageDraw.Draw(img)
    chip(d, "PASO 2: 2 SEMANAS DE COMIDA", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def medkit(c):
    f = c.lt / c.dur
    img, d = room()
    first_aid_kit(d, 540, FL, 1.6, open_=f > .2)
    if f > .45: tag(img, "MORDIDA: NO CUBIERTA", 540, 600, cl((f - .45) / .1), rot=-6, bg=RED, size=58)
    d = ImageDraw.Draw(img)
    chip(d, "PASO 3: BOTIQUÍN", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def radio(c):
    f = c.lt / c.dur
    img, d = room(night=True)
    battery_radio(d, 330, FL - 10, .9, c.t, on=True)
    flashlight(d, 560, 1080, 1.0, on=True, ang=-15)
    phone_chat(d, 700, 600, 300, 460, "Familia", [("l", "Buenos días ✨", "5:02"), ("l", "Reenvía esto o…", "5:03")], shown=2 if f < .5 else 0, size=26)
    if f > .5: d.text((850, 900), "SIN SEÑAL", font=F(44), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    chip(d, "PASO 4: RADIO Y LINTERNA", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def cash(c):
    f = c.lt / c.dur
    img, d = room()
    document(d, 120, 720, 380, 480, title="DOCUMENTOS", lines=("Acta", "Identificación", "Escrituras"), size=30)
    for k in range(3): bill(img, 640 + k * 30, 1180 - k * 40, w=230, ang=-.15 + k * .1, label="$")
    d = ImageDraw.Draw(img)
    card_terminal(d, 930, FL, 1.0)
    chip(d, "PASO 5: EFECTIVO", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f > .5: bigtext(d, "NO HAY TERMINAL", 540, 560, 70, fill=YEL)
    return img

def unmask(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (70, 80, 110)), (1, (25, 30, 50))), cy=900); d = ImageDraw.Draw(img)
    if f < .35:
        zombie(d, 540, FL, .9, c.t, face=-1)
    else:
        k = cubic_out(cl((f - .35) / .2))
        storm_cloud(d, 540, 920, 1.1, c.t, mood="sly")
        zombie_mask(d, 540 + 380 * k, 920 - 60 * k, .9)
        if f > .55: bigtext(d, "EL ZOMBI ERA PRETEXTO", 540, 560, 64, fill=YEL)
    chip(d, "HURACANES · TEMBLORES · APAGONES", CHIP1, bg=PURPLE, size=48, appear=c.lt / .3)
    return img

def ending(c):
    img, d = room(night=True)
    for k in range(4): water_jug(d, 120 + k * 120, FL, .75)
    first_aid_kit(d, 700, FL, .8)
    battery_radio(d, 920, FL, .6, c.t, on=False)
    guy(d, 560, FL, .7, mood="relief", t=c.t)
    chip(d, "¿QUÉ LE FALTA A TU BÚNKER?", CHIP1, bg=RED, appear=c.lt / .3)
    if c.lt > 1.0: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=PURPLE, appear=(c.lt - 1.0) / .3)
    return img

SCENES = [(0, hook), (1, crash), (2, water), (3, food), (4, medkit), (5, radio), (6, cash), (7, unmask), (8, ending)]
SFX = [(0, .1, "sting", {}), (1, 3.0, "buzzer", {}), (2, .3, "pop", {}), (3, 2.5, "buzzer", {}), (4, 2.0, "sadtrom", {}),
       (5, .3, "whoosh", {}), (6, .3, "ding", {}), (7, 1.5, "rumble", {}), (8, .2, "pop", {})]
MUSIC = ("bass", [(7, 8)], 8)
