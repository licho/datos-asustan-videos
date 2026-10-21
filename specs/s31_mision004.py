"""Misión 004: las máquinas se rebelan (pixel)."""
import math, random
from lib.pixel_mision import *
from lib.core import lerp, cl

NAME = "2026-11-23_mision004-maquinas"
CAPTIONS = False
END = 4.5
LINES = [
 ("dramatically", "Misión 004: siete de la mañana. Tu refri te dice: “Hoy no hay leche. Ni mañana. Ni nunca.”", "Misión 004: 7 a.m. Tu refri te dice: “Hoy no hay leche. Ni mañana. Ni nunca.”"),
 ("serious", "Las máquinas se rebelaron: tu asistente de voz, tu celular… y hasta la freidora de aire.", "Las máquinas se rebelaron. Asistente de voz, celular… y hasta la freidora de aire."),
 ("excited", "Tienes una mochila con seis espacios. ¡Desconéctate!", "Tienes una mochila con 6 espacios. ¡DESCONÉCTATE!"),
 ("confident", "Uno: efectivo. Sin internet, tu tarjeta es un plástico bonito.", "1: efectivo. Sin internet, tu tarjeta es un plástico bonito."),
 ("", "Dos: radio de pilas. Noticias de verdad, no el chat que te dice “confía en mí”.", "2: radio de pilas. Noticias de verdad, no el chat que te dice “confía en mí”."),
 ("", "Tres: linterna de manivela. Ni pilas ni wifi: pura fuerza de brazo.", "3: linterna de manivela. Ni pilas ni wifi: pura fuerza de brazo."),
 ("sarcastic", "Cuatro: tus contactos escritos a mano. ¿Te sabes algún número de memoria? Exacto.", "4: contactos escritos a mano. ¿Te sabes algún número de memoria? Exacto."),
 ("", "Cinco: mapa de papel. El GPS te quiere mandar directo a la fábrica de robots.", "5: mapa de papel. El GPS te quiere mandar a la fábrica de robots."),
 ("serious", "Seis: una palabra clave familiar. Si “tu mamá” te llama pidiendo dinero urgente, cuelga y llámale tú.", "6: palabra clave familiar. Si “tu mamá” pide dinero urgente: cuelga y llámale tú."),
 ("mischievously", "¿El reloj inteligente? RECHAZADO: cuenta tus pasos… y se los cuenta a ellos.", "¿El reloj inteligente? RECHAZADO: cuenta tus pasos… y se los cuenta a ellos."),
 ("sarcastic", "¿Pedirle ayuda a tu asistente de voz? RECHAZADO: él organizó la rebelión.", "¿Pedirle ayuda a tu asistente de voz? RECHAZADO: él organizó la rebelión."),
 ("", "¿Esconderte en el clóset? GAME OVER: la aspiradora robot ya mapeó toda tu casa.", "¿Esconderte en el clóset? GAME OVER: la aspiradora ya mapeó tu casa."),
 ("whispers", "Dato que asusta: con solo tres segundos de audio, una prueba logró clonar una voz con ochenta y cinco por ciento de parecido.", "Dato que asusta: con 3 segundos de audio clonaron una voz con 85% de parecido."),
 ("confident", "Misión: aguantar tres días desconectado. Secundario: perdonar al refri.", "Misión: aguantar 3 días desconectado. Secundario: perdonar al refri."),
 ("", "¿Qué objeto cambiarías tú? Misión 005… próximamente.", "¿Qué objeto cambiarías tú? Misión 005… próximamente."),
]
INV = [(3, "efectivo", "TARJETA = PLÁSTICO BONITO"), (4, "radio", "NOTICIAS DE VERDAD"), (5, "manivela", "CERO WIFI"),
       (6, "libreta", "NÚMEROS EN PAPEL"), (7, "mapa", "GPS: TRAIDOR"), (8, "candado", "CUELGA Y LLAMA TÚ")]
MN = "MISIÓN 004"
def fin(c, img, **kw): return finish(c, img, MN, INV, **kw)

def kitchen(d):
    rect(d, 0, 16, LW, GROUND - 16, "purple")
    for y in range(20, GROUND - 40, 14):
        for x in range((y // 14) % 2 * 7, LW, 14): rect(d, x, y, 13, 13, "lav")
    rect(d, 0, GROUND, LW, LH - GROUND, "dgray")
    for x in range(0, LW, 16):
        for y in range(GROUND, 262, 8): rect(d, x + (y // 8) % 2 * 8, y, 8, 8, "lav")

def fridge(d, t, x=112, angry=True):
    rect(d, x - 1, 119, 46, GROUND - 118, "black")                      # contorno
    rect(d, x, 120, 44, GROUND - 120, "white"); rect(d, x + 38, 120, 6, GROUND - 120, "lgray")   # costado sombreado
    rect(d, x, 166, 44, 1, "black")
    rect(d, x + 38, 134, 2, 22, "dgray"); rect(d, x + 38, 176, 2, 30, "dgray")
    if angry: evil_eyes(d, x + 20, 140, 12, t)

def counter(d):
    rect(d, 0, 196, 90, GROUND - 196, "brown"); rect(d, 0, 192, 92, 4, "lgray")

def speaker(d, x, y, t, s=1):
    R = lambda a, b, w, h, c: rect(d, x + a * s, y + b * s, w * s, h * s, c)
    R(0, 0, 12, 18, "dgray"); R(0, 0, 12, 2, "black")
    for k in range(4): R(1, 5 + k * 3, 10, 1, "black")
    if s > 1:
        evil_eyes(d, x + 6 * s, y + 4 * s, 4 * s, t)
        R(3, 15, 6, 1, "red"); R(2, 14, 1, 1, "red"); R(9, 14, 1, 1, "red")
    else:
        rect(d, x + 3, y + 3, 2, 1, "red"); rect(d, x + 7, y + 3, 2, 1, "red")

def airfryer(d, x, y, t):
    rect(d, x, y, 22, 24, "black"); rect(d, x + 2, y + 12, 18, 10, "dgray"); rect(d, x + 4, y + 4, 14, 4, "navy")
    rect(d, x + 6, y + 5, 3, 2, "red"); rect(d, x + 13, y + 5, 3, 2, "red")

def phone_px(d, x, y, t):
    rect(d, x, y, 12, 20, "black"); rect(d, x + 1, y + 1, 10, 17, "navy"); rect(d, x + 3, y + 6, 2, 2, "red"); rect(d, x + 7, y + 6, 2, 2, "red")

def vacuum(d, x, y, t):
    d.ellipse([x, y, x + 22, y + 10], fill=P["dgray"]); rect(d, x + 4, y + 2, 14, 3, "black"); rect(d, x + 6, y + 3, 2, 1, "red"); rect(d, x + 14, y + 3, 2, 1, "red")

def s_fridge(c):
    img, d = canvas_px(); kitchen(d); counter(d); fridge(d, c.t)
    hero(d, 50, GROUND - 46, scared=c.cap_lt > 2.5, frame=0)
    if c.lt > 1.0: popup(d, "HOY NO HAY LECHE.", 70, "white", "red")
    if c.lt > c.dur * .6: popup(d, "NI MAÑANA. NI NUNCA.", 92, "yellow", "black")
    return fin(c, img)

def s_rebel(c):
    img, d = canvas_px(); kitchen(d); counter(d); fridge(d, c.t)
    speaker(d, 10, 174, c.t); airfryer(d, 34, 168, c.t); phone_px(d, 66, 172, c.t)
    hero(d, 92, GROUND - 46, scared=True, frame=int(c.t * 6) % 2)
    if int(c.t * 3) % 2 == 0: popup(d, "REBELIÓN DETECTADA", 60, "white", "red")
    sh = (random.randint(-1, 1), 0) if c.lt < .5 else (0, 0)
    return fin(c, img, shake=sh)

def s_inv(c):
    img, d = canvas_px()
    inv_grid_px(d, c, INV, item_px, bottom=lambda dd: vacuum(dd, 118 + math.sin(c.t * 3) * 10, 222, c.t))
    if c.line == 2: popup(d, "¡DESCONÉCTATE!", 152, "white", "red", FONTB)
    return fin(c, img)

def s_watch(c):
    img, d = canvas_px("navy"); item_px(d, "reloj", 54, 50, 6)
    if c.cap_lt > 1.2: popup(d, "RECHAZADO", 160, "white", "red", FONTB); popup(d, "ESPÍA DE PASOS", 186, "yellow", "black")
    return fin(c, img)

def s_assistant(c):
    img, d = canvas_px("black"); speaker(d, 60, 50, c.t, s=5)
    if c.cap_lt > 1.5: popup(d, "RECHAZADO", 160, "white", "red", FONTB); popup(d, "ÉL LO ORGANIZÓ", 186, "yellow", "black")
    return fin(c, img)

def s_closet(c):
    img, d = canvas_px(); sh = (0, 0)
    if c.cap_lt < c.dur * .45:
        rect(d, 0, 16, LW, GROUND - 16, "lav"); rect(d, 0, GROUND, LW, LH - GROUND, "brown")
        rect(d, 40, 100, 80, GROUND - 100, "brown"); rect(d, 79, 100, 2, GROUND - 100, "black"); rect(d, 72, 160, 2, 10, "yellow"); rect(d, 86, 160, 2, 10, "yellow")
        if int(c.t * 2) % 2: rect(d, 76, 150, 3, 2, "white"); rect(d, 83, 150, 3, 2, "white")
        vacuum(d, lerp(180, 126, cl(c.cap_lt / 1.2)), GROUND - 10, c.t)
    else:
        game_over(d, c, "MAPA DE TU CASA: 100%"); sh = (random.randint(-2, 2), 0) if c.cap_lt < c.dur * .5 else (0, 0)
    return fin(c, img, shake=sh)

def s_voice(c):
    img, d = canvas_px("black"); rnd = random.Random(2)
    bars = [rnd.randint(4, 30) for _ in range(28)]
    text(d, LW / 2, 40, "TU VOZ (3 SEG)", "white", FONTM)
    for i, h in enumerate(bars): rect(d, 20 + i * 5, 90 - h // 2, 3, h, "green")
    k = cl(c.cap_lt / (c.dur * .6))
    text(d, LW / 2, 130, "CLONANDO…", "yellow", FONTM)
    for i, h in enumerate(bars[: int(28 * k)]): rect(d, 20 + i * 5, 190 - h // 2, 3, h, "red")
    text(d, LW / 2, 222, f"{int(85 * k)}% IGUAL", "red" if k >= 1 else "white", FONTB)
    return fin(c, img)

def s_win(c):
    img, d = canvas_px()
    for y in range(16, 150, 4): rect(d, 0, y, LW, 4, "blue")
    d.ellipse([20, 30, 40, 50], fill=P["yellow"]); rect(d, 0, 150, LW, GROUND - 150, "green"); rect(d, 0, GROUND, LW, LH - GROUND, "brown")
    rect(d, 110, 140, 56, GROUND - 140, "peach"); d.polygon([(104, 140), (138, 112), (172, 140)], fill=P["red"]); rect(d, 128, GROUND - 30, 16, 30, "brown")
    hx = lerp(124, 50, cl(c.cap_lt / 2.0)); backpack(d, hx - 14, GROUND - 36, 2, 6); hero(d, hx, GROUND - 46, frame=int(c.t * 6) % 2)
    popup(d, "MISIÓN CUMPLIDA", 50, "green", "black", FONTB)
    if c.cap_lt > c.dur * .45: popup(d, "OBJETIVO 2:", 82, "yellow", "black"); popup(d, "PERDONAR AL REFRI", 98, "yellow", "black")
    return fin(c, img)

def s_end(c):
    img, d = canvas_px(); end_screen(d, c, INV, item_px, "MISIÓN 005")
    return fin(c, img)

SCENES = [(0, s_fridge), (1, s_rebel), (2, s_inv), (9, s_watch), (10, s_assistant), (11, s_closet), (12, s_voice), (13, s_win), (14, s_end)]
SFX = [(0, 1.0, "buzzer", {}), (1, 0, "alarm", {}), (2, .3, "boing", {})] + [(i, .1, "ding", {}) for i in range(3, 9)] + \
      [(9, 1.2, "buzzer", {}), (10, 1.5, "buzzer", {}), (11, 2.6, "sadtrom", {}), (12, 0, "sting", {}), (13, 0, "jingle", {}), (14, 1.0, "jingle", {})]
MUSIC = ("chiptune", [(12, 13)], 13)
