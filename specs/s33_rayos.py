"""Un rayo es 5 veces más caliente que el Sol (y 5 mitos de tormenta)."""
import math, random
from lib.core import *
from lib.personajes import guy, stamp_guy
from lib.props import sun, thermo, building, bolt, ground_current, ranger_hat, tree, house, car, clouds, sign_board

NAME = "2026-11-25_rayos"
END = 4.5
LINES = [
 ("dramatically", "Un rayo es cinco veces más caliente que la superficie del Sol.", "Un rayo es *5 veces más caliente* que la superficie del Sol"),
 ("mischievously", "Casi veintiocho mil grados… y aun así, mucha gente sigue creyendo estos mitos.", "*Casi 28,000 °C*… y aun así, mucha gente cree *estos mitos*"),
 ("sarcastic", "Mito uno: “un rayo nunca cae dos veces en el mismo lugar”. Falso: a un rascacielos de Nueva York le caen unos veintitrés al año.", "Mito 1: “nunca cae dos veces en el mismo lugar”. *Falso: ~23 al año*"),
 ("", "Y un guardabosques recibió siete rayos en su vida. Récord mundial.", "Un guardabosques recibió *7 rayos*. Récord mundial"),
 ("serious", "Mito dos: “si no está lloviendo, estoy a salvo”. Falso: un rayo puede caer a más de quince kilómetros de la tormenta.", "Mito 2: “si no llueve, estoy a salvo”. *Falso: puede caer a +15 km*"),
 ("", "Mito tres: “me cubro debajo de un árbol”. Es la segunda causa de víctimas por rayo.", "Mito 3: “me cubro bajo un árbol”. *2ª causa de víctimas*"),
 ("", "Mito cuatro: “si me agarra afuera, me acuesto en el suelo”. Error: la corriente corre por el piso. Muévete a un lugar techado.", "Mito 4: “me acuesto en el suelo”. *Error:* muévete a un lugar techado"),
 ("warmly", "Mito cinco: “si tocas a alguien a quien le cayó un rayo, te electrocutas”. Falso: el cuerpo no guarda electricidad. Ayúdalo y llama a emergencias.", "Mito 5: “si lo tocas, te electrocutas”. *Falso:* ayúdalo y llama al *911*"),
 ("confident", "Bonus: el coche sí te protege… pero por el metal, no por las llantas.", "El coche te protege *por el metal*, no por las llantas"),
 ("whispers", "Truco: cuenta los segundos entre el relámpago y el trueno. Cada tres segundos, un kilómetro.", "Cuenta del relámpago al trueno: *cada 3 segundos, 1 km*"),
 ("serious", "Y si escuchas el trueno, ya estás al alcance de un rayo: métete a un lugar cerrado.", "¿Escuchas el trueno? *Métete a un lugar cerrado*"),
 ("", "¿Cuál de estos mitos te creías? Te leo en los comentarios.", "¿Cuál de estos mitos te creías? *Te leo*"),
]
STORM = ((40, 45, 70), (90, 95, 120)); GRASS = (80, 130, 80)

def flash(c, period=1.6, on=.12):
    return (c.lt % period) < on

def ground(d, y=1250, col=GRASS):
    d.rectangle([0, y, W, 1380], fill=col)

def hook(c):
    img, d = canvas(STORM); f = c.lt / c.dur
    if flash(c): d.rectangle([0, 0, W, 1380], fill=(200, 205, 240))
    ground(d)
    clouds(d, 300, 380, 1.4, col=(70, 75, 100)); clouds(d, 620, 360, 1.2, col=(80, 85, 110))
    bolt(d, 170, 450, 200, 1250, seed=int(c.lt / 1.6) + 1, width=16)
    thermo(d, 330, 1100, 1.0, cl(f * 1.6), label="")
    d.text((330, 1240), "RAYO: 27,700 °C", font=F(44), fill=YEL, anchor="mm", stroke_width=4, stroke_fill=BLK)
    sun(d, 800, 760, 150, c.t, mood="scared")
    d.text((800, 960), "SOL: ~5,500 °C", font=F(44), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    chip(d, "5 VECES MÁS QUE EL SOL", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def myths(c):
    img, d = canvas(STORM); ground(d)
    clouds(d, 540, 420, 1.6, col=(70, 75, 100), t=c.t, rain=True)
    if flash(c, 2.0): bolt(d, 750, 480, 900, 1250, seed=3, width=12)
    sign_board(d, 540, 1270, "MITOS DE TORMENTA", size=72, bg=(140, 40, 40), post_h=300)
    return img

def skyscraper(c):
    img, d = canvas(STORM); ground(d, col=(110, 110, 120))
    for x, h in ((150, 500), (930, 560)): building(d, x, 1250, 200, h, (90, 95, 120), lit=.3, seed=x)
    building(d, 540, 1250, 260, 820, (150, 155, 175), lit=.4, seed=5); d.line([(540, 430), (540, 330)], fill=BLK, width=10)
    n = min(23, int(c.lt / max(.1, c.dur * .7) * 23) + 1)
    if flash(c, .5, .1): bolt(d, 460, 0, 540, 330, seed=int(c.lt * 2), width=14, branches=1)
    bigtext(d, f"{n} / AÑO", 540, 560 if False else 1180, 70, fill=YEL)
    chip(d, "MITO 1: NUNCA CAE DOS VECES", CHIP1, bg=PURPLE, size=48, appear=c.lt / .3)
    return img

def ranger(c):
    img, d = canvas(((60, 90, 70), (120, 150, 110))); ground(d, col=(90, 140, 80))
    for x in (150, 930): tree(d, x, 1250, .9, "pine")
    guy(d, 540, 1270, .75, mood="scared", hoodie=(110, 120, 70), t=c.t)
    ranger_hat(d, 540, 1270 - 520 * .75, .75)
    k = int(cl(c.lt / (c.dur * .8)) * 7)
    for i in range(k): bolt(d, 230 + i * 100, 480, 230 + i * 100, 640, seed=i, width=8, branches=0, glow=False)
    chip(d, "7 RAYOS · RÉCORD MUNDIAL", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def bluesky(c):
    img, d = canvas(((110, 180, 240), (190, 220, 245))); f = c.lt / c.dur; ground(d)
    clouds(d, 1000, 470, 1.3, col=(70, 75, 100)); clouds(d, 1080, 430, 1.0, col=(80, 85, 110))
    guy(d, 260, 1270, .65, mood="happy" if f < .5 else "scared", t=c.t)
    if f > .45 and flash(c, 1.4, .25):
        bolt(d, 940, 520, 330, 1250, seed=7, width=12)
    d.line([(300, 1310), (940, 1310)], fill=WHITE, width=4); d.text((620, 1335), "+15 km", font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    chip(d, "MITO 2: SI NO LLUEVE…", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def tree_s(c):
    img, d = canvas(STORM); f = c.lt / c.dur; ground(d)
    tree(d, 540, 1250, 1.3, "round", c.t)
    guy(d, 620, 1270, .55, mood="scared", t=c.t)
    if flash(c, 1.5): bolt(d, 520, 0, 540, 640, seed=9, width=14)
    chip(d, "MITO 3: BAJO UN ÁRBOL", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f > .45: bigtext(d, "RECHAZADO", 540, 520, 110, fill=RED)
    return img

def lie(c):
    img, d = canvas(STORM); f = c.lt / c.dur; ground(d)
    if f < .55:
        stamp_guy(img, 520, 1220, .6, 90, mood="scared", arms="down", t=c.t); d = ImageDraw.Draw(img)
        if flash(c, 1.2): bolt(d, 900, 0, 900, 1250, seed=4, width=12)
        ground_current(d, 900, 1265, c.t, 520)
    else:
        house(d, 870, 1250, .7)
        k = (f - .55) / .45
        guy(d, lerp(250, 760, k), 1270, .55, mood="scared", t=c.t)
        speedlines(d, c.t, n=10, y0=900, y1=1200)
    chip(d, "MITO 4: ACOSTARSE", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def help_s(c):
    img, d = canvas(((90, 100, 130), (140, 150, 170))); ground(d, col=(110, 140, 100))
    stamp_guy(img, 640, 1210, .55, 90, mood="scared", arms="down", t=c.t, hoodie=(60, 120, 200)); d = ImageDraw.Draw(img)
    guy(d, 330, 1270, .62, mood="happy", arms="push", t=c.t)
    sign_board(d, 860, 1280, "LLAMA AL 911", size=40, bg=RED, post_h=200)
    chip(d, "MITO 5: SÍ PUEDES AYUDARLO", CHIP1, bg=GREEN, size=48, appear=c.lt / .3)
    return img

def car_s(c):
    img, d = canvas(STORM); f = c.lt / c.dur; ground(d, col=(80, 80, 90))
    car(d, 540, 1200, 3.0, (60, 120, 200))
    if f > .3:
        S = 3.0
        d.rounded_rectangle([540 - 90 * S, 1200 - 95 * S, 540 + 90 * S, 1200 - 20 * S], int(16 * S), outline=YEL, width=8)
    if flash(c, 1.3): bolt(d, 520, 0, 540, 1200 - 95 * 3, seed=11, width=14)
    if f > .55:
        for x in (540 - 55 * 3, 540 + 55 * 3): xmark(d, x, 1195, .45)
    chip(d, "EL METAL, NO LAS LLANTAS", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def counting(c):
    img, d = canvas(((20, 22, 40), (50, 50, 80))); lt = c.lt; ground(d, col=(40, 50, 45))
    if lt < .25: d.rectangle([0, 0, W, 1380], fill=(220, 225, 255)); bolt(d, 820, 0, 860, 1250, seed=2, width=14)
    n = min(3, int(max(0, lt - .3) / ((c.dur - 1.0) / 3)) + 1) if lt > .3 else 0
    if n: bigtext(d, f"{n}…", 540, 760, 180, fill=WHITE)
    if n >= 3: bigtext(d, "= 1 KM", 540, 1000, 110, fill=YEL)
    chip(d, "RELÁMPAGO → TRUENO", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def indoors(c):
    img, d = canvas(STORM); f = c.lt / c.dur; ground(d)
    house(d, 640, 1250, 1.0, lights=True)
    if f < .6: guy(d, lerp(150, 560, f / .6), 1270, .55, mood="scared", t=c.t)
    if flash(c, 1.6): bolt(d, 150, 0, 200, 1250, seed=6, width=12)
    chip(d, "¿TRUENO? ADENTRO", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .55: chip(d, "30 MIN DESPUÉS DEL ÚLTIMO", CHIP2, bg=GRAY, size=46, appear=(f - .55) * c.dur / .3)
    return img

def ending(c):
    img, d = canvas(STORM)
    if flash(c, 1.8): bolt(d, 540, 0, 540, 700, seed=12, width=14)
    bigtext(d, "¿CUÁL MITO", 540, 820, 100, fill=WHITE); bigtext(d, "TE CREÍAS?", 540, 950, 100, fill=YEL)
    follow_btn(d, c.lt, y=1240, delay=c.dur * .55)
    return img

SCENES = [(0, hook), (1, myths), (2, skyscraper), (3, ranger), (4, bluesky), (5, tree_s), (6, lie), (7, help_s), (8, car_s), (9, counting), (10, indoors), (11, ending)]
SFX = [(0, 0, "rumble", {"d": 2.5}), (0, .1, "thud", {}), (1, .2, "pop", {}), (2, .5, "thud", {}), (3, .5, "ding", {}), (4, 2.5, "thud", {}), (5, 2.0, "buzzer", {}),
       (6, .5, "rumble", {"d": 2.0}), (7, .5, "ding", {}), (8, 1.0, "thud", {}), (9, 0, "thud", {}), (9, 3.0, "rumble", {"d": 2.0}), (10, .5, "rumble", {"d": 2.0}), (11, 2.0, "jingle", {})]
MUSIC = ("bass", [(9, 10)], 11)
