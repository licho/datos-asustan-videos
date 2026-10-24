"""Señales de que tu compañero de trabajo es un robot (serie 'Señales de que…')."""
import math
from lib.core import *
from lib.core import say
from lib.motion import tw, yoyo, layer, shake, back_out, cubic_out, radial_bg
from lib.personajes import guy, robo_cw, anchors
from lib.props import (alarm_clock, wall_clock, phone_chat, monitor, checklist, laptop, mug, captcha, curtain, ball_chain,
                       cardboard_box, chair, table, document)
from lib.fondos import oficina
from lib.efectos import tag
from lib.props import office_desk
def desk2(d, x0, x1, top=1000): office_desk(d, x0, x1, top)

NAME = "2026-12-03_robot-companero"
END = 4.5
LINES = [
 ("mischievously", "Tu compañero contesta correos a las tres de la mañana… con acentos.", "Tu compañero contesta correos *a las 3 a.m.*… *con acentos*"),
 ("serious", "Nadie normal pone acentos a esa hora. Es la señal uno de que es un robot. Revisa las demás… antes de que él te revise a ti.", "*Señal 1* de que es un robot. Revisa las demás… *antes de que él te revise a ti*"),
 ("sarcastic", "Señal dos: nunca va al baño, nunca come y nunca se queja del aire acondicionado. Eso es un electrodoméstico.", "*Señal 2:* no come, no va al baño, no se queja. *Es un electrodoméstico*"),
 ("mischievously", "Señal tres: su foto de perfil es un círculo gris. Y en cada videollamada… “se le traba la cámara”.", "*Señal 3:* foto de perfil gris… y *“se le traba la cámara”*"),
 ("confident", "Señal cuatro: a todo contesta “¡Con gusto!”. ¿Un reporte? “¡Con gusto!”. ¿Sin aguinaldo este año? “¡Con gusto!”.", "*Señal 4:* a todo dice *“¡Con gusto!”*… hasta sin aguinaldo"),
 ("mischievously", "Señal cinco: cuando sale a comer dice “Volveré”… y vuelve. Exactamente a las dos en punto. Ningún humano regresa a tiempo de comer.", "*Señal 5:* dice *“Volveré”*… y vuelve *a las 2:00 en punto*"),
 ("excited", "Señal seis: cuando la página le pregunta “¿Eres un robot?”… se tarda en contestar. Y elige mal los semáforos a propósito.", "*Señal 6:* tarda en contestar *“¿Eres un robot?”*… y falla a propósito"),
 ("whispers", "Dato real: la palabra “robot” se inventó en mil novecientos veinte, para una obra de teatro checa. Viene de “robota”, que significa trabajo forzado.", "Dato real: “robot” nació en *1920*, de *“robota”: trabajo forzado*"),
 ("dramatically", "O sea… desde el primer día, “robot” significó “el que trabaja a la fuerza”.", "Desde el primer día: *“el que trabaja a la fuerza”*"),
 ("sarcastic", "Y la mala noticia no es que sea un robot. Es que lo contrataron para hacer el trabajo de tres personas… y una de ellas eras tú.", "Lo contrataron para el trabajo de *tres personas*… *y una eras tú*"),
 ("sarcastic", "¿Qué otra señal agregarías? Te leo en los comentarios… y si no tienes trabajo mañana: hasta la vista, baby.", "¿Qué otra señal agregarías? *Hasta la vista, baby*"),
]
OFF = oficina()
OFF_N = oficina(night=True)
DESK_Y = 1000                    # superficie de los escritorios

# ------------------------------------------------------------------ escenas
def hook(c):
    img, d = canvas(OFF); lt = c.lt
    guy(d, 270, 1290, .78, mood="scared" if lt > 1.2 else "neutral", look=1, t=c.t)
    robo_cw(d, 800, 1290, .78, c.t, mood="smile", arms="down")
    desk2(d, 40, 520); desk2(d, 560, 1040)
    laptop(d, 430, DESK_Y, .6, back=False)
    laptop(d, 650, DESK_Y, .6, back=False)
    if lt > 2.2:
        a = anchors(800, 1290, .78); say(d, "¿Todo bien, compañero?", a["mouth"], head=a["head_r"], size=42, maxw=380, avoid=[anchors(270, 1290, .78)["box"]])
    chip(d, "¿ES UN ROBOT?", CHIP1, bg=RED, appear=lt / .3)
    return img

def mails(c):
    img, d = canvas(OFF_N); lt = c.lt; f = lt / c.dur
    wall_clock(d, 220, 640, 110, c.t, hour=3, minute=0)
    phone_chat(d, 470, 470, 520, 820, "BANDEJA DE ENTRADA", [("l", "Re: Re: Re: Reporte", "3:00"), ("l", "Listo. Revisé acentos.", "3:01"), ("l", "Y comas. Y tildes.", "3:01")], shown=1 + int(f * 3.5), size=30)
    robo_cw(d, 240, 1290, .7, c.t, mood="smile")
    if f > .55: d = tag(img, "SIN UN ERROR", 720, 1180, tw(lt, c.dur * .55, .4, 0, 1, back_out), bg=GREEN)
    chip(d, "SEÑAL #1", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def appliance(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    checklist(d, 60, 480, 600, "NUNCA:", ["Va al baño", "Come", "Se queja del clima"], done=int(f * 4.5), size=48)
    robo_cw(d, 830, 1290, .8, c.t, mood="smile")
    if f > .6: d = tag(img, "ELECTRODOMÉSTICO", 540, 1120, tw(lt, c.dur * .6, .4, 0, 1, back_out), bg=BLUE, size=50)
    chip(d, "SEÑAL #2", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def videocall(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    x0, y0, x1, y1 = 90, 470, 990, 1080
    d.rounded_rectangle([x0, y0, x1, y1], 24, fill=(35, 38, 48), outline=BLK, width=8)
    cw, ch = (x1 - x0 - 60) / 2, (y1 - y0 - 60) / 2
    hoods = [(240, 120, 40), (110, 150, 90), (90, 120, 200)]
    for k in range(4):
        cx0 = x0 + 20 + (k % 2) * (cw + 20); cy0 = y0 + 20 + (k // 2) * (ch + 20)
        d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], 14, fill=(70, 75, 90))
        if k < 3:
            from PIL import Image as _I, ImageDraw as _D
            tile = _I.new("RGB", (int(cw), int(ch)), (85, 92, 110)); td = _D.Draw(tile)
            guy(td, cw / 2, ch + 230 * .45, .45, mood="neutral", t=c.t + k, hoodie=hoods[k])
            mask = _I.new("L", tile.size, 0); _D.Draw(mask).rounded_rectangle([0, 0, tile.size[0] - 1, tile.size[1] - 1], 14, fill=255)
            img.paste(tile, (int(cx0), int(cy0)), mask); d = ImageDraw.Draw(img)
        else:
            d.ellipse([cx0 + cw / 2 - 70, cy0 + ch / 2 - 90, cx0 + cw / 2 + 70, cy0 + ch / 2 + 50], fill=(150, 150, 160), outline=BLK, width=4)
            dots = "." * (1 + int(c.t * 3) % 3)
            d.text((cx0 + cw / 2, cy0 + ch - 30), "Conectando" + dots, font=F(30), fill=WHITE, anchor="mm")
    if f > .55: d = tag(img, "“SE TRABÓ LA CÁMARA”", 540, 1190, tw(lt, c.dur * .55, .4, 0, 1, back_out), bg=GRAY, size=46)
    chip(d, "SEÑAL #3", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def con_gusto(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    guy(d, 260, 1290, .8, mood="scared" if f > .65 else "neutral", t=c.t)
    robo_cw(d, 800, 1290, .8, c.t, mood="smile")
    a, b = anchors(260, 1290, .8), anchors(800, 1290, .8)
    stage = min(2, int(f * 3))
    q = ("¿Un reporte?", "¿Horas extra?", "¿Sin aguinaldo?")[stage]
    say(d, q, a["mouth"], head=a["head_r"], size=44, maxw=380, avoid=[b["box"]])
    if (f * 3) % 1 > .35: say(d, "¡Con gusto!", b["mouth"], head=b["head_r"], size=48, maxw=380, avoid=[a["box"]])
    chip(d, "SEÑAL #4", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def volvere(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    d.rectangle([700, 560, 1000, 1250], fill=(150, 110, 75), outline=BLK, width=6); d.ellipse([720, 900, 745, 925], fill=(230, 200, 60))
    wall_clock(d, 300, 620, 120, c.t, hour=2, minute=0 if f > .45 else 59 - int((1 - f / .45) * 3))
    if f < .4:
        robo_cw(d, 820, 1290, .75, c.t, mood="smile", shades=True)
        a = anchors(820, 1290, .75); say(d, "Volveré.", a["mouth"], head=a["head_r"], size=50, side=-1)
    elif f > .5:
        x = tw(lt, c.dur * .5, .6, 1200, 820, back_out)
        robo_cw(d, x, 1290, .75, c.t, mood="smile", shades=True, arms="up" if f > .7 else "down")
        if f > .7: bigtext(d, "2:00:00", 300, 860, 70, fill=GREEN)
    chip(d, "SEÑAL #5", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def captcha_s(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    picks = tuple(k for k, tt in ((0, .35), (4, .5), (8, .65)) if f > tt)
    captcha(d, 60, 470, 640, picked=picks, checked=f > .8, size=34)
    robo_cw(d, 880, 1290, .6, c.t, mood="blank" if f < .8 else "wink", oil=True)
    chip(d, "SEÑAL #6", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def fact(c):
    img = radial_bg(((0, (70, 40, 50)), (1, (25, 15, 20))), cy=800); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    curtain(d, 90, 470, 990, 1100, open_=tw(lt, .3, 1.5, 0, 1, cubic_out))
    if f > .3:
        k = tw(lt, c.dur * .3, .5, 0, 1, back_out)
        d = layer(img, lambda dd, cx, cy: bigtext(dd, "ROBOTA", cx, cy, 120, fill=YEL), 540, 720, 900, k, k)
        if f > .5: bigtext(d, "= TRABAJO FORZADO", 540, 850, 56, fill=WHITE)
    if f > .7: chip(d, "TEATRO CHECO · 1920", 1180, bg=GRAY, size=44, appear=(f - .7) * c.dur / .3)
    chip(d, "DATO REAL", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def forced(c):
    img, d = canvas(OFF); lt = c.lt
    desk2(d, 200, 900)
    laptop(d, 640, DESK_Y, .8, back=True)
    robo_cw(d, 420, 1290, .75, c.t, mood="smile", arms="push")
    ball_chain(d, 420 - .75 * 50, 1290 - 10, 200, 1250, r=46)
    chip(d, "EL QUE TRABAJA A LA FUERZA", CHIP1, bg=RED, size=46, appear=lt / .3)
    return img

def replaced(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    for i, x in enumerate((200, 540, 880)):
        chair(d, x, 1290, 1.0, kind="oficina")
    robo_cw(d, 540, 1290, .75, c.t, mood="smile", arms="up" if f > .3 else "down")
    bigtext(d, "1 ROBOT = 3 PUESTOS", 540, 560, 64, fill=WHITE)
    if f > .55:
        k = tw(lt, c.dur * .55, .5, 0, 1, back_out)
        d = layer(img, lambda dd, cx, cy: cardboard_box(dd, cx, cy + 200, .8), 880, 1290 - 200, 600, k, k)
    chip(d, "LA MALA NOTICIA", CHIP1, bg=RED, appear=lt / .3)
    return img

def ending(c):
    img, d = canvas(OFF); lt = c.lt; f = lt / c.dur
    robo_cw(d, 760, 1290, .8, c.t, mood="wink" if f > .5 else "smile", shades=f < .5)
    x = tw(lt, c.dur * .3, 1.4, 260, -250, cubic_out)
    guy(d, x, 1290, .7, mood="scared", t=c.t)
    a = anchors(x, 1290, .7); cardboard_box(d, a["hand_r_down"][0] + 10, a["hand_r_down"][1] + 120, .65, label="")
    bigtext(d, "¿QUÉ OTRA", 540, 500, 84, fill=WHITE); bigtext(d, "SEÑAL?", 540, 630, 84, fill=YEL)
    follow_btn(d, lt, y=1240, delay=c.dur * .55)
    return img

SCENES = [(0, mails), (1, hook), (2, appliance), (3, videocall), (4, con_gusto), (5, volvere), (6, captcha_s), (7, fact), (8, forced), (9, replaced), (10, ending)]
SFX = [(0, .2, "pop", {}), (0, 2.2, "boing", {}), (1, .5, "ding", {}), (2, .8, "pop", {}), (2, 3.2, "thud", {}), (3, 2.5, "buzzer", {}),
       (4, 1.0, "pop", {}), (4, 3.0, "pop", {}), (5, 2.0, "whoosh", {}), (5, 3.6, "ding", {}), (6, 1.5, "pop", {}), (6, 3.8, "ding", {}),
       (7, .3, "whoosh", {}), (8, .4, "thud", {}), (9, 2.0, "sadtrom", {}), (10, 2.0, "jingle", {})]
MUSIC = ("chiptune", [(7, 8)], 10)
