"""El animal más peligroso del mundo: el mosquito."""
import math
from lib.core import *
from lib.personajes import guy, mosquito, shark, snake, lion
from lib.props import bed, podium, radar, bucket, tire, flowerpot, cake, balloons, spray, net, skull, egg_raft
from lib.fondos import night_room

NAME = "2026-11-20_mosquito"
END = 5.0
LINES = [
 ("mischievously", "¿Cuál es el animal más peligroso del mundo? ¿El tiburón? ¿El león? ¿La serpiente?", "¿Cuál es el animal *más peligroso* del mundo?"),
 ("dramatically", "No. Es este.", "No. *Es este.*"),
 ("serious", "Solo por la malaria murieron unas seiscientas diez mil personas en 2024, según la OMS.", "Solo por la *malaria* murieron unas *610 mil personas* en 2024"),
 ("", "Las serpientes matan entre ochenta y un mil y ciento treinta y ocho mil al año. ¿Los tiburones? Apenas un puñado.", "Serpientes: *81 a 138 mil* al año. ¿Tiburones? *Apenas un puñado*"),
 ("", "Y eso sin contar el dengue, el zika, el chikungunya y la fiebre amarilla.", "Y eso sin contar *dengue, zika, chikungunya y fiebre amarilla*"),
 ("mischievously", "Solo pican las hembras: necesitan tu sangre para producir sus huevos.", "Solo pican *las hembras*: necesitan tu sangre para *sus huevos*"),
 ("sarcastic", "O sea, técnicamente… eres su baby shower.", "O sea, técnicamente… *eres su baby shower*"),
 ("serious", "Te encuentran por el dióxido de carbono que exhalas, desde decenas de metros. Luego te ven… y al final sienten tu calor.", "Te huelen el *CO₂*, luego *te ven*… y al final *sienten tu calor*"),
 ("whispers", "Y no te pica con una aguja: su trompa tiene seis. Unas cortan, otras sujetan, una succiona… y otra te inyecta saliva para que tu sangre no se coagule.", "Su trompa tiene *seis agujas*: cortan, sujetan, succionan… y *te inyectan saliva*"),
 ("sarcastic", "No te pica. Te opera.", "No te pica. *Te opera.*"),
 ("confident", "Para defenderte, vacía el agua estancada: cubetas, llantas, macetas, que ahí ponen sus huevos. Y usa repelente y mosquitero.", "Vacía el *agua estancada*: ahí ponen sus huevos. Y usa *repelente y mosquitero*"),
 ("mischievously", "Y si a las tres de la mañana escuchas ese zumbido en tu oreja… no es un insecto. Es el depredador número uno del planeta.", "Si a las 3 a.m. escuchas ese zumbido… *es el depredador número uno del planeta*"),
 ("", "¿Tú qué prefieres: un tiburón en la playa… o un mosquito en tu cuarto?", "¿Un *tiburón* en la playa… o un *mosquito* en tu cuarto?"),
]

DARK = ((40, 30, 60), (90, 40, 70)); LIGHT = ((245, 240, 230), (225, 220, 210)); WATER = (120, 180, 220)

def poster(img, cx, cy, kind, t, appear):
    if appear <= 0: return
    sc = pop(appear); d = ImageDraw.Draw(img)
    w, h = 150 * sc, 200 * sc
    bg = {"shark": (90, 160, 220), "lion": (240, 200, 110), "snake": (130, 190, 110)}[kind]
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], int(24 * sc), fill=WHITE, outline=BLK, width=6)
    d.rounded_rectangle([cx - w + 14 * sc, cy - h + 14 * sc, cx + w - 14 * sc, cy + h - 70 * sc], int(16 * sc), fill=bg)
    if sc > .6:
        if kind == "shark": shark(d, cx, cy - 50, .42 * sc, t)
        if kind == "lion": lion(d, cx, cy + 105, .42 * sc, t)
        if kind == "snake": snake(d, cx, cy + 110, .42 * sc, t)
        d.text((cx, cy + h - 36 * sc), "¿?", font=F(50 * sc), fill=BLK, anchor="mm")

def hook(c):
    img, d = canvas(DARK); lt = c.lt; a1 = c.at(1)
    chip(d, "¿EL MÁS PELIGROSO?", CHIP1, bg=RED, appear=lt / .3)
    xs = (200, 540, 880)
    for i, (x, kind) in enumerate(zip(xs, ("shark", "lion", "snake"))):
        poster(img, x, 860, kind, c.t, (lt - a1 * (.3 + .2 * i)) / .35)
    d = ImageDraw.Draw(img)
    if lt >= a1:
        for i, x in enumerate(xs):
            if lt - a1 > .1 * i: xmark(d, x, 860, 1.6)
        k = ease((lt - a1) / 1.0)
        mosquito(d, lerp(1250, 560, k), lerp(450, 600, k) + math.sin(c.t * 5) * 15, lerp(.3, 1.2, k), c.t, mood="angry")
        if lt - a1 > .9: bigtext(d, "¡ESTE!", 540, 1180, 130, fill=YEL)
    return img

def malaria(c):
    img, d = canvas(((70, 20, 30), (130, 40, 40))); lt = c.lt
    chip(d, "MALARIA · 2024", CHIP1, bg=RED, appear=lt / .3)
    n = int(610000 * ease(cl(lt / 2.5)))
    bigtext(d, f"{n:,}".replace(",", ","), 540, 560, 150, fill=WHITE)
    d.text((540, 680), "MUERTES", font=F(60), fill=YEL, anchor="mm")
    shown = int(40 * cl(lt / 2.5))
    for k in range(shown):
        skull(d, 180 + (k % 8) * 103, 820 + (k // 8) * 100, 34)
    d.text((540, 1340), "Fuente: OMS, Informe Mundial de Malaria 2025", font=F(32), fill=(240, 200, 200), anchor="mm")
    return img

def ranking(c):
    img, d = canvas(LIGHT); lt = c.lt
    chip(d, "RANKING DE ASESINOS", CHIP1, bg=PURPLE, appear=lt / .3)
    base = 1320
    tops = podium(d, 540, base, 300, (380, 270, 170), appear=lt / 1.2)
    if lt > 1.0:
        (x1, y1), (x2, y2), (x3, y3) = tops
        mosquito(d, x1, y1 - 165, .75, c.t, mood="happy", fly=False)
        snake(d, x2, y2, .5, c.t)
        shark(d, x3, y3 - 62, .45, c.t, mood="cry" if lt > c.dur * .55 else "neutral")
        for (x, y), txt in zip(tops, ("610 MIL", "81–138 MIL", "UN PUÑADO")):
            d.text((x, base - 40), txt, font=F(36), fill=BLK, anchor="mm")
    return img

DIS = [("DENGUE", (230, 80, 60)), ("ZIKA", (60, 140, 230)), ("CHIKUNGUNYA", (240, 150, 40)), ("FIEBRE AMARILLA", (200, 170, 20))]
def diseases(c):
    img, d = canvas(DARK); lt = c.lt
    mosquito(d, 560, 640 + math.sin(c.t * 4) * 20, 1.0, c.t, mood="angry")
    for i, (txt, col) in enumerate(DIS):
        a = (lt - (.6 + i * c.dur * .17)) / .3
        if a > 0:
            chip(d, txt, 980 + i * 95, bg=col, size=58, appear=a)
    return img

def females(c):
    img, d = canvas(((255, 235, 240), (240, 210, 220))); lt = c.lt
    chip(d, "SOLO LAS HEMBRAS", CHIP1, bg=(220, 70, 140), appear=lt / .3)
    mosquito(d, 400, 740 + math.sin(c.t * 4) * 15, 1.1, c.t, female=True, mood="happy")
    mosquito(d, 900, 1030, .45, c.t, fly=True)
    bubble(d, 870, 860, "Yo solo tomo néctar", size=38, tail=(900, 985), maxw=330)
    if lt > c.dur * .5:
        d.rectangle([0, 1180, W, 1340], fill=WATER); d.line([(0, 1180), (W, 1180)], fill=(80, 140, 190), width=6)
        egg_raft(d, 330, 1195, 2.2)
        chip(d, "HUEVOS", 1270, bg=(80, 60, 50), size=44, appear=(lt - c.dur * .5) / .3)
    return img

def shower(c):
    img, d = canvas(((255, 220, 235), (250, 190, 210))); lt = c.lt
    chip(d, "BABY SHOWER", CHIP1, bg=(220, 70, 140), appear=lt / .3)
    balloons(d, 150, 1150, c.t, 3, .8); balloons(d, 960, 1150, c.t, 3, .7, seed=9)
    d.rectangle([0, 1300, W, 1380], fill=(200, 150, 170))
    cake(d, 330, 1300, .9, c.t, "¡FELICIDADES!")
    mosquito(d, 380, 720 + math.sin(c.t * 4) * 15, .95, c.t, female=True, hat=True, mood="happy")
    guy(d, 700, 1300, .62, mood="scared", t=c.t)
    d.text((700, 1340), "TÚ", font=F(44), fill=BLK, anchor="mm")
    confetti(d, c.t, 40)
    return img

def sensing(c):
    img, d = canvas(((220, 235, 245), (200, 220, 235))); lt = c.lt; f = lt / c.dur
    chip(d, "ASÍ TE ENCUENTRA", CHIP1, bg=BLUE, appear=lt / .3)
    cx, cy = 540, 740
    rings = [(360, "OLOR (CO₂) · 10–50 m", (230, 120, 40), f > .05), (230, "VISTA · 5–15 m", (60, 140, 230), f > .55), (120, "CALOR · menos de 1 m", RED, f > .8)]
    radar(d, cx, cy, [(r, "", col, on) for r, _, col, on in rings], c.t)
    for i, (r, txt, col, on) in enumerate(rings):
        y = 1150 + i * 55; cc = col if on else (160, 160, 165)
        d.ellipse([250, y - 16, 282, y + 16], fill=cc, outline=BLK, width=3)
        d.text((300, y), txt, font=F(42), fill=cc, anchor="lm", stroke_width=4 if on else 0, stroke_fill=WHITE)
    guy(d, cx, 1060, .55, mood="scared" if f > .8 else "neutral", t=c.t)
    for k in range(3):
        ph = (c.t * .7 + k / 3) % 1
        px, py = cx + 50 + ph * 120, 700 - ph * 90
        d.ellipse([px - 10 - ph * 14, py - 10 - ph * 14, px + 10 + ph * 14, py + 10 + ph * 14], outline=(150, 150, 160), width=3)
    if f < .55: mx, my, ms = lerp(90, 160, f / .55), lerp(360, 420, f / .55), .35
    elif f < .8: mx, my, ms = lerp(160, 330, (f - .55) / .25), lerp(420, 600, (f - .55) / .25), .4
    else: mx, my, ms = lerp(330, 400, cl((f - .8) / .15)), lerp(600, 650, cl((f - .8) / .15)), .45
    mosquito(d, mx, my + math.sin(c.t * 6) * 10, ms, c.t, mood="angry")
    return img

NEEDLES = [("CORTA", RED), ("CORTA", RED), ("SUJETA", ORANGE), ("SUJETA", ORANGE), ("SUCCIONA", BLUE), ("SALIVA", GREEN)]
def needles(c):
    img, d = canvas(LIGHT); lt = c.lt
    chip(d, "6 AGUJAS", CHIP1, bg=RED, appear=lt / .3)
    mosquito(d, 330, 600, 1.1, c.t, fly=False, mood="angry")
    tip = (330 + 200 * 1.1, 600 + 70 * 1.1)
    d.rounded_rectangle([80, 820, 1000, 1330], 30, fill=WHITE, outline=BLK, width=6)
    d.line([tip, (300, 860)], fill=(120, 120, 130), width=3); d.line([tip, (900, 860)], fill=(120, 120, 130), width=3)
    for i, (txt, col) in enumerate(NEEDLES):
        a = cl((lt - .4 - i * c.dur * .1) / .3)
        if a <= 0: continue
        y = 890 + i * 72
        d.line([(130, 1075), (130 + 420 * a, y)], fill=col, width=12)
        d.polygon([(130 + 420 * a, y - 10), (130 + 420 * a + 30, y), (130 + 420 * a, y + 10)], fill=col)
        d.text((620, y), txt, font=F(46), fill=col, anchor="lm", stroke_width=3, stroke_fill=WHITE)
    return img

def surgeon(c):
    img, d = canvas(((200, 235, 230), (160, 210, 205))); lt = c.lt
    d.line([(540, 360), (540, 430)], fill=BLK, width=10); d.ellipse([400, 420, 680, 510], fill=(250, 250, 220), outline=BLK, width=6)
    mosquito(d, 470, 820, 1.3, c.t, mask=True, mood="angry")
    bubble(d, 830, 610, "Bisturí.", size=56, tail=(650, 740), maxw=320)
    pts = []
    for k in range(60):
        x = 120 + k * 14; ph = (k - c.t * 30) % 25
        y = 1240 - (90 if ph < 1 else -40 if 1 <= ph < 2 else 0)
        pts.append((x, y))
    d.rounded_rectangle([90, 1150, 990, 1330], 20, fill=(20, 30, 30), outline=BLK, width=5)
    d.line(pts, fill=(80, 240, 120), width=5)
    chip(d, "TE OPERA", CHIP1, bg=RED, appear=(lt - .4) / .3)
    return img

def tips(c):
    img, d = canvas(((180, 220, 245), (210, 235, 250))); lt = c.lt; f = lt / c.dur
    d.rectangle([0, 1180, W, 1380], fill=(170, 150, 120))
    chip(d, "DEFIÉNDETE", CHIP1, bg=GREEN, appear=lt / .3)
    if f < .62:
        empty = f > .4
        bucket(d, 190, 1250, 1.0, water=not empty, larvae=1, t=c.t); tire(d, 540, 1250, 1.0, water=not empty); flowerpot(d, 890, 1250, 1.0, water=not empty)
        if empty:
            for x in (200, 540, 870): check(d, x, 820, 1.2)
        else:
            d.text((540, 640), "AGUA ESTANCADA = GUARDERÍA", font=F(58), fill=RED, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    else:
        spray(d, 250, 1240, 1.1, t=c.t, mist=1)
        d.rectangle([560, 520, 980, 1060], fill=(60, 80, 120), outline=BLK, width=8)
        mosquito(d, 770 + math.sin(c.t * 3) * 60, 780, .55, c.t, mood="angry", flip=True)
        net(d, (575, 535, 965, 1045), col=(240, 240, 240))
        d.text((770, 1110), "MOSQUITERO", font=F(44), fill=BLK, anchor="mm")
    return img

def night(c):
    img = night_room(); d = ImageDraw.Draw(img); lt = c.lt; f = lt / c.dur
    bx, by = 540, 1290
    bed(d, bx, by, 1.0)
    awake = f > .55
    hx, hy = bx - 220, by - 175
    d.ellipse([hx - 70, hy - 70, hx + 70, hy + 70], fill=SKIN, outline=BLK, width=5)
    d.chord([hx - 74, hy - 76, hx + 74, hy + 40], 180, 360, fill=(70, 50, 40))
    for ox in (-25, 25):
        if awake:
            d.ellipse([hx + ox - 18, hy - 10, hx + ox + 18, hy + 26], fill=WHITE, outline=BLK, width=3); d.ellipse([hx + ox - 6, hy + 2, hx + ox + 6, hy + 14], fill=BLK)
        else:
            d.arc([hx + ox - 16, hy, hx + ox + 16, hy + 20], 0, 180, fill=BLK, width=4)
    d.rounded_rectangle([bx - 160, by - 150, bx + 320, by - 90], 20, fill=(70, 110, 190), outline=BLK, width=5)
    if not awake: d.text((hx + 120, hy - 120), "z z Z", font=F(54), fill=(200, 200, 240), anchor="mm")
    a = c.t * 2.2
    mosquito(d, hx + 60 + math.cos(a) * 230, hy - 260 + math.sin(a * 1.7) * 70, .55, c.t, mood="angry", flip=math.sin(a) > 0)
    chip(d, "3:00 A.M.", CHIP1, bg=RED, appear=lt / .3)
    if f > .55: bigtext(d, "DEPREDADOR #1", 540, 680, 100, fill=RED); c.shake = 4 if f < .65 else 0
    return img

def ending(c):
    img, d = canvas(DARK); lt = c.lt
    d.rectangle([30, 520, 525, 1100], fill=(130, 200, 240), outline=WHITE, width=6); d.rectangle([33, 900, 522, 1097], fill=(40, 110, 180))
    shark(d, 275, 890, .62, c.t)
    d.rectangle([555, 520, 1050, 1100], fill=(70, 60, 110), outline=WHITE, width=6)
    mosquito(d, 830, 790 + math.sin(c.t * 4) * 15, .78, c.t, mood="angry")
    d.text((277, 1145), "EN LA PLAYA", font=F(44), fill=WHITE, anchor="mm"); d.text((802, 1145), "EN TU CUARTO", font=F(44), fill=WHITE, anchor="mm")
    bigtext(d, "¿CUÁL PREFIERES?", 540, 420, 90, fill=YEL)
    follow_btn(d, lt, y=1270, delay=c.dur * .85)
    return img

SCENES = [(0, hook), (2, malaria), (3, ranking), (4, diseases), (5, females), (6, shower), (7, sensing), (8, needles), (9, surgeon), (10, tips), (11, night), (12, ending)]
SFX = [(0, .3, "pop", {}), (1, 0, "buzzer", {}), (1, .1, "whine", {"dur": 2.0}), (2, 2.5, "ding", {}), (3, .4, "boing", {}),
       (4, .6, "pop", {}), (4, 2.0, "pop", {}), (4, 3.5, "pop", {}), (5, 0, "whine", {"dur": 1.2}), (6, .3, "jingle", {}),
       (7, 0, "whine", {"dur": 1.0}), (8, .5, "pop", {}), (9, 0, "ding", {}), (10, 2.0, "pop", {}), (11, 0, "whine", {"dur": 4.0, "g": .1}),
       (11, 3.5, "sting", {}), (12, 4.0, "jingle", {})]
MUSIC = ("bass", [(11, 12)], 12)
