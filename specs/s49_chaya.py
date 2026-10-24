"""La planta a la que le tienes que pedir permiso: la chaya (tradición maya de Yucatán). ~45 s."""
import math, random
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, cubic_out, back_out, radial_bg
from lib.personajes import chaya, chaya_leaf_zoom, guy, stamp_guy, anchors
from lib.props import stock_pot, stopwatch, skull, greens_plate, sign_board
from lib.fondos import monte
from lib.efectos import tag, rubber_stamp

NAME = "2026-12-10_chaya-permiso"
END = 4.0
LINES = [
 ("mischievously", "Esta planta exige que le pidas permiso. Y la ciencia le da la razón.", "Esta planta *exige que le pidas permiso*. Y la ciencia *le da la razón*"),
 ("whispers", "Es la chaya. En comunidades mayas de Yucatán se dice que la habitan los espíritus del monte.", "Es *la chaya*. Dicen que la habitan *los espíritus del monte*"),
 ("sarcastic", "Si la cortas sin permiso, se venga: te da comezón… y la comida te sale amarga.", "Si la cortas sin permiso: *comezón*… y comida *amarga*"),
 ("serious", "¿La comezón? Es real: sus hojas tienen pelitos que pican.", "¿La comezón? *Es real*: sus hojas tienen *pelitos que pican*"),
 ("dramatically", "Y cruda, suelta cianuro. Por eso se hierve unos veinte minutos antes de comerla.", "Cruda *suelta cianuro*. Se hierve *unos 20 minutos*"),
 ("mischievously", "Hay quien dice que en olla de aluminio cae mal… pero eso nadie lo ha comprobado.", "¿Olla de aluminio? *Nadie lo ha comprobado*"),
 ("confident", "Bien cocida, es de las verduras más nutritivas: proteína, hierro, calcio y vitamina C.", "Bien cocida: *proteína, hierro, calcio y vitamina C*"),
 ("sarcastic", "O sea: pídele permiso, hiérvela… y no le faltes al respeto. Como a la suegra.", "Pídele permiso, hiérvela… *y respétala. Como a la suegra*"),
 ("", "¿Tú le pedirías permiso? Te leo.", "¿Tú le pedirías permiso? *Te leo*"),
]

def hook(c):
    img, d = monte(c.t)
    chaya(d, 420, 1290, 1.0, c.t, mood="serious", arms="crossed")
    sign_board(d, 900, 1290, "NO CORTAR", size=34, post_h=170)
    chip(d, "PIDE PERMISO", CHIP1, bg=RED)
    if c.lt / c.dur > .5: bigtext(d, "LA CIENCIA LE DA LA RAZÓN", 540, 560, 56, fill=WHITE)
    return img

def spirits(c):
    img, d = monte(c.t, night=True)
    chaya(d, 540, 1290, 1.05, c.t, mood="serious", arms="none", glow=True)
    chip(d, "LA CHAYA · TRADICIÓN MAYA", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def revenge(c):
    f = c.lt / c.dur
    img, d = monte(c.t, seed=9)
    chaya(d, 790, 1290, .8, c.t, mood="angry", arms="crossed")
    sh = math.sin(c.t * 40) * 8 if f > .25 else 0
    guy(d, 270 + sh, 1290, .8, mood="scared" if f > .25 else "neutral", arms="up" if f > .25 else "down", t=c.t)
    if f > .25:
        for k in range(5):
            a = c.t * 6 + k
            x0, y0 = 270 + math.cos(a) * 140, 900 + math.sin(a) * 160
            d.line([(x0, y0), (x0 + 30, y0 - 30)], fill=RED, width=6)
        bigtext(d, "¡COMEZÓN!", 270, 560, 64, fill=YEL)
    if f > .6: tag(img, "Y AMARGA", 760, 640, cl((f - .6) / .1), rot=8, bg=RED, size=54)
    chip(d, "SU VENGANZA", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def hairs(c):
    img = radial_bg(((0, (60, 90, 70)), (1, (30, 50, 40))), cy=900); d = ImageDraw.Draw(img)
    k = cubic_out(cl(c.lt / 1.0))
    chaya_leaf_zoom(d, 540, 1250, lerp(250, 500, k), c.t)
    chip(d, "PELOS URTICANTES", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def boil(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (250, 235, 210)), (1, (215, 190, 160))), cy=900); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(150, 110, 80))
    if f < .4:
        chaya_leaf_zoom(d, 420, 1250, 300, c.t, hairs=False)
        skull(d, 820, 800, 110)
        bigtext(d, "CRUDA = CIANURO", 540, 560, 70, fill=RED)
    else:
        x, top = stock_pot(d, 400, 1290, 1.0, c.t, liquid=(110, 170, 100))
        stopwatch(d, 850, 800, 110, lerp(0, 20 * 60, cl((f - .4) / .5)))
        bigtext(d, "~20 MINUTOS", 540, 560, 70, fill=YEL)
    chip(d, "NUNCA CRUDA", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def aluminum(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (235, 235, 245)), (1, (190, 195, 210))), cy=900); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(150, 110, 80))
    stock_pot(d, 540, 1290, 1.2, c.t, col=(200, 205, 215), liquid=(110, 170, 100))
    d.text((540, 760 + math.sin(c.t * 4) * 10), "?", font=F(160), fill=YEL, anchor="mm", stroke_width=8, stroke_fill=BLK)
    if f > .5: rubber_stamp(img, "NO COMPROBADO", 540, 1000, cl((f - .5) / .1), col=RED, size=78, rot=-10)
    d = ImageDraw.Draw(img)
    chip(d, "¿MITO DE COCINA?", CHIP1, bg=GRAY, appear=c.lt / .3)
    return img

def nutritious(c):
    f = c.lt / c.dur
    img, d = monte(c.t, seed=4)
    chaya(d, 800, 1290, .75, c.t, mood="happy", arms="none")
    d.rectangle([60, 1150, 560, 1180], fill=(150, 100, 60), outline=BLK, width=4)
    for x in (90, 530): d.rectangle([x - 10, 1180, x + 10, 1290], fill=(120, 80, 50), outline=BLK, width=3)
    greens_plate(d, 310, 1150, 1.0)
    for k, (txt, col) in enumerate((("PROTEÍNA", BLUE), ("HIERRO", GRAY), ("CALCIO", PURPLE), ("VITAMINA C", ORANGE))):
        if f > .15 + k * .15: tag(img, txt, 290 + (k % 2) * 300, 640 + (k // 2) * 120, cl((f - .15 - k * .15) / .08), rot=-5 + k * 3, bg=col, size=46)
    d = ImageDraw.Draw(img)
    chip(d, "SUPERVERDURA", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def respect(c):
    img, d = monte(c.t, seed=12)
    chaya(d, 780, 1290, .85, c.t, mood="happy", arms="none")
    bow = 35 * cubic_out(cl(c.lt / 1.0)) * (1 if (c.lt % 2) < 1.4 else .4)
    stamp_guy(img, 290, 1290 - 327 * .8, .8, bow, mood="relief", arms="down", t=c.t)
    d = ImageDraw.Draw(img)
    chip(d, "RESPETO… COMO A LA SUEGRA", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def ending(c):
    img, d = monte(c.t, night=True, seed=6)
    chaya(d, 540, 1290, 1.0, c.t, mood="wink", arms="none", glow=True)
    chip(d, "¿LE PEDIRÍAS PERMISO?", CHIP1, bg=GREEN, appear=c.lt / .3)
    if c.lt > 1.0: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=RED, appear=(c.lt - 1.0) / .3)
    return img

SCENES = [(0, hook), (1, spirits), (2, revenge), (3, hairs), (4, boil), (5, aluminum), (6, nutritious), (7, respect), (8, ending)]
SFX = [(0, .1, "sting", {}), (1, .2, "whoosh", {}), (2, 1.0, "buzzer", {}), (3, .2, "pop", {}), (4, .2, "sting", {}), (4, 2.5, "rumble", {}),
       (5, 2.0, "thud", {}), (6, .5, "ding", {}), (7, .5, "boing", {}), (8, .2, "jingle", {})]
MUSIC = ("pad", [(3, 4)], 4)
