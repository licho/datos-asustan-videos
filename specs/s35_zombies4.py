"""Zombies en el minisúper, parte 4: día 4, sin señal."""
import math
from lib.core import *
from lib.personajes import guy, employee, zombie, don_tono
from lib.props import key_on_neck, ice_machine, counter, phone_chat, wall_clock, clouds, helicopter, whistle, campfire, sign_board
from lib.fondos import store_day, make_store

NAME = "2026-11-27_zombies-parte4"
END = 5.0
LINES = [
 ("dramatically", "Día cuatro del apocalipsis zombi. Se fue la señal… y al celular le queda diez por ciento.", "*Día 4* del apocalipsis zombi. Sin señal… y *10% de batería*"),
 ("sarcastic", "El empleado ya cobra la carga: cincuenta pesos el cinco por ciento.", "El empleado ya cobra la carga: *$50 el 5%*"),
 ("serious", "Regla uno: ahorra batería. Baja el brillo, modo avión y cierra las apps que no uses.", "*Regla 1:* baja el brillo, *modo avión* y cierra las apps"),
 ("", "Regla dos: cuando haya señal, manda mensaje, no llames. Los mensajes pasan más fácil cuando la red está saturada.", "*Regla 2:* manda mensaje, no llames. *Pasa más fácil*"),
 ("sarcastic", "Y no, Don Toño, no es momento de subir historia.", "Y no, Don Toño, *no es momento de subir historia*"),
 ("serious", "Regla tres: para pedir ayuda, todo de a tres. Tres silbidos, tres luces, tres fogatas. Es la señal internacional de auxilio.", "*Regla 3:* todo de a tres. Es la *señal internacional de auxilio*"),
 ("", "Y en la azotea, escribe SOS en letras gigantes.", "En la azotea: *SOS en letras gigantes*"),
 ("mischievously", "Don Toño lo escribió… con papel de baño. Y llovió.", "Don Toño lo escribió… *con papel de baño*. Y llovió."),
 ("dramatically", "Pero esa noche se escucha un helicóptero. ¡Rescate!", "Esa noche… *¡un helicóptero!*"),
 ("", "Todos corren a la azotea… menos uno.", "Todos corren a la azotea… *menos uno*"),
 ("sarcastic", "El empleado: “Yo no me puedo ir. Mi turno termina a las siete.”", "“Yo no me puedo ir. *Mi turno termina a las 7.*”"),
 ("", "¿Tú te subes al helicóptero o te quedas con el hielo? Parte cinco… próximamente.", "¿Helicóptero o *el hielo*? *Parte 5*… próximamente"),
]
STORE = make_store(); FEET = 1300

def bigphone(d, x, y, w=420, h=760):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 50, fill=(30, 30, 35), outline=BLK, width=6)
    d.rounded_rectangle([x - w / 2 + 20, y - h / 2 + 24, x + w / 2 - 20, y + h / 2 - 24], 34, fill=(235, 238, 245))
    return (x - w / 2 + 20, y - h / 2 + 24, x + w / 2 - 20, y + h / 2 - 24)

def battery(d, x, y, pct, w=220):
    d.rounded_rectangle([x - w / 2, y - 50, x + w / 2, y + 50], 12, fill=WHITE, outline=BLK, width=6); d.rectangle([x + w / 2, y - 18, x + w / 2 + 18, y + 18], fill=BLK)
    d.rectangle([x - w / 2 + 10, y - 40, x - w / 2 + 10 + (w - 20) * pct / 100, y + 40], fill=RED if pct <= 20 else GREEN)
    d.text((x, y), f"{pct}%", font=F(46), fill=BLK, anchor="mm")

def s_day4(c):
    img = store_day(c.t); img = img if hasattr(img, "size") else img[0]; img = img.copy(); d = ImageDraw.Draw(img)
    guy(d, 330, FEET, .7, mood="scared", t=c.t)
    battery(d, 760, 640, 10 if int(c.t * 2) % 2 else 9)
    d.text((760, 740), "SIN SEÑAL", font=F(44), fill=RED, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    chip(d, "DÍA 4", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def s_charge(c):
    img, d = canvas(STORE)
    employee(d, 540, FEET - 120, .8, c.t); key_on_neck(d, 540, FEET - 120, .8)
    counter(d, 540, FEET, .8, w=820)
    sign_board(d, 540, 760, "CARGA: $50 = 5%", size=52, bg=(30, 120, 60), post=False)
    chip(d, "EL EMPLEADO COBRA", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def s_battery(c):
    img, d = canvas(((40, 50, 80), (70, 80, 110))); f = c.lt / c.dur
    x0, y0, x1, y1 = bigphone(d, 540, 900)
    for i, (lab, on_at) in enumerate((("BRILLO", .15), ("MODO AVIÓN", .4), ("APPS", .65))):
        yy = y0 + 110 + i * 190; on = f > on_at
        d.text((x0 + 30, yy), lab, font=F(40), fill=BLK, anchor="lm")
        if lab == "BRILLO":
            k = lerp(1, .25, ease(cl((f - .15) / .2))); d.rectangle([x0 + 30, yy + 40, x1 - 30, yy + 60], fill=(200, 200, 205)); d.rectangle([x0 + 30, yy + 40, x0 + 30 + (x1 - x0 - 60) * k, yy + 60], fill=BLUE)
        elif lab == "MODO AVIÓN":
            d.rounded_rectangle([x1 - 130, yy + 25, x1 - 30, yy + 75], 25, fill=GREEN if on else (190, 190, 195)); d.ellipse([x1 - 80 if on else x1 - 128, yy + 27, x1 - 32 if on else x1 - 80, yy + 73], fill=WHITE)
        else:
            n = 4 - int(4 * cl((f - .65) / .25))
            for k in range(n): d.rounded_rectangle([x0 + 30 + k * 85, yy + 30, x0 + 100 + k * 85, yy + 100], 14, fill=[RED, BLUE, ORANGE, PURPLE][k])
    if f < .15: d.rectangle([x0, y0, x1, y1], outline=YEL, width=10)
    chip(d, "REGLA 1: AHORRA BATERÍA", CHIP1, bg=BLUE, appear=c.lt / .3)
    return img

def s_text(c):
    img, d = canvas(((40, 50, 80), (70, 80, 110))); f = c.lt / c.dur
    x0, y0, x1, y1 = bigphone(d, 280, 880, 360, 640)
    d.text((280, y0 + 120), "LLAMANDO…", font=F(40), fill=BLK, anchor="mm")
    if f > .3: d.text((280, y0 + 260), "FALLIDA", font=F(52), fill=RED, anchor="mm"); xmark(d, 280, y0 + 420, .35)
    phone_chat(d, 620, 560, 400, 640, "Familia", [("r", "Estamos bien", "")], shown=1 if f > .5 else 0, size=32)
    if f > .6: d.text((820, 1140), "ENVIADO ✓", font=F(44), fill=GREEN, anchor="mm", stroke_width=4, stroke_fill=WHITE)
    chip(d, "REGLA 2: MENSAJE, NO LLAMADA", CHIP1, bg=GREEN, size=46, appear=c.lt / .3)
    return img

def s_story(c):
    img, d = canvas(STORE)
    don_tono(d, 360, FEET, .75, mood="happy", arms="up", t=c.t)
    hx, hy = 360 + 185 * .75, FEET - 560 * .75                      # mano derecha: sostiene el celular (selfie)
    d.rounded_rectangle([hx - 45, hy - 150, hx + 45, hy + 10], 14, fill=(40, 40, 45), outline=BLK, width=4); d.rectangle([hx - 35, hy - 138, hx + 35, hy - 8], fill=(120, 190, 250))
    d.ellipse([hx - 18, hy - 18, hx + 18, hy + 18], fill=SKIN, outline=BLK, width=2)
    bubble(d, 720, 520, "Día 4 en el apocalipsis #zombis", size=42, tail=(600, 700), maxw=560)
    guy(d, 860, FEET, .62, mood="scared", t=c.t)
    chip(d, "DON TOÑO…", CHIP1, bg=GRAY, appear=c.lt / .3)
    return img

def s_three(c):
    img, d = canvas(((30, 35, 60), (60, 65, 95))); f = c.lt / c.dur
    d.rectangle([0, 1250, W, 1380], fill=(60, 55, 50))
    if f < .5:
        whistle(d, 330, 760, 1.4)
        for k in range(3):
            if f > .1 + k * .12: bigtext(d, "¡PIT!", 760, 560 + k * 170, 80, fill=YEL)
    else:
        for x, y in ((540, 1000), (330, 1250), (750, 1250)): campfire(d, x, y, .9, c.t)
        d.text((540, 650), "3 FOGATAS EN TRIÁNGULO", font=F(50), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    chip(d, "REGLA 3: TODO DE A TRES", CHIP1, bg=ORANGE, appear=c.lt / .3)
    return img

def roof(d):
    d.rectangle([60, 460, 1020, 1320], fill=(150, 150, 160), outline=BLK, width=8)
    for x in range(60, 1020, 120): d.line([(x, 460), (x, 1320)], fill=(135, 135, 145), width=3)

def s_sos(c):
    img, d = canvas(((90, 140, 90), (110, 150, 100))); roof(d)
    k = cl(c.lt / (c.dur * .7))
    if k > 0: d.text((540, 890), "SOS"[:max(1, int(k * 3 + .99))], font=F(330), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=BLK)
    chip(d, "VISTA DESDE ARRIBA", CHIP1, bg=GRAY, appear=c.lt / .3)
    return img

def s_rain(c):
    img, d = canvas(((70, 80, 100), (100, 110, 120))); roof(d); f = c.lt / c.dur
    import random
    rnd = random.Random(int(c.t * 3))
    d.text((540, 890), "SOS", font=F(330), fill=(240, 240, 235), anchor="mm")
    for i in range(int(400 * cl((f - .3) / .6))):
        x, y = rnd.uniform(160, 920), rnd.uniform(720, 1060); r = rnd.uniform(6, 22)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 150, 160))
    clouds(d, 300, 380, 1.3, col=(90, 95, 110), t=c.t, rain=True); clouds(d, 780, 360, 1.2, col=(90, 95, 110), t=c.t + 1, rain=True)
    chip(d, "PAPEL DE BAÑO", CHIP1, bg=RED, appear=c.lt / .3)
    return img

def s_heli(c):
    img, d = canvas(((10, 12, 30), (30, 30, 60))); f = c.lt / c.dur
    helicopter(d, lerp(1100, 540, ease(cl(f / .6))), 420, 1.0, c.t, flip=True, light=f > .5, beam_to=1300)
    d.rectangle([150, 900, 930, 1300], fill=(150, 150, 160), outline=BLK, width=6); d.rectangle([440, 1080, 640, 1300], fill=(255, 230, 120), outline=BLK, width=5)
    d.text((540, 960), "MINISÚPER", font=F(56), fill=(80, 255, 120), anchor="mm")
    chip(d, "¡RESCATE!", CHIP1, bg=GREEN, appear=c.lt / .3)
    return img

def s_run(c):
    img, d = canvas(STORE); f = c.lt / c.dur
    d.rectangle([840, 560, 1020, FEET], fill=(90, 90, 100), outline=BLK, width=5)
    for k in range(6): d.line([(840, FEET - k * 120), (1020, FEET - k * 120 - 60)], fill=(150, 150, 160), width=8)
    d.text((930, 530), "AZOTEA ↑", font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
    employee(d, 250, FEET - 120, .7, c.t); key_on_neck(d, 250, FEET - 120, .7); counter(d, 250, FEET, .7, w=420)
    don_tono(d, lerp(450, 900, cl(f * 1.3)), FEET, .55, mood="happy", arms="up", t=c.t)
    guy(d, lerp(560, 960, cl(f * 1.3 - .1)), FEET, .55, mood="happy", arms="up", t=c.t)
    speedlines(d, c.t, n=8, y0=900, y1=1200)
    return img

def s_shift(c):
    img, d = canvas(STORE)
    wall_clock(d, 860, 560, 90, hour=3, minute=0)
    employee(d, 420, FEET - 120, .9, c.t); key_on_neck(d, 420, FEET - 120, .9); counter(d, 420, FEET, .9, w=640)
    bubble(d, 560, 470, "Mi turno termina a las 7.", size=48, tail=(470, 700), maxw=600)
    chip(d, "MENOS UNO", CHIP1, bg=PURPLE, appear=c.lt / .3)
    return img

def ending(c):
    img, d = canvas(((20, 25, 50), (50, 50, 80)))
    helicopter(d, 300, 640, .6, c.t, flip=True); ice_machine(d, 800, 1000, .8, c.t, glow=0)
    bigtext(d, "¿HELICÓPTERO", 540, 400, 80, fill=WHITE); bigtext(d, "O HIELO?", 540, 500, 80, fill=YEL)
    follow_btn(d, c.lt, y=1250, delay=c.dur * .5)
    return img

SCENES = [(0, s_day4), (1, s_charge), (2, s_battery), (3, s_text), (4, s_story), (5, s_three), (6, s_sos), (7, s_rain), (8, s_heli), (9, s_run), (10, s_shift), (11, ending)]
SFX = [(0, .2, "sting", {}), (1, .5, "ding", {}), (2, 1.0, "pop", {}), (2, 2.2, "pop", {}), (2, 3.4, "pop", {}), (3, 1.2, "buzzer", {}), (3, 2.5, "ding", {}),
       (4, .5, "boing", {}), (5, .5, "pop", {}), (5, 1.2, "pop", {}), (5, 1.9, "pop", {}), (6, .5, "pop", {}), (7, .5, "sadtrom", {}),
       (8, 0, "rumble", {"d": 3.0}), (9, .3, "whoosh", {}), (10, 1.0, "boing", {}), (11, 2.0, "jingle", {})]
MUSIC = ("bass", [(7, 8)], 11)
