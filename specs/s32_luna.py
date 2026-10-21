"""¿Qué pasaría si la Luna desapareciera?"""
import math, random
from lib.core import *
from lib.personajes import guy, crab, coral, wolf
from lib.props import planet_earth, moon_disc, sun_simple, snowflake, phone_small, waves, document, building
from lib.fondos import make_space

NAME = "2026-11-24_luna-desaparece"
END = 4.5
LINES = [
 ("mischievously", "¿Qué pasaría si mañana la Luna desapareciera? Spoiler: no explotaría nada… pero la extrañarías más de lo que crees.", "¿Qué pasaría si mañana *la Luna desapareciera*?"),
 ("serious", "Primero, las noches: sin luna, serían mucho más oscuras. Solo estrellas.", "Las noches serían *mucho más oscuras*. Solo estrellas"),
 ("sarcastic", "Y tu foto de la luna con el celular… pues ya no.", "Y tu foto de la luna con el celular… *pues ya no*"),
 ("serious", "Las mareas quedarían en más o menos un tercio de lo que son hoy. El Sol también jala el mar, pero mucho menos.", "Las mareas quedarían en *un tercio* de lo que son hoy"),
 ("", "Muchos animales que viven al ritmo de la marea tendrían que adaptarse… o desaparecer.", "Animales que viven al ritmo de la marea: *adaptarse… o desaparecer*"),
 ("whispers", "Y los corales usan la luz de la luna como señal para su desove masivo. Sin ella… se quedan sin reloj.", "Los corales usan la luz de la luna para su *desove masivo*. Sin ella… *sin reloj*"),
 ("dramatically", "Pero lo más grave es la inclinación de la Tierra. Hoy la Luna la mantiene estable, en unos veintitrés grados y medio, y gracias a eso tenemos estaciones normales.", "Lo más grave: la Luna mantiene estable la *inclinación de la Tierra* (~23.5°)"),
 ("", "Sin la Luna, en millones de años esa inclinación podría variar muchísimo: estaciones extremas… o casi sin estaciones.", "Sin ella, en millones de años: *estaciones extremas… o casi sin estaciones*"),
 ("confident", "Dato extra: si la Luna nunca hubiera existido, algunos cálculos dicen que el día duraría de seis a doce horas. Más de mil días al año.", "Si *nunca hubiera existido*: días de *6 a 12 horas*. Más de *mil días al año*"),
 ("sarcastic", "Imagínate cuántos lunes.", "Imagínate *cuántos lunes*"),
 ("", "Ah, y se acabarían los eclipses… y los hombres lobo se quedarían sin trabajo.", "Adiós eclipses… y los *hombres lobo sin trabajo*"),
 ("", "¿Qué extrañarías más de la Luna? Te leo en los comentarios.", "¿Qué extrañarías más de la Luna? *Te leo*"),
]
SPACE = make_space(); NIGHT = ((15, 20, 50), (45, 45, 90))

def hook(c):
    img, d = canvas(SPACE); f = c.lt / c.dur
    gone = f > .55
    planet_earth(d, 330, 1060, 230, mood="scared" if gone else "happy")
    if not gone: moon_disc(d, 800, 600, 110)
    elif f < .75:
        k = (f - .55) / .2
        for i in range(10):
            a = i / 10 * 6.28; r = 60 + 200 * k
            d.ellipse([800 + math.cos(a) * r - 40 * (1 - k), 600 + math.sin(a) * r - 40 * (1 - k), 800 + math.cos(a) * r + 40 * (1 - k), 600 + math.sin(a) * r + 40 * (1 - k)], fill=(240, 240, 230))
        bigtext(d, "¡PUF!", 800, 600, 110, fill=YEL)
    chip(d, "¿QUÉ PASARÍA SI…?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def nights(c):
    f = c.lt / c.dur; dark = cl((f - .2) / .3)
    img, d = canvas((lc((40, 50, 100), (5, 5, 15), dark), lc((80, 70, 120), (15, 15, 30), dark)))
    rnd = random.Random(4)
    for i in range(70): x, y = rnd.uniform(0, W), rnd.uniform(400, 1000); r = rnd.uniform(1.5, 3.5); d.ellipse([x - r, y - r, x + r, y + r], fill=(230, 230, 255))
    if dark < .5: moon_disc(d, 820, 520, 90)
    for i, x in enumerate(range(0, W, 180)):
        building(d, x + 90, 1300, 160, 300 + (i * 97) % 300, lc((120, 110, 150) if i % 2 else (100, 120, 150), (70, 70, 95) if i % 2 else (60, 75, 95), dark), lit=.45, seed=i)
    chip(d, "NOCHES MÁS OSCURAS", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def photo(c):
    img, d = canvas(((10, 12, 30), (30, 30, 55))); f = c.lt / c.dur
    rnd = random.Random(2)
    for i in range(90): x, y = rnd.uniform(0, W), rnd.uniform(380, 1250); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(220, 220, 255))
    d.rectangle([0, 1290, W, 1380], fill=(40, 40, 50))
    guy(d, 540, 1300, .7, mood="scared" if f > .5 else "neutral", arms="up", t=c.t)
    hx, hy = 540 + 185 * .7, 1300 - 560 * .7                        # mano derecha del muchacho (brazos arriba)
    d.rounded_rectangle([hx - 70, hy - 230, hx + 70, hy + 10], 20, fill=(70, 70, 80), outline=BLK, width=5); d.rectangle([hx - 56, hy - 212, hx + 56, hy - 14], fill=(5, 5, 10))
    d.text((hx, hy - 113), "?", font=F(80), fill=(160, 160, 180), anchor="mm")
    d.ellipse([hx - 20, hy - 20, hx + 20, hy + 20], fill=SKIN, outline=BLK, width=2)      # la mano sostiene el celular
    chip(d, "SIN LUNA", CHIP1, bg=GRAY, appear=c.lt / .3)
    return img

def tides(c):
    img, d = canvas(((150, 200, 240), (210, 230, 245))); f = c.lt / c.dur
    lvl = lerp(860, 1060, ease(cl((f - .15) / .5)))
    d.rectangle([0, 1100, W, 1380], fill=(235, 210, 150))
    d.polygon([(0, lvl), (W, lvl), (W, 1380), (0, 1380)], fill=(60, 130, 200))
    waves(d, c.t, y=lvl, col=(150, 200, 240))
    d.rectangle([0, 1180, W, 1380], fill=(235, 210, 150))
    gauge(d, 540, 640, 150, lerp(10, 3.3, ease(cl((f - .15) / .5))), 10, "", fg=BLK)
    d.text((540, 690), f"MAREA: {int(lerp(100, 33, ease(cl((f - .15) / .5))))}%", font=F(48), fill=BLK, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    chip(d, "MAREAS: 1/3", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def crabs(c):
    img, d = canvas(((150, 200, 240), (210, 230, 245)))
    d.rectangle([0, 1000, W, 1380], fill=(235, 210, 150)); d.rectangle([0, 960, W, 1000], fill=(60, 130, 200))
    for x in (250, 820): d.ellipse([x - 120, 1180, x + 120, 1230], fill=(200, 180, 130))
    crab(d, 540, 1250, 1.0, c.t, mood="confused")
    bubble(d, 760, 640, "¿Y la marea?", size=50, tail=(600, 980), maxw=440)
    chip(d, "A ADAPTARSE", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def corals(c):
    img, d = canvas(((30, 90, 150), (10, 40, 90))); f = c.lt / c.dur
    d.rectangle([0, 1200, W, 1380], fill=(200, 180, 140))
    coral(d, 200, 1240, 1.1, c.t, "branch", (240, 120, 150), spawn=0); coral(d, 520, 1240, 1.0, c.t, "brain", (250, 170, 90)); coral(d, 860, 1240, 1.2, c.t, "branch", (180, 120, 230))
    cx, cy, r = 540, 650, 130
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=BLK, width=8)
    d.text((cx, cy), "?", font=F(130), fill=RED, anchor="mm")
    chip(d, "DESOVE: ¿CUÁNDO?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def axis(d, cx, cy, r, deg, col=RED):
    a = math.radians(deg)
    dx, dy = math.sin(a) * r * 1.5, math.cos(a) * r * 1.5
    d.line([(cx - dx, cy + dy), (cx + dx, cy - dy)], fill=col, width=10)

def tilt(c):
    img, d = canvas(SPACE); f = c.lt / c.dur
    d.line([(150, 860), (930, 860)], fill=(120, 120, 150), width=3)
    a = c.t * .8; mx, my = 540 + math.cos(a) * 380, 860 + math.sin(a) * 120
    if math.sin(a) < 0: moon_disc(d, mx, my, 50)                      # mitad de atrás: detrás de la Tierra
    planet_earth(d, 540, 860, 200, mood="happy"); axis(d, 540, 860, 200, 23.5)
    if math.sin(a) >= 0: moon_disc(d, mx, my, 50)                     # mitad de enfrente
    d.text((700, 520), "23.5°", font=F(70), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    chip(d, "LA LUNA LA ESTABILIZA", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def wobble(c):
    img, d = canvas(SPACE); f = c.lt / c.dur
    deg = 40 * math.sin(c.t * 2.2) + 35 * math.sin(c.t * 0.9)
    planet_earth(d, 540, 860, 200, mood="scared"); axis(d, 540, 860, 200, deg)
    d.text((540, 1180), f"{abs(int(deg))}°", font=F(70), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    if math.sin(c.t * 1.5) > 0: sun_simple(d, 170, 560, 80, c.t)
    else: snowflake(d, 910, 560, 80)
    chip(d, "EN MILLONES DE AÑOS", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def days(c):
    img, d = canvas(((250, 245, 235), (230, 225, 215))); f = c.lt / c.dur
    n = int(lerp(365, 1000, ease(cl((f - .4) / .4))))
    calendar(d, 540, 820, f"{n:,}", label="DÍAS AL AÑO", col=RED, sc=1.3)
    chip(d, "SI NUNCA HUBIERA EXISTIDO", CHIP1, bg=PURPLE, size=48, appear=c.lt / .3)
    if f < .45: d.text((540, 520), "Día de 6 a 12 horas", font=F(56), fill=BLK, anchor="mm")
    return img

def mondays(c):
    img, d = canvas(((250, 245, 235), (230, 225, 215))); lt = c.lt
    k = int(cl(lt / (c.dur * .8)) * 16)
    for i in range(k):
        x, y = 190 + (i % 4) * 233, 520 + (i // 4) * 200
        d.rounded_rectangle([x - 100, y - 80, x + 100, y + 80], 14, fill=WHITE, outline=BLK, width=4)
        d.rectangle([x - 100, y - 80, x + 100, y - 40], fill=RED, outline=BLK, width=4)
        d.text((x, y + 20), "LUNES", font=F(40), fill=BLK, anchor="mm")
    return img

def wolf_s(c):
    img, d = canvas(NIGHT); lt = c.lt
    d.rectangle([0, 1280, W, 1380], fill=(40, 40, 55))
    wolf(d, 330, 1290, .75, c.t, mood="sad")
    document(d, 600, 520, 400, 560, "CURRÍCULUM", ["Nombre: Lupo", "Disponible:", "  siempre (?)"], size=30, stamp=("SIN LUNA", RED))
    chip(d, "HOMBRES LOBO: SIN TRABAJO", CHIP1, bg=GRAY, size=48, appear=lt / .3)
    return img

def ending(c):
    img, d = canvas(SPACE); lt = c.lt
    planet_earth(d, 540, 820, 230, mood="sad")
    bigtext(d, "¿QUÉ EXTRAÑARÍAS", 540, 450, 80, fill=WHITE); bigtext(d, "DE LA LUNA?", 540, 1150, 80, fill=YEL)
    follow_btn(d, lt, y=1290, delay=c.dur * .6)
    return img

SCENES = [(0, hook), (1, nights), (2, photo), (3, tides), (4, crabs), (5, corals), (6, tilt), (7, wobble), (8, days), (9, mondays), (10, wolf_s), (11, ending)]
SFX = [(0, 3.5, "pop", {}), (0, 3.6, "whoosh", {}), (2, 1.5, "sadtrom", {}), (3, 1.0, "whoosh", {}), (4, .5, "boing", {}), (6, .5, "ding", {}),
       (7, .2, "rumble", {"d": 2.5}), (8, 2.0, "ding", {}), (9, .2, "pop", {}), (9, .8, "pop", {}), (9, 1.4, "pop", {}), (10, 1.0, "sadtrom", {}), (11, 2.5, "jingle", {})]
MUSIC = ("pad", [], None)
