"""¿Qué pasaría si los humanos desapareciéramos? (serie ¿Qué pasaría si…?). Caricatura con cámara."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.core import say
from lib.motion import tw, yoyo, layer, shake, back_out, cubic_out, radial_bg
from lib.personajes import louse, hawk, rat, roach, alien_cw
from lib.props import phone_chat, planet_earth, empty_clothes, plastic_bag, old_tv, tombstone, shades, trash_can, tears, house
from lib.fondos import city_street, subway_tunnel, forest_city
from lib.efectos import tag, snow_fall, sound_waves
from reels_engine.camera import Shot, film, path, pan, zoom_out, ken_burns, impact, handheld

NAME = "2026-12-07_humanos-desaparecen"
END = 4.5
LINES = [
 ("mischievously", "Si mañana desapareciéramos todos, los únicos que llorarían serían… los piojos.", "Si desapareciéramos todos, los únicos que llorarían… *los piojos*"),
 ("dramatically", "En dos o tres días, el metro de Nueva York se inunda. Hoy lo salvan bombas que sacan cuarenta y nueve millones de litros de agua al día. Sin nadie que las prenda… glu, glu.", "En 2 o 3 días *el metro de Nueva York se inunda*: 49 millones de litros al día… *glu, glu*"),
 ("sarcastic", "¿Por qué los piojos? Solo viven en humanos… y sin una cabeza se mueren en uno o dos días. Nadie les va a hacer funeral.", "¿Por qué? *Solo viven en humanos*. Sin cabeza, mueren en *1 o 2 días*"),
 ("mischievously", "En las ciudades frías, las cucarachas tampoco la libran: sin calefacción, no aguantan el invierno. En las calientes… siguen como si nada. Ellas nunca nos necesitaron.", "Ciudades frías: *cucarachas congeladas*. Calientes: *como si nada*"),
 ("serious", "Las ratas de ciudad pierden su comida favorita: nuestra basura. Y los halcones se dan un banquete.", "Las ratas pierden *nuestra basura*… y los halcones *se dan un banquete*"),
 ("dramatically", "A los veinte años, las calles de Nueva York empiezan a hundirse: las columnas que las sostienen por debajo se oxidan.", "Año 20: *las calles se hunden*. Las columnas de abajo *se oxidan*"),
 ("serious", "En menos de cien años, la mayoría de las casas ya se cayeron… y la ciudad vuelve a ser bosque.", "En menos de 100 años: *la ciudad vuelve a ser bosque*"),
 ("whispers", "Pero hay cosas que duran miles de años: el plástico… y nuestras señales de radio y tele, viajando por el espacio para siempre.", "Lo que dura miles de años: *el plástico* y *nuestras señales de radio y tele*"),
 ("sarcastic", "O sea: lo último que va a quedar de la humanidad son bolsas de plástico… y tus telenovelas.", "Nuestro legado: *bolsas de plástico… y telenovelas*"),
 ("", "¿Qué crees que dure más: tu casa… o tu ex? Te leo en los comentarios.", "¿Qué dura más: *tu casa… o tu ex*? Te leo en comentarios"),
]
SPACE = ((0, (35, 30, 70)), (.6, (15, 12, 40)), (1, (5, 5, 18)))

def stars(d, n=70, seed=4, box=(0, 0, W, H)):
    r = random.Random(seed)
    for k in range(n):
        x, y = r.uniform(box[0], box[2]), r.uniform(box[1], box[3]); s = r.choice((2, 3, 4))
        d.ellipse([x - s, y - s, x + s, y + s], fill=(240, 240, 255))

# ------------------------------------------------------------------ escenas
def hook(c):
    """Desde el cuadro 0: ropa vacía en la calle y un piojo llorando encima con su maleta."""
    f = c.lt / c.dur
    world, d = city_street(c.t)
    for x, col, cp in ((290, (240, 120, 40), (200, 40, 50)), (800, (90, 160, 220), (60, 60, 70))): empty_clothes(d, x, 1290, 1.0, hoodie=col, cap=cp)
    louse(d, 260, 1262, .55, c.t, mood="sad")
    img = Image.new("RGB", (W, H)); film(img, world, path(c.lt, [(0, Shot(330, 1170, 1.9)), (c.dur * .7, Shot(540, 1090, 1.12))]))
    d = ImageDraw.Draw(img)
    chip(d, "¿Y SI DESAPARECEMOS?", CHIP1, bg=RED)
    if f > .45: tag(img, "LOS ÚNICOS QUE LLORAN", 540, 600, cl((f - .45) / .15), rot=-6, bg=PURPLE, size=56)
    return img

def subway(c):
    f = c.lt / c.dur
    world, d = subway_tunnel(c.t, water=cl(tw(c.lt, c.dur * .45, c.dur * .95, 0, 1.15)))
    if f > .7:
        for k in range(4):
            bx = 300 + k * 160; by = 700 - ((c.t * 120 + k * 70) % 200)
            d.ellipse([bx - 16, by - 16, bx + 16, by + 16], outline=(170, 210, 250), width=5)
    img = Image.new("RGB", (W, H)); film(img, world, handheld(path(c.lt, [(0, Shot(540, 1000, 1.25)), (c.dur, Shot(540, 960, 1.0))]), c.t, 3))
    d = ImageDraw.Draw(img)
    chip(d, "DÍA 3", CHIP1, bg=BLUE, appear=c.lt / .3)
    if f > .2:
        n = int(lerp(0, 49, cl((f - .2) / .3)))
        bigtext(d, f"{n} MILLONES DE LITROS", 540, 560, 62, fill=YEL)
        bigtext(d, "AL DÍA", 540, 640, 54, fill=WHITE)
    if f > .82: bigtext(d, "GLU, GLU…", 540, 1240, 80, fill=WHITE)
    return img

def lice(c):
    img = radial_bg(((0, (150, 140, 170)), (1, (80, 75, 100))), cy=800); d = ImageDraw.Draw(img); f = c.lt / c.dur
    d.rectangle([0, 1290, W, 1380], fill=(90, 130, 70))
    tombstone(d, 720, 1290, 1.6, text="CABEZA")
    x = tw(c.lt, 0, c.dur * .3, -150, 420)
    louse(d, x, 1290, 2.0, c.t, mood="sad")
    louse(d, 960, 1290, 1.1, c.t + 1, mood="sad", suitcase=False, flip=True)
    chip(d, "LOS ÚNICOS QUE NOS EXTRAÑAN", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if f > .35: bigtext(d, "SOLO VIVEN EN HUMANOS", 540, 580, 58, fill=WHITE)
    if f > .55: bigtext(d, "SIN CABEZA: 1 O 2 DÍAS", 540, 670, 58, fill=YEL)
    if f > .8: tag(img, "SIN FUNERAL", 760, 880, cl((f - .8) / .1), rot=8, bg=RED)
    return img

def roaches(c):
    img = Image.new("RGB", (W, H)); f = c.lt / c.dur
    top = radial_bg(((0, (190, 215, 240)), (1, (120, 150, 200))), cy=700).crop((0, 0, W, 900)); img.paste(top, (0, 0))
    bot = radial_bg(((0, (255, 215, 130)), (1, (240, 140, 60))), cy=1100).crop((0, 900, W, H)); img.paste(bot, (0, 900))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 860, W, 900], fill=(240, 245, 255)); d.rectangle([0, 1280, W, 1380], fill=(200, 160, 90))
    d.line([(0, 900), (W, 900)], fill=BLK, width=8)
    snow_fall(d, c.t, n=14, box=(0, 480, W, 860))
    if f > .1:
        sh = math.sin(c.t * 40) * 6
        roach(d, 640 + sh, 790, .65, 0, walk=False)
        ice = Image.new("RGBA", (520, 120), (170, 220, 255, 110)); img.paste(ice, (380, 735), ice); d = ImageDraw.Draw(img)   # bloque de hielo
        d.rectangle([380, 735, 900, 855], outline=(120, 190, 240), width=8); d.line([(420, 760), (480, 760)], fill=WHITE, width=6); d.line([(420, 780), (450, 780)], fill=WHITE, width=6)
        d.text((240, 670), "CIUDAD FRÍA", font=F(46), fill=BLK, anchor="mm")
    if f > .45:
        roach(d, 620, 1190, .7, c.t, walk=True)
        shades(d, 620 + 190 * .7, 1190, w=64, vertical=True, arms=-30)
        d.text((240, 1000), "CIUDAD CALIENTE", font=F(46), fill=BLK, anchor="mm")
    chip(d, "CUCARACHAS", CHIP1, bg=ORANGE, appear=c.lt / .3)
    if f > .75: bigtext(d, "NUNCA NOS NECESITARON", 540, 540, 56, fill=YEL)
    return img

def rats(c):
    world, d = city_street(c.t, decay=.1, seed=7); f = c.lt / c.dur
    trash_can(d, 300, 1300, 1.0, full=False)
    rat(d, 560, 1300, 1.3, c.t)
    if f > .45:
        k = cl((f - .45) / .3)
        hawk(d, lerp(1250, 770, k), lerp(450, 1060, k), 1.6, c.t, flip=True, dive=k > .3)
    img = Image.new("RGB", (W, H)); film(img, world, path(c.lt, [(0, Shot(420, 1100, 1.4)), (c.dur * .5, Shot(540, 960, 1.0))]))
    d = ImageDraw.Draw(img)
    chip(d, "RATAS", CHIP1, bg=GRAY, appear=c.lt / .3)
    if .15 < f: bigtext(d, "SIN BASURA = SIN COMIDA", 540, 560, 58, fill=WHITE)
    if f > .8: tag(img, "BANQUETE", 760, 760, cl((f - .8) / .1), rot=8, bg=GREEN)
    return img

def year20(c):
    f = c.lt / c.dur
    world, d = city_street(c.t, decay=.45, seed=4)
    sink = cl((f - .3) / .5)
    if sink > 0:
        d.polygon([(200, 1190), (880, 1190), (840, 1190 + 110 * sink), (240, 1190 + 110 * sink)], fill=(35, 30, 30), outline=BLK)
        for k in range(4):
            px = 300 + k * 160
            d.rectangle([px - 14, 1190 + 40 * sink, px + 14, 1190 + 110 * sink], fill=(170, 90, 50), outline=BLK, width=3)
    view = Shot(540, 1000, 1.15)
    if .3 < f < .8: view = handheld(view, c.t, 10)
    img = Image.new("RGB", (W, H)); film(img, world, view)
    d = ImageDraw.Draw(img)
    chip(d, "AÑO 20", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .5: bigtext(d, "COLUMNAS OXIDADAS", 540, 580, 64, fill=ORANGE)
    return img

_FC = None
def year100(c):
    global _FC
    if _FC is None: _FC = forest_city()[0]
    w, h = _FC.size
    s = path(c.lt, [(0, Shot(w * .5, h * .5, 3.0)), (c.dur * .85, Shot(w * .5, h * .5, 1.0))])
    img = Image.new("RGB", (W, H)); film(img, _FC, s)
    d = ImageDraw.Draw(img)
    chip(d, "AÑO 100", CHIP1, bg=GREEN, appear=c.lt / .3)
    if c.lt / c.dur > .55: bigtext(d, "BIENVENIDO, BOSQUE", 540, 560, 64, fill=WHITE)
    return img

def year10k(c):
    img = radial_bg(SPACE, cy=900); d = ImageDraw.Draw(img); stars(d, seed=9); f = c.lt / c.dur
    planet_earth(d, 300, 940, 190, "sad", look=(.5, 0))
    for k in range(4):
        r = 210 + ((c.t * 120 + k * 50) % 160)
        d.arc([300 - r, 940 - r, 300 + r, 940 + r], 300, 60, fill=(150, 230, 255), width=8)
    if f > .1:
        plastic_bag(d, 820, 700 + math.sin(c.t * 1.5) * 30, 1.0, c.t)
        d.text((820, 820), "PLÁSTICO", font=F(42), fill=WHITE, anchor="mm")
    if f > .45: d.text((820, 1220), "SEÑALES DE\nRADIO Y TELE", font=F(42), fill=(150, 230, 255), anchor="mm", align="center")
    chip(d, "AÑO 10,000", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def legacy(c):
    img = radial_bg(((0, (70, 60, 110)), (1, (25, 20, 50))), cy=900); d = ImageDraw.Draw(img); stars(d, 40, seed=2, box=(0, 480, W, 1000)); f = c.lt / c.dur
    d.ellipse([-200, 1250, 1280, 1500], fill=(150, 140, 120)); d.rectangle([0, 1300, W, 1380], fill=(150, 140, 120))
    plastic_bag(d, 140, 1220, .8, c.t)
    old_tv(d, 800, 1300, 1.15, c.t, show="novela")
    alien_cw(d, 400, 1300, .95, c.t, mood="blank" if f < .5 else "smile", arms="down")
    hx, hy = 400, 1300 - 510 * .95
    if f > .5: tears(d, hx, hy + 10 * .95 + 22, 1.33, c.t)
    chip(d, "NUESTRO LEGADO", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .2: bigtext(d, "BOLSAS DE PLÁSTICO…", 540, 560, 60, fill=WHITE)
    if f > .55: bigtext(d, "…Y TELENOVELAS", 540, 640, 60, fill=YEL)
    return img

def question(c):
    img = radial_bg(((0, (60, 70, 120)), (1, (25, 25, 60))), cy=900); d = ImageDraw.Draw(img); f = c.lt / c.dur
    for x, label in ((280, "TU CASA"), (800, "TU EX")):
        d.rounded_rectangle([x - 220, 620, x + 220, 1260], 30, fill=(245, 240, 230), outline=BLK, width=6)
        d.text((x, 1200), label, font=F(52), fill=BLK, anchor="mm")
    house(d, 280, 1100, .8)
    phone_chat(d, 615, 650, 370, 480, "Ex", [("l", "hola", "3:12"), ("l", "¿sigues vivo?", "3:13"), ("l", "te extraño 🙃", "3:15")], shown=1 + int(f * 5), size=30)
    bigtext(d, "VS", 540, 940, 90, fill=YEL)
    chip(d, "¿QUÉ DURA MÁS?", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .5: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=PURPLE, appear=(f - .5) / .1)
    return img

SCENES = [(0, hook), (1, subway), (2, lice), (3, roaches), (4, rats), (5, year20), (6, year100), (7, year10k), (8, legacy), (9, question)]
SFX = [(0, .2, "sting", {}), (0, 4.2, "whoosh", {}), (1, 0, "rumble", {}), (1, 7.5, "splat", {}), (2, .3, "sadtrom", {}), (2, 6.5, "thud", {}),
       (3, .5, "buzzer", {}), (3, 5.0, "ding", {}), (4, 3.0, "whoosh", {}), (4, 5.5, "pop", {}), (5, 2.0, "rumble", {}),
       (6, .2, "whoosh", {}), (7, 0, "sting", {}), (8, 3.0, "boing", {}), (9, .2, "pop", {})]
MUSIC = ("pad", [(7, 8)], 8)
