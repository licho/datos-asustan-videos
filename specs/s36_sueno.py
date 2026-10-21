"""¿Qué pasaría si dejaras de dormir? (con café y humor negro)"""
import math
from lib.core import *
from lib.personajes import guy, ghost, brain, rat, heart_face, anchors, medal
from lib.props import mug, hourglass, car, road, phone_chat, wall_clock, monitor, sofa
from lib.fondos import night_room

NAME = "2026-11-28_dejar-de-dormir"
END = 4.5
LINES = [
 ("mischievously", "¿Qué pasaría si dejaras de dormir? Spoiler: el café no te va a salvar.", "¿Qué pasaría si *dejaras de dormir*? El café *no te va a salvar*"),
 ("sarcastic", "Hora dieciocho: tus reflejos ya andan como si te hubieras tomado unas copas. “No pasa nada, otro café.”", "*18 horas:* reflejos como con *unas copas*. “Otro café.”"),
 ("", "Hora veinticuatro: como pasado de copas. Y hay quien maneja así… con un café en la mano, como si fuera cinturón de seguridad.", "*24 horas:* como *pasado de copas*. Y hay quien maneja así"),
 ("whispers", "Luego llegan los microsueños: tu cerebro se apaga unos segundos sin avisarte. Te deja en visto.", "*Microsueños:* tu cerebro se apaga unos segundos. *Te deja en visto*"),
 ("mischievously", "Día dos: café número ocho. Arriba de cuatrocientos miligramos al día ya te pasaste. Y mil doscientos de golpe pueden darte convulsiones.", "Más de *400 mg al día* ya es mucho. *1,200 de golpe:* convulsiones"),
 ("sarcastic", "Día tres: algunas personas empiezan a alucinar. Si la sombra del rincón te saluda, no es un fantasma: es tu cerebro pidiendo cama.", "*Día 3:* alucinaciones. Si la sombra te saluda… *es tu cerebro pidiendo cama*"),
 ("dramatically", "En los sesenta, un estudiante aguantó once días despierto. Su premio: no poder ni concentrarse.", "Un estudiante aguantó *11 días despierto*. Premio: *no poder ni concentrarse*"),
 ("whispers", "Dato que asusta: a ratas sin nada de sueño por unas dos semanas les resultó mortal. Y no, no les faltaba café.", "Ratas sin dormir *~2 semanas*: *mortal*. Y no, no les faltaba café"),
 ("confident", "Los adultos necesitan al menos siete horas. Y el café de las seis de la tarde: a las once, la mitad sigue en ti.", "Adultos: *7+ horas*. El café de las 6 p.m.: *a las 11, la mitad sigue en ti*"),
 ("sarcastic", "Así que ese “un capítulo más” a las tres de la mañana es básicamente un experimento científico. Y tú eres la rata.", "“Un capítulo más” a las 3 a.m.… *y tú eres la rata*"),
 ("", "¿Cuántos cafés llevas hoy? Te leo en los comentarios.", "¿Cuántos cafés llevas hoy? *Te leo*"),
]
NROOM = night_room(); FEET = 1290

def s_hook(c):
    img, d = canvas(NROOM)
    guy(d, 420, FEET, .75, mood="scared", arms="push", t=c.t)
    hx, hy = 420 + 200 * .75, FEET - 285 * .75
    mug(d, hx + 40, hy + 120, .8, c.t)                                      # la taza en la mano
    d.ellipse([hx - 20, hy - 20, hx + 20, hy + 20], fill=SKIN, outline=BLK, width=2)   # mano encima del asa
    chip(d, "¿Y SI DEJAS DE DORMIR?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def s_18(c):
    img, d = canvas(((40, 45, 80), (80, 80, 120))); f = c.lt / c.dur
    bigtext(d, "18 H", 300, 620, 150, fill=YEL)
    gauge(d, 300, 960, 160, lerp(10, 5, ease(f)), 10, "", fg=WHITE); d.text((300, 1010), "REFLEJOS", font=F(40), fill=WHITE, anchor="mm")
    n = 1 + int(4 * cl(f / .8))
    for k in range(n): mug(d, 780, 1290 - k * 150, .55, c.t, steam=(k == n - 1))
    return img

def s_24(c):
    img, d = canvas(((110, 170, 230), (190, 215, 240))); f = c.lt / c.dur
    road(d, 1000, 1300, c.t, speed=600)
    car(d, 540 + math.sin(c.t * 4) * 220, 1150, 2.2, (60, 120, 200))
    bigtext(d, "24 H", 540, 600, 150, fill=RED)
    if f > .5: chip(d, "EL CAFÉ NO ES CINTURÓN", CHIP2 + 380, bg=RED, size=46, appear=(f - .5) * c.dur / .3)
    return img

def s_micro(c):
    img, d = canvas(((40, 45, 80), (80, 80, 120))); f = c.lt / c.dur
    off = int(c.t * 1.5) % 3 == 0
    brain(d, 300, 760, .75, c.t, mood="happy", eyes_open=not off)
    if off: d.text((300, 960), "OFF", font=F(60), fill=RED, anchor="mm")
    phone_chat(d, 580, 520, 430, 560, "Cerebro", [("r", "¿Sigues ahí?", "visto")], size=34)
    chip(d, "MICROSUEÑOS", CHIP1, bg=GRAY, appear=c.lt / .3)
    return img

def s_coffee(c):
    img, d = canvas(((60, 35, 30), (110, 70, 50))); f = c.lt / c.dur
    mug(d, 260, 1150, 1.1, c.t, label="#8")
    mg = int(lerp(0, 1200, ease(cl(f / .85))))
    gauge(d, 760, 780, 190, mg, 1200, "", fg=WHITE)
    d.text((760, 840), f"{mg} mg", font=F(60), fill=YEL if mg < 400 else RED, anchor="mm", stroke_width=4, stroke_fill=BLK)
    if mg > 400: heart_face(d, 760, 1100, 1.0, c.t)
    chip(d, "DÍA 2: CAFÉ #8", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def s_ghost(c):
    img, d = canvas(NROOM); f = c.lt / c.dur
    d.polygon([(0, 380), (380, 380), (380, 1290), (0, 1290)], fill=(25, 22, 35))
    d = ghost(img, 220, 820, .55, c.t, mood="happy", arms="wave", alpha=cl((f - .2) / .3) * .8)
    guy(d, 760, FEET, .7, mood="scared", t=c.t)
    chip(d, "DÍA 3", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def s_student(c):
    img, d = canvas(((240, 235, 225), (220, 215, 205))); f = c.lt / c.dur
    calendar(d, 300, 760, int(lerp(1, 11, ease(cl(f / .6)))), label="DÍAS", col=RED, sc=1.0)
    guy(d, 760, FEET, .72, mood="scared", t=c.t)
    if f > .6:
        a = anchors(760, FEET, .72)
        medal(d, a["chest"][0], a["chest"][1], .9, neck=a["neck"])          # colgada del cuello, sobre el pecho
    chip(d, "11 DÍAS · FERIA DE CIENCIAS", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def s_rats(c):
    img, d = canvas(((220, 230, 235), (190, 205, 210))); f = c.lt / c.dur
    d.rectangle([110, 760, 760, 1240], outline=(120, 130, 140), width=8)
    for x in range(110, 760, 50): d.line([(x, 760), (x, 1240)], fill=(150, 160, 170), width=3)
    rat(d, 400, 1220, 1.1, c.t); mug(d, 640, 1230, .35, c.t)
    hourglass(d, 900, 900, .9, frac=cl(f / .9), t=c.t)
    chip(d, "DATO QUE ASUSTA", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def s_seven(c):
    img, d = canvas(((40, 45, 80), (80, 80, 120))); f = c.lt / c.dur
    hr = 6 + 5 * ease(cl((f - .3) / .5))
    wall_clock(d, 300, 760, 170, hour=hr, minute=(hr % 1) * 60)
    mug(d, 780, 1150, 1.0, c.t, level=1 - .5 * ease(cl((f - .3) / .5)))
    d.text((780, 1220), "50% SIGUE AHÍ" if f > .8 else "", font=F(44), fill=YEL, anchor="mm", stroke_width=4, stroke_fill=BLK)
    chip(d, "ADULTOS: 7+ HORAS", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def s_tv(c):
    img, d = canvas(NROOM); f = c.lt / c.dur
    monitor(d, 540, 460, 1020, 760, "text:¿Sigues viendo?", col=WHITE)
    wall_clock(d, 200, 560, 90, hour=3, minute=0)
    sofa(d, 540, 1290, .9)
    guy(d, 540, 1160, .6, mood="scared", t=c.t)
    if f > .55:
        hy = 1160 - 520 * .6
        for sx in (-1, 1): d.ellipse([540 + sx * 75 - 40, hy - 130, 540 + sx * 75 + 40, hy - 50], fill=(235, 235, 240), outline=BLK, width=4); d.ellipse([540 + sx * 75 - 22, hy - 112, 540 + sx * 75 + 22, hy - 68], fill=(250, 190, 200))
        chip(d, "TÚ ERES LA RATA", CHIP1, bg=RED, appear=(f - .55) * c.dur / .3)
    return img

def ending(c):
    img, d = canvas(((60, 35, 30), (110, 70, 50)))
    mug(d, 540, 1100, 1.4, c.t)
    bigtext(d, "¿CUÁNTOS CAFÉS", 540, 430, 80, fill=WHITE); bigtext(d, "LLEVAS HOY?", 540, 540, 80, fill=YEL)
    follow_btn(d, c.lt, y=1250, delay=c.dur * .5)
    return img

SCENES = [(0, s_hook), (1, s_18), (2, s_24), (3, s_micro), (4, s_coffee), (5, s_ghost), (6, s_student), (7, s_rats), (8, s_seven), (9, s_tv), (10, ending)]
SFX = [(0, .2, "sting", {}), (1, .5, "pop", {}), (1, 1.5, "pop", {}), (1, 2.5, "pop", {}), (2, .3, "skid", {}), (3, 1.0, "buzzer", {}), (4, 1.0, "alarm", {}),
       (5, 1.0, "sting", {}), (6, 3.0, "ding", {}), (7, .5, "sadtrom", {}), (8, 1.0, "ding", {}), (9, 3.0, "boing", {}), (10, 2.0, "jingle", {})]
MUSIC = ("pad", [], None)
