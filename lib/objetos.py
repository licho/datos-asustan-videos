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
