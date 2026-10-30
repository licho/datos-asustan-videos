"""Objetos nuevos dibujados directo en lib."""
import math, random
from .core import F, BLK, WHITE, RED, YEL, dk, lc, pop, cl

def podium(d, cx, base, w=250, heights=(330, 230, 160), cols=((240, 190, 40), (190, 195, 205), (205, 130, 60)), appear=1.0):
    """Podio 1-2-3 (1 al centro, 2 izq, 3 der). Devuelve [(x, y_top)] en orden 1,2,3."""
    xs = (cx, cx - w, cx + w); tops = []
    for i, (px, h, c) in enumerate(zip(xs, heights, cols)):
        hh = h * cl(appear * 3 - i * .5 if appear < 1 else 1)
        d.rectangle([px - w / 2 + 6, base - hh, px + w / 2 - 6, base], fill=c, outline=BLK, width=6)
        if hh > 80: d.text((px, base - hh + 55), str(i + 1), font=F(80), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)
        tops.append((px, base - hh))
    return tops

def radar(d, cx, cy, rings, t=0.0):
    """rings=[(radio, texto, color, activo)] de mayor a menor."""
    for r, label, col, on in rings:
        c = col if on else (200, 200, 205)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=10 if on else 5)
        if on:
            ph = (t * .8) % 1
            rr = r * (0.9 + 0.1 * ph)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=lc(c, WHITE, ph), width=3)
        d.text((cx, cy - r - 4), label, font=F(40), fill=c if on else (150, 150, 155), anchor="md", stroke_width=5, stroke_fill=WHITE)

def bucket(d, x, y, s=1.0, water=True, larvae=0.0, t=0.0):
    """Cubeta; y = piso."""
    S = lambda v: v * s
    d.polygon([(x - S(95), y - S(190)), (x + S(95), y - S(190)), (x + S(75), y), (x - S(75), y)], fill=(70, 130, 210), outline=BLK, width=5)
    d.arc([x - S(95), y - S(300), x + S(95), y - S(90)], 200, 340, fill=(60, 60, 60), width=int(S(8)))
    if water:
        d.ellipse([x - S(90), y - S(205), x + S(90), y - S(175)], fill=(120, 180, 210), outline=BLK, width=3)
        for k in range(int(larvae * 6)):
            px = x - S(60) + k * S(24); py = y - S(190) + math.sin(t * 6 + k) * S(4)
            d.line([(px, py), (px + S(10), py + S(4))], fill=BLK, width=max(2, int(S(4))))

def tire(d, x, y, s=1.0, water=True):
    """Llanta tirada; y = piso."""
    S = lambda v: v * s
    d.ellipse([x - S(140), y - S(110), x + S(140), y], fill=(40, 40, 45), outline=BLK, width=5)
    d.ellipse([x - S(70), y - S(80), x + S(70), y - S(30)], fill=(120, 180, 210) if water else (90, 80, 70))
    for k in range(10):
        a = k / 10 * 2 * math.pi
        d.line([(x + math.cos(a) * S(105), y - S(55) + math.sin(a) * S(40)), (x + math.cos(a) * S(130), y - S(55) + math.sin(a) * S(50))], fill=(80, 80, 85), width=4)

def flowerpot(d, x, y, s=1.0, water=True):
    """Maceta con plato de agua; y = piso."""
    S = lambda v: v * s
    d.ellipse([x - S(110), y - S(30), x + S(110), y + S(6)], fill=(170, 90, 60), outline=BLK, width=4)
    if water: d.ellipse([x - S(90), y - S(26), x + S(90), y - S(4)], fill=(120, 180, 210))
    d.polygon([(x - S(80), y - S(200)), (x + S(80), y - S(200)), (x + S(60), y - S(20)), (x - S(60), y - S(20))], fill=(200, 110, 70), outline=BLK, width=5)
    for k, a in enumerate((-0.6, 0, 0.6)):
        bx, by = x + math.sin(a) * S(140), y - S(200) - math.cos(a) * S(140)
        d.line([(x, y - S(200)), (bx, by)], fill=(60, 140, 60), width=int(S(10)))
        d.ellipse([bx - S(40), by - S(25), bx + S(40), by + S(25)], fill=(80, 170, 80), outline=BLK, width=3)

def cake(d, x, y, s=1.0, t=0.0, text=""):
    """Pastel con velas; y = base."""
    S = lambda v: v * s
    d.rounded_rectangle([x - S(150), y - S(130), x + S(150), y], S(20), fill=(250, 200, 220), outline=BLK, width=5)
    d.rounded_rectangle([x - S(110), y - S(230), x + S(110), y - S(130)], S(18), fill=(250, 220, 235), outline=BLK, width=5)
    for k in range(7):
        d.ellipse([x - S(150) + k * S(50) - S(14), y - S(140), x - S(150) + k * S(50) + S(14), y - S(110)], fill=WHITE)
    for k in range(3):
        cx = x - S(60) + k * S(60)
        d.rectangle([cx - S(8), y - S(300), cx + S(8), y - S(230)], fill=(120, 190, 250), outline=BLK, width=2)
        fl = 1 + .15 * math.sin(t * 12 + k)
        d.ellipse([cx - S(10) * fl, y - S(335) * 1, cx + S(10) * fl, y - S(300)], fill=(255, 190, 40), outline=(230, 100, 30), width=2)
    if text: d.text((x, y - S(65)), text, font=F(S(30)), fill=(200, 40, 100), anchor="mm")

def balloons(d, x, y, t=0.0, n=3, s=1.0, seed=4, cols=((230, 60, 80), (60, 140, 230), (250, 200, 40), (120, 200, 90))):
    """Racimo de globos atado en (x, y)."""
    rnd = random.Random(seed); S = lambda v: v * s
    for k in range(n):
        bx = x + S((k - (n - 1) / 2) * 90) + math.sin(t * 2 + k) * S(10); by = y - S(260 + rnd.random() * 80)
        d.line([(x, y), (bx, by + S(70))], fill=(90, 90, 90), width=2)
        d.ellipse([bx - S(55), by - S(70), bx + S(55), by + S(70)], fill=cols[k % len(cols)], outline=BLK, width=4)
        d.ellipse([bx - S(30), by - S(45), bx - S(12), by - S(20)], fill=WHITE)

def spray(d, x, y, s=1.0, label="REPELENTE", t=0.0, mist=0.0):
    """Lata de spray; y = base."""
    S = lambda v: v * s
    d.rounded_rectangle([x - S(60), y - S(260), x + S(60), y], S(18), fill=(60, 170, 120), outline=BLK, width=5)
    d.rectangle([x - S(30), y - S(300), x + S(30), y - S(260)], fill=(200, 200, 205), outline=BLK, width=4)
    d.rectangle([x - S(15), y - S(330), x + S(25), y - S(300)], fill=(230, 60, 60), outline=BLK, width=3)
    d.text((x, y - S(130)), label, font=F(S(26)), fill=WHITE, anchor="mm", stroke_width=2, stroke_fill=BLK)
    for k in range(int(mist * 12)):
        u = ((t * 1.5 + k / 12) % 1)
        px = x + S(40) + u * S(260); py = y - S(320) - u * S(40) + math.sin(k * 7) * u * S(70)
        r = S(6 + 14 * u)
        d.ellipse([px - r, py - r, px + r, py + r], outline=(70, 130, 200), width=4)

def net(d, box, col=(255, 255, 255), step=26):
    """Mosquitero: rejilla dentro de box=(x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), step): d.line([(x, y0), (x, y1)], fill=col, width=2)
    for y in range(int(y0), int(y1), step): d.line([(x0, y), (x1, y)], fill=col, width=2)
    d.rectangle(box, outline=col, width=4)

def skull(d, x, y, r=30, col=WHITE):
    """Calavera tipo ícono."""
    d.ellipse([x - r, y - r, x + r, y + r * .8], fill=col, outline=BLK, width=max(2, r // 10))
    d.rounded_rectangle([x - r * .55, y + r * .4, x + r * .55, y + r * 1.1], r * .2, fill=col, outline=BLK, width=max(2, r // 10))
    for ox in (-.38, .38): d.ellipse([x + ox * r - r * .25, y - r * .2, x + ox * r + r * .25, y + r * .3], fill=BLK)
    d.polygon([(x, y + r * .35), (x - r * .1, y + r * .55), (x + r * .1, y + r * .55)], fill=BLK)

def egg_raft(d, x, y, s=1.0, n=14):
    """Huevecillos (balsa de huevos) flotando."""
    for k in range(n):
        px = x + (k % 7 - 3) * 16 * s; py = y + (k // 7) * 14 * s
        d.ellipse([px - 6 * s, py - 10 * s, px + 6 * s, py + 10 * s], fill=(70, 60, 50), outline=BLK)

def camera(d, x, y, s=1.0, t=0.0, rec=True, tripod=True, facing=1):
    """Videocámara (opcional sobre tripié). (x, y) = centro de la cámara; facing=1 apunta a la derecha."""
    S = lambda v: v * s; f = facing
    if tripod:
        for dx in (-110, 0, 110): d.line([(x, y + S(60)), (x + S(dx), y + S(470))], fill=(60, 60, 65), width=int(S(12)))
    d.rounded_rectangle([x - S(130), y - S(70), x + S(110), y + S(70)], int(S(20)), fill=(50, 50, 55), outline=BLK, width=5)
    lx = x + f * S(110)
    d.polygon([(lx, y - S(45)), (lx + f * S(90), y - S(70)), (lx + f * S(90), y + S(70)), (lx, y + S(45))], fill=(70, 70, 80), outline=BLK)
    d.ellipse([lx + f * S(70) - S(14), y - S(60), lx + f * S(70) + S(14), y + S(60)], fill=(120, 160, 200), outline=BLK, width=3)
    d.rectangle([x - S(100), y - S(110), x - S(20), y - S(70)], fill=(40, 40, 45), outline=BLK, width=3)
    if rec and int(t * 2) % 2 == 0: d.ellipse([x - S(110), y - S(55), x - S(80), y - S(25)], fill=RED)

def rec_frame(d, t, label="REC", box=(40, 470, 1040, 1330)):
    """Marco de cámara grabando: esquinas + REC parpadeando + contador."""
    from .core import F
    x0, y0, x1, y1 = box; L = 70
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(cx, cy), (cx + sx * L, cy)], fill=WHITE, width=8); d.line([(cx, cy), (cx, cy + sy * L)], fill=WHITE, width=8)
    if int(t * 2) % 2 == 0: d.ellipse([x0 + 30, y0 + 30, x0 + 66, y0 + 66], fill=RED)
    d.text((x0 + 80, y0 + 48), label, font=F(44), fill=WHITE, anchor="lm")
    m, sec = divmod(int(t), 60); d.text((x1 - 30, y0 + 48), f"00:{m:02d}:{sec:02d}", font=F(40), fill=WHITE, anchor="rm")

def snowflake(d, x, y, r=50, col=(120, 190, 250), width=8):
    for k in range(6):
        a = k * math.pi / 3
        ex, ey = x + math.cos(a) * r, y + math.sin(a) * r
        d.line([(x, y), (ex, ey)], fill=col, width=width)
        for u in (.55,):
            mx, my = x + math.cos(a) * r * u, y + math.sin(a) * r * u
            for da in (-.6, .6): d.line([(mx, my), (mx + math.cos(a + da) * r * .3, my + math.sin(a + da) * r * .3)], fill=col, width=width - 2)

def ranger_hat(d, x, y, s=1.0, col=(150, 110, 60)):
    """Sombrero de guardabosques; (x, y) = centro de la cabeza (ponlo sobre guy: x, pies - 520·s)."""
    S = lambda v: v * s
    d.ellipse([x - S(170), y - S(30), x + S(170), y + S(30)], fill=col, outline=BLK, width=5)
    d.polygon([(x - S(90), y - S(10)), (x - S(70), y - S(120)), (x, y - S(150)), (x + S(70), y - S(120)), (x + S(90), y - S(10))], fill=col, outline=BLK)
    d.rectangle([x - S(88), y - S(40), x + S(88), y - S(15)], fill=dk(col, .7))

def sarcophagus(d, x, y, s=1.0, col=(220, 170, 60)):
    """Sarcófago de pie; y = base."""
    S = lambda v: v * s
    pts = [(x - S(90), y), (x - S(110), y - S(300)), (x - S(100), y - S(480)), (x, y - S(560)), (x + S(100), y - S(480)), (x + S(110), y - S(300)), (x + S(90), y)]
    d.polygon(pts, fill=col, outline=BLK, width=5)
    d.polygon([(x - S(80), y - S(470)), (x, y - S(545)), (x + S(80), y - S(470)), (x + S(85), y - S(380)), (x - S(85), y - S(380))], fill=(40, 70, 160), outline=BLK)
    d.ellipse([x - S(45), y - S(500), x + S(45), y - S(400)], fill=(230, 190, 120), outline=BLK, width=3)
    for sx in (-1, 1): d.ellipse([x + sx * S(18) - S(7), y - S(462), x + sx * S(18) + S(7), y - S(450)], fill=BLK)
    for k in range(4): d.line([(x - S(80), y - S(330) + k * S(70)), (x + S(80), y - S(330) + k * S(70))], fill=dk(col, .7), width=4)
    d.rectangle([x - S(15), y - S(400), x + S(15), y - S(360)], fill=(40, 70, 160))

def gift(d, x, y, s=1.0, col=(220, 60, 70), ribbon=(250, 210, 60), bandage=False):
    """Regalo envuelto; y = base. bandage=True: envuelto en vendas."""
    S = lambda v: v * s
    body = (235, 225, 195) if bandage else col
    d.rectangle([x - S(80), y - S(130), x + S(80), y], fill=body, outline=BLK, width=4)
    d.rectangle([x - S(90), y - S(160), x + S(90), y - S(125)], fill=body, outline=BLK, width=4)
    if bandage:
        for k in range(6): d.line([(x - S(80), y - S(150) + k * S(28)), (x + S(80), y - S(135) + k * S(28))], fill=(190, 175, 140), width=4)
    else:
        d.rectangle([x - S(14), y - S(160), x + S(14), y], fill=ribbon)
    d.ellipse([x - S(50), y - S(195), x, y - S(155)], outline=ribbon if not bandage else (190, 175, 140), width=int(S(10)))
    d.ellipse([x, y - S(195), x + S(50), y - S(155)], outline=ribbon if not bandage else (190, 175, 140), width=int(S(10)))

def ring_light(d, x, y, r=170, on=True):
    d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 250, 220) if on else (150, 150, 150), width=int(r * .18))
    d.ellipse([x - r * 1.1, y - r * 1.1, x + r * 1.1, y + r * 1.1], outline=BLK, width=4); d.ellipse([x - r * .8, y - r * .8, x + r * .8, y + r * .8], outline=BLK, width=4)

def helicopter(d, x, y, s=1.0, t=0.0, flip=False, light=False, col=(200, 60, 50), beam_to=1300):
    """Helicóptero de rescate (cartoon). facing derecha salvo flip. (x, y) = centro de la cabina. beam_to = y donde termina el reflector."""
    S = lambda v: v * s; f = -1 if flip else 1
    if light:
        sp = (beam_to - y) * .22
        d.polygon([(x - S(40), y + S(80)), (x + S(40), y + S(80)), (x + sp, beam_to), (x - sp, beam_to)], fill=(255, 250, 200))
    d.line([(x - f * S(100), y), (x - f * S(330), y - S(30))], fill=col, width=int(S(36)))
    d.polygon([(x - f * S(320), y - S(30)), (x - f * S(360), y - S(110)), (x - f * S(300), y - S(40))], fill=col, outline=BLK)
    ph = t * 40
    d.ellipse([x - f * S(345) - S(30) * abs(math.cos(ph)), y - S(55), x - f * S(345) + S(30) * abs(math.cos(ph)), y - S(5)], outline=BLK, width=3)
    d.ellipse([x - S(160), y - S(90), x + S(160), y + S(90)], fill=col, outline=BLK, width=6)
    d.chord([x + f * S(20) - S(110) if f > 0 else x - S(130), y - S(75), x + S(130) if f > 0 else x - f * S(20) + S(110), y + S(30)], 180 if f > 0 else 180, 360, fill=(170, 220, 250), outline=BLK, width=4)
    d.text((x - f * S(40), y + S(40)), "RESCATE", font=F(S(34)), fill=WHITE, anchor="mm")
    for dx in (-80, 80): d.line([(x + S(dx), y + S(85)), (x + S(dx), y + S(125))], fill=BLK, width=int(S(8)))
    d.line([(x - S(140), y + S(125)), (x + S(140), y + S(125))], fill=BLK, width=int(S(10)))
    d.line([(x, y - S(90)), (x, y - S(125))], fill=BLK, width=int(S(12)))
    L = S(380) * abs(math.cos(ph))
    d.line([(x - L, y - S(128)), (x + L, y - S(128))], fill=(60, 60, 65), width=int(S(12)))

def whistle(d, x, y, s=1.0, col=(240, 160, 40)):
    S = lambda v: v * s
    d.rounded_rectangle([x - S(110), y - S(40), x + S(40), y + S(40)], int(S(30)), fill=col, outline=BLK, width=5)
    d.ellipse([x - S(10), y - S(70), x + S(110), y + S(50)], fill=col, outline=BLK, width=5)
    d.ellipse([x + S(25), y - S(35), x + S(75), y + S(15)], fill=dk(col, .5))
    d.arc([x - S(160), y - S(40), x - S(100), y + S(40)], 90, 270, fill=(120, 120, 130), width=int(S(8)))

def campfire(d, x, y, s=1.0, t=0.0):
    """Fogata; y = suelo."""
    S = lambda v: v * s
    for a in (-1, 1): d.line([(x - S(90) * a, y), (x + S(90) * a, y - S(40))], fill=(120, 80, 50), width=int(S(26)))
    for k, (c, h) in enumerate((((240, 90, 30), 210), ((250, 180, 40), 150), ((255, 240, 150), 80))):
        w = S(80 - k * 22); fl = math.sin(t * 12 + k) * S(8)
        d.polygon([(x - w, y - S(20)), (x + fl, y - S(h)), (x + w, y - S(20))], fill=c)

def mug(d, x, y, s=1.0, t=0.0, col=(240, 240, 235), level=1.0, steam=True, label=None):
    """Taza de café; y = base. level 0..1 = cuánto café queda (se ve por arriba)."""
    S = lambda v: v * s
    d.ellipse([x + S(40), y - S(170), x + S(150), y - S(60)], outline=BLK, width=int(S(22))); d.ellipse([x + S(40), y - S(170), x + S(150), y - S(60)], outline=col, width=int(S(12)))
    d.rounded_rectangle([x - S(100), y - S(220), x + S(100), y], int(S(30)), fill=col, outline=BLK, width=5)
    d.ellipse([x - S(100), y - S(240), x + S(100), y - S(200)], fill=(110, 70, 40) if level > .05 else (220, 220, 215), outline=BLK, width=4)
    if label: d.text((x, y - S(110)), label, font=F(S(50)), fill=(110, 70, 40), anchor="mm")
    if steam and level > .05:
        for k in range(3):
            ph = t * 2 + k
            d.arc([x - S(60) + k * S(45), y - S(340) + math.sin(ph) * S(10), x - S(20) + k * S(45), y - S(250)], 100, 260, fill=(170, 170, 190), width=int(S(8)))

def hourglass(d, x, y, s=1.0, frac=.5, t=0.0):
    """Reloj de arena (x, y = centro). frac = arena que ya cayó."""
    S = lambda v: v * s
    d.rectangle([x - S(90), y - S(170), x + S(90), y - S(150)], fill=(140, 95, 55), outline=BLK, width=3); d.rectangle([x - S(90), y + S(150), x + S(90), y + S(170)], fill=(140, 95, 55), outline=BLK, width=3)
    d.polygon([(x - S(70), y - S(150)), (x + S(70), y - S(150)), (x + S(8), y), (x + S(70), y + S(150)), (x - S(70), y + S(150)), (x - S(8), y)], fill=(220, 235, 245), outline=BLK)
    top = S(140) * (1 - frac); bot = S(140) * frac
    d.polygon([(x - S(70) * top / S(140), y - top + S(2)), (x + S(70) * top / S(140), y - top + S(2)), (x, y)], fill=(230, 190, 100))
    d.polygon([(x - S(70), y + S(150)), (x + S(70), y + S(150)), (x + S(70) - S(60) * (bot / S(140)), y + S(150) - bot), (x - S(70) + S(60) * (bot / S(140)), y + S(150) - bot)], fill=(230, 190, 100))
    if 0 < frac < 1: d.line([(x, y), (x, y + S(150) - bot)], fill=(230, 190, 100), width=int(S(5)))

def pyramid(d, x, y, s=1.0, built=1.0, col=(225, 190, 120)):
    """Pirámide; y = base. built 0..1 = qué tanto está construida (de abajo hacia arriba)."""
    S = lambda v: v * s; h = S(420); w = S(440)
    top = y - h * built; wt = w * (1 - built)
    d.polygon([(x - w, y), (x - wt, top), (x + wt, top), (x + w, y)], fill=col, outline=BLK)
    d.polygon([(x, y - h if built >= 1 else top), (x + wt if built < 1 else x, top), (x + w, y), (x + S(60), y)], fill=dk(col, .82))
    for k in range(1, 8):
        yy = y - h * k / 8
        if yy >= top: hw = w * (1 - k / 8); d.line([(x - hw, yy), (x + hw, yy)], fill=dk(col, .7), width=3)
    d.polygon([(x - w, y), (x, y - h), (x + w, y)] if built >= 1 else [(x - w, y), (x - wt, top), (x + wt, top), (x + w, y)], outline=BLK)

def rocket(d, x, y, s=1.0, t=0.0, flame=True):
    """Cohete; (x, y) = base."""
    S = lambda v: v * s
    if flame:
        fl = S(60) + math.sin(t * 25) * S(15)
        d.polygon([(x - S(40), y), (x, y + fl + S(60)), (x + S(40), y)], fill=(250, 150, 40)); d.polygon([(x - S(22), y), (x, y + fl), (x + S(22), y)], fill=(255, 230, 120))
    for sx in (-1, 1): d.polygon([(x + sx * S(50), y - S(120)), (x + sx * S(110), y + S(10)), (x + sx * S(50), y)], fill=(220, 60, 60), outline=BLK)
    d.rounded_rectangle([x - S(55), y - S(330), x + S(55), y], int(S(30)), fill=(240, 240, 245), outline=BLK, width=5)
    d.polygon([(x - S(55), y - S(300)), (x, y - S(420)), (x + S(55), y - S(300))], fill=(220, 60, 60), outline=BLK)
    d.ellipse([x - S(28), y - S(250), x + S(28), y - S(194)], fill=(120, 190, 250), outline=BLK, width=4)

def nopal(d, x, y, s=1.0):
    """Nopal sobre una roca (como en el escudo). y = base de la roca."""
    S = lambda v: v * s; G = (80, 150, 80)
    d.ellipse([x - S(110), y - S(60), x + S(110), y + S(10)], fill=(140, 120, 110), outline=BLK, width=4)
    for (dx, dy, w, h) in ((0, -170, 55, 110), (-80, -260, 45, 85), (80, -270, 45, 85), (0, -330, 40, 75)):
        d.ellipse([x + S(dx) - S(w), y + S(dy) - S(h), x + S(dx) + S(w), y + S(dy) + S(h)], fill=G, outline=BLK, width=4)
    for (dx, dy) in ((-80, -340), (80, -350), (0, -400)): d.ellipse([x + S(dx) - S(12), y + S(dy) - S(14), x + S(dx) + S(12), y + S(dy) + S(14)], fill=(220, 50, 90), outline=BLK, width=2)

def outhouse(d, x, y, s=1.0, door=0.0, label="WC"):
    """Letrina de madera con luna en la puerta. y = piso. door 0..1 = abierta."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); WD, DK = (160, 110, 60), (120, 80, 45)
    d.polygon([(x - S(150), y - S(470)), (x, y - S(540)), (x + S(150), y - S(470))], fill=(110, 60, 40), outline=BLK)
    d.rectangle([x - S(130), y - S(470), x + S(130), y], fill=WD, outline=BLK, width=W_(5))
    for k in range(1, 5): d.line([(x - S(130) + k * S(52), y - S(470)), (x - S(130) + k * S(52), y)], fill=DK, width=W_(3))
    dw = S(180) * (1 - door * .8)
    d.rectangle([x - S(90), y - S(420), x - S(90) + dw, y - S(5)], fill=dk(WD, .9), outline=BLK, width=W_(5))
    if door < .3:
        mx, my = x - S(90) + dw / 2, y - S(340)
        d.chord([mx - S(30), my - S(30), mx + S(30), my + S(30)], 60, 300, fill=(40, 30, 25)); d.ellipse([mx - S(10), my - S(30), mx + S(40), my + S(26)], fill=dk(WD, .9))
    if label: d.text((x, y - S(500)), label, font=F(int(S(48))), fill=WHITE, anchor="mm", stroke_width=W_(4), stroke_fill=BLK)

def white_flag(d, x, y, s=1.0, t=0.0, h=380):
    """Bandera blanca ondeando (rendición). (x, y) = base del palo."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.line([(x, y), (x, y - S(h))], fill=BLK, width=W_(14)); d.line([(x, y), (x, y - S(h))], fill=(150, 110, 70), width=W_(8))
    top = y - S(h) + S(10); pts_t, pts_b = [], []
    for k in range(9):
        u = k / 8; wy = math.sin(t * 6 - u * 5) * S(14) * u
        pts_t.append((x + u * S(200), top + wy)); pts_b.append((x + u * S(200), top + S(130) + wy))
    d.polygon(pts_t + pts_b[::-1], fill=WHITE, outline=BLK); d.line(pts_t, fill=BLK, width=W_(4)); d.line(pts_b, fill=BLK, width=W_(4))

def helmet(d, x, y, s=1.0, col=(80, 100, 60)):
    """Casco militar grande suelto. (x, y) = centro de la orilla de abajo."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.chord([x - S(200), y - S(200), x + S(200), y + S(70)], 180, 360, fill=col, outline=BLK, width=W_(7))
    d.rounded_rectangle([x - S(230), y - S(70), x + S(230), y - S(40)], int(S(12)), fill=dk(col, .8), outline=BLK, width=W_(5))
    d.arc([x - S(140), y - S(170), x + S(40), y - S(10)], 200, 260, fill=lc(col, WHITE, .4), width=W_(14))

def tortillas(d, x, y, s=1.0):
    """Paquete de tortillas envuelto en papel (de la tortillería). (x, y) = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.ellipse([x - S(80), y - S(30), x + S(80), y + S(40)], fill=(235, 215, 160), outline=BLK, width=W_(4))
    d.polygon([(x - S(85), y), (x - S(60), y - S(60)), (x + S(60), y - S(60)), (x + S(85), y), (x + S(70), y + S(35)), (x - S(70), y + S(35))], fill=(240, 240, 235), outline=BLK)
    d.text((x, y - S(10)), "1 KG", font=F(int(S(32))), fill=(200, 60, 50), anchor="mm")

def coffin(d, x, y, s=1.0, col=(120, 75, 45), open_=False):
    """Ataúd de madera de lado (velorio). y = piso (sobre su base)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rectangle([x - S(230), y - S(80), x + S(230), y], fill=(70, 60, 60), outline=BLK, width=W_(4))
    pts = [(x - S(260), y - S(150)), (x - S(200), y - S(250)), (x + S(260), y - S(250)), (x + S(280), y - S(150)), (x + S(260), y - S(80)), (x - S(200), y - S(80))]
    d.polygon(pts, fill=col, outline=BLK); d.line(pts + [pts[0]], fill=BLK, width=W_(5))
    d.line([(x - S(230), y - S(160)), (x + S(270), y - S(160))], fill=dk(col, .7), width=W_(5))
    for hx in (-120, 60, 200): d.rounded_rectangle([x + S(hx) - S(25), y - S(125), x + S(hx) + S(25), y - S(105)], int(S(6)), fill=(220, 190, 80), outline=BLK, width=W_(2))

def candle(d, x, y, s=1.0, t=0.0, col=(250, 245, 225)):
    """Vela encendida; y = base."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rectangle([x - S(18), y - S(120), x + S(18), y], fill=col, outline=BLK, width=W_(3))
    fl = S(6) * math.sin(t * 12)
    d.polygon([(x - S(14), y - S(130)), (x + fl, y - S(185)), (x + S(14), y - S(130))], fill=(255, 190, 40), outline=(220, 120, 20))
    d.ellipse([x - S(14), y - S(150), x + S(14), y - S(118)], fill=(255, 190, 40))

def shopping_cart(d, x, y, s=1.0, flip=False, items=True):
    """Carrito del súper; y = piso, empuja hacia la derecha (flip = izquierda). Agarradera en (x - 150s·f, y - 260s)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); f = -1 if flip else 1
    basket = [(x - f * S(120), y - S(250)), (x + f * S(140), y - S(250)), (x + f * S(110), y - S(90)), (x - f * S(100), y - S(90))]
    if items:
        for k, c in enumerate(((230, 80, 70), (80, 160, 230), (250, 200, 50))):
            bx = x - f * S(70) + f * k * S(65); d.rectangle([bx - S(28), y - S(300) + k * S(15), bx + S(28), y - S(200)], fill=c, outline=BLK, width=W_(3))
    d.polygon(basket, fill=(200, 205, 215)); 
    for k in range(1, 5): d.line([(x - f * S(120) + f * k * S(52), y - S(250)), (x - f * S(100) + f * k * S(42), y - S(90))], fill=(130, 135, 145), width=W_(4))
    d.line(basket + [basket[0]], fill=BLK, width=W_(7))
    d.line([(x - f * S(120), y - S(250)), (x - f * S(160), y - S(270))], fill=BLK, width=W_(9))
    d.line([(x - f * S(100), y - S(90)), (x - f * S(90), y - S(40)), (x + f * S(110), y - S(40))], fill=BLK, width=W_(7))
    for wx in (-80, 90): d.ellipse([x + f * S(wx) - S(22), y - S(44), x + f * S(wx) + S(22), y], fill=(50, 50, 55), outline=BLK, width=W_(3))

def time_clock(d, x, y, s=1.0, card_text="ENTRADA: 1509", full=1.0):
    """Reloj checador de pared con tarjeta. (x, y) = centro del aparato. full = qué tan llena está la tarjeta."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rounded_rectangle([x - S(150), y - S(200), x + S(150), y + S(180)], int(S(20)), fill=(200, 200, 210), outline=BLK, width=W_(6))
    d.ellipse([x - S(100), y - S(170), x + S(100), y + S(30)], fill=WHITE, outline=BLK, width=W_(5))
    for k in range(12):
        a = k / 12 * 6.283; d.line([(x + math.sin(a) * S(80), y - S(70) - math.cos(a) * S(80)), (x + math.sin(a) * S(90), y - S(70) - math.cos(a) * S(90))], fill=BLK, width=W_(4))
    d.line([(x, y - S(70)), (x + S(45), y - S(70))], fill=BLK, width=W_(7)); d.line([(x, y - S(70)), (x, y - S(140))], fill=BLK, width=W_(5))
    d.rectangle([x - S(90), y + S(70), x + S(90), y + S(95)], fill=(40, 40, 45))
    cx0, cy0 = x - S(70), y + S(80)
    d.rectangle([cx0, cy0, cx0 + S(140), cy0 + S(300)], fill=(250, 240, 200), outline=BLK, width=W_(4))
    d.text((cx0 + S(70), cy0 + S(30)), card_text, font=F(int(S(20))), fill=BLK, anchor="mm")
    n = int(12 * full)
    for k in range(n): d.line([(cx0 + S(15), cy0 + S(60) + k * S(19)), (cx0 + S(125), cy0 + S(60) + k * S(19))], fill=(200, 60, 60) if k % 3 == 2 else (60, 60, 160), width=W_(4))

def templo(d, x, y, s=1.0, col=(200, 185, 160), twin=True, tiers=4):
    """Pirámide mesoamericana escalonada (tipo Templo Mayor): cuerpos escalonados, escalinata al frente y templo(s) arriba.
    y = piso. twin=True: dos templos (Tláloc azul y Huitzilopochtli rojo); False: uno."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); DK = dk(col, .8)
    w0, th = 420, 70
    for k in range(tiers):
        w = w0 - k * 70; yb = y - k * th
        pts = [(x - S(w / 2), yb), (x + S(w / 2), yb), (x + S(w / 2 - 18), yb - S(th)), (x - S(w / 2 - 18), yb - S(th))]
        d.polygon(pts, fill=col if k % 2 == 0 else dk(col, .93)); d.line(pts + [pts[0]], fill=BLK, width=W_(4))
        d.line([(x - S(w / 2 - 6), yb - S(th * .3)), (x + S(w / 2 - 6), yb - S(th * .3))], fill=DK, width=W_(3))
    top = y - tiers * th; tw_ = w0 - tiers * 70
    sw = 80 if twin else 60
    for xs in ((-1, 1) if twin else (0,)):
        cx = x + xs * S(tw_ / 4 + 6)
        d.polygon([(cx - S(sw / 2), y), (cx + S(sw / 2), y), (cx + S(sw / 2 - 12), top), (cx - S(sw / 2 - 12), top)], fill=lc(col, (255, 255, 255), .25), outline=BLK)
        for k in range(1, tiers * 3): yy = y - k * S(th / 3); d.line([(cx - S(sw / 2 - 6), yy), (cx + S(sw / 2 - 6), yy)], fill=DK, width=W_(2))
    temples = (((-1), (60, 110, 190)), (1, (190, 60, 50))) if twin else ((0, (190, 60, 50)),)
    for xs, rc in temples:
        cx = x + xs * S(tw_ / 4 + 6); tw2 = S(tw_ / 2 - 14) if twin else S(tw_ - 30)
        d.rectangle([cx - tw2 / 2, top - S(80), cx + tw2 / 2, top], fill=(235, 225, 205), outline=BLK, width=W_(4))
        d.rectangle([cx - S(14), top - S(50), cx + S(14), top], fill=(40, 30, 30))
        d.rectangle([cx - tw2 / 2 - S(6), top - S(115), cx + tw2 / 2 + S(6), top - S(80)], fill=rc, outline=BLK, width=W_(4))

def curtain(d, x0, y0, x1, y1, open_=0.0, col=(170, 30, 45)):
    """Telón de teatro. open_ 0..1 = qué tan abierto. Dibuja el escenario de fondo, las cortinas y la cenefa."""
    d.rectangle([x0, y0, x1, y1], fill=(40, 30, 35))
    d.rectangle([x0, y1 - 40, x1, y1], fill=(120, 80, 50), outline=BLK, width=4)
    half = (x1 - x0) / 2; cw = half * (1 - .78 * open_)
    for side in (-1, 1):
        a = x0 if side < 0 else x1 - cw; b = a + cw
        d.rectangle([a, y0, b, y1 - 40], fill=col, outline=BLK, width=4)
        for k in range(1, 5): xx = a + cw * k / 5; d.line([(xx, y0 + 60), (xx + side * 8, y1 - 40)], fill=dk(col, .75), width=5)
    d.rectangle([x0, y0, x1, y0 + 70], fill=dk(col, .85), outline=BLK, width=4)
    for k in range(9): xx = x0 + (x1 - x0) * (k + .5) / 9; d.chord([xx - 40, y0 + 40, xx + 40, y0 + 100], 0, 180, fill=dk(col, .85), outline=BLK)

def ball_chain(d, x, y, bx, by, r=45):
    """Grillete en el tobillo (x, y) con cadena hasta una bola de preso en (bx, by)."""
    n = 7
    for k in range(n):
        u = (k + .5) / n; cx = x + (bx - x) * u; cy = y + (by - y) * u + math.sin(u * math.pi) * 18
        d.ellipse([cx - 13, cy - 8, cx + 13, cy + 8], outline=(70, 70, 80), width=5)
    d.ellipse([x - 22, y - 14, x + 22, y + 14], outline=(60, 60, 70), width=7)
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(45, 45, 52), outline=BLK, width=4)
    d.ellipse([bx - r * .55, by - r * .6, bx - r * .1, by - r * .2], fill=(95, 95, 105))

def cardboard_box(d, x, y, s=1.0, label="OBJETOS PERSONALES", items=True):
    """Caja de cartón de 'despedido' con cosas asomando. y = base."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    if items:
        d.rectangle([x - S(80), y - S(250), x - S(30), y - S(150)], fill=(90, 160, 90), outline=BLK, width=W_(3))
        d.line([(x - S(55), y - S(250)), (x - S(55), y - S(300))], fill=(60, 120, 60), width=W_(6))
        d.ellipse([x - S(80), y - S(330), x - S(30), y - S(290)], fill=(90, 170, 80), outline=BLK, width=W_(3))
        d.rectangle([x + S(10), y - S(230), x + S(90), y - S(150)], fill=(240, 240, 235), outline=BLK, width=W_(3))
        d.line([(x + S(90), y - S(210)), (x + S(110), y - S(195)), (x + S(90), y - S(175))], fill=BLK, width=W_(4))
    d.polygon([(x - S(150), y - S(170)), (x + S(150), y - S(170)), (x + S(135), y), (x - S(135), y)], fill=(200, 160, 110), outline=BLK)
    d.line([(x - S(150), y - S(170)), (x + S(150), y - S(170)), (x + S(135), y), (x - S(135), y), (x - S(150), y - S(170))], fill=BLK, width=W_(5))
    d.polygon([(x - S(150), y - S(170)), (x - S(190), y - S(230)), (x - S(40), y - S(230)), (x - S(20), y - S(170))], fill=(185, 145, 95), outline=BLK)
    if label: d.text((x, y - S(85)), label, font=F(int(S(19))), fill=(90, 60, 30), anchor="mm")

def open_box(d, x, y, s=1.0, col=(220, 60, 70), ribbon=(250, 210, 60), front=True):
    """Caja de regalo abierta (sin tapa). y = base. Llama con front=False antes del personaje (fondo de la caja)
    y con front=True después (frente de la caja) para que el personaje quede 'dentro'."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    if not front:
        d.polygon([(x - S(120), y - S(190)), (x + S(120), y - S(190)), (x + S(95), y - S(225)), (x - S(95), y - S(225))], fill=dk(col, .6), outline=BLK)
        return
    d.rectangle([x - S(120), y - S(190), x + S(120), y], fill=col, outline=BLK, width=W_(5))
    d.rectangle([x - S(16), y - S(190), x + S(16), y], fill=ribbon, outline=BLK, width=W_(2))

def box_lid(d, x, y, s=1.0, col=(220, 60, 70), ribbon=(250, 210, 60), ang=0.0):
    """Tapa de regalo con moño (x, y = centro de la tapa)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); a = math.radians(ang)
    def R(px, py): return (x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a))
    pts = [R(-S(132), -S(20)), R(S(132), -S(20)), R(S(132), S(20)), R(-S(132), S(20))]
    d.polygon(pts, fill=col, outline=BLK); d.line(pts + [pts[0]], fill=BLK, width=W_(4))
    for sx in (-1, 1):
        cx, cy = R(sx * S(30), -S(45)); d.ellipse([cx - S(30), cy - S(22), cx + S(30), cy + S(22)], outline=ribbon, width=W_(12))

def bookshelf_crooked(d, x, y, s=1.0, lean=8):
    """Librero recién armado y chueco. y = base."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); WD = (175, 130, 85)
    top = y - S(520); dx = S(lean * 6)
    d.polygon([(x - S(150), y), (x + S(150), y), (x + S(150) + dx, top), (x - S(150) + dx, top)], fill=WD, outline=BLK)
    d.line([(x - S(150), y), (x + S(150), y), (x + S(150) + dx, top), (x - S(150) + dx, top), (x - S(150), y)], fill=BLK, width=W_(6))
    for k in range(1, 4):
        u = k / 4; yy = y - S(520) * u; xx = dx * u
        d.line([(x - S(150) + xx, yy + (S(18) if k == 2 else 0)), (x + S(150) + xx, yy - (S(10) if k == 2 else 0))], fill=BLK, width=W_(8))
    for k in range(3): d.rectangle([x - S(110) + k * S(55) + dx * .2, y - S(110) - k * S(4), x - S(80) + k * S(55) + dx * .2, y - S(15)], fill=[(60, 120, 200), (200, 70, 60), (240, 190, 60)][k], outline=BLK, width=W_(2))

def screw(d, x, y, s=1.0, ang=20):
    S = lambda v: v * s; a = math.radians(ang); W_ = lambda v: max(2, int(v * s))
    p0 = (x - math.cos(a) * S(22), y - math.sin(a) * S(22)); p1 = (x + math.cos(a) * S(22), y + math.sin(a) * S(22))
    d.line([p0, p1], fill=(150, 150, 160), width=W_(8)); d.ellipse([p0[0] - S(9), p0[1] - S(9), p0[0] + S(9), p0[1] + S(9)], fill=(170, 170, 180), outline=BLK, width=W_(2))

def scroll(d, x, y, w, h, title="", lines=(), size=34, fine=None):
    """Pergamino largo con rollos arriba y abajo. (x, y) = esquina sup. izq. fine = letra chiquita al pie."""
    P = (245, 230, 190)
    d.rectangle([x, y + 25, x + w, y + h - 25], fill=P, outline=BLK, width=4)
    for yy in (y + 25, y + h - 25): d.rounded_rectangle([x - 20, yy - 25, x + w + 20, yy + 25], 25, fill=dk(P, .9), outline=BLK, width=4)
    if title: d.text((x + w / 2, y + 85), title, font=F(int(size * 1.1)), fill=(170, 40, 40), anchor="mm")
    for i, ln in enumerate(lines): d.text((x + 40, y + 140 + i * (size + 16)), ln, font=F(size), fill=(60, 40, 30), anchor="lm")
    if fine: d.text((x + w / 2, y + h - 65), fine, font=F(int(size * .55)), fill=(60, 40, 30), anchor="mm")

def sausages(d, x0, y0, x1, y1, n=5):
    """Cadena de salchichas de (x0,y0) a (x1,y1)."""
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        a = (x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0); b = (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1)
        d.line([a, b], fill=BLK, width=52); d.line([a, b], fill=(200, 100, 80), width=42)
        d.ellipse([b[0] - 6, b[1] - 6, b[0] + 6, b[1] + 6], fill=(150, 70, 55))

def fish(d, x, y, s=1.0, col=(120, 180, 220)):
    """Pescado de caricatura (el de 'así de grande'); (x, y) = centro, mira a la derecha."""
    S = lambda v: v * s
    d.polygon([(x - S(90), y), (x - S(140), y - S(40)), (x - S(140), y + S(40))], fill=col, outline=BLK)
    d.ellipse([x - S(110), y - S(45), x + S(70), y + S(45)], fill=col, outline=BLK, width=4)
    d.ellipse([x + S(25), y - S(18), x + S(45), y + 2], fill=BLK)

def office_desk(d, x0, x1, top=1000, floor=1290, col=(150, 110, 75)):
    """Escritorio de oficina visto de frente: cubierta, dos patas y cajonera. Pon a la persona ANTES (queda detrás)."""
    d.rectangle([x0, top, x1, top + 34], fill=col, outline=BLK, width=5)
    for x in (x0 + 30, x1 - 60): d.rectangle([x, top + 34, x + 30, floor], fill=dk(col, .8), outline=BLK, width=4)
    d.rectangle([x1 - 200, top + 34, x1 - 60, top + 200], fill=dk(col, .87), outline=BLK, width=4)
    d.line([(x1 - 160, top + 115), (x1 - 100, top + 115)], fill=BLK, width=5)

def xmas_tree(d, x, y, s=1.0, t=0.0):
    """Arbolito de Navidad (pino con esferas que parpadean). y = base."""
    from reels_engine.exterior import tree
    tree(d, x, y, s, kind="pine", col=(50, 140, 80))
    for k, (dx, dy, c) in enumerate(((-60, -200, RED), (50, -260, YEL), (-30, -340, (80, 140, 240)), (70, -150, (240, 140, 40)), (0, -430, RED))):
        on = (int(t * 3) + k) % 3 != 0
        d.ellipse([x + dx * s - 14, y + dy * s - 14, x + dx * s + 14, y + dy * s + 14], fill=c if on else dk(c, .5), outline=BLK, width=3)

def empty_clothes(d, x, y, s=1.0, hoodie=(240, 120, 40), pants=(50, 80, 150), cap=(200, 40, 50), phone=True):
    """Ropa vacía tirada en el piso con forma de persona acostada (alguien que desapareció): capucha y gorra, sudadera con
    mangas abiertas, pantalón de mezclilla con cinturón, tenis y un celular. Vista desde arriba en perspectiva. (x, y) = centro en el piso;
    mide ~460*s de largo."""
    k = .5                                                     # perspectiva (aplanado vertical)
    P = lambda u, v: (x + u * s, y - 18 * s + v * s * k)
    W_ = lambda v: max(2, int(v * s))
    def poly(pts, col, w=4):
        q = [P(*p) for p in pts]; d.polygon(q, fill=col, outline=BLK); d.line(q + [q[0]], fill=BLK, width=W_(w), joint="curve")
    def oval(u, v, ru, rv, col, w=4):
        q = [P(u + ru * math.cos(a / 16 * math.pi), v + rv * math.sin(a / 16 * math.pi)) for a in range(32)]
        d.polygon(q, fill=col, outline=BLK); d.line(q + [q[0]], fill=BLK, width=W_(w))
    d.ellipse([x - 290 * s, y - 34 * s, x + 230 * s, y + 10 * s], fill=(70, 70, 78))
    # pantalón: dos piernas un poco abiertas
    for sv in (-1, 1):
        poly([(-40, sv * 4), (-40, sv * 58), (150, sv * 78), (160, sv * 30)], pants)
        d.line([P(-20, sv * 30), P(140, sv * 52)], fill=dk(pants, .7), width=W_(3))
    poly([(-50, -60), (-30, -60), (-30, 60), (-50, 60)], (90, 60, 40), 3)              # cinturón
    oval(-40, 0, 9, 14, (230, 200, 80), 3)
    # sudadera: torso + mangas abiertas
    for sv in (-1, 1): poly([(-150, sv * 50), (-110, sv * 70), (-40, sv * 150), (-15, sv * 128), (-80, sv * 42)], hoodie)
    for sv in (-1, 1): oval(-28, sv * 140, 16, 20, dk(hoodie, .8), 3)              # puños
    poly([(-180, -68), (-40, -62), (-40, 62), (-180, 68)], hoodie)
    poly([(-120, -30), (-60, -26), (-60, 26), (-120, 30)], dk(hoodie, .85), 3)         # bolsa canguro
    for sv in (-1, 1): d.line([P(-172, sv * 14), P(-130, sv * 10)], fill=WHITE, width=W_(4))   # cordones
    oval(-215, 0, 46, 62, dk(hoodie, .8))                                              # capucha vacía
    oval(-212, 0, 26, 40, (40, 30, 30), 3)
    # gorra junto a la capucha
    oval(-250, -95, 34, 30, cap, 3); poly([(-222, -110), (-188, -118), (-184, -78), (-222, -82)], dk(cap, .75), 3)
    # tenis al final de cada pierna (vistos desde arriba, punta hacia arriba)
    for sv in (-1, 1):
        oval(178, sv * 66, 30, 30, (250, 250, 250))
        oval(196, sv * 66, 10, 22, (200, 60, 60), 3)
        for kk in range(3): d.line([P(160 + kk * 9, sv * 66 - 14), P(160 + kk * 9, sv * 66 + 14)], fill=BLK, width=W_(3))
    if phone:
        px, py = P(70, -150)
        d.rounded_rectangle([px - 34 * s, py - 14 * s, px + 34 * s, py + 14 * s], int(6 * s), fill=(30, 30, 35), outline=BLK, width=W_(3))
        d.rounded_rectangle([px - 28 * s, py - 9 * s, px + 28 * s, py + 9 * s], int(4 * s), fill=(150, 210, 255))

def plastic_bag(d, x, y, s=1.0, t=0.0, col=(240, 240, 245), text=None):
    """Bolsa de plástico flotando (se mece). (x, y) = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); sw = math.sin(t * 2) * S(10)
    body = [(x - S(70), y - S(40) + sw * .3), (x + S(70), y - S(40) - sw * .3), (x + S(85), y + S(70)), (x - S(85), y + S(70))]
    d.polygon(body, fill=col, outline=BLK); d.line(body + [body[0]], fill=BLK, width=W_(4))
    for sx in (-1, 1): d.arc([x + sx * S(45) - S(30), y - S(95), x + sx * S(45) + S(30), y - S(25)], 180, 360, fill=BLK, width=W_(6))
    for k in range(3): d.line([(x - S(50) + k * S(45), y - S(20)), (x - S(60) + k * S(50), y + S(55))], fill=(200, 200, 210), width=W_(3))
    if text: d.text((x, y + S(20)), text, font=F(int(S(24))), fill=(200, 60, 60), anchor="mm")

def old_tv(d, x, y, s=1.0, t=0.0, screen=(120, 180, 220), show="novela"):
    """Tele vieja de perilla con antenas. y = base. show: novela (corazón y dos siluetas) | static | blank."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    for sx in (-1, 1): d.line([(x, y - S(300)), (x + sx * S(90), y - S(420))], fill=BLK, width=W_(6))
    d.rounded_rectangle([x - S(170), y - S(300), x + S(170), y - S(30)], int(S(24)), fill=(150, 105, 70), outline=BLK, width=W_(5))
    sx0, sy0, sx1, sy1 = x - S(145), y - S(275), x + S(80), y - S(55)
    d.rounded_rectangle([sx0, sy0, sx1, sy1], int(S(20)), fill=screen, outline=BLK, width=W_(4))
    if show == "novela":
        cx, cy = (sx0 + sx1) / 2, (sy0 + sy1) / 2
        for k, dx in enumerate((-40, 40)): d.ellipse([cx + S(dx) - S(18), cy - S(50), cx + S(dx) + S(18), cy - S(14)], fill=(60, 50, 60)); d.rectangle([cx + S(dx) - S(22), cy - S(14), cx + S(dx) + S(22), cy + S(60)], fill=(60, 50, 60))
        hb = 1 + .15 * math.sin(t * 6)
        d.polygon([(cx - S(18) * hb, cy - S(70)), (cx, cy - S(50)), (cx + S(18) * hb, cy - S(70)), (cx, cy - S(90))], fill=(230, 60, 90))
    elif show == "static":
        import random as _r; r = _r.Random(int(t * 12))
        for k in range(60):
            px, py = r.uniform(sx0, sx1 - 8), r.uniform(sy0, sy1 - 4); d.rectangle([px, py, px + S(8), py + S(4)], fill=(230, 230, 230))
    for k in range(2): d.ellipse([x + S(100) - S(18), y - S(250) + k * S(80) - S(18), x + S(100) + S(18), y - S(250) + k * S(80) + S(18)], fill=(90, 90, 95), outline=BLK, width=W_(3))
    for sx in (-1, 1): d.line([(x + sx * S(120), y - S(30)), (x + sx * S(140), y)], fill=BLK, width=W_(8))

def tombstone(d, x, y, s=1.0, text="Q.E.P.D.", col=(170, 170, 180)):
    """Lápida de caricatura; y = base."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rounded_rectangle([x - S(80), y - S(170), x + S(80), y], int(S(70)), fill=col, outline=BLK, width=W_(4))
    d.rectangle([x - S(80), y - S(90), x + S(80), y], fill=col)
    d.line([(x - S(80), y - S(90)), (x - S(80), y)], fill=BLK, width=W_(4)); d.line([(x + S(80), y - S(90)), (x + S(80), y)], fill=BLK, width=W_(4))
    d.text((x, y - S(95)), text, font=F(int(S(26))), fill=(70, 70, 80), anchor="mm")
    d.rectangle([x - S(100), y - S(10), x + S(100), y + S(6)], fill=(90, 140, 70))

def shades(d, x, y, w=60, col=(25, 25, 30), vertical=False, arms=0):
    """Lentes oscuros para cualquier personaje; (x, y) = centro entre los ojos, w = ancho total.
    vertical=True: lentes uno arriba del otro (personajes de perfil con ojos encimados, como la cucaracha).
    arms: largo de las patitas hacia atrás (negativo = hacia la izquierda), 0 = sin patitas."""
    if not vertical:
        h = w * .28
        for sx in (-1, 1): d.rounded_rectangle([x + sx * w * .27 - w * .22, y - h / 2, x + sx * w * .27 + w * .22, y + h / 2], int(h * .3), fill=col, outline=BLK, width=3)
        d.line([(x - w * .06, y - h * .2), (x + w * .06, y - h * .2)], fill=BLK, width=4)
        if arms:
            for sx in (-1, 1): d.line([(x + sx * w * .49, y - h * .3), (x + sx * w * .49 + sx * abs(arms), y - h * .6)], fill=BLK, width=4)
        return
    r = w * .25
    for sy in (-1, 1):
        cy = y + sy * w * .26
        if arms: d.line([(x, cy), (x + arms, cy + sy * w * .05)], fill=BLK, width=max(3, int(w * .07)))
        d.rounded_rectangle([x - r, cy - r, x + r, cy + r], int(r * .5), fill=col, outline=BLK, width=3)
        d.line([(x - r * .5, cy - r * .45), (x - r * .1, cy - r * .45)], fill=(120, 120, 140), width=max(2, int(w * .04)))
    d.line([(x + r * .6, y - w * .05), (x + r * .6, y + w * .05)], fill=BLK, width=max(3, int(w * .07)))

def trash_can(d, x, y, s=1.0, full=False):
    """Bote de basura metálico de calle; y = base. full: con bolsas asomando."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); G = (150, 155, 165)
    if full:
        for k, (dx, c) in enumerate(((-30, (60, 60, 70)), (25, (40, 110, 60)))): d.ellipse([x + S(dx) - S(45), y - S(260), x + S(dx) + S(45), y - S(180)], fill=c, outline=BLK, width=W_(3))
    d.polygon([(x - S(90), y - S(220)), (x + S(90), y - S(220)), (x + S(75), y), (x - S(75), y)], fill=G, outline=BLK); d.line([(x - S(90), y - S(220)), (x + S(90), y - S(220)), (x + S(75), y), (x - S(75), y), (x - S(90), y - S(220))], fill=BLK, width=W_(4))
    for k in range(4): d.line([(x - S(60) + k * S(40), y - S(205)), (x - S(52) + k * S(35), y - S(15))], fill=dk(G, .8), width=W_(5))
    d.rounded_rectangle([x - S(100), y - S(238), x + S(100), y - S(214)], int(S(10)), fill=dk(G, .9), outline=BLK, width=W_(3))

def torta(d, x, y, s=1.0):
    """Torta (bolillo relleno de jamón, jitomate y lechuga) de lado; (x, y) = centro. ~200s de ancho."""
    W_ = lambda v: max(2, int(v * s)); S = lambda v: v * s
    d.chord([x - S(100), y - S(70), x + S(100), y + S(30)], 180, 360, fill=(220, 160, 80), outline=BLK, width=W_(4))
    for k in range(3): d.arc([x - S(70) + k * S(45), y - S(60), x - S(30) + k * S(45), y - S(30)], 200, 340, fill=(180, 120, 60), width=W_(4))
    d.rectangle([x - S(96), y - S(20), x + S(96), y - S(8)], fill=(110, 190, 80), outline=BLK, width=W_(2))
    d.rectangle([x - S(92), y - S(8), x + S(92), y + S(4)], fill=(230, 80, 70), outline=BLK, width=W_(2))
    d.rectangle([x - S(96), y + S(4), x + S(96), y + S(16)], fill=(240, 160, 170), outline=BLK, width=W_(2))
    d.chord([x - S(100), y - S(10), x + S(100), y + S(50)], 0, 180, fill=(220, 160, 80), outline=BLK, width=W_(4))

def soup_bowl(d, x, y, s=1.0, t=0.0, lemon=True):
    """Plato hondo de caldo de pollo humeante (pierna con hueso, zanahoria, calabacita) sobre su platito, con limón al lado;
    y = base (ponlo sobre la superficie de una mesa). ~330s de ancho."""
    W_ = lambda v: max(2, int(v * s)); S = lambda v: v * s
    d.ellipse([x - S(175), y - S(22), x + S(175), y + S(8)], fill=(235, 235, 240), outline=BLK, width=W_(4))       # platito
    d.chord([x - S(150), y - S(230), x + S(150), y], 0, 180, fill=(250, 250, 250), outline=BLK, width=W_(5))       # cuerpo del plato
    d.arc([x - S(120), y - S(150), x + S(120), y - S(40)], 20, 160, fill=(90, 140, 200), width=W_(6))              # rayita azul
    d.ellipse([x - S(150), y - S(140), x + S(150), y - S(90)], fill=(250, 250, 250), outline=BLK, width=W_(5))      # borde
    d.ellipse([x - S(132), y - S(134), x + S(132), y - S(96)], fill=(235, 180, 80))                               # caldo
    d.ellipse([x - S(80), y - S(128), x + S(10), y - S(102)], fill=(225, 175, 115), outline=BLK, width=W_(3))      # pierna
    d.line([(x + S(5), y - S(118)), (x + S(55), y - S(150))], fill=(250, 245, 230), width=W_(14))                 # hueso
    d.ellipse([x + S(45), y - S(162), x + S(70), y - S(140)], fill=(250, 245, 230), outline=BLK, width=W_(2))
    d.ellipse([x + S(30), y - S(122), x + S(70), y - S(104)], fill=(240, 140, 60), outline=BLK, width=W_(2))       # zanahoria
    d.ellipse([x - S(120), y - S(122), x - S(85), y - S(106)], fill=(120, 190, 90), outline=BLK, width=W_(2))      # calabacita
    for k in range(3):
        sx = x - S(60) + k * S(60); off = math.sin(t * 3 + k) * S(8)
        d.arc([sx - S(18) + off, y - S(250), sx + S(18) + off, y - S(200)], 90, 270, fill=(235, 235, 240), width=W_(6))
        d.arc([sx - S(18) - off, y - S(205), sx + S(18) - off, y - S(155)], 270, 90, fill=(235, 235, 240), width=W_(6))
    if lemon:
        lx, ly = x + S(215), y
        d.pieslice([lx - S(40), ly - S(40), lx + S(40), ly + S(40)], 180, 360, fill=(150, 210, 80), outline=BLK, width=W_(4))
        d.pieslice([lx - S(30), ly - S(30), lx + S(30), ly + S(30)], 180, 360, fill=(220, 240, 150))
        for a in (215, 270, 325): d.line([(lx, ly), (lx + S(28) * math.cos(math.radians(a)), ly + S(28) * math.sin(math.radians(a)))], fill=(150, 200, 80), width=W_(3))

def place_setting(d, x, y, s=1.0, food=None):
    """Lugar en la mesa visto de frente: plato con cubiertos a los lados y copa. y = superficie de la mesa.
    food: None | "pavo" (pierna de pavo)."""
    W_ = lambda v: max(2, int(v * s)); S = lambda v: v * s
    d.ellipse([x - S(80), y - S(16), x + S(80), y + S(8)], fill=WHITE, outline=BLK, width=W_(4))
    d.ellipse([x - S(55), y - S(10), x + S(55), y + S(3)], outline=(200, 200, 210), width=W_(2))
    for sx, tip in ((-1, "fork"), (1, "knife")):
        fx = x + sx * S(105)
        d.line([(fx, y - S(70)), (fx, y)], fill=(170, 170, 180), width=W_(8))
        if tip == "fork":
            for k in (-1, 0, 1): d.line([(fx + k * S(7), y - S(90)), (fx + k * S(7), y - S(68))], fill=(170, 170, 180), width=W_(4))
        else: d.ellipse([fx - S(7), y - S(100), fx + S(9), y - S(55)], fill=(190, 190, 200), outline=BLK, width=W_(2))
    if food == "pavo":
        d.ellipse([x - S(45), y - S(45), x + S(25), y - S(5)], fill=(190, 120, 60), outline=BLK, width=W_(3))
        d.line([(x + S(15), y - S(28)), (x + S(55), y - S(50))], fill=(250, 245, 230), width=W_(12))

def snack_plate(d, x, y, s=1.0, flag=True):
    """Platito de botana con palillo y banderita; y = base. Pon la botana encima en (x, y - 20s)."""
    W_ = lambda v: max(2, int(v * s)); S = lambda v: v * s
    d.ellipse([x - S(170), y - S(30), x + S(170), y + S(10)], fill=(250, 250, 250), outline=BLK, width=W_(4))
    d.ellipse([x - S(120), y - S(20), x + S(120), y], outline=(200, 200, 210), width=W_(3))
    if flag:
        d.line([(x + S(60), y - S(15)), (x + S(80), y - S(150))], fill=(210, 180, 120), width=W_(6))
        d.polygon([(x + S(80), y - S(150)), (x + S(130), y - S(138)), (x + S(78), y - S(118))], fill=RED, outline=BLK)

def pet_collar(d, x, y, w=60, col=(220, 50, 60)):
    """Collar de mascota con plaquita dorada; (x, y) = centro del cuello, w = ancho."""
    d.rounded_rectangle([x - w / 2, y - w * .12, x + w / 2, y + w * .12], int(w * .1), fill=col, outline=BLK, width=3)
    d.ellipse([x - w * .12, y + w * .05, x + w * .12, y + w * .29], fill=(250, 210, 60), outline=BLK, width=3)

def stopwatch(d, x, y, r=110, secs=0.0, total=240, col=(240, 240, 245)):
    """Cronómetro con botón y aguja; secs = segundos transcurridos (una vuelta = total). Muestra MM:SS abajo. (x, y) = centro."""
    d.rectangle([x - r * .15, y - r * 1.3, x + r * .15, y - r * 1.05], fill=(170, 170, 180), outline=BLK, width=4)
    d.ellipse([x - r * .25, y - r * 1.45, x + r * .25, y - r * 1.25], fill=RED, outline=BLK, width=4)
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=BLK, width=8)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        d.line([(x + math.sin(a) * r * .8, y - math.cos(a) * r * .8), (x + math.sin(a) * r * .92, y - math.cos(a) * r * .92)], fill=BLK, width=4)
    a = (secs % total) / total * 2 * math.pi
    d.line([(x, y), (x + math.sin(a) * r * .75, y - math.cos(a) * r * .75)], fill=RED, width=8)
    d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=BLK)
    m, sct = int(secs) // 60, int(secs) % 60
    d.text((x, y + r + 50), f"{m}:{sct:02d}", font=F(int(r * .55)), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=BLK)

def vertebrae(d, x, y0, y1, n=7, w=80, col=(245, 240, 225), labels=False):
    """Columna de n vértebras apiladas entre y0 (arriba) y y1 (abajo), centrada en x; para comparar cuellos."""
    seg = (y1 - y0) / n
    d.line([(x, y0), (x, y1)], fill=(200, 80, 80), width=max(4, int(w * .12)))
    for k in range(n):
        a, b = y0 + k * seg + seg * .1, y0 + (k + 1) * seg - seg * .1
        d.rounded_rectangle([x - w / 2, a, x + w / 2, b], int(min(w, b - a) * .25), fill=col, outline=BLK, width=4)
        d.line([(x + w / 2, (a + b) / 2), (x + w / 2 + w * .25, (a + b) / 2 - seg * .1)], fill=BLK, width=4)
        if labels: d.text((x - w / 2 - 30, (a + b) / 2), str(k + 1), font=F(max(18, int(min(40, seg * .5)))), fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=BLK)

def pillow(d, x, y, w=140, col=(240, 240, 255), stripe=(150, 170, 230)):
    """Almohada (vista de lado, un poco aplastada); (x, y) = centro."""
    h = w * .45
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], int(h * .45), fill=col, outline=BLK, width=4)
    d.line([(x - w * .35, y), (x + w * .35, y)], fill=stripe, width=max(3, int(w * .05)))

def social_house(d, x, y, s=1.0, col=(240, 225, 190), bars=True, door=0.0, cobweb=False, tinaco=True, lit=False, num=None):
    """Casita de interés social de un piso vista de frente (block, azotea plana, tinaco, rejas). y = piso; ~320s de ancho.
    door 0..1 = qué tan abierta está la puerta (0 cerrada). cobweb: telarañas (casa abandonada). num: número de la casa."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    x0, x1, top = x - S(160), x + S(160), y - S(250)
    d.rectangle([x0, top, x1, y], fill=col, outline=BLK, width=W_(5))
    for k in range(1, 6):                                                    # hiladas de block
        d.line([(x0 + S(4), top + k * S(42)), (x1 - S(4), top + k * S(42))], fill=dk(col, .9), width=W_(2))
    d.rectangle([x0 - S(10), top - S(18), x1 + S(10), top], fill=dk(col, .85), outline=BLK, width=W_(4))   # pretil
    if tinaco:
        d.rounded_rectangle([x1 - S(110), top - S(95), x1 - S(30), top - S(18)], int(S(14)), fill=(40, 40, 45), outline=BLK, width=W_(4))
        d.rectangle([x1 - S(100), top - S(108), x1 - S(40), top - S(92)], fill=(40, 40, 45), outline=BLK, width=W_(3))
    # ventana con rejas
    wx0, wy0, wx1, wy1 = x0 + S(30), top + S(70), x0 + S(150), top + S(170)
    d.rectangle([wx0, wy0, wx1, wy1], fill=(255, 220, 120) if lit else (120, 170, 210), outline=BLK, width=W_(4))
    if bars:
        for k in range(1, 6): d.line([(wx0 + k * (wx1 - wx0) / 6, wy0), (wx0 + k * (wx1 - wx0) / 6, wy1)], fill=(50, 50, 55), width=W_(5))
        d.line([(wx0, (wy0 + wy1) / 2), (wx1, (wy0 + wy1) / 2)], fill=(50, 50, 55), width=W_(5))
    # puerta (se abre hacia adentro: se ve más angosta)
    dx0, dx1 = x1 - S(120), x1 - S(35)
    d.rectangle([dx0, top + S(80), dx1, y], fill=(40, 30, 30), outline=BLK, width=W_(4))
    dw = (dx1 - dx0) * (1 - .8 * door)
    d.rectangle([dx0, top + S(80), dx0 + dw, y], fill=(150, 90, 50), outline=BLK, width=W_(4))
    if door < .5: d.ellipse([dx0 + dw - S(18), top + S(165), dx0 + dw - S(8), top + S(175)], fill=(230, 200, 80))
    if num: d.text((x0 + S(90), top + S(210)), str(num), font=F(int(S(30))), fill=BLK, anchor="mm")
    if cobweb:
        for cx, cy, sx in ((x0, top, 1), (x1, top, -1)):
            for k in range(1, 4): d.arc([cx - S(30 * k), cy - S(30 * k), cx + S(30 * k), cy + S(30 * k)], 0 if sx > 0 else 90, 90 if sx > 0 else 180, fill=(235, 235, 240), width=W_(2))
            for a in (10, 45, 80): 
                import math as _m
                d.line([(cx, cy), (cx + sx * S(95) * _m.cos(_m.radians(a)), cy + S(95) * _m.sin(_m.radians(a)))], fill=(235, 235, 240), width=W_(2))

def delivery_bag(d, x, y, s=1.0, col=(240, 140, 40)):
    """Mochila térmica de repartidor (cubo sin marca); (x, y) = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rectangle([x - S(70), y - S(70), x + S(70), y + S(70)], fill=col, outline=BLK, width=W_(5))
    d.polygon([(x - S(70), y - S(70)), (x - S(40), y - S(95)), (x + S(100), y - S(95)), (x + S(70), y - S(70))], fill=dk(col, .85), outline=BLK)
    d.line([(x - S(40), y - S(10)), (x + S(40), y - S(10))], fill=WHITE, width=W_(8))

def lunchbox(d, x, y, s=1.0, col=(80, 140, 220)):
    """Lonchera; y = base, x = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.arc([x - S(30), y - S(105), x + S(30), y - S(55)], 180, 360, fill=BLK, width=W_(8))
    d.rounded_rectangle([x - S(60), y - S(80), x + S(60), y], int(S(12)), fill=col, outline=BLK, width=W_(4))
    d.line([(x - S(60), y - S(55)), (x + S(60), y - S(55))], fill=dk(col, .7), width=W_(4))

def sweat(d, x, y, t, s=1.0, n=2, col=(120, 190, 255)):
    """Gotas de sudor que caen junto a una cabeza en (x, y)."""
    for k in range(n):
        u = (t * 1.5 + k / n) % 1
        cx, cy = x + k * 22 * s, y + u * 50 * s
        d.polygon([(cx, cy - 14 * s), (cx - 8 * s, cy + 2 * s), (cx + 8 * s, cy + 2 * s)], fill=col)
        d.ellipse([cx - 8 * s, cy - 6 * s, cx + 8 * s, cy + 10 * s], fill=col, outline=BLK, width=2)

def bathroom_scale(d, x, y, s=1.0, text="", col=(235, 235, 240)):
    """Báscula de baño vista de frente; y = piso. text = lo que marca la pantallita. Devuelve la y de la superficie."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rounded_rectangle([x - S(230), y - S(70), x + S(230), y], int(S(24)), fill=col, outline=BLK, width=W_(5))
    d.rounded_rectangle([x - S(110), y - S(58), x + S(110), y - S(14)], int(S(8)), fill=(40, 60, 50), outline=BLK, width=W_(3))
    if text: d.text((x, y - S(36)), text, font=F(int(S(30))), fill=(120, 255, 150), anchor="mm")
    return y - S(70)

def atom_ball(d, x, y, r=40, kind="H"):
    """Bolita de átomo para animar fusión: H (hidrógeno, azul) o He (helio, naranja, más grande)."""
    col = (110, 170, 255) if kind == "H" else (255, 170, 70)
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=BLK, width=max(3, int(r * .1)))
    d.ellipse([x - r * .5, y - r * .6, x - r * .1, y - r * .2], fill=lc(col, WHITE, .5))
    d.text((x, y + r * .05), kind, font=F(int(r * .8)), fill=BLK, anchor="mm")

def light_bill(d, x, y, w=420, total="$4,850", title="RECIBO DE LUZ"):
    """Recibo de luz genérico (sin marca); (x, y) = esquina superior izquierda."""
    h = w * 1.35
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BLK, width=5)
    d.rectangle([x, y, x + w, y + w * .18], fill=(90, 160, 90), outline=BLK, width=5)
    d.text((x + w / 2, y + w * .09), title, font=F(int(w * .085)), fill=WHITE, anchor="mm")
    for k in range(5): d.line([(x + w * .1, y + w * (.3 + k * .12)), (x + w * (.9 - .2 * (k % 2)), y + w * (.3 + k * .12))], fill=(190, 190, 195), width=6)
    d.text((x + w * .1, y + h - w * .28), "TOTAL A PAGAR", font=F(int(w * .07)), fill=BLK, anchor="lm")
    d.text((x + w * .9, y + h - w * .14), total, font=F(int(w * .14)), fill=RED, anchor="rm")

def stock_pot(d, x, y, s=1.0, t=0.0, col=(170, 175, 185), liquid=(90, 150, 220), boil=True, part="all"):
    """Olla grande con asas, vista de frente un poco desde arriba; y = base. Devuelve (x, y_borde).
    Para meter algo ADENTRO (que se vea sumergido): stock_pot(..., part="back"), dibuja la cosa con su centro cerca
    de y_borde, y luego stock_pot(..., part="front") tapa la parte de abajo con el cuerpo de la olla."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    top = y - S(300)
    if part in ("all", "back"):
        for sx in (-1, 1): d.rounded_rectangle([x + sx * S(250) - S(40), top + S(50), x + sx * S(250) + S(40), top + S(80)], int(S(12)), fill=dk(col, .8), outline=BLK, width=W_(4))
        d.ellipse([x - S(240), top - S(40), x + S(240), top + S(40)], fill=dk(col, .7), outline=BLK, width=W_(6))
        d.ellipse([x - S(215), top - S(28), x + S(215), top + S(28)], fill=liquid)
    if part in ("all", "front"):
        body = [(x - S(240), top)] + [(x - S(240) * math.cos(a / 20 * math.pi), top + S(40) * math.sin(a / 20 * math.pi)) for a in range(21)] + [(x + S(240), top), (x + S(240), y - S(30)), (x + S(210), y), (x - S(210), y), (x - S(240), y - S(30))]
        d.polygon(body, fill=col, outline=BLK); d.line(body + [body[0]], fill=BLK, width=W_(6), joint="curve")
        d.arc([x - S(240), top - S(40), x + S(240), top + S(40)], 0, 180, fill=BLK, width=W_(6))
        if boil:
            import random as _r
            r = _r.Random(int(t * 8))
            for k in range(7):
                bx = x + r.choice((-1, 1)) * r.uniform(S(120), S(195)); by = top + r.uniform(-S(22), S(10)); br = S(r.uniform(10, 22))
                d.ellipse([bx - br, by - br, bx + br, by + br], outline=WHITE, width=W_(4))
        for k in range(3): d.line([(x - S(180) + k * S(180), top + S(120)), (x - S(140) + k * S(180), top + S(120))], fill=lc(col, WHITE, .5), width=W_(6))
    return x, top

def solar_panel(d, x, y, w=220, tilt=.35):
    """Panel solar inclinado (para azoteas); (x, y) = centro de la base."""
    h = w * .55
    pts = [(x - w / 2, y), (x + w / 2, y), (x + w / 2 - w * .12, y - h), (x - w / 2 + w * .12, y - h)]
    d.polygon(pts, fill=(40, 70, 140), outline=BLK); d.line(pts + [pts[0]], fill=BLK, width=4)
    for k in range(1, 4):
        u = k / 4
        d.line([(x - w / 2 + w * u, y), (x - w / 2 + w * .12 + (w - w * .24) * u, y - h)], fill=(150, 180, 230), width=3)
    for k in range(1, 3):
        v = k / 3
        d.line([(x - w / 2 + w * .12 * v, y - h * v), (x + w / 2 - w * .12 * v, y - h * v)], fill=(150, 180, 230), width=3)
    d.line([(x, y), (x, y + 18)], fill=(90, 90, 95), width=8)

def fried_egg(d, x, y, s=1.0):
    """Huevo estrellado visto desde arriba; (x, y) = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    pts = [(x + S(80 + 12 * math.sin(k * 1.7)) * math.cos(k / 12 * 2 * math.pi), y + S(55 + 10 * math.sin(k * 2.3)) * math.sin(k / 12 * 2 * math.pi)) for k in range(12)]
    d.polygon(pts, fill=WHITE, outline=BLK); d.line(pts + [pts[0]], fill=BLK, width=W_(3), joint="curve")
    d.ellipse([x - S(26), y - S(22), x + S(26), y + S(22)], fill=(250, 190, 40), outline=BLK, width=W_(3))
    d.ellipse([x - S(14), y - S(14), x - S(4), y - S(6)], fill=(255, 235, 150))

def greens_plate(d, x, y, s=1.0, egg=True, col=(70, 140, 60)):
    """Plato con verdura picada (chaya, espinaca…) y opcionalmente un huevo; y = base del plato."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.ellipse([x - S(200), y - S(60), x + S(200), y + S(10)], fill=WHITE, outline=BLK, width=W_(4))
    import random as _r
    r = _r.Random(4)
    for k in range(26):
        gx, gy = x + r.uniform(-S(140), S(140)), y - S(25) + r.uniform(-S(18), S(14))
        d.ellipse([gx - S(16), gy - S(9), gx + S(16), gy + S(9)], fill=col if k % 2 else dk(col, .8), outline=BLK, width=W_(2))
    if egg: fried_egg(d, x + S(40), y - S(40), .8 * s)

def water_jug(d, x, y, s=1.0, level=1.0):
    """Garrafón de agua de 20 L (azul transparente, sin marca); y = base."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    body = [x - S(70), y - S(230), x + S(70), y]
    d.rounded_rectangle(body, int(S(30)), fill=(190, 225, 250), outline=BLK, width=W_(5))
    if level > 0:
        d.rounded_rectangle([x - S(62), y - S(222) * level, x + S(62), y - S(8)], int(S(24)), fill=(110, 180, 240))
    for k in (1, 2): d.line([(x - S(70), y - S(230) * k / 3), (x + S(70), y - S(230) * k / 3)], fill=(90, 150, 210), width=W_(4))
    d.polygon([(x - S(40), y - S(230)), (x + S(40), y - S(230)), (x + S(20), y - S(275)), (x - S(20), y - S(275))], fill=(190, 225, 250), outline=BLK)
    d.rectangle([x - S(24), y - S(300), x + S(24), y - S(272)], fill=(60, 120, 220), outline=BLK, width=W_(4))
    d.line([(x - S(45), y - S(200)), (x - S(45), y - S(40))], fill=WHITE, width=W_(8))

def first_aid_kit(d, x, y, s=1.0, open_=False):
    """Botiquín blanco con cruz roja; y = base."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rounded_rectangle([x - S(130), y - S(160), x + S(130), y], int(S(18)), fill=WHITE, outline=BLK, width=W_(5))
    d.arc([x - S(45), y - S(205), x + S(45), y - S(130)], 180, 360, fill=BLK, width=W_(12))
    d.rectangle([x - S(20), y - S(130), x + S(20), y - S(30)], fill=RED); d.rectangle([x - S(55), y - S(100), x + S(55), y - S(60)], fill=RED)
    if open_:
        for k, col in enumerate(((240, 220, 180), (200, 230, 250), WHITE)):
            d.rounded_rectangle([x - S(110) + k * S(75), y - S(230) - k * S(10), x - S(50) + k * S(75), y - S(165)], int(S(8)), fill=col, outline=BLK, width=W_(3))

def battery_radio(d, x, y, s=1.0, t=0.0, on=True):
    """Radio de pilas con antena y bocina; y = base. on: ondas de sonido."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.line([(x + S(80), y - S(170)), (x + S(150), y - S(330))], fill=BLK, width=W_(6))
    d.rounded_rectangle([x - S(150), y - S(180), x + S(150), y], int(S(24)), fill=(200, 80, 60), outline=BLK, width=W_(5))
    d.ellipse([x - S(130), y - S(150), x - S(10), y - S(30)], fill=(60, 60, 65), outline=BLK, width=W_(4))
    for k in range(3): d.ellipse([x - S(70) - S(12) * (k + 1), y - S(90) - S(12) * (k + 1), x - S(70) + S(12) * (k + 1), y - S(90) + S(12) * (k + 1)], outline=(110, 110, 115), width=W_(3))
    d.rectangle([x + S(20), y - S(150), x + S(130), y - S(100)], fill=(250, 230, 150), outline=BLK, width=W_(3))
    d.line([(x + S(50 + 30 * math.sin(t)), y - S(150)), (x + S(50 + 30 * math.sin(t)), y - S(100))], fill=RED, width=W_(4))
    for k in range(2): d.ellipse([x + S(40) + k * S(55), y - S(80), x + S(80) + k * S(55), y - S(40)], fill=(60, 60, 65), outline=BLK, width=W_(3))
    if on:
        for k in range(3):
            r = S(95 + ((t * 80 + k * 27) % 80))
            d.arc([x - S(70) - r, y - S(90) - r, x - S(70) + r, y - S(90) + r], 150, 210, fill=WHITE, width=W_(6))

def flashlight(d, x, y, s=1.0, on=True, ang=0.0):
    """Linterna de mano apuntando a la derecha (ang en grados); (x, y) = centro del mango."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    P = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    if on:
        d.polygon([P(S(90), -S(30)), P(S(420), -S(140)), P(S(420), S(140)), P(S(90), S(30))], fill=(255, 245, 170))
    body = [P(-S(90), -S(22)), P(S(40), -S(22)), P(S(90), -S(40)), P(S(90), S(40)), P(S(40), S(22)), P(-S(90), S(22))]
    d.polygon(body, fill=(60, 60, 70), outline=BLK); d.line(body + [body[0]], fill=BLK, width=W_(4))
    d.line([P(S(88), -S(36)), P(S(88), S(36))], fill=(255, 250, 200), width=W_(8))

def card_terminal(d, x, y, s=1.0, text="SIN CONEXIÓN"):
    """Terminal de pago con tarjeta (sin marca); y = base. text = lo que dice la pantallita."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.rounded_rectangle([x - S(90), y - S(260), x + S(90), y], int(S(22)), fill=(60, 60, 70), outline=BLK, width=W_(5))
    d.rectangle([x - S(70), y - S(240), x + S(70), y - S(160)], fill=(160, 200, 160), outline=BLK, width=W_(3))
    d.text((x, y - S(200)), text, font=F(int(S(15))), fill=(150, 30, 30) if "SIN" in text else BLK, anchor="mm")
    for i in range(3):
        for j in range(3): d.rounded_rectangle([x - S(60) + j * S(43), y - S(140) + i * S(42), x - S(30) + j * S(43), y - S(112) + i * S(42)], int(S(6)), fill=(200, 200, 205), outline=BLK, width=W_(2))
    d.rectangle([x - S(60), y - S(275), x + S(60), y - S(255)], fill=(40, 40, 45))

def storm_cloud(d, x, y, s=1.0, t=0.0, mood="sly", rain=True):
    """Nube de tormenta con cara (huracán/tormenta personificada) y rayito; (x, y) = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    G = (110, 115, 135)
    if rain:
        for k in range(10):
            rx = x - S(200) + k * S(44); ry = y + S(120) + ((t * 300 + k * 37) % S(160))
            d.line([(rx, ry), (rx - S(10), ry + S(30))], fill=(120, 180, 240), width=W_(5))
    for dx, dy, r in ((-150, 20, 110), (-50, -50, 140), (80, -30, 130), (180, 30, 100), (20, 50, 130)):
        d.ellipse([x + S(dx) - S(r), y + S(dy) - S(r), x + S(dx) + S(r), y + S(dy) + S(r)], fill=G, outline=BLK, width=W_(5))
    for dx, dy, r in ((-150, 20, 104), (-50, -50, 134), (80, -30, 124), (180, 30, 94), (20, 50, 124)):
        d.ellipse([x + S(dx) - S(r), y + S(dy) - S(r), x + S(dx) + S(r), y + S(dy) + S(r)], fill=G)
    for sx in (-1, 1):
        ex, ey = x + sx * S(60), y - S(10)
        d.ellipse([ex - S(24), ey - S(24), ex + S(24), ey + S(24)], fill=WHITE, outline=BLK, width=W_(3)); d.ellipse([ex - S(10), ey - S(8), ex + S(10), ey + S(12)], fill=BLK)
        if mood == "sly": d.line([(ex - sx * S(30), ey - S(36)), (ex + sx * S(26), ey - S(26))], fill=BLK, width=W_(8))
    d.arc([x - S(50), y + S(10), x + S(50), y + S(70)], 20, 160, fill=BLK, width=W_(7))
    bolt = [(x + S(150), y + S(90)), (x + S(120), y + S(170)), (x + S(155), y + S(170)), (x + S(125), y + S(260)), (x + S(200), y + S(150)), (x + S(165), y + S(150)), (x + S(190), y + S(90))]
    d.polygon(bolt, fill=(255, 220, 60), outline=BLK)

def zombie_mask(d, x, y, s=1.0):
    """Máscara de zombi (cara verde con liga) — para el chiste de 'quitarse la máscara'; (x, y) = centro."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.ellipse([x - S(80), y - S(95), x + S(80), y + S(95)], fill=(130, 180, 110), outline=BLK, width=W_(5))
    for sx in (-1, 1):
        d.ellipse([x + sx * S(32) - S(20), y - S(30) - S(16), x + sx * S(32) + S(20), y - S(30) + S(16)], fill=BLK)
    d.rectangle([x - S(40), y + S(30), x + S(40), y + S(50)], fill=(60, 20, 20))
    for k in range(4): d.polygon([(x - S(40) + k * S(20), y + S(30)), (x - S(30) + k * S(20), y + S(42)), (x - S(20) + k * S(20), y + S(30))], fill=WHITE)
    d.line([(x - S(80), y), (x - S(130), y + S(20))], fill=BLK, width=W_(4))
