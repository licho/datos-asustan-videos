"""Misión 006: ayudar a Santa a entregar los juguetes (pixel, navideña, con cámara)."""
import math, random
from PIL import Image, ImageDraw
from lib.pixel_mision import *
from lib.core import lerp, cl
from reels_engine.camera import Shot, path, pan, zoom_in, impact, handheld

NAME = "2026-12-17_mision006-santa"
CAPTIONS = False
END = 4.5
LINES = [
 ("dramatically", "Misión 006: veinticuatro de diciembre, once de la noche. Santa tiene gripa… y te eligió a ti para repartir los regalos.", "Misión 006: 24 de diciembre, 11 p.m. Santa tiene gripa… y te eligió a ti."),
 ("excited", "Tienes un costal con seis espacios. ¡Al trineo!", "Tienes un costal con 6 espacios. ¡AL TRINEO!"),
 ("confident", "Uno: la lista, revisada dos veces. No quieres dejarle carbón al niño equivocado… otra vez.", "1: la lista, revisada dos veces. Carbón al niño equivocado… otra vez no."),
 ("", "Dos: zanahorias para los renos. Es la gasolina del trineo, y no aceptan tarjeta.", "2: zanahorias. Gasolina de reno… y no aceptan tarjeta."),
 ("", "Tres: calcetines térmicos. El trineo no tiene techo, ni calefacción, ni dignidad.", "3: calcetines térmicos. Sin techo, sin calefacción, sin dignidad."),
 ("sarcastic", "Cuatro: pantuflas. Si despiertas al perro de la casa, se acaba la misión.", "4: pantuflas. Si despiertas al perro, se acaba la misión."),
 ("", "Cinco: una llave maestra. La mitad de las casas ya no tiene chimenea.", "5: llave maestra. La mitad de las casas ya no tiene chimenea."),
 ("serious", "Seis: un mapa de husos horarios. Empiezas donde la Navidad llega primero: la Isla de Navidad, en el Pacífico.", "6: mapa de husos horarios. Empiezas en el Pacífico: en la Isla de Navidad."),
 ("mischievously", "¿El GPS del celular? RECHAZADO: te manda por la autopista en plena Nochebuena.", "¿El GPS del celular? RECHAZADO: te manda por la autopista en Nochebuena."),
 ("sarcastic", "¿Aceptar la leche y galletas de cada casa? RECHAZADO: en la casa quinientos ya vas en coma de azúcar.", "¿Leche y galletas en cada casa? RECHAZADO: en la casa 500… coma de azúcar."),
 ("", "¿Sentarte a probar los tamales de la tía? GAME OVER: te quedas dormido en el sillón… y te envuelven de regalo.", "¿Probar los tamales de la tía? GAME OVER: te dormiste… y te envolvieron de regalo."),
 ("whispers", "Dato que asusta: en el mundo hay unos dos mil trescientos millones de niños. Aunque fueran tres por casa, y tuvieras un día completo, serían casi nueve mil casas… por segundo.", "Dato que asusta: 2,300 millones de niños. Con 3 por casa: ¡casi 9,000 casas por segundo!"),
 ("confident", "Misión: entregar todo antes del amanecer. Secundario: no despertar a la abuela.", "Misión: entregar todo antes del amanecer. Secundario: no despertar a la abuela."),
 ("", "¿Qué meterías tú al costal? Misión 007… próximamente.", "¿Qué meterías tú al costal? Misión 007… próximamente."),
]
INV = [(2, "lista", "REVISADA 2 VECES"), (3, "zanahoria", "GASOLINA DE RENO"), (4, "calcetines", "CERO DIGNIDAD"),
       (5, "pantuflas", "NO DESPIERTES AL PERRO"), (6, "llave", "ADIÓS CHIMENEA"), (7, "globo", "EMPIEZA EN EL PACÍFICO")]
MN = "MISIÓN 006"
def fin(c, img, **kw): return finish(c, img, MN, INV, **kw)

def sack_carrier(d, n):
    h = 10 + n * 3
    d.ellipse([56, 230 - h, 84, 232], fill=P["brown"]); rect(d, 66, 226 - h, 8, 3, "yellow")

# ------------------------------------------------------------------ escenas
def s_intro(c):
    world = Image.new("RGB", (360, LH)); d = ImageDraw.Draw(world)
    night_sky_px(d, 360, GROUND, c.t)
    snow_ground_px(d, GROUND, 360, LH)
    rect(d, 8, 120, 160, GROUND - 120, "lav"); rect(d, 8, 120, 160, 1, "black")          # cuarto de Santa (ventana grande)
    rect(d, 10, 122, 156, GROUND - 124, "purple"); santa_bed_px(d, 40, GROUND - 4, c.t)
    house_px(d, 210, GROUND, 50, 36, lit=True)
    hero(d, 300, GROUND - 46, scared=c.lt > c.dur * .55, frame=0)
    s = pan(c.lt, c.dur * .35, c.dur * .3, Shot(88, 170, 1.15), Shot(272, 170, 1.15))
    img = px_film(world, s.x, s.y, s.zoom); di = ImageDraw.Draw(img)
    if c.lt < c.dur * .35: popup(di, "SANTA: 39° DE FIEBRE", 40, "white", "red")
    elif c.lt > c.dur * .7: popup(di, "TE ELIGIÓ A TI", 40, "yellow", "black")
    return fin(c, img)

def roof_world(c, sack=6):
    world = Image.new("RGB", (LW, LH)); d = ImageDraw.Draw(world)
    night_sky_px(d, LW, GROUND, c.t, seed=5)
    snow_ground_px(d, GROUND, LW, LH)
    house_px(d, 20, GROUND, 140, 70, lit=False)
    sleigh_px(d, 34, 132, c.t, sack=sack, reindeer=3)
    return world

def s_sack(c):
    world = roof_world(c)
    s = zoom_in(c.lt, .3, 1.4, (46, 132), 1.0, 2.4, start=Shot(90, 160, 1.0))
    img = px_film(world, s.x, s.y, s.zoom); di = ImageDraw.Draw(img)
    if c.lt > 1.6: popup(di, "¡AL TRINEO!", 40, "white", "red", FONTB)
    return fin(c, img)

def s_inv(c):
    img, d = canvas_px()
    inv_grid_px(d, c, INV, xmas_item_px, title="COSTAL  6 ESPACIOS", carrier=sack_carrier,
                bottom=lambda dd: reindeer_px(dd, 118 + math.sin(c.t * 3) * 8, 220, c.t))
    return fin(c, img)

def s_gps(c):
    img, d = canvas_px("navy")
    xmas_item_px(d, "celular", 54, 44, 6)
    rect(d, 68, 62, 44, 50, "dgray")
    for k in range(6): rect(d, 70 + k * 7, 86 - (k % 2) * 6, 6, 3, "red")
    text(d, LW / 2, 70, "TRÁFICO", "red", FONTM)
    sh = (0, 0)
    if c.cap_lt > 1.3:
        popup(d, "RECHAZADO", 160, "white", "red", FONTB); popup(d, "AUTOPISTA EN NOCHEBUENA", 186, "yellow", "black")
        if c.cap_lt < 1.6: sh = (random.randint(-2, 2), 0)
    return fin(c, img, shake=sh)

def s_cookies(c):
    img, d = canvas_px("purple")
    n = min(500, int(c.cap_lt * 220))
    for k in range(min(6, n // 60 + 1)): cookie_milk_px(d, 14 + (k % 3) * 54, 40 + (k // 3) * 44, 3)
    text(d, LW / 2, 140, f"CASA {n}", "white", FONTB)
    sh = (0, 0)
    if c.cap_lt > c.dur * .55:
        popup(d, "RECHAZADO", 166, "white", "red", FONTB); popup(d, "COMA DE AZÚCAR", 192, "yellow", "black")
    return fin(c, img, shake=sh)

def s_tamales(c):
    img, d = canvas_px(); sh = (0, 0)
    if c.cap_lt < c.dur * .5:
        rect(d, 0, 16, LW, GROUND - 16, "purple"); rect(d, 0, GROUND, LW, LH - GROUND, "brown")
        d.polygon([(140, 120), (160, 200), (120, 200)], fill=P["dgreen"]); rect(d, 137, 200, 6, 10, "brown")
        for k, (x, y, col) in enumerate(((135, 150, "red"), (145, 175, "yellow"), (130, 185, "blue"))):
            if (int(c.t * 3) + k) % 2: rect(d, x, y, 3, 3, col)
        rect(d, 10, 196, 80, GROUND - 196, "red"); rect(d, 10, 190, 80, 8, "red"); rect(d, 8, 186, 6, 30, "red")
        rect(d, 96, 200, 34, 4, "brown"); rect(d, 100, 204, 3, GROUND - 204, "brown"); rect(d, 124, 204, 3, GROUND - 204, "brown")
        for k in range(3): tamal_px(d, 98 + k * 9, 188, 1)
        hero(d, 50, 160, scared=False, frame=0)
        if c.cap_lt > c.dur * .25: text(d, 70, 140, "Z z z", "white", FONTM)
    else:
        game_over(d, c, "TE ENVOLVIERON DE REGALO", skull=False)
        rect(d, 62, 50, 56, 50, "red"); rect(d, 87, 50, 6, 50, "yellow"); rect(d, 62, 72, 56, 6, "yellow")
        d.ellipse([74, 38, 88, 50], outline=P["yellow"], width=3); d.ellipse([92, 38, 106, 50], outline=P["yellow"], width=3)
        if c.cap_lt < c.dur * .5 + .5: sh = (random.randint(-3, 3), random.randint(-1, 1))
    return fin(c, img, shake=sh)

def houses_world(t):
    w, h = 1440, 2560
    world = Image.new("RGB", (w, h), P["navy"]); d = ImageDraw.Draw(world)
    r = random.Random(4); cols = ("peach", "lgray", "pink", "lav", "orange", "white")
    for row in range(0, h, 64):
        rect(d, 0, row + 60, w, 4, "white")
        for col in range(0, w, 60):
            house_px(d, col + 6, row + 60, 44, 26, wall=r.choice(cols), roof=r.choice(("red", "brown", "dgreen")), lit=(col // 60 + row // 64) % 3 != 0)
    return world

_HW = None
def s_houses(c):
    global _HW
    if _HW is None: _HW = houses_world(0)
    cx, cy = 720 + 28, 1280 + 40
    s = path(c.cap_lt, [(0, Shot(cx, cy, 2.4)), (c.dur * .75, Shot(cx, cy, .14))])
    img = px_film(_HW, s.x, s.y, s.zoom); d = ImageDraw.Draw(img)
    k = cl(c.cap_lt / (c.dur * .75))
    n = int(lerp(1, 9000, k ** 2))
    popup(d, f"{n:,} CASAS", 30, "white", "red", FONTB)
    if k > .9: popup(d, "¡POR SEGUNDO!", 60, "yellow", "black", FONTB)
    return fin(c, img)

def s_win(c):
    img, d = canvas_px()
    for y in range(16, GROUND, 4):
        u = (y - 16) / (GROUND - 16); rect(d, 0, y, LW, 4, "navy" if u < .35 else "purple" if u < .6 else "pink" if u < .8 else "orange")
    d.ellipse([70, GROUND - 14, 110, GROUND + 26], fill=P["yellow"])
    snow_ground_px(d, GROUND, LW, LH)
    for k in range(3): house_px(d, 8 + k * 60, GROUND, 44, 28, lit=False)
    x = lerp(-60, 200, cl(c.cap_lt / c.dur)); sleigh_px(d, x, 80 + math.sin(c.t * 3) * 4, c.t, sack=0, reindeer=3)
    popup(d, "MISIÓN CUMPLIDA", 34, "green", "black", FONTB)
    if c.cap_lt > c.dur * .45: popup(d, "SECUNDARIO:", 130, "yellow", "black"); popup(d, "NO DESPERTAR A LA ABUELA", 146, "yellow", "black")
    return fin(c, img)

def s_end(c):
    img, d = canvas_px(); end_screen(d, c, INV, xmas_item_px, "MISIÓN 007", title="COSTAL  6/6", question="¿QUÉ METERÍAS TÚ?")
    return fin(c, img)

SCENES = [(0, s_intro), (1, s_sack), (2, s_inv), (8, s_gps), (9, s_cookies), (10, s_tamales), (11, s_houses), (12, s_win), (13, s_end)]
SFX = [(0, .2, "jingle", {}), (0, 3.0, "whoosh", {}), (1, .3, "whoosh", {}), (1, 1.6, "ding", {})] + [(i, .1, "ding", {}) for i in range(2, 8)] + \
      [(8, 1.3, "buzzer", {}), (9, 2.5, "buzzer", {}), (10, 2.6, "sadtrom", {}), (11, 0, "sting", {}), (12, 0, "jingle", {}), (13, 1.0, "jingle", {})]
MUSIC = ("chiptune", [(11, 12)], 12)
