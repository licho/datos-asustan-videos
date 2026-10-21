"""La cucaracha que vive sin cabeza — versión spec (lib)."""
import math
from lib.core import *
from lib.personajes import roach, roach_head
from lib.props import sandal, glass
from lib.fondos import make_kitchen
from lib.core import calendar

NAME = "2026-11-19_cucaracha-sin-cabeza"
KITCHEN = make_kitchen(); PLAIN = ((250, 240, 225), (230, 215, 195))

LINES = [
 ("mischievously", "¿Sabías que una cucaracha puede vivir… sin cabeza?", "¿Sabías que una cucaracha puede vivir… *sin cabeza*?"),
 ("dramatically", "Hasta una semana.", "*Hasta una semana.*"),
 ("serious", "No respira por la boca: respira por unos agujeritos en el cuerpo llamados espiráculos.", "No respira por la boca: respira por unos agujeritos llamados *espiráculos*"),
 ("", "Y no se desangra, porque su sangre circula a baja presión y la herida se sella rápido.", "Y no se desangra: su sangre circula *a baja presión* y la herida *se sella rápido*"),
 ("sarcastic", "Entonces, ¿de qué muere? De sed. Sin boca, no puede tomar agua.", "¿De qué muere? *De sed.* Sin boca, no puede tomar agua"),
 ("whispers", "Eso sí: la cabeza, por su lado, puede seguir moviendo las antenas durante horas.", "Y la cabeza, por su lado, *puede seguir moviendo las antenas durante horas*"),
 ("sarcastic", "Así que la próxima vez que le des un chanclazo… asegúrate de que sea definitivo.", "La próxima vez que le des un chanclazo… *asegúrate de que sea definitivo*"),
 ("mischievously", "¿A qué le tienes más miedo: a la cucaracha… o a la cucaracha voladora?", "¿A qué le tienes más miedo: a la cucaracha… *o a la cucaracha voladora*?"),
]
END = 5.0

def hook(c):
    img, d = canvas(KITCHEN); v = c.lt
    x = lerp(-200, 480, ease(v / 2.2)); popped = v >= 2.4
    roach(d, x, 1170, 1.1, c.t, head=not popped)
    if popped:
        k = ease((v - 2.4) / 0.6)
        roach_head(d, lerp(x + 190, 860, k), 1200 - 30 * k - math.sin(k * math.pi) * 420, 1.0, c.t)
        if v < 3.2: bigtext(d, "¡POP!", 700, 600, 120, fill=YEL); c.shake = 6
    chip(d, "¿SIN CABEZA?", CHIP1, bg=RED, appear=v / 0.3)
    if v >= c.at(1): calendar(d, 540, 560, int(lerp(1, 7, cl((v - c.at(1)) / 1.2))))
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
    if lt > 2.0: chip(d, "ASEGÚRATE", CHIP1, bg=RED, appear=(lt - 2.0) / 0.3)
    return img

def ending(c):
    img, d = canvas(((40, 30, 40), (90, 60, 50))); lt = c.lt
    d.ellipse([60, 560, 1020, 1330], fill=(150, 120, 100))                 # foco de luz: las patas se distinguen
    if lt < 3.0:
        roach(d, 360, 1150, 0.9, c.t); bigtext(d, "¿CUCARACHA…", 540, 380, 90, fill=WHITE)
    else:
        k = ease((lt - 3.0) / 2.0)
        roach(d, 540, lerp(1100, 760, k), lerp(0.8, 2.0, k), c.t, wings=1.0, walk=False)
        bigtext(d, "¿…O VOLADORA?", 540, 380, 90, fill=RED)
        follow_btn(d, lt, y=1220, delay=5.5)
    return img

SCENES = [(0, hook), (2, spiracles), (3, pressure), (4, thirst), (5, head), (6, chancla), (7, ending)]
SFX = [(0, 2.4, "pop", {}), (1, 0.0, "sting", {}), (4, 1.5, "sadtrom", {}), (6, 0.6, "splat", {}), (6, 2.0, "splat", {}), (7, 3.0, "buzzer", {}), (7, 5.5, "jingle", {})]
MUSIC = ("bass", [(4, 6)], 7)
