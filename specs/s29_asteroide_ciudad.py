"""¿Qué tan grande tendría que ser un asteroide para destruir una ciudad? (diciembre)"""
import math, random
from lib.core import *
from lib.personajes import guy, dino
from lib.props import asteroid, car, planet_earth, building, tree, cracks, ruler, wanted, blob_map, radar, window, moon_disc, sun_simple
from lib.fondos import make_space

NAME = "2026-12_asteroide-ciudad"
END = 5.0
LINES = [
 ("mischievously", "¿Qué tan grande tendría que ser una roca espacial para borrar tu ciudad del mapa? Vamos subiendo de tamaño.", "¿Qué tan grande tendría que ser para *borrar tu ciudad del mapa*?"),
 ("confident", "Del tamaño de un coche: cae más o menos una vez al año… y se quema en el cielo. Bonito espectáculo, cero daños.", "Tamaño *coche*: cae *una vez al año*… y se quema en el cielo"),
 ("serious", "Veinte metros: Cheliábinsk, 2013. Explotó en el aire y rompió ventanas en toda la ciudad.", "*20 metros:* Cheliábinsk, 2013. *Rompió ventanas en toda la ciudad*"),
 ("dramatically", "Unos sesenta metros: Tunguska, Siberia, 1908. Derribó ochenta millones de árboles en más de dos mil kilómetros cuadrados.", "*~60 metros:* Tunguska, 1908. *80 millones de árboles* derribados"),
 ("whispers", "Más que toda la Ciudad de México. Y no dejó cráter: explotó antes de tocar el suelo.", "Más que *toda la Ciudad de México*. Y *sin cráter*: explotó en el aire"),
 ("serious", "A ese tamaño los astrónomos le llaman asesino de ciudades.", "A ese tamaño le llaman *“asesino de ciudades”*"),
 ("sarcastic", "Y en 2024 encontraron uno: el 2024 YR4, de unos sesenta metros. Primero, que tal vez chocaba con la Tierra: descartado. Luego, que con la Luna: también descartado. Va a pasar a unos veintitrés mil kilómetros.", "*2024 YR4*, ~60 m. ¿Contra la Tierra? *Descartado.* ¿Contra la Luna? *Tampoco*"),
 ("serious", "Ciento cuarenta metros: ya no es una ciudad, es una región entera. Y todavía nos falta encontrar cerca de la mitad de los de ese tamaño.", "*140 metros:* una región entera. Y nos falta encontrar *cerca de la mitad*"),
 ("dramatically", "¿Diez kilómetros? Ese ya lo conoces: cayó en Yucatán y se acabaron los dinosaurios.", "*¿10 kilómetros?* Cayó en *Yucatán*… y adiós dinosaurios"),
 ("mischievously", "Resumen: veinte metros te rompen la ventana. Sesenta, la ciudad. Diez kilómetros… la especie.", "20 m: *tu ventana*. 60 m: *tu ciudad*. 10 km: *la especie*"),
 ("", "¿A qué tamaño le tendrías miedo? Te leo en los comentarios.", "¿A qué tamaño le tendrías miedo? *Te leo*"),
]
MARKS = [(.06, "COCHE"), (.27, "20 m"), (.48, "60 m"), (.69, "140 m"), (.94, "10 km")]
SKY = ((120, 180, 235), (200, 225, 245)); NIGHT = ((15, 20, 50), (50, 50, 90))

def city_row(d, x0, x1, base, seed=1, lit=0.0, h=(380, 720)):
    rnd = random.Random(seed); x = x0
    cols = [(180, 150, 120), (150, 160, 190), (200, 170, 140), (170, 130, 150), (140, 170, 160)]
    out = []
    while x < x1:
        w = rnd.randint(140, 210); hh = rnd.randint(*h)
        building(d, x + w / 2, base, w - 14, hh, rnd.choice(cols), lit=lit, seed=rnd.randint(0, 99)); out.append((x + 7, base - hh, x + w - 7, base)); x += w
    return out

def scale(d, cur, appear=1.0):
    ruler(d, 40, 520, 1290, MARKS, current=cur, appear=appear)

def hook(c):
    img, d = canvas(SKY); lt = c.lt
    d.rectangle([0, 1300, W, 1380], fill=(110, 110, 115))
    city_row(d, 300, W, 1300, seed=2)
    k = ease(cl(lt / 2.0))
    asteroid(d, lerp(1250, 900, k), lerp(300, 520, k), 110, c.t, face="angry")
    scale(d, None, appear=cl((lt - 1.0) / 2.0))
    chip(d, "¿CUÁNTO MIDE EL PELIGRO?", CHIP1, bg=RED, appear=lt / .3)
    return img

def car_lvl(c):
    img, d = canvas(NIGHT); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(60, 70, 60))
    u = (lt * .45) % 1.15
    if u < 1: asteroid(d, lerp(1150, 380, u), lerp(380, 760, u), 34 * (1 - u * .7), c.t, face=None, fire=1.6, ang=-.45)
    car(d, 760, 1270, 1.3, (220, 70, 60))
    guy(d, 520, 1280, .55, mood="happy", arms="up", t=c.t)
    scale(d, 0)
    chip(d, "≈ 1 VEZ AL AÑO", CHIP1, bg=BLUE, appear=lt / .3)
    if f > .7: chip(d, "DAÑOS: 0", CHIP2, bg=GREEN, appear=(f - .7) * c.dur / .3)
    return img

def chelyabinsk(c):
    img, d = canvas(((200, 215, 235), (235, 240, 245))); lt = c.lt
    d.rectangle([0, 1300, W, 1380], fill=(230, 235, 240))
    boxes = city_row(d, 300, W, 1300, seed=5, h=(420, 680))
    boom = lt > c.dur * .35
    if not boom:
        k = lt / (c.dur * .35); asteroid(d, lerp(1000, 700, k), lerp(380, 520, k), 40, c.t, face="angry", fire=1.0, ang=-.7)
    else:
        b = (lt - c.dur * .35)
        if b < .3: d.rectangle([0, 0, W, 1380], fill=(255, 250, 235)); c.shake = 10
        for i, bx in enumerate(boxes): cracks(d, bx, seed=i, n=5)
        bigtext(d, "¡CRASH!", 690, 640, 120, fill=YEL)
    scale(d, 1)
    chip(d, "CHELIÁBINSK · 2013", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def tunguska(c):
    img, d = canvas(((210, 225, 235), (230, 235, 225))); lt = c.lt
    d.rectangle([0, 1000, W, 1380], fill=(120, 150, 90))
    wave = cl((lt - .8) / 2.2) * 900; cx = 690
    rows = [(1080, .45), (1180, .55), (1290, .65)]
    for yy, s in rows:
        for k in range(7):
            x = 330 + k * 120 + (yy % 100)
            dist = abs(x - cx)
            if dist < wave:
                ang = 80 if x > cx else -80
                d = stamp(img, lambda dd, X, Y, **kw: tree(dd, X, Y + 140, s, "pine"), x, yy - 20, size=400, angle=-ang * cl((wave - dist) / 120))
            else: tree(d, x, yy, s, "pine")
    if lt < .9: asteroid(d, lerp(1000, cx, lt / .9), lerp(500, 820, lt / .9), 45, c.t, face="angry", fire=1.0, ang=-.7)
    elif lt < 1.2: d.ellipse([cx - 200, 700, cx + 200, 1000], fill=(255, 240, 180)); c.shake = 8
    scale(d, 2)
    chip(d, "TUNGUSKA · 1908", CHIP1, bg=ORANGE, appear=lt / .3)
    n = int(80_000_000 * ease(cl((lt - 1.0) / 2.5)))
    if lt > 1.0: bigtext(d, f"{n:,} ÁRBOLES", 690, 560, 62, fill=WHITE)
    return img

def mapa(c):
    img, d = canvas(((235, 230, 215), (220, 215, 200))); lt = c.lt
    k = ease(cl(lt / 1.2))
    d.ellipse([540 - 300 * k, 840 - 300 * k, 540 + 300 * k, 840 + 300 * k], fill=(250, 200, 190), outline=RED, width=8)
    blob_map(d, 540, 840, 250, seed=4, fill=(150, 155, 170), label="CDMX ≈ 1,500 km²", size=44)
    if k > .9: d.text((540, 500), "TUNGUSKA ≈ 2,150 km²", font=F(52), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    if lt > c.dur * .55: chip(d, "SIN CRÁTER", CHIP1, bg=RED, appear=(lt - c.dur * .55) / .3)
    return img

def poster(c):
    img, d = canvas(((60, 45, 40), (110, 80, 60))); lt = c.lt
    sc = pop(lt / .4)
    box = wanted(d, 540 - 330 * sc, 430, 660 * sc, 820, "SE BUSCA", "ASESINO DE CIUDADES") if sc > .3 else None
    if box: asteroid(d, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 170 * sc, c.t, face="angry")
    return img

SPACE = make_space()
def yr4(c):
    img, d = canvas(SPACE); lt = c.lt; f = lt / c.dur
    planet_earth(d, 270, 820, 170, mood="happy" if f < .3 else "happy")
    moon_disc(d, 800, 1050, 85)
    if f < .45:
        u = f / .45; ax, ay = lerp(1100, 470, u), lerp(420, 640, u)
    else:
        u = (f - .45) / .55; ax, ay = lerp(470, 1000, u), lerp(640, 900, u) + math.sin(u * 3.1) * -60
    asteroid(d, ax, ay, 55, c.t, face="angry" if f < .75 else "sad")
    d.text((min(ax, W - 130), ay - 90), "2024 YR4", font=F(40), fill=YEL, anchor="mm", stroke_width=4, stroke_fill=BLK)
    for th, (x, y) in ((.33, (270, 1060)), (.72, (800, 1210))):
        if f > th:
            sc = pop((f - th) * c.dur / .3)
            d.rounded_rectangle([x - 190 * sc, y - 45 * sc, x + 190 * sc, y + 45 * sc], 12, fill=WHITE, outline=GREEN, width=8)
            d.text((x, y), "DESCARTADO", font=F(max(8, 50 * sc)), fill=GREEN, anchor="mm")
    if f > .8: d.text((800, 930), "pasa a ~22,900 km", font=F(38), fill=WHITE, anchor="mm")
    chip(d, "EL “ASESINO” DE 2024", CHIP1, bg=RED, appear=lt / .3)
    return img

def region(c):
    img, d = canvas(((10, 30, 30), (20, 50, 50))); lt = c.lt; f = lt / c.dur
    cx, cy = 690, 860
    radar(d, cx, cy, [(330, "", (80, 220, 140), True), (210, "", (80, 220, 140), True), (100, "", (80, 220, 140), True)], c.t)
    a = c.t * 1.5; d.line([(cx, cy), (cx + math.cos(a) * 330, cy + math.sin(a) * 330)], fill=(120, 255, 170), width=5)
    rnd = random.Random(3)
    for i in range(24):
        r = rnd.uniform(60, 320); an = rnd.uniform(0, 6.28); x, y = cx + math.cos(an) * r, cy + math.sin(an) * r
        if i % 2 == 0: d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(120, 255, 170))
        elif f > .45: d.text((x, y), "?", font=F(40), fill=(250, 200, 60), anchor="mm")
    scale(d, 3)
    chip(d, "UNA REGIÓN ENTERA", CHIP1, bg=RED, appear=lt / .3)
    if f > .45: chip(d, "~LA MITAD SIN DESCUBRIR", CHIP2, bg=ORANGE, size=46, appear=(f - .45) * c.dur / .3)
    return img

def chicxulub(c):
    img, d = canvas(((255, 190, 120), (250, 230, 170))); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1180, W, 1380], fill=(190, 160, 100))
    tree(d, 420, 1190, .5, "palm", c.t); tree(d, 1000, 1200, .55, "palm", c.t)
    sh = 60 + 600 * ease(f)
    d.ellipse([690 - sh, 1290 - sh * .12, 690 + sh, 1290 + sh * .12], fill=(120, 90, 60))
    dino(d, 720, 1280, 1.0, c.t)
    asteroid(d, 690, lerp(-200, 330, ease(f)), lerp(120, 330, ease(f)), c.t, face="angry", fire=.6, ang=-1.57)
    scale(d, 4)
    chip(d, "YUCATÁN · HACE 66 MILLONES DE AÑOS", CHIP1, bg=RED, size=42, appear=lt / .3)
    return img

def summary(c):
    img, d = canvas(((245, 240, 230), (225, 220, 210))); lt = c.lt
    chip(d, "RESUMEN", CHIP1, bg=PURPLE, appear=lt / .3)
    rows = [("20 m", "TU VENTANA"), ("60 m", "TU CIUDAD"), ("10 km", "LA ESPECIE")]
    for i, (sz, txt) in enumerate(rows):
        a = (lt - c.dur * (.1 + i * .28)) / .3
        if a <= 0: continue
        y = 620 + i * 250; sc = pop(a)
        d.rounded_rectangle([100, y - 100 * sc, 980, y + 100 * sc], 30, fill=WHITE, outline=BLK, width=6)
        if sc > .7:
            if i == 0: window(d, 140, y - 75, 300, y + 75, "day"); cracks(d, (152, y - 63, 288, y + 63), seed=2, n=3, col=(60, 60, 60))
            if i == 1: city_row(d, 130, 300, y + 80, seed=7, h=(90, 150))
            if i == 2: dino(d, 230, y + 85, .42, c.t)
            d.text((350, y - 35), sz, font=F(60), fill=RED, anchor="lm"); d.text((350, y + 40), txt, font=F(56), fill=BLK, anchor="lm")
    return img

def ending(c):
    img, d = canvas(SPACE); lt = c.lt
    asteroid(d, 540, 780, 190, c.t, face="angry")
    bigtext(d, "¿A QUÉ TAMAÑO", 540, 440, 84, fill=WHITE); bigtext(d, "LE TIENES MIEDO?", 540, 1060, 84, fill=YEL)
    follow_btn(d, lt, y=1240, delay=c.dur * .6)
    return img

SCENES = [(0, hook), (1, car_lvl), (2, chelyabinsk), (3, tunguska), (4, mapa), (5, poster), (6, yr4), (7, region), (8, chicxulub), (9, summary), (10, ending)]
SFX = [(0, .2, "whoosh", {}), (1, 1.0, "ding", {}), (2, 1.6, "thud", {}), (2, 1.65, "splat", {}), (3, .9, "rumble", {"d": 3.0}),
       (4, .2, "pop", {}), (5, .1, "sting", {}), (6, 2.6, "buzzer", {}), (6, 6.0, "buzzer", {}), (7, 2.0, "ding", {}),
       (8, 2.5, "rumble", {"d": 3.0}), (9, .5, "pop", {}), (9, 2.0, "pop", {}), (9, 3.6, "pop", {}), (10, 2.0, "jingle", {})]
MUSIC = ("bass", [(4, 5)], 10)
