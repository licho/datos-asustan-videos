"""Guía laboral Ep. 5: la momia busca trabajo (diciembre)."""
import math
from lib.core import *
from lib.personajes import guy, mummy
from lib.props import table, counter, document, sarcophagus, gift, ring_light, camera, rec_frame, monitor, sign_board
from lib.fondos import office

NAME = "2026-12_momia-trabajos"
END = 4.5
LINES = [
 ("mischievously", "Guía laboral para monstruos, episodio cinco: la momia.", "Guía laboral para monstruos, *episodio 5: la momia*"),
 ("sarcastic", "Su currículum: cinco mil años de experiencia… acostada. Referencias: un faraón. No contesta.", "*5,000 años de experiencia*… acostada. Referencias: un faraón. *No contesta.*"),
 ("confident", "Trabajo número uno: envolvedora de regalos en diciembre. Nadie envuelve más rápido. Practica en ella misma todos los días.", "*Trabajo #1:* envolver regalos. *Practica en ella misma* todos los días"),
 ("serious", "Trabajo número dos: enfermera. Ya llega con las vendas puestas.", "*Trabajo #2:* enfermera. *Ya llega con las vendas puestas*"),
 ("mischievously", "Trabajo número tres: guía de museo. La única que puede decir “yo estuve ahí”… y la única a la que le cobran entrada para ver a sus parientes.", "*Trabajo #3:* guía de museo. “Yo estuve ahí”… y *le cobran por ver a sus parientes*"),
 ("excited", "Trabajo número cuatro: influencer de belleza. Su rutina: sal especial, setenta días de secado… y nunca, nunca se moja.", "*Trabajo #4:* influencer de belleza. Rutina: *sal y 70 días de secado*"),
 ("whispers", "Dato real: momificar a alguien tardaba unos setenta días… y el cerebro se sacaba por la nariz con un gancho.", "Dato real: momificar tardaba *~70 días*… y el cerebro *salía por la nariz*"),
 ("dramatically", "El verdadero problema no es la maldición. Es que lleva cinco mil años trabajando…", "El verdadero problema: *5,000 años trabajando*…"),
 ("sarcastic", "…y la afore le dice que le faltan semanas cotizadas.", "…y la afore dice que *le faltan semanas cotizadas*"),
 ("", "¿Qué otro monstruo quieres que busque trabajo? Te leo en los comentarios.", "¿Qué otro monstruo quieres que *busque trabajo*?"),
]
OFFICE = office()

def intro(c):
    img, d = canvas(OFFICE); lt = c.lt
    mummy(d, lerp(-150, 560, ease(cl(lt / 2.5))), 1290, .8, c.t, "forward", trail=1.0)
    chip(d, "GUÍA LABORAL · EP. 5", CHIP1, bg=PURPLE, appear=lt / .3)
    if lt > .8: bigtext(d, "LA MOMIA", 540, 660, 110, fill=WHITE)
    return img

def cv(c):
    img, d = canvas(((40, 60, 90), (70, 80, 110))); f = c.lt / c.dur
    document(d, 130, 440, 620, 860, "CURRÍCULUM", ["Nombre: (en jeroglíficos)", "Experiencia: 5,000 años", "   … acostada", "Referencias:", " · Faraón (no contesta)" if f > .55 else ""], size=32)
    sarcophagus(d, 640, 1240, .35)
    mummy(d, 900, 1290, .5, c.t, "down", "happy")
    return img

def wrap(c):
    img, d = canvas(((200, 40, 50), (150, 30, 40))); f = c.lt / c.dur
    for k in range(9): d.ellipse([60 + k * 115 - 10, 470 + (k % 2) * 30, 60 + k * 115 + 10, 490 + (k % 2) * 30], fill=YEL if k % 2 else (120, 220, 120))
    mummy(d, 540, 1150, .75, c.t, "forward", "happy")
    top = counter(d, 540, 1290, .9, w=900, col=(120, 80, 50))
    for i, x in enumerate((230, 400, 700, 860)):
        if f > .15 + i * .15: gift(d, x, top, .8, col=[(60, 130, 220), (60, 170, 90), (230, 160, 40), (150, 70, 190)][i], bandage=(i % 2 == 1))
    chip(d, "TRABAJO #1: ENVOLVER REGALOS", CHIP1, bg=GREEN, size=48, appear=c.lt / .3)
    return img

def nurse(c):
    img, d = canvas(((210, 235, 235), (180, 215, 215))); f = c.lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(150, 175, 180))
    d.rectangle([700, 420, 1000, 560], fill=WHITE, outline=BLK, width=5); d.rectangle([835, 440, 865, 540], fill=RED); d.rectangle([800, 475, 900, 505], fill=RED)
    mummy(d, 330, 1270, .75, c.t, "forward", "happy", hat="nurse")
    guy(d, 820, 1270, .65, mood="happy" if f > .5 else "scared", t=c.t)
    k = cl((f - .2) / .5)
    if k > 0: d.line([(330 + 250 * .75, 1270 - 380 * .75), (lerp(530, 720, k), lerp(985, 1050, k))], fill=(235, 225, 195), width=18)
    chip(d, "TRABAJO #2: ENFERMERA", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def museum(c):
    img, d = canvas(((235, 215, 175), (210, 185, 145))); f = c.lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(150, 110, 80))
    for x in (230, 850):
        d.rectangle([x - 130, 620, x + 130, 1250], fill=(200, 230, 245), outline=BLK, width=6)
        sarcophagus(d, x, 1230, .95)
        d.rectangle([x - 130, 620, x + 130, 1250], outline=(255, 255, 255), width=3)
    mummy(d, 540, 1280, .7, c.t, "wave", "happy")
    if f > .5: sign_board(d, 540, 900, "ENTRADA: $90", size=40, bg=(60, 60, 70), post=False)
    chip(d, "TRABAJO #3: GUÍA DE MUSEO", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def influencer(c):
    img, d = canvas(((250, 210, 230), (230, 180, 210))); f = c.lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(200, 160, 190))
    ring_light(d, 540, 780, 300)
    mummy(d, 540, 1270, .8, c.t, "wave", "happy")
    rec_frame(d, c.t)
    if f > .45: chip(d, "RUTINA: SAL + 70 DÍAS", CHIP2 + 760, bg=PURPLE, size=48, appear=(f - .45) * c.dur / .3)
    chip(d, "TRABAJO #4: INFLUENCER", CHIP1, bg=(220, 70, 140), appear=c.lt / .3)
    return img

def fact(c):
    img, d = canvas(((245, 235, 210), (225, 210, 180))); f = c.lt / c.dur
    calendar(d, 300, 760, "70", label="DÍAS", col=RED, sc=1.0)
    nx, ny = 760, 760
    d.polygon([(nx - 60, ny - 200), (nx + 80, ny + 60), (nx - 60, ny + 80)], fill=(230, 190, 150), outline=BLK)
    d.ellipse([nx - 30, ny + 40, nx + 10, ny + 70], fill=(120, 80, 60))
    if f > .45:
        d.line([(nx + 260, ny - 60), (nx + 40, ny + 30)], fill=(120, 120, 130), width=10)
        d.arc([nx + 10, ny + 10, nx + 70, ny + 70], 90, 300, fill=(120, 120, 130), width=10)
    chip(d, "DATO REAL", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f > .45: chip(d, "40 DÍAS EN SAL (NATRÓN)", 1120, bg=GRAY, size=44, appear=(f - .45) * c.dur / .3)
    return img

def office_window(c):
    img, d = canvas(((215, 220, 230), (190, 195, 205)))
    d.rectangle([0, 1250, W, 1380], fill=(140, 140, 150))
    d.rectangle([520, 420, 1040, 1250], fill=(170, 175, 190), outline=BLK, width=6); d.rectangle([570, 500, 990, 820], fill=(200, 230, 245), outline=BLK, width=5)
    d.text((780, 460), "TRÁMITES", font=F(48), fill=BLK, anchor="mm")
    mummy(d, 300, 1280, .75, c.t, "down", "neutral")
    chip(d, "EL VERDADERO PROBLEMA", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def afore(c):
    img, d = canvas(((215, 220, 230), (190, 195, 205))); f = c.lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(140, 140, 150))
    monitor(d, 500, 460, 1040, 820, "blank"); d.text((770, 590), "SEMANAS", font=F(64), fill=RED, anchor="mm"); d.text((770, 680), "INSUFICIENTES", font=F(56), fill=RED, anchor="mm")
    mummy(d, 300, 1280, .75, c.t, "up", "scared", trail=.6)
    c.shake = 3 if f < .3 else 0
    bigtext(d, "5,000 AÑOS", 770, 1000, 70, fill=YEL)
    return img

def ending(c):
    img, d = canvas(((60, 50, 80), (100, 80, 110)))
    mummy(d, 540, 1140, .7, c.t, "wave", "happy")
    bigtext(d, "¿QUÉ OTRO", 540, 430, 90, fill=WHITE); bigtext(d, "MONSTRUO?", 540, 540, 90, fill=YEL)
    follow_btn(d, c.lt, y=1240, delay=c.dur * .5)
    return img

SCENES = [(0, intro), (1, cv), (2, wrap), (3, nurse), (4, museum), (5, influencer), (6, fact), (7, office_window), (8, afore), (9, ending)]
SFX = [(0, .1, "jingle", {}), (1, .3, "pop", {}), (2, .5, "pop", {}), (2, 1.5, "pop", {}), (2, 2.5, "pop", {}), (3, 1.0, "whoosh", {}),
       (4, 3.0, "ding", {}), (5, .3, "pop", {}), (6, 2.5, "splat", {}), (7, 0, "sting", {}), (8, 0, "buzzer", {}), (8, .5, "sadtrom", {}), (9, 2.0, "jingle", {})]
MUSIC = ("waltz", [(7, 8)], 9)
