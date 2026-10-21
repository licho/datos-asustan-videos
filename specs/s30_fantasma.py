"""Guía laboral Ep. 4: el fantasma busca trabajo."""
import math
from lib.core import *
from lib.personajes import guy, ghost
from lib.props import table, laptop, floor_lamp, house, sign_board, document, phone_chat, camera, rec_frame, monitor, door, clouds, moon_disc
from lib.fondos import office, night_room

NAME = "2026-11-21_fantasma-trabajos"
END = 4.5
LINES = [
 ("mischievously", "Guía laboral para monstruos, episodio cuatro: el fantasma.", "Guía laboral para monstruos, *episodio 4: el fantasma*"),
 ("sarcastic", "Su currículum: ciento cincuenta años de experiencia… en la misma casa. Habilidades: atravesar paredes y aparecer a las tres de la mañana.", "*150 años de experiencia*… en la misma casa"),
 ("confident", "Trabajo número uno: agente inmobiliario. Vende la casa embrujada como “con mucho carácter”… y con inquilino incluido.", "*Trabajo #1:* agente inmobiliario. Casa “con mucho carácter”… *e inquilino incluido*"),
 ("serious", "Trabajo número dos: soporte técnico. Cliente: “Se me prenden y se apagan las luces solas”. Él: “Sí… ese soy yo.”", "*Trabajo #2:* soporte técnico. “Las luces parpadean solas”. *“Ese soy yo.”*"),
 ("mischievously", "Trabajo número tres: Recursos Humanos. Te entrevista, te dice “nosotros te llamamos”… y desaparece. Literal. Es el rey del ghosting.", "*Trabajo #3:* Recursos Humanos. “Nosotros te llamamos”… *y desaparece. Literal.*"),
 ("excited", "Trabajo número cuatro: estrella de programas paranormales. Por fin le pagan por salir en cámara… pero siempre sale borroso.", "*Trabajo #4:* estrella paranormal. Por fin en cámara… *pero sale borroso*"),
 ("dramatically", "El verdadero problema no es que esté muerto. Atraviesa paredes, puertas y espejos… pero hay algo que no puede atravesar:", "Atraviesa paredes, puertas y espejos… *pero hay algo que no puede atravesar*"),
 ("whispers", "el SAT. Le llegó una auditoría por ciento cincuenta años sin declarar.", "*El SAT.* Auditoría por *150 años sin declarar*"),
 ("", "¿Qué otro monstruo quieres que busque trabajo? Te leo en los comentarios.", "¿Qué otro monstruo quieres que *busque trabajo*?"),
]
OFFICE = office(); OFFICE_N = office(night=True); NROOM = night_room()
TIE = (200, 40, 50)

def intro(c):
    img, d = canvas(OFFICE); lt = c.lt
    d = ghost(img, 540, 960, .8, c.t, mood="happy", tie=TIE)
    table(d, 540, 1300, .8, w=760)
    chip(d, "GUÍA LABORAL · EP. 4", CHIP1, bg=PURPLE, appear=lt / .3)
    if lt > .8: bigtext(d, "EL FANTASMA", 540, 620, 100, fill=WHITE)
    return img

def cv(c):
    img, d = canvas(((30, 35, 60), (55, 55, 85))); lt = c.lt; f = lt / c.dur
    document(d, 150, 440, 640, 860, "CURRÍCULUM", ["Nombre: (ilegible)", "Experiencia: 150 años", "   en la misma casa", "Habilidades:", " · atravesar paredes" if f > .45 else "", " · aparecer a las 3 a.m." if f > .6 else ""], size=34)
    d.rectangle([560, 1020, 760, 1220], fill=(235, 235, 235), outline=BLK, width=4)
    d.text((660, 1090), "FOTO:", font=F(28), fill=(90, 90, 90), anchor="mm"); d.text((660, 1135), "(no salió)", font=F(26), fill=(90, 90, 90), anchor="mm")
    ghost(img, 900, 980, .55, c.t, mood="smug")
    return img

def realtor(c):
    img, d = canvas(((20, 25, 55), (60, 55, 95))); lt = c.lt; f = lt / c.dur
    moon_disc(d, 860, 560, 70, crescent=True, bg=(30, 33, 65))
    d.rectangle([0, 1240, W, 1380], fill=(50, 70, 50))
    house(d, 540, 1260, 1.05, wall=(170, 160, 175), roof=(70, 60, 80), lights=True)
    d = ghost(img, 540 - 150 * 1.05, 1260 - 200 * 1.05, .17, c.t, mood="happy", bob=False)
    sign_board(d, 900, 1290, "SE VENDE", size=40, bg=(200, 40, 50), post_h=160)
    d = ghost(img, 170, 980, .5, c.t, mood="happy", tie=TIE, arms="wave")
    chip(d, "TRABAJO #1: AGENTE INMOBILIARIO", CHIP1, bg=BLUE, size=46, appear=lt / .3)
    if f > .25: bubble(d, 420, 470, "¡Con mucho carácter!" if f < .62 else "¡Inquilino incluido!", size=46, tail=(220, 800), maxw=560)
    return img

def support(c):
    img, d = canvas(NROOM); lt = c.lt; f = lt / c.dur
    on = int(c.t * 6) % 3 != 0
    floor_lamp(d, 900, 1290, .9, on=on)
    d = ghost(img, 330, 900, .75, c.t, mood="smug" if f > .55 else "happy", headset=True)
    top = table(d, 330, 1300, .7, w=480); laptop(d, 330, top, .7)
    chip(d, "TRABAJO #2: SOPORTE TÉCNICO", CHIP1, bg=ORANGE, size=48, appear=lt / .3)
    if f > .15: bubble(d, 600, 480, "CLIENTE: “Las luces se prenden y apagan solas”", size=40, maxw=820, fill=(230, 240, 255))
    if f > .55: bubble(d, 560, 640, "Sí… ese soy yo.", size=50, tail=(400, 720), maxw=500)
    return img

def hr(c):
    img, d = canvas(OFFICE); lt = c.lt; f = lt / c.dur
    a = 1.0 if f < .5 else max(0, 1 - (f - .5) / .2)
    d = ghost(img, 300, 900, .7, c.t, mood="happy", tie=TIE, alpha=a)
    table(d, 420, 1300, .7, w=520)
    guy(d, 820, 1290, .62, mood="happy" if f < .55 else "scared", t=c.t)
    chip(d, "TRABAJO #3: RECURSOS HUMANOS", CHIP1, bg=GREEN, size=48, appear=lt / .3)
    if .2 < f < .55: bubble(d, 380, 530, "Nosotros te llamamos.", size=46, tail=(320, 690), maxw=520)
    if f > .7:
        phone_chat(d, 110, 460, 420, 470, "Recursos Humanos", [("r", "¿Hubo noticias?", "visto")], size=32)
        bigtext(d, "GHOSTING", 320, 1000, 80, fill=RED)
    return img

def tv(c):
    img, d = canvas(NROOM); lt = c.lt; f = lt / c.dur
    d.ellipse([20, 620, 470, 1180], fill=(110, 95, 110))                        # luz de la lámpara del set
    camera(d, 240, 860, .8, c.t)
    d = ghost(img, 760, 880, .8, c.t, mood="happy", arms="wave", pixel=16 if f > .45 else 0)
    rec_frame(d, c.t)
    chip(d, "TRABAJO #4: ESTRELLA PARANORMAL", CHIP1, bg=RED, size=46, appear=lt / .3)
    if f > .45: chip(d, "CALIDAD: 144p", CHIP2 + 820, bg=GRAY, size=44, appear=(f - .45) * c.dur / .3)
    return img

def wall(c):
    img, d = canvas(((70, 70, 90), (40, 40, 55))); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(60, 55, 65))
    for y in range(560, 1250, 50):
        for x in range(380 + (y // 50 % 2) * 40, 560, 80): d.rectangle([x, y, x + 76, y + 46], fill=(170, 90, 70), outline=(110, 60, 50), width=3)
    if f < .62:
        gx = lerp(120, 940, f / .62)
        inside = 360 < gx < 580
        ghost(img, gx, 900, .6, c.t, mood="happy", alpha=.55 if inside else 1)
    else:
        door(d, 640, 640, 940, 1250, col=(130, 135, 145), knob=True); d.rounded_rectangle([700, 700, 880, 770], 10, fill=WHITE, outline=BLK, width=4); d.text((790, 735), "SAT", font=F(50), fill=BLK, anchor="mm")
        k = (f - .62) / .38; gx = 520 if k > .25 else lerp(300, 540, k / .25)
        d = ghost(img, gx, 900, .6, c.t, mood="scared" if k > .25 else "happy")
        if .25 < k < .55: bigtext(d, "¡BONK!", 600, 560, 100, fill=YEL); c.shake = 6
    chip(d, "EL VERDADERO PROBLEMA", CHIP1, bg=RED, appear=lt / .3)
    return img

def audit(c):
    img, d = canvas(((235, 235, 240), (210, 210, 220))); lt = c.lt
    document(d, 90, 440, 640, 860, "AUDITORÍA", ["Contribuyente: Fantasma", "Periodo: 1876–2026", "Años sin declarar: 150"], size=34, stamp=("SIN DECLARAR", RED))
    d = ghost(img, 890, 960, .5, c.t, mood="scared", col=(225, 240, 255), bob=False)
    c.shake = 3
    chip(d, "SAT", CHIP1, bg=(120, 30, 50), appear=lt / .3)
    return img

def ending(c):
    img, d = canvas(((30, 35, 60), (60, 55, 90))); lt = c.lt
    d = ghost(img, 540, 860, .9, c.t, mood="happy", tie=TIE, arms="wave")
    bigtext(d, "¿QUÉ OTRO", 540, 430, 90, fill=WHITE); bigtext(d, "MONSTRUO?", 540, 540, 90, fill=YEL)
    follow_btn(d, lt, y=1250, delay=c.dur * .5)
    return img

SCENES = [(0, intro), (1, cv), (2, realtor), (3, support), (4, hr), (5, tv), (6, wall), (7, audit), (8, ending)]
SFX = [(0, .1, "jingle", {}), (1, .3, "pop", {}), (2, .2, "ding", {}), (3, .5, "buzzer", {"g": .15}), (3, 1.4, "buzzer", {"g": .15}), (4, 3.5, "whoosh", {}), (5, .3, "pop", {}),
       (6, 4.0, "thud", {}), (6, 4.05, "boing", {}), (7, 0, "sting", {}), (8, 2.0, "jingle", {})]
MUSIC = ("waltz", [(7, 8)], 8)
