"""¿Cómo duermen las jirafas? (dato curioso corto, ~50 s). Gancho: sueñan menos de media hora por noche."""
import math
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, cubic_out, back_out, radial_bg
from lib.personajes import giraffe, lion, guy, anchors
from lib.props import stopwatch, vertebrae, mug, arrow
from lib.fondos import savanna
from lib.efectos import tag
from reels_engine.camera import Shot, film, path

NAME = "2026-12-19_jirafas-duermen"
END = 4.5
LINES = [
 ("mischievously", "Una jirafa sueña… menos de media hora por noche.", "Una jirafa sueña… *menos de media hora por noche*"),
 ("sarcastic", "Y ni siquiera de corrido: en ratitos de dos a cuatro minutos. Ni te da para un capítulo.", "Y en ratitos de *2 a 4 minutos*. Ni te da para un capítulo"),
 ("mischievously", "Para soñar se echa… y hace algo rarísimo: dobla su cuello de casi dos metros hacia atrás, como un arco, y recarga la cabeza en su propio trasero.", "Dobla su cuello de *casi 2 metros* hacia atrás… y se recarga *en su propio trasero*"),
 ("sarcastic", "Y ese cuello tiene los mismos siete huesos que el tuyo… solo que cada uno mide hasta veinticinco centímetros. Ni la mejor almohada cervical lo arregla.", "*Los mismos 7 huesos* que tu cuello… pero de *hasta 25 cm cada uno*"),
 ("serious", "Es que en esa fase los músculos se aflojan: si estuviera parada, se iría de boca.", "En esa fase *los músculos se aflojan*: parada, *se iría de boca*"),
 ("dramatically", "¿Y por qué tan poquito? Echada no ve bien ni se levanta rápido… y los leones lo saben.", "Echada no ve bien ni se levanta rápido… *y los leones lo saben*"),
 ("confident", "Por eso duermen por turnos: mientras una sueña, las demás vigilan.", "Duermen *por turnos*: una sueña, *las demás vigilan*"),
 ("sarcastic", "Así que la próxima vez que digas “no dormí nada”… acuérdate de la jirafa: soñó dos minutos y se fue a trabajar.", "¿“No dormí nada”? La jirafa *soñó 2 minutos y se fue a trabajar*"),
 ("", "¿Tú cuántas horas duermes? Te leo en los comentarios.", "¿Tú cuántas horas duermes? *Te leo*"),
]
GS = .9                                     # escala de la jirafa parada (cabeza ~ 1290 - 710·GS)

def zzz(d, x, y, t, col=WHITE):
    for k in range(3):
        u = (t * .6 + k / 3) % 1
        d.text((x + u * 60, y - u * 140), "z", font=F(int(40 + 30 * u)), fill=col, anchor="mm", stroke_width=4, stroke_fill=BLK)

# ------------------------------------------------------------------ escenas
def hook(c):
    img, d = savanna(c.t)
    giraffe(d, 400 + math.sin(c.t * 1.5) * 12, 1290, GS, c.t, eyes="sleepy", bags=True)
    stopwatch(d, 850, 800, 110, 29 * 60 + 59)
    chip(d, "MENOS DE 30 MIN", CHIP1, bg=RED)
    bigtext(d, "SOÑANDO", 850, 1010, 46, fill=YEL)
    return img

def bouts(c):
    img, d = savanna(c.t)
    secs = (c.lt * 55) % 180
    nod = cl(secs / 150) * .35
    giraffe(d, 400, 1290, GS, c.t, eyes="closed", droop=nod)
    stopwatch(d, 850, 800, 110, secs)
    if secs > 165: bigtext(d, "¡DESPIERTA!", 850, 1050, 52, fill=RED)
    chip(d, "RATITOS DE 2 A 4 MIN", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def neck_arc(c):
    f = c.lt / c.dur
    world, d = savanna(c.t, seed=7)
    k = cubic_out(cl((f - .12) / .6))
    H = giraffe(d, 560, 1290, 1.05, c.t, pose="lie", curl=k, eyes="closed" if k > .5 else "open")
    if k > .97: zzz(d, H[0] + 40, H[1] - 60, c.t)
    img = Image.new("RGB", (W, 1920)); film(img, world, path(c.lt, [(0, Shot(560, 1000, 1.0)), (c.dur * .8, Shot(520, 1080, 1.25))]))
    d = ImageDraw.Draw(img)
    chip(d, "CUELLO EN ARCO", CHIP1, bg=GREEN, appear=c.lt / .3)
    if f < .45: bigtext(d, "CUELLO: ~2 METROS", 540, 560, 64, fill=WHITE)
    elif f > .78: tag(img, "ALMOHADA: SU TRASERO", 540, 600, cl((f - .78) / .1), rot=-6, bg=RED, size=56)
    return img

def bones(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (70, 90, 130)), (1, (30, 40, 70))), cy=900); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(60, 70, 100))
    guy(d, 250, 1290, .9, t=c.t)
    a = anchors(250, 1290, .9)
    hy = a["neck"][1] - 22
    d.rounded_rectangle([250 - 30, hy - 6, 250 + 30, a["chest"][1] + 10], 10, fill=(30, 40, 70), outline=WHITE, width=3)
    vertebrae(d, 250, hy, a["chest"][1] + 4, n=7, w=28)
    d.text((250, 560), "TÚ", font=F(64), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)
    vertebrae(d, 760, 640, 1260, n=7, w=96, labels=True)
    d.text((760, 560), "JIRAFA", font=F(64), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    if f > .35:
        seg = (1260 - 640) / 7; ry0, ry1 = 640 + seg * 3, 640 + seg * 4
        d.line([(860, ry0), (860, ry1)], fill=YEL, width=8)
        for yy in (ry0, ry1): d.line([(840, yy), (880, yy)], fill=YEL, width=8)
        d.text((950, (ry0 + ry1) / 2), "25 cm", font=F(48), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=BLK)
    chip(d, "7 HUESOS · HASTA 25 CM C/U", CHIP1, bg=BLUE, appear=c.lt / .3)
    if f > .72: tag(img, "NI LA ALMOHADA CERVICAL", 540, 1180, cl((f - .72) / .1), rot=-5, bg=RED, size=50)
    return img

def floppy(c):
    f = c.lt / c.dur
    img, d = savanna(c.t, seed=9)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    droop = cl(f / .5)
    giraffe(ld, 420, 1290, GS, c.t, eyes="closed", droop=droop)
    ang = -14 * cubic_out(cl((f - .45) / .3))
    rot = lay.rotate(ang, resample=Image.BICUBIC, center=(420 + 125 * GS, 1290))
    img.paste(rot, (0, 0), rot); d = ImageDraw.Draw(img)
    chip(d, "MÚSCULOS: APAGADOS", CHIP1, bg=ORANGE, appear=c.lt / .3)
    if f > .6: bigtext(d, "¡SE IRÍA DE BOCA!", 540, 560, 70, fill=RED)
    return img

def lions(c):
    f = c.lt / c.dur
    img, d = savanna(c.t, night=True, seed=3)
    H = giraffe(d, 330, 1290, .85, c.t, pose="lie", curl=1, eyes="closed")
    zzz(d, H[0] + 40, H[1] - 60, c.t)
    if f > .35:
        ly = 1290 + 160 * (1 - cubic_out(cl((f - .35) / .25)))
        lion(d, 850, ly, .75, c.t)
        nx, ny = 850, ly - 260 * .75
        d.polygon([(nx - 50, ny - 10), (nx + 50, ny - 10), (nx, ny + 70)], fill=WHITE, outline=BLK)
    for k in range(16):                                           # pasto alto delante del león
        gx = 640 + k * 28; d.polygon([(gx - 14, 1295), (gx + 4, 1130 - (k % 3) * 25), (gx + 14, 1295)], fill=(70, 70, 50), outline=BLK)
    chip(d, "ECHADA = PRESA FÁCIL", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if f > .7: bigtext(d, "LOS LEONES LO SABEN", 540, 560, 64, fill=YEL)
    return img

def shifts(c):
    img, d = savanna(c.t, seed=11)
    giraffe(d, 230, 1290, .62, c.t, binoculars=True, flip=True)
    H = giraffe(d, 560, 1290, .62, c.t, pose="lie", curl=1, eyes="closed")
    zzz(d, H[0] + 30, H[1] - 40, c.t, col=WHITE)
    giraffe(d, 830, 1290, .62, c.t, binoculars=True)
    chip(d, "TURNOS DE VIGILANCIA", CHIP1, bg=GREEN, appear=c.lt / .3)
    if c.lt / c.dur > .4: bigtext(d, "UNA SUEÑA, DOS VIGILAN", 540, 560, 58, fill=WHITE)
    return img

def to_work(c):
    f = c.lt / c.dur
    img, d = savanna(c.t, seed=13)
    d.rounded_rectangle([830, 1000, 1040, 1080], 12, fill=(240, 240, 235), outline=BLK, width=5)
    d.text((935, 1040), "OFICINA →", font=F(36), fill=BLK, anchor="mm"); d.line([(935, 1080), (935, 1290)], fill=(110, 80, 50), width=12)
    x = lerp(250, 520, f)
    giraffe(d, x, 1290, .8, c.t, eyes="sleepy", bags=True, walk=True, tie=(200, 40, 50))
    chip(d, "¿“NO DORMÍ NADA”?", CHIP1, bg=RED, appear=c.lt / .3)
    if f > .45: bigtext(d, "SOÑÓ 2 MIN… Y A TRABAJAR", 540, 560, 58, fill=YEL)
    return img

def ending(c):
    img, d = savanna(c.t, night=True, seed=3)
    H = giraffe(d, 540, 1290, .95, c.t, pose="lie", curl=1, eyes="closed")
    zzz(d, H[0] + 40, H[1] - 60, c.t)
    chip(d, "¿CUÁNTAS HORAS DUERMES?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if c.lt > 1.5: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=RED, appear=(c.lt - 1.5) / .3)
    return img

SCENES = [(0, hook), (1, bouts), (2, neck_arc), (3, bones), (4, floppy), (5, lions), (6, shifts), (7, to_work), (8, ending)]
SFX = [(0, .1, "sting", {}), (1, .2, "pop", {}), (2, .8, "whoosh", {}), (2, 6.0, "ding", {}), (3, .3, "pop", {}), (3, 6.5, "boing", {}),
       (4, 2.5, "thud", {}), (5, 1.5, "rumble", {}), (6, .3, "ding", {}), (7, .3, "pop", {}), (8, .2, "jingle", {})]
MUSIC = ("waltz", [(5, 6)], 6)
