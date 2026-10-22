"""Los ejércitos más grandes de la historia (y el verdadero ganador: las hormigas). Sin armas en pantalla."""
import math
from lib.core import *
from lib.core import say
from lib.motion import power_in, tw, yoyo, layer, glow, shake, back_out, elastic_out, cubic_out, bounce_out, radial_bg, linear
from lib.personajes import guy, soldier, napoleon, scribe, emu, army_ant, ant_column, rat, rat_skeleton, anchors, medal
from lib.props import document, outhouse, white_flag, helmet, tortillas, bar_chart, blob_map, arrow, snowflake, phone_chat, sign_board

NAME = "2026-12_ejercitos"
END = 4.5
LINES = [
 ("mischievously", "¿Cuál ha sido el ejército más grande? Spoiler: no usa uniforme… ni pide permiso para ir al baño.", "¿El ejército *más grande*? Spoiler: *no usa uniforme*… *ni pide permiso*"),
 ("serious", "Un historiador griego juró que el persa Jerjes invadió Grecia con más de cinco millones de personas.", "Un historiador griego juró que Jerjes invadió Grecia con *más de 5 millones*"),
 ("sarcastic", "Hoy se calcula que eran trescientos mil, cuando mucho. Redondeó como tu tío cuando cuenta cuánto pescó.", "Hoy se calcula: *unos 300 mil*, cuando mucho. Redondeó como *tu tío pescando*"),
 ("", "Napoleón entró a Rusia con cuatrocientos cincuenta mil soldados. Regresaron unos ciento veinte mil.", "Napoleón entró a Rusia con *450 mil*. Regresaron *unos 120 mil*"),
 ("mischievously", "Casi la mitad de los que faltaron cayó por tifo y diarrea. Invicto en media Europa… y lo derrotó el baño.", "Casi la mitad cayó por *tifo y diarrea*. Invicto en media Europa… *lo derrotó el baño*"),
 ("dramatically", "Alemania mandó más de tres punto ocho millones de soldados contra la Unión Soviética. Le fue igual que a Napoleón.", "1941: *+3.8 millones* contra la Unión Soviética. *Le fue igual que a Napoleón*"),
 ("", "Por el Ejército Rojo pasaron unos treinta y cuatro millones. Eso no es un ejército, es un país con casco.", "Por el Ejército Rojo pasaron *34 millones*. Eso es *un país con casco*"),
 ("sarcastic", "Hoy el más grande es el de China: unos dos millones. Imagínate la fila de la tortillería.", "Hoy: China, *unos 2 millones*. Imagínate *la fila de las tortillas*"),
 ("", "Australia mandó al ejército contra veinte mil emús.", "1932: Australia mandó al ejército contra *20 mil emús*"),
 ("sarcastic", "En dos meses cayeron menos de mil… y se retiraron. Perdieron contra pollos gigantes.", "En dos meses cayeron *menos de mil*… y se retiraron. *Perdieron contra pollos gigantes*"),
 ("whispers", "El verdadero ganador: una sola colonia de hormigas guerreras africanas puede tener más de veinte millones de soldados.", "Una sola colonia de hormigas guerreras: *más de 20 millones*"),
 ("mischievously", "Si un animal pequeño no puede escapar, lo dejan en los huesos. Sin sueldo, sin vacaciones… y sin quejarse en el grupo.", "Lo dejan *en los huesos*. Sin sueldo, sin vacaciones… *y sin quejarse en el grupo*"),
 ("", "¿Qué da más miedo: Napoleón con diarrea o veinte millones de hormigas? Te leo.", "¿Napoleón con diarrea o *20 millones de hormigas*? *Te leo*"),
]
NIGHT = ((0, (70, 50, 120)), (.6, (30, 22, 70)), (1, (12, 10, 35)))
DESERT = ((0, (255, 225, 160)), (.6, (235, 175, 100)), (1, (180, 110, 70)))
SNOW = ((0, (235, 245, 255)), (.6, (190, 215, 240)), (1, (130, 160, 200)))
OUTBACK = ((0, (255, 210, 150)), (.6, (230, 140, 70)), (1, (160, 70, 40)))
DAY = ((0, (210, 235, 255)), (.6, (150, 195, 240)), (1, (90, 130, 190)))
SOIL = ((0, (215, 190, 140)), (.6, (170, 130, 85)), (1, (110, 75, 45)))

def ground(d, col, y=1290):
    d.rectangle([0, y, W, 1380], fill=col); d.line([(0, y), (W, y)], fill=dk(col, .75), width=6)

def snow_fall(d, t, n=18, seed=5):
    import random; r = random.Random(seed)
    for k in range(n):
        x0, sp, sz = r.uniform(0, W), r.uniform(60, 140), r.uniform(14, 26)
        y = 480 + (t * sp + r.uniform(0, 800)) % 820; x = x0 + math.sin(t * 2 + k) * 25
        snowflake(d, x, y, sz, col=WHITE, width=4)

def rubber_stamp(img, text, x, y, k, col=RED, size=78):
    def fn(dd, cx, cy):
        f = F(size); w = dd.textlength(text, font=f) + 60
        dd.rounded_rectangle([cx - w / 2, cy - size * .85, cx + w / 2, cy + size * .85], 18, outline=col, width=12)
        dd.text((cx, cy), text, font=f, fill=col, anchor="mm")
    return layer(img, fn, x, y, 1000, sx=k, sy=k, rot=-10)

def fish(d, x, y, s=1.0):
    S = lambda v: v * s
    d.polygon([(x - S(90), y), (x - S(140), y - S(40)), (x - S(140), y + S(40))], fill=(120, 180, 220), outline=BLK)
    d.ellipse([x - S(110), y - S(45), x + S(70), y + S(45)], fill=(120, 180, 220), outline=BLK, width=4)
    d.ellipse([x + S(25), y - S(18), x + S(45), y + 2], fill=BLK)

# ------------------------------------------------------------------ escenas
def s_hook(c):
    img = radial_bg(NIGHT, cy=800); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (90, 80, 110))
    for i in range(4):
        x = 150 + i * 250 + lt * 25; up = i == 2 and lt > 1.0
        soldier(d, x, 1285 + yoyo(lt + i * .3, 0, .5, 0, -10), .68, c.t, era="modern", arms="up" if up else "down", mood="neutral")
    if lt > 1.0:
        a = anchors(150 + 2 * 250 + lt * 25, 1285, .68); say(d, "¿Puedo ir al baño?", a["mouth"], head=a["head_r"], size=44, maxw=420, avoid=[anchors(150 + i * 250 + lt * 25, 1285, .68)["box"] for i in (0, 1, 3)])
    if lt > 2.2:
        army_ant(d, tw(lt, 2.2, 2.5, -200, 520), 1308, 1.0, c.t, helmet=True)
    chip(d, "¿EL MÁS GRANDE?", CHIP1, bg=RED, appear=lt / .3)
    return img

def s_xerxes(c):
    img = radial_bg(DESERT, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (225, 185, 120))
    for i in range(6): soldier(d, 520 + i * 95, 1180, .28, c.t, era="persian")
    scribe(d, 250, 1290, .62, c.t, mood="happy", arms="push")
    document(d, 330, 1000, 180, 230, title="HISTORIAS", lines=("Jerjes trajo", "5,283,220", "personas"), size=22)
    n = int(tw(lt, .4, 2.2, 0, 5283220, cubic_out))
    bigtext(d, f"{n:,}", 540, 600, 120, fill=WHITE); bigtext(d, "PERSONAS (SEGÚN HERÓDOTO)", 540, 720, 44, fill=YEL)
    chip(d, "PERSIA · 480 a.C.", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def s_real(c):
    img = radial_bg(DESERT, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (225, 185, 120))
    drop = tw(lt, .1, .8, 0, 1, power_in)
    if drop < 1:
        txt = "5,283,220"; f = F(120); x0 = 540 - d.textlength(txt, font=f) / 2
        if drop < .08: d.text((540, 600), txt, font=f, fill=WHITE, anchor="mm", stroke_width=12, stroke_fill=BLK)
        else:
          for i, ch in enumerate(txt):
            x = x0 + d.textlength(txt[:i], font=f) + (i - 4) * 28 * min(1, drop * 8); y = 600 + drop * (700 + i * 60) + i * 30 * min(1, drop * 8)
            if y < 1250: d.text((x, y), ch, font=f, fill=WHITE, anchor="lm", stroke_width=12, stroke_fill=BLK)
    k = tw(lt, 1.0, .5, 0, 1, back_out)
    if k > 0:
        d = layer(img, lambda dd, cx, cy: bigtext(dd, "~300,000", cx, cy, 130, fill=YEL), 540, 600, 900, k, k)
        if k > .6: bigtext(d, "CÁLCULO DE HOY (CUANDO MUCHO)", 540, 720, 40, fill=WHITE)
    up = lt > 2.2
    scribe(d, 540, 1290, .62, c.t, mood="happy", arms="up" if up else "down")
    if up:
        fish(d, 540, 1290 - .62 * 700, .9)
        say(d, "¡Así de grande!", (540, 1290 - .62 * 470), head=.62 * 125, size=46, side=1, avoid=[(400, 760, 680, 900)])
    chip(d, "LE AGREGÓ CEROS", CHIP1, bg=PURPLE, appear=lt / .3)
    return img

def s_napoleon(c):
    img = radial_bg(SNOW, cy=700); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (240, 245, 250))
    snow_fall(d, c.t)
    napoleon(d, 230 + shake(lt, 0, 99, 4, 30), 1290, .6, c.t, mood="scared")
    frac = tw(lt, .5, 1.5, 0, 1, cubic_out)
    bar_chart(d, 420, 600, 1020, [("ENTRARON", 450000, (45, 65, 140)), ("VOLVIERON", 120000 if lt > 2.6 else 450000 * (1 - tw(lt, 1.6, 1.0, 0, .73, cubic_out)), (200, 60, 60))],
              vmax=450000, frac=frac, size=50, bar_h=110, gap=70, fmt=lambda v: f"{round(v, -3):,.0f}")
    chip(d, "RUSIA · 1812", CHIP1, bg=BLUE, appear=lt / .3)
    return img

def s_toilet(c):
    img = radial_bg(SNOW, cy=700); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (240, 245, 250))
    snow_fall(d, c.t, n=10)
    outhouse(d, 900, 1290, .75)
    for i in range(6):
        x = 110 + i * 80; soldier(d, x, 1200 - i * 4, .26, c.t + i, era="napoleon", mood="scared")
    nx = 640 + shake(lt, 0, 99, 5, 25)
    napoleon(d, nx, 1290, .55, c.t, mood="scared", sweat=True)
    if lt > .8:
        a = anchors(nx, 1290, .55); say(d, "¿Ya mero?", a["mouth"], head=a["head_r"], size=48, avoid=[(780, 860, 1020, 1290)])
    if lt > c.dur * .55:
        k = tw(lt, c.dur * .55, .4, 0, 1, back_out); d = rubber_stamp(img, "DERROTADO", 540, 640, k)
    chip(d, "TIFO Y DIARREA", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def s_1941(c):
    img = radial_bg(NIGHT, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    blob_map(d, 240, 1000, 140, seed=4, fill=(150, 150, 160), label="ALEMANIA", size=34)
    blob_map(d, 720, 990, 260, seed=9, fill=(190, 120, 110), label="UNIÓN SOVIÉTICA", size=38)
    for i, yy in enumerate((880, 1000, 1120)):
        k = tw(lt, .3 + i * .25, 1.2, 0, 1, cubic_out)
        if k > 0: arrow(d, 330, yy, 330 + 330 * k, yy - 20 * k, col=RED, w=18)
    bigtext(d, "+3,800,000", 540, 580, 110, fill=WHITE); bigtext(d, "SOLDADOS", 540, 670, 44, fill=YEL)
    if lt > c.dur * .65:
        snow_fall(d, c.t, n=14, seed=8)
        k = tw(lt, c.dur * .65, .4, 0, 1, back_out); d = rubber_stamp(img, "IGUAL QUE NAPOLEÓN", 540, 1180, k, size=62)
    chip(d, "1941 · LA INVASIÓN MÁS GRANDE", CHIP1, bg=RED, size=48, appear=lt / .3)
    return img

def s_redarmy(c):
    img = radial_bg(NIGHT, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    blob_map(d, 540, 1000, 300, seed=9, fill=(190, 120, 110))
    n = int(tw(lt, .2, 1.8, 0, 34000000, cubic_out)); bigtext(d, f"{n:,}", 540, 540, 110, fill=WHITE); bigtext(d, "PERSONAS EN LA GUERRA", 540, 630, 44, fill=YEL)
    if lt > c.dur * .45:
        hy = tw(lt, c.dur * .45, .6, 520, 900, bounce_out); helmet(d, 540, hy, 1.25)
        if hy > 890:
            for sx in (-1, 1): d.ellipse([540 + sx * 90 - 22, 960, 540 + sx * 90 + 22, 1004], fill=WHITE, outline=BLK, width=4); d.ellipse([540 + sx * 90 - 8, 974, 540 + sx * 90 + 8, 990], fill=BLK)
            d.arc([480, 1030, 600, 1100], 20, 160, fill=BLK, width=8)
    chip(d, "UN PAÍS CON CASCO", CHIP1, bg=RED, appear=lt / .3)
    return img

def s_china(c):
    img = radial_bg(DAY, cy=700); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 900, W, 1380], fill=(170, 200, 130)); d.line([(0, 900), (W, 900)], fill=(120, 150, 90), width=5)
    sign_board(d, 140, 960, "TORTILLERÍA", size=26, post_h=60)
    for i in range(14, -1, -1):
        u = i / 14; s = .45 - .38 * u; x = 780 - 560 * u ** .8; y = 1240 - 300 * u ** .9
        soldier(d, x, y, s, c.t + i, era="modern")
    gx = 950; guy(d, gx, 1300, .5, mood="scared", t=c.t)
    a = anchors(gx, 1300, .5); tortillas(d, a["hand_l_down"][0], a["hand_l_down"][1] + 10, .55)
    if lt > 1.6: say(d, "Llego el martes…", a["mouth"], head=a["head_r"], size=42, maxw=360)
    bigtext(d, "~2,000,000", 540, 580, 100, fill=WHITE); bigtext(d, "MILITARES ACTIVOS", 540, 670, 44, fill=YEL)
    chip(d, "HOY: CHINA", CHIP1, bg=RED, appear=lt / .3)
    return img

def s_emus(c):
    img = radial_bg(OUTBACK, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (200, 120, 60))
    for i, x in enumerate((140, 330)): soldier(d, x, 1290, .45, c.t, era="modern", binoculars=True)
    for i in range(3):
        x = 560 + i * 190 + math.sin(c.t * 3 + i * 1.7) * 40; y = 1290 - (i % 2) * 90
        emu(d, x, y, .42 if i % 2 else .5, c.t + i * .4, flip=math.cos(c.t * 3 + i * 1.7) < 0, mood="crazy")
    n = int(tw(lt, .3, 1.5, 0, 20000, cubic_out)); bigtext(d, f"{n:,} EMÚS", 540, 600, 100, fill=WHITE)
    chip(d, "AUSTRALIA · 1932", CHIP1, bg=ORANGE, appear=lt / .3)
    return img

def s_retreat(c):
    img = radial_bg(OUTBACK, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (200, 120, 60))
    soldier(d, 300, 1290, .55, c.t, era="modern", mood="scared")
    a = anchors(300, 1290, .55)
    if lt > .8: white_flag(d, a["hand_r_down"][0] + 10, 1290, .9, c.t, h=560)
    ex = 760; es = .75; emu(d, ex, 1290, es, c.t, run=False)
    if lt > c.dur * .45:
        k = tw(lt, c.dur * .45, .4, 0, 1, back_out)
        if k > .5: medal(d, ex + es * 150, 1290 - es * 330, 1.2, text="1º", neck=(ex + es * 140, 1290 - es * 400))
    bigtext(d, "MENOS DE 1,000", 540, 590, 92, fill=WHITE); bigtext(d, "EN 2 MESES", 540, 685, 50, fill=YEL)
    chip(d, "SE RETIRARON", CHIP1, bg=GRAY, appear=lt / .3)
    return img

def s_ants(c):
    img = radial_bg(SOIL, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    frac = tw(lt, .3, 2.6, 0, 1, linear)
    bar_chart(d, 40, 520, 930, [("JERJES", 300000, (150, 60, 110)), ("NAPOLEÓN", 450000, (45, 65, 140)), ("CHINA HOY", 2000000, (200, 60, 60)),
                                ("1941", 3800000, (110, 110, 120)), ("HORMIGAS", 20000000, (150, 60, 30))], vmax=20000000, frac=frac, size=48, bar_h=88, gap=34,
              fmt=lambda v: f"{v / 1e6:g} M" if v >= 1e6 else f"{v / 1e3:g} mil")
    ant_column(d, [(-80, 1270), (300, 1220), (700, 1280), (1160, 1230)], c.t, .45)
    chip(d, "EL VERDADERO GANADOR", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def s_bones(c):
    img = radial_bg(SOIL, cy=760); d = ImageDraw.Draw(img); lt = c.lt
    ground(d, (150, 110, 70))
    half = c.dur * .5
    if lt < half * .55: rat(d, 600, 1285, 1.4, c.t)
    else: rat_skeleton(d, 600, 1285, 1.5)
    if lt < half:
        ant_column(d, [(-80, 1310), (1160, 1310)], c.t, .6, gap=70)
    else:
        k = tw(lt, half, .5, 0, 1, back_out)
        d = layer(img, lambda dd, cx, cy: phone_chat(dd, cx - 210, cy - 300, 420, 600, "GRUPO OFICINA", [], size=34), 300, 820, 760, k, k)
        if lt > half + .6: sign_board(d, 790, 1150, "SIN SUELDO", size=40, post_h=200)
        if lt > half + 1.4: sign_board(d, 790, 880, "SIN VACACIONES", size=40, post=False)
        if lt > half + 1.2:
            d.text((300, 860), "0 quejas", font=F(40), fill=(120, 120, 130), anchor="mm")
    chip(d, "EN LOS HUESOS", CHIP1, bg=GREEN, appear=lt / .3)
    return img

def ending(c):
    img = radial_bg(NIGHT, cy=800); d = ImageDraw.Draw(img); lt = c.lt
    d.rectangle([0, 860, 535, 1290], fill=(225, 235, 245)); d.rectangle([545, 860, W, 1290], fill=(160, 120, 80))
    outhouse(d, 420, 1280, .5); napoleon(d, 210 + shake(lt, 0, 99, 4, 25), 1280, .45, c.t, mood="scared", sweat=True)
    for r in range(4):
        for k in range(4):
            army_ant(d, 600 + k * 120 + (r % 2) * 50, 980 + r * 95, .35, c.t + r + k, helmet=(r + k) % 3 == 0)
    bigtext(d, "¿QUIÉN TE DA", 540, 560, 80, fill=WHITE); bigtext(d, "MÁS MIEDO?", 540, 665, 80, fill=YEL)
    follow_btn(d, lt, y=1240, delay=c.dur * .5)
    return img

SCENES = [(0, s_hook), (1, s_xerxes), (2, s_real), (3, s_napoleon), (4, s_toilet), (5, s_1941), (6, s_redarmy), (7, s_china),
          (8, s_emus), (9, s_retreat), (10, s_ants), (11, s_bones), (12, ending)]
SFX = [(0, 1.0, "pop", {}), (0, 2.2, "boing", {}), (1, .4, "whoosh", {}), (2, .2, "splat", {}), (2, 1.0, "ding", {}), (2, 2.2, "boing", {}),
       (3, 1.6, "sadtrom", {}), (4, .8, "pop", {}), (4, 3.0, "thud", {}), (5, .3, "whoosh", {}), (5, 4.5, "thud", {}), (6, 2.0, "boing", {}),
       (7, 1.6, "pop", {}), (8, .3, "skid", {}), (9, .8, "sadtrom", {}), (9, 2.5, "ding", {}), (10, .3, "rumble", {}), (11, 1.0, "splat", {}),
       (11, 3.5, "pop", {}), (12, 2.0, "jingle", {})]
MUSIC = ("bass", [(10, 11)], 12)
