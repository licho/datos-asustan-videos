"""La cucaracha que vive sin cabeza — versión spec (lib)."""
import math
from lib.core import *
from lib.personajes import roach, roach_head, guy, tyranno
from lib.props import sandal, glass, stopwatch, bubbles, sign_board
from lib.fondos import make_kitchen, savanna
from lib.core import calendar

NAME = "2026-11-19_cucaracha-sin-cabeza"
KITCHEN = make_kitchen(); PLAIN = ((250, 240, 225), (230, 215, 195))

LINES = [
 ("dramatically", "Esta cucaracha no tiene cabeza… y va a vivir una semana más.", "Esta cucaracha *no tiene cabeza*… y va a vivir *una semana más*"),
 ("serious", "¿Cómo? No respira por la boca: respira por unos agujeritos en el cuerpo llamados espiráculos.", "¿Cómo? No respira por la boca: usa unos agujeritos llamados *espiráculos*"),
 ("", "Y no se desangra, porque su sangre circula a baja presión y la herida se sella rápido.", "Y no se desangra: su sangre circula *a baja presión* y la herida *se sella rápido*"),
 ("sarcastic", "Entonces, ¿de qué muere? De sed. Sin boca, no puede tomar agua.", "¿De qué muere? *De sed.* Sin boca, no puede tomar agua"),
 ("mischievously", "Y eso no es todo: aguanta la respiración hasta cuarenta minutos.", "Y eso no es todo: aguanta la respiración *hasta 40 minutos*"),
 ("sarcastic", "Y sin comer aguanta un mes. Tú no aguantas ni del quince al treinta.", "Sin comer aguanta *un mes*. Tú no aguantas *ni del 15 al 30*"),
 ("dramatically", "Su familia ya caminaba por la Tierra hace trescientos millones de años… antes que los dinosaurios.", "Su familia ya andaba aquí hace *300 millones de años*… *antes que los dinosaurios*"),
 ("sarcastic", "O sea, no se metió a tu cocina: tú construiste tu cocina en su casa.", "No se metió a tu cocina: *tú construiste tu cocina en su casa*"),
 ("whispers", "Eso sí: la cabeza, por su lado, puede seguir moviendo las antenas durante horas.", "Y la cabeza, por su lado, *puede seguir moviendo las antenas durante horas*"),
 ("serious", "Y corre a metro y medio por segundo. A tu tamaño, serían más de trescientos kilómetros por hora.", "Corre a *1.5 m por segundo*. A tu tamaño: *más de 300 km/h*"),
 ("sarcastic", "Por eso nunca le atinas con la chancla… y si le atinas, asegúrate de que sea definitivo.", "Por eso nunca le atinas con la chancla… y si le atinas, *que sea definitivo*"),
 ("mischievously", "¿A qué le tienes más miedo: a la cucaracha… o a la cucaracha voladora?", "¿A qué le tienes más miedo: a la cucaracha… *o a la cucaracha voladora*?"),
]
END = 5.0

def hook(c):
    """Desde el cuadro 0: la cucaracha ya va caminando sin cabeza y la cabeza mueve las antenas aparte."""
    img, d = canvas(KITCHEN); v = c.lt
    roach(d, 400 + math.sin(c.t * 2) * 30, 1130, 1.5, c.t, head=False)
    roach_head(d, 830, 1200, 1.3, c.t)
    chip(d, "SIN CABEZA", CHIP1, bg=RED)
    calendar(d, 540, 560, int(lerp(1, 7, cl(v / max(1.0, c.dur * .9)))))
    return img

def spiracles(c):
    img, d = canvas(PLAIN)
    roach(d, 500, 900, 2.2, c.t, head=False, walk=False)
    for i in range(5):
        px = 500 - 264 + i * 121; py = 812; ph = (c.t * 1.2 + i * 0.2) % 1
        d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(250, 240, 220), outline=BLK, width=3)
        d.ellipse([px - 8 - ph * 30, py - 40 - ph * 120, px + 8 + ph * 30, py - 24 - ph * 120], outline=(150, 190, 230), width=4)
    chip(d, "ESPIRÁCULOS", CHIP2 - 60, bg=BLUE, appear=c.lt / 0.3)
    if c.lt > 1.5: bigtext(d, "BOCA: ✗", 540, 480, 70, fill=RED)
    return img

def pressure(c):
    img, d = canvas(PLAIN)
    roach(d, 440, 950, 2.0, c.t, head=False, walk=False); nx = 770
    d.rounded_rectangle([nx - 40, 880, nx + 40, 1020], 20, fill=(240, 220, 180), outline=BLK, width=4)
    d.line([(nx - 30, 910), (nx + 30, 990)], fill=(200, 170, 130), width=6); d.line([(nx - 30, 990), (nx + 30, 910)], fill=(200, 170, 130), width=6)
    gauge(d, 540, 600, 170, 2.5 + 0.5 * math.sin(c.t * 3), 10, "", fg=BLK); d.text((540, 650), "PRESIÓN: BAJA", font=F(44), fill=BLK, anchor="mm")
    chip(d, "NO SE DESANGRA", CHIP1 - 20, bg=GREEN, appear=(c.lt - 0.5) / 0.3)
    return img

def thirst(c):
    img, d = canvas(KITCHEN)
    roach(d, lerp(250, 520, ease(c.lt / 2.0)), 1180, 1.0, c.t, head=False, walk=c.lt < 2.0)
    glass(d, 820, 1220); calendar(d, 540, 560, 7)
    if c.lt > 1.5:
        bigtext(d, "...", 690, 1000, 90, fill=BLK); chip(d, "MUERE DE SED", CHIP1, bg=ORANGE, appear=(c.lt - 1.5) / 0.3)
    return img

WATER = (150, 200, 235)

def breath(c):
    """Pecera con agua: la cucaracha abajo, burbujitas y cronómetro que llega a 40:00."""
    img, d = canvas(KITCHEN)
    x0, x1, y0, y1 = 170, 910, 760, 1290
    d.rectangle([x0, y0 + 40, x1, y1], fill=WATER)
    roach(d, 420, y1 - 45, 0.85, c.t, walk=False)
    bubbles(d, c.t, 460, 560, y1 - 90, n=10, seed=4)
    d.rectangle([x0, y0, x1, y1], outline=BLK, width=8)
    d.line([(x0, y0 + 40), (x1, y0 + 40)], fill=(90, 150, 200), width=6)
    secs = 2400 * cl(c.lt / max(1.0, c.dur * .85))
    stopwatch(d, 540, 560, 120, secs, total=2400)
    chip(d, "AGUANTA LA RESPIRACIÓN", CHIP1, bg=BLUE, appear=c.lt / 0.3)
    return img

def hungry(c):
    """La cucaracha tan tranquila junto al plato vacío; tú, el día 30, sin quincena."""
    img, d = canvas(KITCHEN); f = c.lt / c.dur
    d.ellipse([140, 1250, 440, 1300], fill=(245, 245, 240), outline=BLK, width=5)      # plato vacío en el piso
    roach(d, 290, 1215, 0.8, c.t, walk=False)
    calendar(d, 290, 640, 30, label="DÍA", sc=0.55)
    chip(d, "UN MES SIN COMER", CHIP1, bg=GREEN, appear=c.lt / 0.3)
    k = cl((f - .35) / .2)
    guy(d, 770, 1290, .8, mood="scared" if k > .5 else "neutral", arms="up" if k > .5 else "down", t=c.t)
    if k > 0:
        calendar(d, 770, 600, int(lerp(15, 30, k)), label="QUINCENA", col=RED, sc=0.55)
    return img

def ancient(c):
    """Hace 300 millones de años la cucaracha ya estaba; el dinosaurio llega tarde."""
    img, d = savanna(c.t, seed=5); f = c.lt / c.dur
    d.ellipse([560, 1240, 860, 1310], fill=(120, 110, 100), outline=BLK, width=5)        # piedra
    roach(d, 710, 1238, 0.45, c.t, walk=False)
    k = cl((f - .3) / .4)
    tyranno(d, lerp(-300, 260, k), 1300, .95, c.t, mood="grin" if k < 1 else "grin", run=k < 1)
    chip(d, "HACE 300 MILLONES DE AÑOS", CHIP1, bg=ORANGE, size=48, appear=c.lt / 0.3)
    if f > .7: chip(d, "LLEGÓ PRIMERO", CHIP2, bg=RED, appear=(f - .7) / .08)
    return img

def owner(c):
    """La cucaracha con su letrero de 'MI CASA'; tú eres el inquilino."""
    img, d = canvas(KITCHEN); f = c.lt / c.dur
    sign_board(d, 300, 1290, "MI CASA", size=60, post_h=200)
    roach(d, 380, 1215, 0.8, c.t, walk=False)
    guy(d, 790, 1290, .8, mood="scared" if f > .4 else "neutral", t=c.t)
    if f > .45: bigtext(d, "TÚ ERES EL INQUILINO", 540, 560, 64, fill=YEL)
    chip(d, "LA CASA ES SUYA", CHIP1, bg=PURPLE, appear=c.lt / 0.3)
    return img

def sprint(c):
    """Cucaracha a toda velocidad con velocímetro."""
    img, d = canvas(KITCHEN); f = c.lt / c.dur
    speedlines(d, c.t, n=18, col=(150, 130, 110), y0=1080, y1=1280)
    roach(d, 540 + math.sin(c.t * 6) * 40, 1180, 1.1, c.t * 3)
    gauge(d, 540, 640, 170, 10 * cl(f / .6), 10, "", fg=BLK)
    bigtext(d, "320 km/h" if f > .55 else "1.5 m/s", 540, 720, 80, fill=YEL if f > .55 else WHITE)
    chip(d, "VELOCIDAD", CHIP1, bg=RED, appear=c.lt / 0.3)
    if f > .55: chip(d, "A TU TAMAÑO", CHIP2, bg=GRAY, appear=(f - .55) / .08)
    return img

def head(c):
    img, d = canvas(KITCHEN)
    roach_head(d, 420, 1220, 1.8, c.t)
    chip(d, "LA CABEZA SIGUE", CHIP1, bg=GRAY, appear=c.lt / 0.3)
    if c.lt > 1.2: chip(d, "MOVIENDO LAS ANTENAS… HORAS", CHIP2, bg=RED, size=44, appear=(c.lt - 1.2) / 0.3)
    return img

def chancla(c):
    img, d = canvas(KITCHEN); lt = c.lt
    hit = (lt % 1.4) < 0.25 and lt > 0.6
    roach(d, 600 + math.sin(c.t * 3) * 120, 1180, 1.0, c.t)
    sy = 960 if hit else 960 - 380 * abs(math.sin(lt / 1.4 * math.pi))
    d.line([(640, -40), (600, sy - 60)], fill=(220, 175, 140), width=70)
    sn = sandal(d, 0, 0, 1.0, 90); img.paste(sn, (210, int(sy - 350)), sn); d = ImageDraw.Draw(img)
    d.ellipse([545, sy - 120, 655, sy - 20], fill=SKIN, outline=BLK, width=4)
    if hit: bigtext(d, "¡PAS!", 540, 560, 140, fill=YEL); c.shake = 10
    if lt > 2.0: chip(d, "QUE SEA DEFINITIVO", CHIP1, bg=RED, appear=(lt - 2.0) / 0.3)
    return img

def ending(c):
    img, d = canvas(((40, 30, 40), (90, 60, 50))); lt = c.lt
    d.ellipse([60, 560, 1020, 1300], fill=(150, 120, 100))                 # foco de luz: las patas se distinguen
    if lt < 3.0:
        roach(d, 360, 1150, 0.9, c.t); bigtext(d, "¿CUCARACHA…", 540, 380, 90, fill=WHITE)
    else:
        k = ease((lt - 3.0) / 2.0)
        roach(d, 540, lerp(1100, 760, k), lerp(0.8, 2.0, k), c.t, wings=1.0, walk=False)
        bigtext(d, "¿…O VOLADORA?", 540, 380, 90, fill=RED)
        follow_btn(d, lt, y=1220, delay=5.5)
    return img

SCENES = [(0, hook), (1, spiracles), (2, pressure), (3, thirst), (4, breath), (5, hungry), (6, ancient), (7, owner), (8, head), (9, sprint), (10, chancla), (11, ending)]
SFX = [(0, 0.0, "sting", {}), (0, 1.5, "pop", {}), (3, 1.5, "sadtrom", {}), (4, 3.0, "ding", {}), (5, 2.0, "sadtrom", {}), (6, 1.5, "rumble", {}), (7, 2.0, "boing", {}),
       (9, .2, "whoosh", {}), (9, 2.5, "skid", {}), (10, 0.6, "splat", {}), (10, 2.0, "splat", {}), (11, 3.0, "buzzer", {}), (11, 5.5, "jingle", {})]
MUSIC = ("bass", [(3, 4)], 11)
