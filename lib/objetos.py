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
