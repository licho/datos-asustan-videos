"""¿Cuánta energía genera el Sol? (dato curioso, ~50 s). Gancho "hice la cuenta": 1 segundo de Sol = 600 mil años de energía humana."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, cubic_out, back_out, radial_bg
from lib.fondos import make_space
from lib.personajes import guy, anchors
from lib.props import (sun, planet_earth, phone_small, bathroom_scale, atom_ball, light_bill, stock_pot, solar_panel,
                       social_house, wall_clock, fish, shades)
from lib.fondos import living_room
from lib.efectos import tag, rubber_stamp

NAME = "2026-12-21_sol-energia"
END = 4.0
LINES = [
 ("mischievously", "Hice la cuenta: en un solo segundo, el Sol produce la energía que la humanidad usaría en más de seiscientos mil años.", "*1 segundo de Sol* = la energía de la humanidad en *600 mil años*"),
 ("sarcastic", "Cada segundo convierte unos cuatro millones de toneladas de su propia masa en energía. Baja de peso sin dieta… y sin gimnasio.", "Pierde *4 millones de toneladas por segundo*. Sin dieta… *y sin gimnasio*"),
 ("serious", "Para lograrlo, fusiona seiscientos millones de toneladas de hidrógeno. Por segundo.", "Fusiona *600 millones de toneladas* de hidrógeno. *Por segundo*"),
 ("excited", "¿Y qué harías con un solo segundo de esa energía? Cargarle el celular a todas las personas del planeta, todos los días… durante más de dos mil millones de años.", "Con *1 segundo*: cargar el celular de todo el planeta, diario, por *+2,000 millones de años*"),
 ("dramatically", "Y con menos de diez segundos, podrías hervir todos los océanos de la Tierra. Caldo de mariscos para todos.", "Con *menos de 10 segundos*: hervir *todos los océanos*. Caldo de mariscos"),
 ("whispers", "Y a la Tierra solo le llega una migaja: menos de una parte en dos mil millones.", "A la Tierra le llega *una migaja*: menos de *1 parte en 2,000 millones*"),
 ("confident", "Aun así, con esa migaja, en hora y media nos cae toda la energía que la humanidad usa en un año.", "Con esa migaja, en *hora y media* nos cae la energía de *todo un año*"),
 ("sarcastic", "Y tú, todavía peleándote con el recibo de la luz.", "Y tú… *peleándote con el recibo de la luz*"),
 ("", "¿Ya pusiste paneles solares o sigues pagando? Te leo.", "¿Paneles solares… *o sigues pagando*? Te leo"),
]

def space(t, seed=7):
    return make_space(t, seed=seed)

def big_sun(d, x, y, r, t, mood="happy", glasses=False):
    sun(d, x, y, r, t, mood)
    if glasses: shades(d, x, y - r * .1, w=r * 1.0)

# ------------------------------------------------------------------ escenas
def hook(c):
    img = space(c.t); d = ImageDraw.Draw(img); f = c.lt / c.dur
    big_sun(d, 540, 1000, 270, c.t, glasses=True)
    n = int(lerp(0, 600000, cubic_out(cl(f / .7))))
    bigtext(d, f"{n:,} AÑOS", 540, 570, 92, fill=YEL)
    d.text((540, 655), "DE ENERGÍA HUMANA", font=F(48), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)
    chip(d, "1 SEGUNDO DE SOL", CHIP1, bg=ORANGE)
    return img

def weight(c):
    img = radial_bg(((0, (250, 235, 215)), (1, (215, 195, 170))), cy=900); d = ImageDraw.Draw(img); f = c.lt / c.dur
    d.rectangle([0, 1290, W, 1380], fill=(170, 130, 90))
    n = int(4_000_000 * f)
    top = bathroom_scale(d, 540, 1290, 1.4, f"-{n:,} t")
    big_sun(d, 540, top - 260 * 1.15, 260, c.t, mood="happy")
    chip(d, "−4 MILLONES TON/SEG", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .55: tag(img, "SIN DIETA NI GYM", 540, 560, cl((f - .55) / .1), rot=-6, bg=GREEN, size=56)
    return img

def fusion(c):
    img = space(c.t, 3); d = ImageDraw.Draw(img); f = c.lt / c.dur
    d.ellipse([540 - 430, 900 - 430, 540 + 430, 900 + 430], fill=(255, 140, 40), outline=(255, 200, 80), width=12)
    d.ellipse([540 - 300, 900 - 300, 540 + 300, 900 + 300], fill=(255, 190, 70))
    for k in range(4):
        ph = (c.t * .9 + k / 4) % 1; ang = k * math.pi / 2 + .4
        cx, cy = 540 + math.cos(ang) * 150, 900 + math.sin(ang) * 150
        if ph < .6:
            dd = 120 * (1 - ph / .6)
            for sgn in (-1, 1): atom_ball(d, cx + sgn * dd * math.cos(ang + 1.57), cy + sgn * dd * math.sin(ang + 1.57), 34, "H")
        else:
            if ph < .68: d.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(255, 255, 220))
            atom_ball(d, cx, cy, 48, "He")
    n = int(lerp(0, 600, cl(f / .6)))
    bigtext(d, f"{n} MILLONES DE TONELADAS", 540, 560, 56, fill=YEL)
    chip(d, "FUSIÓN NUCLEAR", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if f > .7: bigtext(d, "¡POR SEGUNDO!", 540, 1290, 80, fill=WHITE)
    return img

def phones(c):
    img = space(c.t, 9); d = ImageDraw.Draw(img); f = c.lt / c.dur
    big_sun(d, 905, 840, 130, c.t)
    for i in range(4):
        for j in range(4):
            x, y = 110 + j * 175, 760 + i * 150
            d.line([(x + 30, y - 60), (830, 840 + (i - 1.5) * 30)], fill=(60, 60, 70), width=4)
    for i in range(4):
        for j in range(4):
            x, y = 110 + j * 175, 760 + i * 150
            phone_small(d, x, y, .45)
            lvl = cl(f * 1.6 - (i + j) * .05)
            d.rectangle([x - 22, y + 30 - 60 * lvl, x + 22, y + 30], fill=(80, 220, 120))
    yrs = int(lerp(0, 2_000_000_000, cubic_out(cl((f - .3) / .6))))
    if f > .3: bigtext(d, f"{yrs:,} AÑOS", 540, 560, 66, fill=YEL)
    chip(d, "¿QUÉ HARÍAS CON 1 SEGUNDO?", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def oceans(c):
    img = space(c.t, 11); d = ImageDraw.Draw(img); f = c.lt / c.dur
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); big_sun(ImageDraw.Draw(lay), 540, 1420, 380, c.t, mood="happy")   # el Sol como estufa
    lay = lay.crop((0, 0, W, 1370)); img.paste(lay, (0, 0), lay); d = ImageDraw.Draw(img)
    x, top = stock_pot(d, 540, 1230, 1.25, c.t)
    planet_earth(d, x, top - 40, 150, "scared")
    if f > .35:
        k = ((c.t * .8) % 1)
        fish(d, 830 + 60 * k, top - 60 - math.sin(k * math.pi) * 150, .8)
    secs = lerp(0, 9.3, cl(f / .7))
    bigtext(d, f"{secs:.1f} SEGUNDOS", 540, 560, 76, fill=YEL)
    chip(d, "OCÉANOS HIRVIENDO", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .7: tag(img, "CALDO DE MARISCOS", 540, 690, cl((f - .7) / .1), rot=-5, bg=ORANGE, size=54)
    return img

def crumb(c):
    img = space(c.t, 5); d = ImageDraw.Draw(img); f = c.lt / c.dur
    cx, cy = 120, 900
    for k in range(18):
        a = -math.pi / 2 + k * math.pi / 17
        L = 1300
        if math.sin(a) > 0: L = min(L, (1360 - cy) / math.sin(a))
        if math.sin(a) < 0: L = min(L, (500 - cy) / math.sin(a))
        d.line([(cx + math.cos(a) * 330, cy + math.sin(a) * 330), (cx + math.cos(a) * L, cy + math.sin(a) * L)], fill=(255, 220, 120), width=6)
    big_sun(d, cx, cy, 300, c.t)
    ex, ey = 930, 900 + math.tan(math.atan2(0, 1)) * 0
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(80, 140, 230), outline=WHITE, width=3)
    if f > .25:
        d.ellipse([ex - 60, ey - 60, ex + 60, ey + 60], outline=YEL, width=6)
        d.text((ex, ey - 110), "TÚ", font=F(54), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    chip(d, "UNA MIGAJA", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if f > .5: bigtext(d, "1 PARTE EN 2,000 MILLONES", 540, 560, 56, fill=WHITE)
    return img

def hour(c):
    img = space(c.t, 13); d = ImageDraw.Draw(img); f = c.lt / c.dur
    planet_earth(d, 330, 950, 220, "happy")
    wall_clock(d, 800, 760, 130, c.t, hour=1, minute=int(lerp(0, 30, cl(f / .6))))
    d.rounded_rectangle([640, 980, 960, 1060], 20, outline=WHITE, width=6)
    d.rounded_rectangle([652, 992, 652 + 296 * cl(f / .6), 1048], 14, fill=(250, 200, 60))
    d.text((800, 1110), "ENERGÍA DE 1 AÑO", font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    chip(d, "1.5 HORAS = 1 AÑO", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def bill(c):
    img, d = living_room(); f = c.lt / c.dur
    d.rectangle([640, 520, 1000, 860], fill=(140, 200, 245), outline=(240, 240, 240), width=12)
    sun(d, 820, 690, 110, c.t, mood="happy")
    for k in range(2): d.text((900 + k * 40, 600 - k * 30), "JA", font=F(40), fill=RED, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    a = anchors(330, 1290, .85)
    guy(d, 330, 1290, .85, mood="scared", t=c.t)
    light_bill(d, 470, 880, 300, total="$4,850")
    hx, hy = a["hand_r_down"]; d.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], fill=SKIN, outline=BLK, width=3)
    chip(d, "¿Y EL RECIBO?", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def ending(c):
    img = radial_bg(((0, (250, 220, 150)), (1, (240, 160, 90))), cy=700); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(150, 150, 140))
    sun(d, 820, 600, 130, c.t, mood="happy")
    social_house(d, 420, 1290, 1.6)
    for k in range(2): solar_panel(d, 300 + k * 230, 1290 - 250 * 1.6 - 18, 200)
    chip(d, "¿PANELES… O RECIBO?", CHIP1, bg=GREEN, appear=c.lt / .3)
    if c.lt > 1.0: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=RED, appear=(c.lt - 1.0) / .3)
    return img

SCENES = [(0, hook), (1, weight), (2, fusion), (3, phones), (4, oceans), (5, crumb), (6, hour), (7, bill), (8, ending)]
SFX = [(0, .1, "sting", {}), (1, .3, "boing", {}), (2, .2, "rumble", {}), (3, .3, "ding", {}), (4, .3, "rumble", {}), (4, 4.0, "splat", {}),
       (5, .2, "whoosh", {}), (6, .3, "ding", {}), (7, .2, "sadtrom", {}), (8, .2, "pop", {})]
MUSIC = ("pad", [(5, 6)], 6)
