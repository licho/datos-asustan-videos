"""Guía laboral Ep. 7: el duende de Santa (lo despidieron)."""
import math, random
from lib.core import *
from lib.core import say
from lib.motion import tw, yoyo, layer, shake, back_out, cubic_out, radial_bg
from lib.personajes import guy, elf, anchors
from lib.props import (document, open_box, box_lid, bookshelf_crooked, screw, scroll, sausages, cardboard_box, phone_chat,
                       snowflake, gift, tree)
from lib.fondos import oficina

NAME = "2026-12-15_duende-trabajos"
END = 4.5
LINES = [
 ("mischievously", "Guía laboral para monstruos, episodio siete: el duende de Santa.", "Guía laboral para monstruos, *episodio 7: el duende de Santa*"),
 ("sarcastic", "Su currículum: trescientos años armando juguetes en el Polo Norte… sin aguinaldo y sin calefacción. Motivo de salida: lo despidieron.", "*300 años* armando juguetes… *sin aguinaldo*. Motivo de salida: *despedido*"),
 ("dramatically", "¿Por qué? Se quedó dormido dentro de una caja, lo envolvieron… y lo entregaron. Un niño pidió una bicicleta y le llegó un duende con resaca.", "Se durmió en una caja… *y lo entregaron*. Pidió bici… *le llegó un duende con resaca*"),
 ("confident", "Trabajo número uno: repartidor de paquetería. Entrega en todo el mundo en una sola noche… pero el resto del año, tu paquete “va en camino” tres semanas.", "*Trabajo #1:* repartidor. Una noche para el mundo… *tres semanas para tu paquete*"),
 ("serious", "Trabajo número dos: armador de muebles. Arma lo que sea sin instructivo… y siempre le sobran tres tornillos. Igual que a ti.", "*Trabajo #2:* armador de muebles. *Siempre le sobran tres tornillos*"),
 ("mischievously", "Trabajo número tres: Recursos Humanos. Tiene trescientos años de experiencia haciendo listas de quién se portó mal… ahora decide quién no regresa el lunes.", "*Trabajo #3:* Recursos Humanos. La lista de quién se portó mal… *ahora es de despidos*"),
 ("whispers", "Dato real: en Islandia no hay un duende navideño… hay trece. Y son de cuidado: uno roba salchichas, otro lame cucharas y otro azota puertas en la madrugada.", "Dato real: en Islandia *hay 13 duendes*: uno roba salchichas, otro lame cucharas…"),
 ("dramatically", "El verdadero problema no es el despido. Es que trabajó trescientos años para el mismo jefe…", "El verdadero problema: *300 años con el mismo jefe*…"),
 ("sarcastic", "…y su liquidación fue un suéter navideño. Que pica.", "…y su liquidación fue *un suéter navideño. Que pica.*"),
 ("", "¿Qué otro monstruo quieres que busque trabajo? Te leo en los comentarios.", "¿Qué otro monstruo quieres que *busque trabajo*?"),
]
NIGHT = ((0, (40, 55, 110)), (.6, (20, 28, 65)), (1, (8, 10, 30)))
SNOWY = ((0, (230, 240, 252)), (1, (180, 200, 228)))

def snow_fall(d, t, n=16, seed=5, col=WHITE):
    r = random.Random(seed)
    for k in range(n):
        x0, sp, sz = r.uniform(0, W), r.uniform(60, 130), r.uniform(12, 22)
        y = 480 + (t * sp + r.uniform(0, 800)) % 820; x = x0 + math.sin(t * 2 + k) * 25
        snowflake(d, x, y, sz, col=col, width=4)

def tag(img, text, x, y, k, rot=-10, bg=RED, size=56):
    def fn(dd, cx, cy):
        f = F(size); w = dd.textlength(text, font=f) + 70
        dd.rounded_rectangle([cx - w / 2, cy - size * .8, cx + w / 2, cy + size * .8], 30, fill=bg, outline=BLK, width=6)
        dd.text((cx, cy), text, font=f, fill=WHITE, anchor="mm")
    return layer(img, fn, x, y, 1000, sx=k, sy=k, rot=rot)

def room(night=False):
    img = radial_bg(((0, (250, 225, 200)), (1, (215, 170, 140))) if not night else NIGHT, cy=800); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, W, 1380], fill=(150, 100, 70)); d.line([(0, 1250), (W, 1250)], fill=(110, 70, 45), width=6)
    return img, d

def xmas_tree(d, x, y, s, t):
    tree(d, x, y, s, kind="pine", col=(50, 140, 80))
    for k, (dx, dy, c) in enumerate(((-60, -200, RED), (50, -260, YEL), (-30, -340, (80, 140, 240)), (70, -150, (240, 140, 40)), (0, -430, RED))):
        on = (int(t * 3) + k) % 3 != 0
        d.ellipse([x + dx * s - 14, y + dy * s - 14, x + dx * s + 14, y + dy * s + 14], fill=c if on else dk(c, .5), outline=BLK, width=3)

# ------------------------------------------------------------------ escenas
def intro(c):
    img = radial_bg(NIGHT, cy=800); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 1250, W, 1380], fill=(235, 242, 252)); snow_fall(d, c.t)
    bx, by, s = 540, 1270, 1.2
    open_box(d, bx, by, s, front=False)
    if lt > .4:
        pop_y = tw(lt, .4, .7, by - 10, by - 150, back_out)
        elf(d, bx, pop_y, .9, c.t, mood="happy", arms="up" if lt > 1.0 else "down")
    open_box(d, bx, by, s)
    k = tw(lt, .35, .9, 0, 1, cubic_out)
    box_lid(d, bx + k * 300, by - 250 * s - k * 320 + k * k * 260, s, ang=-k * 40)
    if lt > .8: bigtext(d, "EL DUENDE DE SANTA", 540, 520, 76, fill=WHITE)
    chip(d, "GUÍA LABORAL · EP. 7", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def cv(c):
    img, d = canvas(((40, 60, 90), (70, 80, 110))); lt = c.lt; f = lt / c.dur
    document(d, 80, 460, 640, 760, "CURRÍCULUM", ["Experiencia: 300 años", "Lugar: Polo Norte", "Aguinaldo: no", "Calefacción: no", "", "Motivo de salida:" if f > .55 else ""], size=34)
    elf(d, 870, 1290, .8, c.t, mood="sad" if f > .55 else "happy")
    if f > .62: d = tag(img, "DESPEDIDO", 360, 1060, tw(lt, c.dur * .62, .4, 0, 1, back_out), rot=-12)
    chip(d, "CURRÍCULUM", CHIP1, bg=GRAY, appear=lt / .3)
    return img

def fired(c):
    img, d = room(); lt = c.lt; f = lt / c.dur
    xmas_tree(d, 170, 1250, 1.1, c.t)
    bx, by = 560, 1265
    open_box(d, bx, by, 1.0, col=(60, 120, 200), front=False)
    if f > .25: elf(d, bx, tw(lt, c.dur * .25, .6, by + 100, by - 110, back_out), .75, c.t, mood="sleepy", arms="scratch" if f > .5 else "down")
    open_box(d, bx, by, 1.0, col=(60, 120, 200))
    if f < .25: box_lid(d, bx, by - 210, 1.0, col=(60, 120, 200))
    else: box_lid(d, bx - 260, by - 20, 1.0, col=(60, 120, 200), ang=10)
    gx = 880; guy(d, gx, 1290, .55, mood="scared" if f > .45 else "neutral", look=-1, t=c.t, hoodie=(90, 160, 220))
    if f > .55: a = anchors(gx, 1290, .55); say(d, "¿Y mi bici?", a["mouth"], head=a["head_r"], size=46, maxw=320, avoid=[(400, 700, 720, 1290)])
    chip(d, "¿POR QUÉ LO CORRIERON?", CHIP1, bg=RED, appear=lt / .3)
    return img

def courier(c):
    img, d = canvas(((235, 225, 210), (210, 195, 175))); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(160, 150, 140))
    elf(d, 280, 1290, .8, c.t, mood="happy", arms="hold")
    cardboard_box(d, 280, 1290 - 150, .55, label="FRÁGIL", items=False)
    phone_chat(d, 520, 470, 500, 760, "RASTREO DE PAQUETE", [("l", "24 dic: entregado ✓", ""), ("l", "Tu pedido: va en camino", "día 1"), ("l", "Va en camino…", "día 12"), ("l", "Va en camino……", "día 21")],
               shown=1 + int(f * 4.2), size=28)
    chip(d, "TRABAJO #1: REPARTIDOR", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def furniture(c):
    img, d = canvas(((240, 232, 220), (215, 205, 190))); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(170, 140, 110))
    bookshelf_crooked(d, 330, 1290, 1.0, lean=6 + 2 * math.sin(c.t * 2))
    elf(d, 780, 1290, .8, c.t, mood="happy" if f < .5 else "sly", arms="point" if f < .5 else "down", flip=True)
    if f > .45:
        for k, (x, a) in enumerate(((600, 20), (680, -30), (930, 60))):
            if f > .45 + k * .1: screw(d, x, 1280, 1.4, a)
    if f > .75: d = tag(img, "SOBRARON 3", 540, 560, tw(lt, c.dur * .75, .4, 0, 1, back_out), bg=ORANGE)
    chip(d, "TRABAJO #2: ARMADOR", CHIP1, bg=ORANGE, appear=lt / .3)
    return img

def hr(c):
    img, d = canvas(oficina()); lt = c.lt; f = lt / c.dur
    scroll(d, 90, 470, 460, 760, "SE PORTÓ MAL", ["· Pedro", "· Ana", "· Toño", "· Tú" if f > .5 else ""], size=40, fine="(lista de despidos)" if f > .6 else None)
    elf(d, 800, 1290, .85, c.t, mood="sly", arms="point", flip=True)
    chip(d, "TRABAJO #3: RECURSOS HUMANOS", CHIP1, bg=PURPLE, size=46, appear=lt / .3)
    return img

def iceland(c):
    img = radial_bg(((0, (60, 70, 120)), (1, (20, 22, 50))), cy=760); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(110, 80, 60))
    d.rectangle([820, 640, 1040, 1250], fill=(120, 80, 50), outline=BLK, width=6); d.ellipse([845, 940, 870, 965], fill=YEL)
    elf(d, 180, 1290, .75, c.t, mood="sly", arms="up", col=(130, 100, 80), hat=(150, 60, 50))
    sausages(d, 180 + .75 * 130, 1290 - .75 * 420, 330, 1240, n=5)
    elf(d, 480, 1290, .75, c.t + 1, mood="happy", arms="hold", col=(110, 110, 120), hat=(90, 90, 100))
    a = (480 - .75 * 55, 1290 - .75 * 200)
    d.line([(a[0], a[1]), (a[0] + 10, a[1] - 110)], fill=(170, 130, 80), width=10); d.ellipse([a[0] - 12, a[1] - 150, a[0] + 32, a[1] - 100], fill=(190, 150, 100), outline=BLK, width=3)
    door_k = abs(math.sin(c.t * 4)) if f > .5 else 0
    d.polygon([(820, 640), (820 + 200 * (1 - door_k * .6), 660), (820 + 200 * (1 - door_k * .6), 1230), (820, 1250)], fill=(150, 100, 60), outline=BLK)
    elf(d, 740, 1290, .75, c.t + 2, mood="sly", arms="point", col=(90, 120, 90), hat=(60, 80, 140))
    if f > .35: chip(d, "ISLANDIA: 13 DUENDES", CHIP2 + 380, bg=GRAY, size=48, appear=(f - .35) * c.dur / .3)
    chip(d, "DATO REAL", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def problem(c):
    img, d = canvas(oficina()); lt = c.lt
    elf(d, 540, 1290, .85, c.t, mood="sad")
    bigtext(d, "300 AÑOS", 540, 560, 96, fill=YEL); bigtext(d, "MISMO JEFE", 540, 670, 60, fill=WHITE)
    chip(d, "EL VERDADERO PROBLEMA", CHIP1, bg=RED, appear=lt / .3)
    return img

def sweater(c):
    img, d = canvas(oficina()); lt = c.lt
    elf(d, 540 + shake(lt, .3, 99, 8, 30), 1290, .9, c.t, mood="sad", arms="scratch", sweater=True)
    bigtext(d, "LIQUIDACIÓN:", 540, 540, 70, fill=WHITE); bigtext(d, "1 SUÉTER", 540, 640, 84, fill=YEL)
    chip(d, "QUE PICA", CHIP1, bg=RED, appear=lt / .3)
    return img

def ending(c):
    img = radial_bg(NIGHT, cy=800); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 1250, W, 1380], fill=(235, 242, 252)); snow_fall(d, c.t, n=10)
    elf(d, 540, 1290, .85, c.t, mood="happy", arms="up")
    bigtext(d, "¿QUÉ OTRO", 540, 470, 86, fill=WHITE); bigtext(d, "MONSTRUO?", 540, 590, 86, fill=YEL)
    follow_btn(d, lt, y=1240, delay=c.dur * .5)
    return img

SCENES = [(0, intro), (1, cv), (2, fired), (3, courier), (4, furniture), (5, hr), (6, iceland), (7, problem), (8, sweater), (9, ending)]
SFX = [(0, .4, "boing", {}), (0, 1.0, "jingle", {}), (1, 3.0, "thud", {}), (2, 1.2, "pop", {}), (2, 3.5, "boing", {}), (3, .8, "ding", {}),
       (4, 2.5, "pop", {}), (4, 3.6, "buzzer", {}), (5, 2.0, "pop", {}), (6, .3, "whoosh", {}), (7, 0, "sting", {}), (8, .3, "sadtrom", {}), (9, 2.0, "jingle", {})]
MUSIC = ("waltz", [(6, 7)], 9)
