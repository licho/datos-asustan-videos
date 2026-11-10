"""Cómo saber si tu crush es un espía (~63 s). Gancho: hay espías entrenados para enamorarte (y dejan 5 señales).
Guiños sutiles a la noticia del director de una empresa de chips (sin nombres ni marcas; la cita es un personaje genérico)."""
import math
from PIL import Image, ImageDraw
from lib.core import *
from lib.motion import tw, yoyo, cubic_out, back_out, radial_bg
from lib.personajes import guy, anchors, spy_date, mom_chancla, scammer, songbird, heart_face
from lib.props import table, candle, honey_jar, chips_bag, gpu_card, detective_board, phone_chat, ticket, document, door, padlock
from lib.efectos import tag, rubber_stamp

NAME = "2026-11-10_crush-espia"
END = 3.0
LINES = [
 ("dramatically", "Hay espías entrenados para enamorarte… y dejan cinco señales.", "Hay espías *entrenados para enamorarte*… y dejan *5 señales*"),
 ("serious", "Se llama trampa de miel. En la Guerra Fría, a ellas les decían “gorriones”… y a ellos, “cuervos”.", "Se llama *trampa de miel*. A ellas les decían *“gorriones”*… y a ellos, *“cuervos”*"),
 ("sarcastic", "Señal uno: le interesa más tu empresa de chips que tu signo. Y no, no habla de las papitas.", "*Señal 1:* le interesa más tu *empresa de chips* que tu signo. *Y no, no son papitas*"),
 ("mischievously", "Señal dos: es demasiado perfecto. Le gusta todo lo que te gusta… como si hubiera estudiado tu perfil.", "*Señal 2:* es *demasiado perfecto*… como si hubiera *estudiado tu perfil*"),
 ("serious", "Porque lo estudió: una agencia de inteligencia detectó más de diez mil acercamientos de espías disfrazados en redes de trabajo.", "Porque lo estudió: *más de 10 mil acercamientos* de espías disfrazados en redes"),
 ("sarcastic", "Señal tres: paga la cena, el taxi y te invita un viaje con todo pagado. En México eso no es amor… es sospechoso.", "*Señal 3:* paga todo y te invita un viaje. Eso no es amor… *es sospechoso*"),
 ("mischievously", "Señal cuatro: primero te pide la clave del wifi… luego la de tu correo… luego la de tu trabajo.", "*Señal 4:* la clave del *wifi*… luego del *correo*… luego *la del trabajo*"),
 ("dramatically", "Y la última es la peor. Señal cinco: no quiere conocer a tu mamá. O es espía… o es casado.", "*Señal 5:* no quiere conocer a tu mamá. *O es espía… o es casado*"),
 ("sarcastic", "La buena noticia: si no eres dueño de la empresa más valiosa del mundo, ningún gobierno va a gastar un espía en ti.", "Si no eres dueño de *la empresa más valiosa del mundo*… *nadie gasta un espía en ti*"),
 ("whispers", "La mala: es más probable que sea un estafador.", "La mala: *es más probable que sea un estafador*"),
 ("", "¿Cuál de estas señales te ha tocado? Te leo.", "¿Cuál de estas señales te ha tocado? *Te leo*"),
]
WALL = ((0, (120, 50, 60)), (1, (55, 20, 35)))
CHIP = "¿AMOR O ESPIONAJE?"

def restaurant(c):
    """Cena romántica: pared vino, piso, mesa con mantel y vela."""
    img = radial_bg(WALL, cy=700); d = ImageDraw.Draw(img)
    d.rectangle([0, 1290, W, 1380], fill=(90, 55, 45)); d.line([(0, 1290), (W, 1290)], fill=BLK, width=4)
    for k in range(3): d.rounded_rectangle([140 + k * 300, 560, 300 + k * 300, 760], 18, fill=(150, 70, 80), outline=(90, 30, 45), width=4)
    return img, d

def date_scene(d, c, lover_mood="relief", spy_mood="neutral", spy_x=830, notes=True):
    """Pareja en la mesa: el enamorado a la izquierda, la cita espía a la derecha."""
    guy(d, 240, 1290, .95, mood=lover_mood, t=c.t)
    spy_date(d, spy_x, 1290, .95, mood=spy_mood, t=c.t)
    table(d, 535, 1300, .85, w=560, cloth=(240, 235, 225))
    candle(d, 535, 1300 - 330 * .85, .9, c.t)
    if notes:                                                # libreta escondida bajo la mesa
        a = anchors(spy_x, 1290, .95); hx, hy = a["hand_l_down"]
        d.rectangle([hx - 50, hy - 20, hx + 20, hy + 60], fill=(250, 245, 220), outline=BLK, width=3)
        for k in range(3): d.line([(hx - 40, hy - 5 + k * 18), (hx + 10, hy - 5 + k * 18)], fill=(80, 80, 90), width=3)

def chips2(d, k, n, appear):
    chip(d, f"SEÑAL {k}/5", CHIP2, bg=RED, appear=appear)

# ------------------------------------------------------------------ escenas
def hook(c):
    img, d = restaurant(c)
    date_scene(d, c)
    heart_face(d, 240, 520, .8, c.t)
    chip(d, CHIP, CHIP1, bg=PURPLE)
    if c.lt / c.dur > .55: chip(d, "5 SEÑALES", CHIP2, bg=RED, appear=(c.lt - .55 * c.dur) / .3)
    return img

def honey(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (255, 235, 180)), (1, (230, 170, 80))), cy=900); d = ImageDraw.Draw(img)
    honey_jar(d, 540, 1290, 1.1)
    if f > .35:
        k = cubic_out(cl((f - .35) / .3))
        songbird(d, lerp(-150, 270, k), 640, .9, c.t, shades_on=True)
        songbird(d, lerp(1230, 810, k), 640, .9, c.t + .3, col=(35, 35, 45), belly=(70, 70, 80), shades_on=True, flip=True)
        if k > .95:
            bigtext(d, "GORRIONES", 270, 790, 46, fill=YEL); bigtext(d, "CUERVOS", 810, 790, 46, fill=YEL)
    chip(d, "TRAMPA DE MIEL", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def sign1(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    date_scene(d, c, lover_mood="neutral")
    a = anchors(830, 1290, .95)
    say(d, "¿Y a cuántos chips tienes acceso?", a["mouth"], a["head_r"], avoid=[(0, 1250, W, 1400)])
    if f > .5:
        chips_bag(d, 440, 1018, .45); gpu_card(d, 640, 975, .42)
        tag(img, "CHIPS ≠ PAPITAS", 540, 1200, cl((f - .5) / .1), rot=-5, bg=PURPLE, size=50); d = ImageDraw.Draw(img)
    chip(d, CHIP, CHIP1, bg=PURPLE); chips2(d, 1, 5, c.lt / .3)
    return img

def sign2(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    detective_board(d, 540, 640, 620, 340, c.t, label="TU PERFIL")
    spy_date(d, 880, 1290, .85, t=c.t)
    guy(d, 200, 1290, .85, mood="relief" if f < .6 else "scared", t=c.t)
    if f > .6: tag(img, "LO ESTUDIÓ", 540, 1000, cl((f - .6) / .1), rot=-6, bg=RED, size=56); d = ImageDraw.Draw(img)
    chip(d, CHIP, CHIP1, bg=PURPLE); chips2(d, 2, 5, c.lt / .3)
    return img

def proof(c):
    f = c.lt / c.dur
    img = radial_bg(((0, (60, 70, 110)), (1, (25, 30, 55))), cy=900); d = ImageDraw.Draw(img)
    msgs = [("l", "¡Hola! Vi tu perfil", "9:01"), ("l", "Tengo una oferta increíble", "9:02"), ("l", "¿En qué proyectos trabajas?", "9:02"), ("l", "Te invito a un viaje", "9:03")]
    phone_chat(d, 200, 480, 680, 660, "Perfil perfecto ✔", msgs, shown=min(4, 1 + int(f * 5)), size=36)
    n = int(lerp(0, 10000, cubic_out(cl(f / .7))))
    bigtext(d, f"+{n:,}", 540, 1250, 110, fill=YEL)
    chip(d, "ACERCAMIENTOS DE ESPÍAS", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def sign3(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    date_scene(d, c, lover_mood="relief" if f < .55 else "scared", notes=False)
    document(d, 230, 490, 270, 190, title="CUENTA", lines=("Cena: PAGADO", "Taxi: PAGADO"), size=28, stamp=None)
    document(d, 580, 490, 270, 190, title="VUELO", lines=("Todo pagado", "Ida y vuelta"), size=28, stamp=None)
    if f > .55: rubber_stamp(img, "SOSPECHOSO", 540, 600, cl((f - .55) / .1), col=RED, size=70, rot=-8); d = ImageDraw.Draw(img)
    chip(d, CHIP, CHIP1, bg=PURPLE); chips2(d, 3, 5, c.lt / .3)
    return img

def sign4(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    date_scene(d, c, lover_mood="neutral")
    asks = ["CLAVE DEL WIFI", "CLAVE DEL CORREO", "CLAVE DEL TRABAJO"]
    for i, s in enumerate(asks):
        if f > .1 + i * .28:
            k = cl((f - .1 - i * .28) / .1)
            bigtext(d, s, 540, 520 + i * 105, int(56 + 12 * i * k), fill=YEL if i < 2 else RED)
    chip(d, CHIP, CHIP1, bg=PURPLE); chips2(d, 4, 5, c.lt / .3)
    return img

def sign5(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    door(d, 60, 640, 360, 1290, opened=1.0 if f > .3 else 0.0, inside=(250, 230, 180))
    if f > .3: mom_chancla(d, 210, 1290, .8, mood="neutral", arms="up", t=c.t)
    k = cubic_out(cl((f - .45) / .35))
    spy_date(d, lerp(780, 1300, k), 1290, .9, mood="scared" if f > .4 else "neutral", t=c.t * (1 + 2 * k))
    if f > .62: tag(img, "O ES ESPÍA… O ES CASADO", 600, 600, cl((f - .62) / .1), rot=-5, bg=RED, size=48); d = ImageDraw.Draw(img)
    chip(d, CHIP, CHIP1, bg=PURPLE); chips2(d, 5, 5, c.lt / .3)
    return img

def relief(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    date_scene(d, c, lover_mood="relief", notes=False)
    bigtext(d, "¿LA EMPRESA MÁS VALIOSA?", 540, 520, 58, fill=WHITE)
    if f > .45: bigtext(d, "TÚ: PURA QUINCENA", 540, 610, 62, fill=YEL)
    chip(d, "LA BUENA NOTICIA", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def reveal(c):
    f = c.lt / c.dur
    img, d = restaurant(c)
    guy(d, 240, 1290, .95, mood="scared" if f > .4 else "neutral", t=c.t)
    if f < .4: spy_date(d, 830, 1290, .95, t=c.t)
    else: scammer(d, 830, 1290, .95, mood="relief", t=c.t)
    table(d, 535, 1300, .85, w=560, cloth=(240, 235, 225))
    if f > .5: rubber_stamp(img, "ESTAFA", 540, 560, cl((f - .5) / .1), col=RED, size=80, rot=-10); d = ImageDraw.Draw(img)
    chip(d, "LA MALA", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def ending(c):
    img, d = restaurant(c)
    date_scene(d, c, notes=False)
    chip(d, "¿CUÁL TE HA TOCADO?", CHIP1, bg=PURPLE, appear=c.lt / .3)
    if c.lt > 1.0: chip(d, "TE LEO EN COMENTARIOS", CHIP2, bg=RED, appear=(c.lt - 1.0) / .3)
    return img

SCENES = [(0, hook), (1, honey), (2, sign1), (3, sign2), (4, proof), (5, sign3), (6, sign4), (7, sign5), (8, relief), (9, reveal), (10, ending)]
SFX = [(0, .1, "sting", {}), (1, .3, "whoosh", {}), (2, .3, "pop", {}), (3, .3, "pop", {}), (4, .5, "ding", {}), (5, .3, "pop", {}), (5, 3.5, "buzzer", {}),
       (6, .3, "pop", {}), (7, .3, "pop", {}), (7, 1.5, "thud", {}), (7, 2.5, "skid", {}), (8, .3, "ding", {}), (9, 1.0, "sadtrom", {}), (10, .2, "pop", {})]
MUSIC = ("bass", [(9, 10)], 10)
