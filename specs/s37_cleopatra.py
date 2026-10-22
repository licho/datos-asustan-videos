"""Cleopatra vivió más cerca de la Luna que de las pirámides (datos de tiempo)."""
import math
from lib.core import *
from lib.core import say
from lib.motion import tw, yoyo, layer, glow, shake, back_out, elastic_out, cubic_out, bounce_out, radial_bg, space_bg
from lib.personajes import guy, cleopatra, mammoth, stego, trex, anchors
from lib.props import pyramid, rocket, nopal, building, document, picture, phone_small

NAME = "2026-11-30_cleopatra-tiempo"
END = 4.5
LINES = [
 ("mischievously", "Cleopatra vivió más cerca de la llegada a la Luna… que de la construcción de la Gran Pirámide.", "Cleopatra vivió *más cerca de la llegada a la Luna*… que de la Gran Pirámide"),
 ("serious", "La pirámide tiene unos cuatro mil quinientos años. Cuando Cleopatra nació, ya tenía más de dos mil.", "Cuando Cleopatra nació, la pirámide *ya tenía más de 2,000 años*"),
 ("sarcastic", "Para ella, la pirámide era más antigua… que ella para nosotros.", "Para ella, la pirámide era *más antigua que ella para nosotros*"),
 ("", "Y su familia ni siquiera era egipcia: venía de Macedonia, en Grecia. Gobernaron Egipto siglos… sin aprender egipcio. Ella sí.", "Su familia venía de *Macedonia*. Siglos sin aprender egipcio… *ella sí*"),
 ("dramatically", "Más: cuando se construían las pirámides, todavía había mamuts vivos, en una isla del Ártico.", "Cuando se construían las pirámides… *todavía había mamuts*"),
 ("mischievously", "La Universidad de Oxford ya daba clases… antes de que se fundara Tenochtitlan.", "Oxford ya daba clases… *antes de que se fundara Tenochtitlan*"),
 ("sarcastic", "Sí: hay universidades más viejas que el imperio azteca. Y siguen cobrando colegiatura.", "Más viejas que el imperio azteca… *y siguen cobrando colegiatura*"),
 ("whispers", "Y el más fuerte: el tiranosaurio vivió más cerca de nosotros… que del estegosaurio.", "El T-rex vivió *más cerca de nosotros* que del estegosaurio"),
 ("", "Entre ellos hay más de ochenta millones de años. Entre el T-rex y tú, sesenta y seis.", "Entre ellos: *+80 millones de años*. Entre el T-rex y tú: *66*"),
 ("sarcastic", "O sea, para el estegosaurio, el T-rex era el futuro. Y tú también.", "Para el estegosaurio, el T-rex era el futuro. *Y tú también.*"),
 ("", "¿Cuál te rompió más la cabeza? Te leo en los comentarios.", "¿Cuál te rompió más la cabeza? *Te leo*"),
]
DESERT = ((0, (255, 225, 160)), (.6, (235, 175, 100)), (1, (180, 110, 70)))
SAND = (225, 185, 120)

def timeline(d, lt, y=1150, labels=True):
    d.line([(90, y), (990, y)], fill=WHITE, width=8)
    pts = [(130, "2560 a.C."), (585, "30 a.C."), (950, "1969")]
    for i, (x, lab) in enumerate(pts):
        if lt > .2 + i * .5: d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=YEL, outline=BLK, width=4); d.text((x, y + 55), lab, font=F(38), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    if labels and lt > 1.8:
        for (a, b, txt, col) in ((130, 585, "~2,530 AÑOS", RED), (585, 950, "~2,000 AÑOS", GREEN)):
            k = tw(lt, 1.8, .6, 0, 1, cubic_out); yy = y - 70
            d.line([(a + 20, yy), (a + 20 + (b - a - 40) * k, yy)], fill=col, width=10)
            if k > .9: d.text(((a + b) / 2, yy - 45), txt, font=F(40), fill=col, anchor="mm", stroke_width=5, stroke_fill=WHITE)

def s_hook(c):
    img = space_bg(c.t, stops=((0, (60, 40, 110)), (.6, (25, 18, 60)), (1, (8, 6, 25)))); d = ImageDraw.Draw(img); lt = c.lt
    timeline(d, lt)
    sc = [tw(lt, .2 + i * .5, .5, 0, 1, back_out) for i in range(3)]
    d = layer(img, lambda dd, cx, cy: pyramid(dd, cx, cy + 150, .35), 185, 830, 420, sc[0], sc[0])
    d = layer(img, lambda dd, cx, cy: cleopatra(dd, cx, cy + 230, .55, c.t, mood="happy"), 585, 720 + yoyo(lt, 1.5, .8, 0, -8), 520, sc[1], sc[1])
    d = layer(img, lambda dd, cx, cy: rocket(dd, cx, cy + 140, .55, c.t), 950, 790, 420, sc[2], sc[2])
    chip(d, "DATOS QUE ROMPEN EL TIEMPO", CHIP1, bg=PURPLE, size=48, appear=lt / .3)
    return img

def s_age(c):
    img = radial_bg(DESERT, cy=700); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 1180, W, 1380], fill=SAND)
    pyramid(d, 330, 1200, 1.0)
    d = layer(img, lambda dd, cx, cy: cleopatra(dd, cx, cy + 230, .65, c.t, mood="neutral"), tw(lt, 0, .8, 1200, 820, back_out), 1200 - 230, 560)
    n = int(tw(lt, .6, 1.6, 0, 2000, cubic_out))
    bigtext(d, f"+{n:,} AÑOS", 470, 640, 80, fill=WHITE)
    chip(d, "LA PIRÁMIDE YA ERA ANTIGUA", CHIP1, bg=ORANGE, size=48, appear=lt / .3)
    return img

def s_old(c):
    img = radial_bg(DESERT, cy=700); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 1180, W, 1380], fill=SAND)
    pyramid(d, 280, 1200, .9)
    cleopatra(d, 780, 1200, .7, c.t, mood="bored", arms="point")
    if lt > .6:
        sc = tw(lt, .6, .4, 0, 1, back_out)
        if sc > .3: say(d, "Qué viejita…", mouth=(780, 1200 - 495 * .7), head=90 * .7, size=int(54 * sc), side=-1)
    return img

def s_family(c):
    img = radial_bg(((0, (250, 240, 220)), (1, (210, 195, 170))), cy=800); d = ImageDraw.Draw(img); lt = c.lt
    for i, x in enumerate((200, 540, 880)):
        if lt > .2 + i * .3:
            picture(d, x - 120, 520, x + 120, 820, "portrait", label="PTOLOMEO" if i < 2 else "CLEOPATRA")
    d.rectangle([380, 880, 700, 960], fill=(30, 90, 170), outline=BLK, width=4); d.text((540, 920), "MACEDONIA", font=F(40), fill=WHITE, anchor="mm")
    if lt > c.dur * .6:
        cleopatra(d, 540, 1290, .45, c.t, mood="happy")
        say(d, "¡Ya hablo egipcio!", mouth=(540, 1290 - 495 * .45), head=90 * .45, size=42, maxw=380, side=1)
    chip(d, "¿EGIPCIA?", CHIP1, bg=BLUE, appear=lt / .3)
    return img

def s_mammoth(c):
    img, d = canvas(((210, 230, 245), (240, 245, 250))); lt = c.lt
    d.rectangle([0, 860, W, 880], fill=BLK)
    d.rectangle([0, 760, W, 860], fill=(240, 245, 250))
    d = layer(img, lambda dd, cx, cy: mammoth(dd, cx, cy + 180, .55, c.t), tw(lt, 0, .9, -300, 360, back_out), 760 - 180, 560)
    d.text((880, 520), "ÁRTICO", font=F(44), fill=BLUE, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    img2 = radial_bg(DESERT, cy=1100); img.paste(img2.crop((0, 880, W, 1380)), (0, 880)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, 1380], fill=SAND)
    pyramid(d, 640, 1260, .6, built=tw(lt, .5, 2.5, .2, .7, cubic_out))
    d.text((200, 960), "EGIPTO", font=F(44), fill=(160, 70, 30), anchor="mm", stroke_width=4, stroke_fill=WHITE)
    chip(d, "MISMA ÉPOCA", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def s_oxford(c):
    img, d = canvas(((150, 200, 240), (210, 230, 245))); lt = c.lt
    d.rectangle([0, 1250, W, 1380], fill=(110, 150, 90))
    s1 = tw(lt, .1, .6, 0, 1, back_out)
    if s1 > .05:
        building(d, 270, 1250, 300 * s1, 520 * s1, (190, 170, 140), seed=4)
        for dx in (-120, 120): d.polygon([(270 + dx * s1 - 30, 1250 - 520 * s1), (270 + dx * s1, 1250 - 620 * s1), (270 + dx * s1 + 30, 1250 - 520 * s1)], fill=(150, 130, 110), outline=BLK)
    d.text((270, 1300), "OXFORD · 1096", font=F(42), fill=BLK, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    s2 = tw(lt, c.dur * .45, .6, 0, 1, back_out)
    if s2 > .05:
        d.ellipse([600, 1080, 1020, 1250], fill=(80, 160, 210), outline=BLK, width=4)
        d = layer(img, lambda dd, cx, cy: nopal(dd, cx, cy + 200, .8), 810, 1170 - 200, 520, s2, s2)
        d.text((810, 1300), "TENOCHTITLAN · 1325", font=F(40), fill=BLK, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    chip(d, "229 AÑOS ANTES", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def s_tuition(c):
    img = radial_bg(((0, (250, 245, 235)), (1, (215, 210, 200))), cy=800); d = ImageDraw.Draw(img); lt = c.lt
    sc = tw(lt, 0, .5, .6, 1, back_out)
    d = layer(img, lambda dd, cx, cy: document(dd, cx - 260, cy - 340, 520, 680, "COLEGIATURA", ["Alumno: tú", "Desde: 1096", "Total: $$$$$$"], size=34, stamp=("PAGO PENDIENTE", RED)), 540, 880, 760, sc, sc, tw(lt, 0, .5, -8, 0, back_out))
    return img

def s_dinos(c):
    img = radial_bg(((0, (250, 220, 170)), (1, (200, 140, 90))), cy=800); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 1250, W, 1380], fill=(170, 130, 80))
    stego(d, 190, 1260, .5, c.t)
    d = layer(img, lambda dd, cx, cy: trex(dd, cx, cy + 260, .55, c.t, roar=(lt % 1.5) < .4), 560, 1260 - 260, 640, 1, tw(lt, .3, .6, .8, 1, elastic_out))
    guy(d, 930, 1270, .45, mood="happy", t=c.t)
    chip(d, "EL MÁS FUERTE", CHIP1, bg=RED, appear=lt / .3)
    return img

def s_ruler(c):
    img = space_bg(c.t); d = ImageDraw.Draw(img); lt = c.lt
    x0, x1, y = 90, 990, 900
    xa, xb, xc = x0, x0 + (x1 - x0) * 84 / 150, x1                # 150 Ma → 66 Ma → hoy
    k1 = tw(lt, .3, 1.0, 0, 1, cubic_out); k2 = tw(lt, 1.4, 1.0, 0, 1, cubic_out)
    d.rectangle([xa, y - 30, xa + (xb - xa) * k1, y + 30], fill=RED, outline=BLK, width=4)
    d.rectangle([xb, y - 30, xb + (xc - xb) * k2, y + 30], fill=GREEN, outline=BLK, width=4)
    if k1 > .95: d.text(((xa + xb) / 2, y - 80), "+80 MILLONES", font=F(44), fill=RED, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    if k2 > .95: d.text(((xb + xc) / 2, y - 80), "66 MILLONES", font=F(44), fill=GREEN, anchor="mm", stroke_width=5, stroke_fill=WHITE)
    for x, lab in ((xa, "ESTEGO"), (xb, "T-REX"), (xc, "TÚ")): d.text((x if x > 150 else 160, y + 80), lab, font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    chip(d, "REGLA DEL TIEMPO", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def s_future(c):
    img = radial_bg(((0, (250, 220, 170)), (1, (200, 140, 90))), cy=800); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 1250, W, 1380], fill=(170, 130, 80))
    stego(d, 300, 1260 + shake(lt, 1.0, .5, 8) * 0, .7, c.t, mood="confused")
    guy(d, 820, 1270, .6, mood="happy", arms="up", t=c.t)
    a = anchors(820, 1270, .6); hx, hy = a["hand_r_up"]
    d.rounded_rectangle([hx - 40, hy - 130, hx + 40, hy + 8], 14, fill=(40, 40, 45), outline=BLK, width=4); d.rectangle([hx - 30, hy - 118, hx + 30, hy - 8], fill=(120, 190, 250))
    d.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], fill=SKIN, outline=BLK, width=2)
    if lt > .5: say(d, "¿¿Y eso??", mouth=(300 + .7 * 300, 1260 - .7 * 120), head=.7 * 70, size=int(54 * tw(lt, .5, .4, .4, 1, back_out)))
    chip(d, "EL FUTURO", CHIP1, bg=BLUE, appear=lt / .3)
    return img

def ending(c):
    img = space_bg(c.t, stops=((0, (60, 40, 110)), (.6, (25, 18, 60)), (1, (8, 6, 25)))); d = ImageDraw.Draw(img); lt = c.lt
    d = layer(img, lambda dd, cx, cy: pyramid(dd, cx, cy + 150, .5), 270, 950, 520, 1, 1)
    d = layer(img, lambda dd, cx, cy: cleopatra(dd, cx, cy + 230, .55, c.t, mood="happy", arms="up"), 760, 900 + yoyo(lt, 0, .7, 0, -12), 520)
    bigtext(d, "¿CUÁL TE ROMPIÓ", 540, 430, 76, fill=WHITE); bigtext(d, "LA CABEZA?", 540, 530, 76, fill=YEL)
    follow_btn(d, lt, y=1250, delay=c.dur * .5)
    return img

SCENES = [(0, s_hook), (1, s_age), (2, s_old), (3, s_family), (4, s_mammoth), (5, s_oxford), (6, s_tuition), (7, s_dinos), (8, s_ruler), (9, s_future), (10, ending)]
SFX = [(0, .2, "pop", {}), (0, .7, "pop", {}), (0, 1.2, "pop", {}), (0, 1.9, "whoosh", {}), (1, .6, "ding", {}), (2, .6, "boing", {}), (3, 2.5, "pop", {}),
       (4, .3, "thud", {}), (5, 2.0, "pop", {}), (6, .1, "buzzer", {}), (7, .3, "thud", {}), (8, .3, "whoosh", {}), (8, 1.4, "whoosh", {}), (9, .5, "boing", {}), (10, 2.0, "jingle", {})]
MUSIC = ("bass", [(7, 8)], 10)
