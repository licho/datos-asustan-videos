"""Guía laboral Ep. 6: la Llorona busca trabajo."""
import math
from lib.core import *
from lib.core import say
from lib.motion import tw, yoyo, layer, glow, shake, back_out, cubic_out, radial_bg
from lib.personajes import guy, llorona, anchors
from lib.props import document, alarm_clock, bed, coffin, candle, shopping_cart, time_clock, codex, pyramid, sign_board, moon_disc, templo
from lib.fondos import make_store, office

NAME = "2026-12_llorona-trabajos"
END = 4.5
LINES = [
 ("mischievously", "Guía laboral para monstruos, episodio seis: la Llorona.", "Guía laboral para monstruos, *episodio 6: la Llorona*"),
 ("sarcastic", "Su currículum: más de quinientos años de experiencia… en turno nocturno. Habilidades: llorar a todo pulmón y aparecer cerca del agua.", "*+500 años de experiencia*… en turno nocturno. Llora *a todo pulmón*"),
 ("confident", "Trabajo número uno: despertador humano. Grita “¡Ay, mis hijos!” a las tres de la mañana. Nadie se queda dormido… ni vuelve a dormir nunca.", "*Trabajo #1:* despertador. Nadie se queda dormido… *ni vuelve a dormir*"),
 ("serious", "Trabajo número dos: plañidera profesional. La contratan para llorar en los velorios… y es tan buena que los dolientes le piden que le baje.", "*Trabajo #2:* plañidera. Tan buena que *le piden que le baje*"),
 ("mischievously", "Trabajo número tres: voceadora del súper. “¡Aaay, mis hijos!… Su mamá los espera en la caja tres.”", "*Trabajo #3:* voceadora del súper. *“Su mamá los espera en caja 3”*"),
 ("excited", "Trabajo número cuatro: influencer de sonidos para dormir. Tiene un millón de seguidores… y ninguno ha logrado dormir.", "*Trabajo #4:* sonidos para dormir. *Un millón de seguidores… cero dormidos*"),
 ("whispers", "Dato real: un códice del siglo dieciséis cuenta que, unos diez años antes de que llegaran los españoles, en Tenochtitlan se oía de noche a una mujer llorando: “Hijitos míos, ya tenemos que irnos lejos.”", "Dato real: un códice cuenta que *en Tenochtitlan se oía llorar a una mujer*, años antes de los españoles"),
 ("dramatically", "El verdadero problema no es que asuste. Es que la ley dice que el turno nocturno es de siete horas como máximo…", "La ley dice: turno nocturno, *7 horas máximo*…"),
 ("sarcastic", "…y ella lleva quinientos años sin checar salida.", "…y ella lleva *500 años sin checar salida*"),
 ("", "¿Qué otro monstruo quieres que busque trabajo? Te leo en los comentarios.", "¿Qué otro monstruo quieres que *busque trabajo*?"),
]
RIVER = ((0, (60, 70, 130)), (.6, (25, 30, 70)), (1, (8, 10, 30)))
STORE = make_store()
OFFICE = office()

def river_night(c, y=1150, moon=(900, 790)):
    img = radial_bg(RIVER, cy=700); d = ImageDraw.Draw(img)
    if moon: moon_disc(d, moon[0], moon[1], 60, bg=(30, 35, 80))
    d.rectangle([0, y, W, 1380], fill=(30, 60, 110))
    for k in range(6):
        yy = y + 25 + k * 40; ph = c.t * 2 + k
        d.line([(x, yy + math.sin(x / 70 + ph) * 6) for x in range(0, W + 40, 40)], fill=(80, 120, 180), width=4)
    d.rectangle([0, y - 20, W, y], fill=(40, 70, 50))
    return img, d

def wail_waves(d, x, y, t, n=3, col=(200, 220, 255)):
    for k in range(n):
        r = 60 + ((t * 140 + k * 60) % 180)
        for sx in (-1, 1):
            a0, a1 = (300, 60) if sx > 0 else (120, 240)
            d.arc([x - r, y - r, x + r, y + r], a0, a1, fill=col, width=7)

def tag(img, text, x, y, k, rot=-10, bg=RED, size=58):
    def fn(dd, cx, cy):
        f = F(size); w = dd.textlength(text, font=f) + 70
        dd.rounded_rectangle([cx - w / 2, cy - size * .8, cx + w / 2, cy + size * .8], 30, fill=bg, outline=BLK, width=6)
        dd.text((cx, cy), text, font=f, fill=WHITE, anchor="mm")
    return layer(img, fn, x, y, 900, sx=k, sy=k, rot=rot)

def intro(c):
    img, d = river_night(c); lt = c.lt
    x = tw(lt, 0, 2.2, 1250, 560, cubic_out)
    llorona(d, x, 1130, .85, c.t, mood="wail", arms="up" if lt > 2.0 else "down")
    if lt > 2.0: wail_waves(d, 560, 1130 - .85 * 545, c.t)
    chip(d, "GUÍA LABORAL · EP. 6", CHIP1, bg=PURPLE, appear=lt / .3)
    if lt > .8: bigtext(d, "LA LLORONA", 540, 510, 100, fill=WHITE)
    return img

def cv(c):
    img, d = canvas(((40, 50, 90), (70, 75, 115))); f = c.lt / c.dur
    document(d, 90, 440, 640, 820, "CURRÍCULUM", ["Experiencia: +500 años", "Turno: nocturno", "Habilidades:",
                                                  " · Llorar a todo pulmón" if f > .45 else "", " · Aparecer junto al agua" if f > .6 else ""], size=32)
    llorona(d, 850, 1290, .62, c.t, mood="happy", arms="point" if f > .45 else "down")
    chip(d, "CURRÍCULUM", CHIP1, bg=GRAY, appear=c.lt / .3)
    return img

def alarm(c):
    img = radial_bg(((0, (50, 45, 90)), (1, (15, 12, 35))), cy=800); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(70, 55, 60))
    d.rectangle([640, 470, 1000, 800], fill=(20, 25, 60), outline=BLK, width=10); d.line([(820, 470), (820, 800)], fill=BLK, width=8)
    moon_disc(d, 920, 560, 45, bg=(20, 25, 60))
    alarm_clock(d, 170, 1250, 1.1, c.t, ring=True, text="3:00")
    jump = -abs(math.sin(lt * 9)) * 30 if f > .3 else 0
    guy(d, 420 + shake(lt, .5, 99, 6, 30), 1290 + jump, .6, mood="scared", arms="up" if f > .3 else "down", t=c.t)
    llorona(d, 820, 1250, .55, c.t, mood="wail", arms="up")
    wail_waves(d, 820, 1250 - .55 * 545, c.t, n=2)
    if f > .55:
        a = anchors(420, 1290, .6); say(d, "Ya no vuelvo a dormir", a["mouth"], head=a["head_r"], size=42, maxw=380, avoid=[(700, 850, 950, 1260)])
    chip(d, "TRABAJO #1: DESPERTADOR", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def wake(c):
    img = radial_bg(((0, (90, 70, 110)), (1, (35, 25, 50))), cy=800); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(60, 45, 55))
    coffin(d, 500, 1250, .75)
    for x in (300, 720): candle(d, x, 1250, .9, c.t)
    llorona(d, 180, 1130, .55, c.t, mood="wail", arms="up"); wail_waves(d, 180, 1130 - .55 * 545, c.t, n=2)
    for i, x in enumerate((830, 980)):
        guy(d, x, 1290, .45, mood="scared", t=c.t + i, hoodie=(60, 60, 70))
    if f > .5:
        a = anchors(980, 1290, .45); say(d, "¡Bájele tantito!", a["mouth"], head=a["head_r"], size=44, maxw=380, avoid=[anchors(830, 1290, .45)["box"]])
    chip(d, "TRABAJO #2: PLAÑIDERA", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def store(c):
    img, d = canvas(STORE); lt = c.lt; f = lt / c.dur
    llorona(d, 300, 1250, .62, c.t, mood="wail" if f < .5 else "happy", arms="mic")
    for i in range(2):
        k = tw(lt, .6 + i * .4, 2.5, 0, 1, cubic_out); x = 700 + i * 170 + k * 700
        guy(d, x, 1290, .45, mood="scared", arms="push", t=c.t + i, hoodie=((60, 140, 200), (200, 90, 90))[i])
        shopping_cart(d, x + 150, 1290, .5)
    if f > .25:
        txt = "¡Aaay, mis hijos!" if f < .55 else "…su mamá los espera en caja 3"
        say(d, txt, (300, 1250 - .62 * 510), head=.62 * 95, size=44, maxw=460, side=1)
    chip(d, "TRABAJO #3: VOCEADORA", CHIP1, bg=ORANGE, appear=lt / .3)
    return img

def influencer(c):
    img = radial_bg(((0, (250, 200, 225)), (1, (190, 130, 175))), cy=760); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    px0, py0, px1, py1 = 260, 450, 820, 1300
    d.rounded_rectangle([px0, py0, px1, py1], 50, fill=(25, 25, 30), outline=BLK, width=6)
    d.rounded_rectangle([px0 + 22, py0 + 60, px1 - 22, py1 - 60], 30, fill=(30, 40, 90))
    for k in range(14):
        x = px0 + 60 + (k * 37) % 470; y = py0 + 100 + ((c.t * 300 + k * 90) % 560)
        d.line([(x, y), (x - 6, y + 26)], fill=(140, 170, 230), width=4)
    d = layer(img, lambda dd, cx, cy: llorona(dd, cx, cy + 260, .55, c.t, mood="wail", arms="down"), 540, 900, 700)
    d.rectangle([px0 + 22, py1 - 190, px1 - 22, py1 - 60], fill=(0, 0, 0))
    d.text((540, py1 - 150), "LLUVIA Y LLANTO", font=F(40), fill=WHITE, anchor="mm"); d.text((540, py1 - 100), "10 HORAS", font=F(36), fill=YEL, anchor="mm")
    n = int(tw(lt, .3, 1.8, 0, 1000000, cubic_out))
    chip(d, f"{n:,} SEGUIDORES", CHIP2, bg=(220, 70, 140), size=46, appear=(lt - .3) / .3)
    if f > .6:
        k = tw(lt, c.dur * .6, .4, 0, 1, back_out)
        d = tag(img, "0 DORMIDOS", 820, 1180, k, rot=-12)
    chip(d, "TRABAJO #4: INFLUENCER", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def fact(c):
    img, d = river_night(c, y=1100, moon=(940, 900)); lt = c.lt; f = lt / c.dur
    codex(d, 90, 470, 990, 760, unroll=tw(lt, .2, 1.6, 0, 1, cubic_out))
    templo(d, 220, 1085, .75, col=(150, 140, 160)); templo(d, 950, 1085, .45, col=(140, 130, 150), twin=False)
    d = layer(img, lambda dd, cx, cy: llorona(dd, cx, cy + 260, .5, c.t, mood="wail", arms="up"), 640, 1250 - 260, 700, alpha=tw(lt, 1.5, 1.5, 0, .75))
    if f > .55: chip(d, "CÓDICE FLORENTINO · 1509", 830, bg=GRAY, size=44, appear=(f - .55) * c.dur / .3)
    chip(d, "DATO REAL", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def law(c):
    img, d = canvas(OFFICE); lt = c.lt
    d.rectangle([0, 1250, W, 1380], fill=(140, 140, 150))
    time_clock(d, 820, 800, .95, full=.3)
    llorona(d, 300, 1260, .75, c.t, mood="sad", arms="down")
    bigtext(d, "MÁX. 7 HORAS", 540, 500, 84, fill=YEL); bigtext(d, "TURNO NOCTURNO", 540, 590, 50, fill=WHITE)
    chip(d, "EL VERDADERO PROBLEMA", CHIP1, bg=RED, appear=lt / .3)
    return img

def overtime(c):
    img, d = canvas(OFFICE); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(140, 140, 150))
    time_clock(d, 820, 800, .95, full=tw(lt, 0, 1.2, .3, 1.0))
    llorona(d, 300, 1260, .75, c.t, mood="wail", arms="up")
    bigtext(d, "500 AÑOS", 540, 530, 90, fill=YEL)
    if f > .45:
        k = tw(lt, c.dur * .45, .4, 0, 1, back_out)
        d = tag(img, "DEMANDA LABORAL", 560, 1180, k, rot=-8)
    chip(d, "SIN CHECAR SALIDA", CHIP1, bg=RED, appear=lt / .3)
    return img

def ending(c):
    img, d = river_night(c); lt = c.lt
    llorona(d, 540, 1120, .7, c.t, mood="happy", arms="point")
    bigtext(d, "¿QUÉ OTRO", 540, 470, 86, fill=WHITE); bigtext(d, "MONSTRUO?", 540, 570, 86, fill=YEL)
    follow_btn(d, lt, y=1240, delay=c.dur * .5)
    return img

SCENES = [(0, intro), (1, cv), (2, alarm), (3, wake), (4, store), (5, influencer), (6, fact), (7, law), (8, overtime), (9, ending)]
SFX = [(0, .1, "whoosh", {}), (0, 2.0, "sting", {}), (1, .3, "pop", {}), (2, .2, "alarm", {}), (2, 1.5, "boing", {}), (3, 2.0, "pop", {}),
       (4, .6, "skid", {}), (5, .3, "pop", {}), (5, 3.0, "ding", {}), (6, .2, "whoosh", {}), (7, 0, "sting", {}), (8, .2, "buzzer", {}), (8, 1.5, "thud", {}), (9, 2.0, "jingle", {})]
MUSIC = ("waltz", [(6, 7)], 9)
