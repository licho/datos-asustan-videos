"""Ventajas de tu casa de Infonavit en un apocalipsis zombi (~45 s, humor). Gancho: es el búnker perfecto."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, cubic_out, back_out, radial_bg
from lib.personajes import guy, zombie, stamp_guy, stamp_point, anchors
from lib.props import social_house, delivery_bag, lunchbox, sweat, road, sign_board, document, padlock
from lib.efectos import tag, rubber_stamp, sound_waves

NAME = "2026-10-24_infonavit-zombis"
END = 4.0
LINES = [
 ("mischievously", "Tu casa de Infonavit es el búnker perfecto contra zombis. Y tengo pruebas.", "Tu casa de Infonavit es *el búnker perfecto* contra zombis"),
 ("sarcastic", "Ventaja uno: está tan lejos que los zombis se cansan antes de llegar. Ni el repartidor la encuentra.", "*Ventaja 1:* tan lejos que los zombis *se cansan antes de llegar*"),
 ("confident", "Dos: paredes de block y rejas en todas las ventanas. Ya venía blindada.", "*Ventaja 2:* block y rejas. *Ya venía blindada*"),
 ("mischievously", "Tres: hay casas de apenas treinta metros cuadrados. Cierras una puerta… y ya aseguraste toda la casa.", "*Ventaja 3:* casas de *30 m²*. Cierras una puerta… *y ya*"),
 ("sarcastic", "Cuatro: el vecino está tan pegado que lo oyes estornudar. Alarma gratis.", "*Ventaja 4:* oyes al vecino estornudar. *Alarma gratis*"),
 ("confident", "Cinco: si te encuentran, te cambias. Hay unas seiscientas mil viviendas abandonadas.", "*Ventaja 5:* te cambias de casa. Hay *600 mil abandonadas*"),
 ("mischievously", "Y tú ya entrenaste: dos horas de camión diario. Correr de zombis es cardio ligero.", "*2 horas de camión diario*: correr de zombis es *cardio ligero*"),
 ("dramatically", "El único problema: los zombis algún día se van… el crédito no.", "Los zombis algún día se van… *el crédito no*"),
 ("", "¿Qué otra ventaja le encuentras? Te leo.", "¿Qué otra ventaja le encuentras? *Te leo*"),
]
DAY = ((0, (190, 220, 245)), (1, (140, 180, 220)))
DUSK = ((0, (250, 190, 120)), (1, (170, 90, 110)))
COLS = [(240, 225, 190), (200, 220, 240), (240, 200, 200), (210, 235, 200)]

def street(bg=DAY, ground=(150, 150, 140)):
    img = radial_bg(bg, cy=700); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=ground); d.line([(0, 1290), (W, 1290)], fill=BLK, width=4)
    return img, d

def row(d, xs, s, y=1290, **kw):
    for i, x in enumerate(xs): social_house(d, x, y, s, col=COLS[i % 4], **kw)

def qmark(d, x, y, t):
    d.text((x, y + math.sin(t * 5) * 8), "?", font=F(70), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)

# ------------------------------------------------------------------ escenas
def hook(c):
    f = c.lt / c.dur
    img, d = street()
    row(d, (-60, 260), .95)
    social_house(d, 620, 1290, 1.25, col=COLS[2])
    row(d, (990,), .95)
    for k, x in enumerate((180, 930)):
        zombie(d, x, 1300, .55, c.t + k, face=1 if k == 0 else -1)
        qmark(d, x, 1300 - 620 * .55 - 50, c.t + k)
    rubber_stamp(img, "BÚNKER", 620, 1290 - 150 * 1.25, 1.0, col=RED, size=80, rot=-8)
    d = ImageDraw.Draw(img)
    chip(d, "EL BÚNKER PERFECTO", CHIP1, bg=RED)
    if f > .55: bigtext(d, "Y TENGO PRUEBAS", 540, 560, 64, fill=WHITE)
    return img

def far(c):
    f = c.lt / c.dur
    img, d = street(ground=(200, 180, 120))
    road(d, 1180, 1290)
    sign_board(d, 850, 1180, "FRACC. → LEJÍSIMOS", size=34)
    for k, x0 in enumerate((120, 360)):
        x = x0 + 60 * cl(f) * (1 - .3 * k)
        zombie(d, x, 1300, .55, c.t * .4 + k, face=1)
        sweat(d, x + 60, 1300 - 620 * .55 + 20, c.t + k)
    zx = lerp(560, 640, (math.sin(c.t * 1.5) + 1) / 2)
    zombie(d, zx, 1300, .55, c.t, face=1 if math.sin(c.t * 1.5) > 0 else -1)
    delivery_bag(d, zx - 60, 1300 - 330 * .55 - 10, .45)
    if f > .5: qmark(d, zx, 1300 - 620 * .55 - 50, c.t)
    chip(d, "VENTAJA 1: DIFÍCIL ACCESO", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def armored(c):
    f = c.lt / c.dur
    img, d = street()
    social_house(d, 540, 1290, 1.6, col=COLS[0])
    k = (c.lt * 1.2) % 1
    zx = lerp(-60, 330, min(1, k / .6)) - (40 * math.sin((k - .6) / .4 * math.pi) if k > .6 else 0)
    zombie(d, zx, 1300, .62, c.t, face=1)
    if .6 < k < .8: bigtext(d, "¡BOING!", 320, 760, 70, fill=YEL)
    chip(d, "VENTAJA 2: BLINDADA", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def tiny(c):
    f = c.lt / c.dur
    img, d = street()
    social_house(d, 540, 1290, 1.7, col=COLS[1], door=1 - cl((f - .15) / .25))
    a = anchors(330, 1290, .7)
    guy(d, 300, 1290, .7, arms="push", t=c.t)
    if f > .45: padlock(img, 540 + 160 * 1.7 - 80 * 1.7, 1290 - 140, h=150, locked=True)
    d = ImageDraw.Draw(img)
    chip(d, "VENTAJA 3: SOLO 30 m²", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if f > .55: bigtext(d, "CASA ASEGURADA", 540, 560, 70, fill=YEL)
    return img

def neighbor(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (245, 235, 215)), (1, (215, 200, 175))), cy=900); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(170, 130, 90))
    d.rectangle([525, 480, 555, 1290], fill=(200, 190, 175), outline=BLK, width=4)        # pared delgadita
    guy(d, 280, 1290, .75, hoodie=(90, 160, 220), t=c.t)
    sneeze = f > .3
    if sneeze:
        a = anchors(280, 1290, .75)
        bigtext(d, "¡ACHÚ!", 300, 620, 66, fill=WHITE)
        sound_waves(d, a["mouth"][0] + 120, a["mouth"][1], c.t, n=3)
    guy(d, 800, 1290, .75, mood="scared" if sneeze else "neutral", arms="up" if sneeze else "down", t=c.t)
    chip(d, "VENTAJA 4: ALARMA INCLUIDA", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def move_out(c):
    f = c.lt / c.dur
    img, d = street()
    social_house(d, 250, 1290, 1.4, col=COLS[0])
    social_house(d, 830, 1290, 1.4, col=COLS[3], door=.8, cobweb=True)
    for k, x in enumerate((60, 190)): zombie(d, x, 1305, .5, c.t + k, face=1)
    k = cl((f - .1) / .45)
    gx = lerp(420, 800, k); gy = 1290 - 327 * .6 - math.sin(k * math.pi) * 300
    stamp_guy(img, gx, gy, .6, -15 * math.sin(k * math.pi), mood="scared", arms="up", t=c.t)
    d = ImageDraw.Draw(img)
    chip(d, "VENTAJA 5: CAMBIO DE CASA", CHIP1, bg=GRAY, appear=c.lt / .3)
    if f > .45:
        n = int(lerp(0, 600000, cl((f - .45) / .3)))
        bigtext(d, f"{n:,} VACÍAS", 540, 560, 72, fill=YEL)
    return img

def cardio(c):
    f = c.lt / c.dur
    img, d = street(ground=(200, 180, 120))
    road(d, 1180, 1290, c.t, speed=1.0)
    for k, x in enumerate((120, 300)):
        zombie(d, x, 1300, .5, c.t * .3 + k, face=1)
        sweat(d, x + 55, 1300 - 620 * .5 + 20, c.t + k)
    gx, gy = 720, 1290 - 230 + abs(math.sin(c.t * 9)) * -20
    stamp_guy(img, gx, gy, .7, -10, mood="relief", arms="down", t=c.t)
    d = ImageDraw.Draw(img)
    hx, hy = stamp_point(gx, gy, .7, -10, anchors(gx, gy + 300 * .7, .7)["hand_r_down"])
    lunchbox(d, hx + 10, hy + 75, .6)
    d.ellipse([hx - 14, hy - 14, hx + 14, hy + 14], fill=SKIN, outline=BLK, width=3)
    chip(d, "YA ENTRENASTE", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f > .25: bigtext(d, "2 HORAS DE CAMIÓN DIARIO", 540, 560, 56, fill=WHITE)
    return img

def credit(c):
    f = c.lt / c.dur
    img, d = street(bg=DUSK)
    social_house(d, 300, 1290, 1.0, col=COLS[0], lit=True)
    guy(d, 660, 1290, .8, mood="scared" if f > .4 else "relief", t=c.t)
    document(d, 720, 560, 330, 420, title="CRÉDITO", lines=("Zombis: 0", "Te faltan:", "20 AÑOS"), size=34)
    if f > .45: rubber_stamp(img, "SIGUE", 885, 900, cl((f - .45) / .1), col=RED, size=60, rot=-12)
    d = ImageDraw.Draw(img)
    chip(d, "EL VERDADERO MONSTRUO", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def ending(c):
    img, d = street(bg=DUSK)
    row(d, (40, 360, 680, 1000), .9, lit=True)
    chip(d, "¿QUÉ OTRA VENTAJA?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if c.lt > 1.0: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=RED, appear=(c.lt - 1.0) / .3)
    return img

SCENES = [(0, hook), (1, far), (2, armored), (3, tiny), (4, neighbor), (5, move_out), (6, cardio), (7, credit), (8, ending)]
SFX = [(0, .1, "sting", {}), (1, .2, "whoosh", {}), (2, .5, "boing", {}), (2, 1.3, "boing", {}), (3, 1.0, "thud", {}), (3, 1.8, "ding", {}),
       (4, 1.0, "pop", {}), (5, .8, "whoosh", {}), (6, .2, "skid", {}), (7, 1.5, "sadtrom", {}), (8, .2, "pop", {})]
MUSIC = ("bass", [(7, 8)], 8)
