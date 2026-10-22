"""Criaturas nuevas (cartoon). Se dibujan sobre img (no sobre d) cuando necesitan transparencia."""
import math
from PIL import Image, ImageDraw, ImageFilter
from .core import BLK, WHITE, RED, dk

def ghost_draw(d, x, y, s=1.0, t=0.0, mood="happy", tie=None, headset=False, col=(245, 248, 255), arms="down"):
    """Fantasma de sábana. (x, y) = centro del cuerpo. Alto ~420·s. mood: happy | scared | sad | smug."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    top, bot, hw = y - S(210), y + S(170), S(140)
    pts = []
    for k in range(41):                                   # cúpula
        a = math.pi + k / 40 * math.pi
        pts.append((x + math.cos(a) * hw, top + S(140) + math.sin(a) * S(140)))
    n = 8
    for k in range(n + 1):                                # orilla ondulada (de derecha a izquierda)
        u = 1 - k / n; px = x - hw + u * 2 * hw
        py = bot + (S(28) if k % 2 == 0 else -S(8)) + math.sin(t * 5 + k) * S(10)
        pts.append((px + S(18) * math.sin(t * 2), py))
    d.polygon(pts, fill=col, outline=BLK, width=W_(5))
    for side in (-1, 1):                                  # bracitos
        if arms == "up" and side > 0:
            d.ellipse([x + side * hw - S(30), y - S(120), x + side * hw + S(30), y - S(60)], fill=col, outline=BLK, width=W_(4))
        elif arms == "wave" and side > 0:
            wy = y - S(90) + math.sin(t * 10) * S(25)
            d.ellipse([x + hw - S(10), wy - S(30), x + hw + S(50), wy + S(30)], fill=col, outline=BLK, width=W_(4))
        else:
            d.ellipse([x + side * hw - S(30), y - S(10), x + side * hw + S(30), y + S(50)], fill=col, outline=BLK, width=W_(4))
    ey = y - S(90)
    for side in (-1, 1):
        ex = x + side * S(48)
        if mood == "scared":
            d.ellipse([ex - S(26), ey - S(34), ex + S(26), ey + S(34)], fill=WHITE, outline=BLK, width=W_(4)); d.ellipse([ex - S(9), ey - S(9), ex + S(9), ey + S(9)], fill=BLK)
        elif mood == "smug":
            d.chord([ex - S(24), ey - S(30), ex + S(24), ey + S(30)], 0, 180, fill=BLK)
        else:
            d.ellipse([ex - S(20), ey - S(30), ex + S(20), ey + S(30)], fill=(40, 40, 60))
            d.ellipse([ex - S(9) + S(6), ey - S(20), ex + S(3) + S(6), ey - S(6)], fill=WHITE)
    my = y - S(10)
    if mood == "scared": d.ellipse([x - S(24), my - S(20), x + S(24), my + S(40)], fill=(40, 40, 60))
    elif mood == "sad": d.arc([x - S(40), my, x + S(40), my + S(50)], 200, 340, fill=BLK, width=W_(6))
    else: d.arc([x - S(45), my - S(40), x + S(45), my + S(20)], 20, 160, fill=BLK, width=W_(6))
    if tie:
        d.polygon([(x - S(18), y + S(20)), (x + S(18), y + S(20)), (x, y + S(45))], fill=tie, outline=BLK)
        d.polygon([(x - S(12), y + S(42)), (x + S(12), y + S(42)), (x + S(20), y + S(140)), (x, y + S(165)), (x - S(20), y + S(140))], fill=tie, outline=BLK)
    if headset:
        d.arc([x - hw * .9, top + S(10), x + hw * .9, y + S(20)], 200, 340, fill=(50, 50, 55), width=W_(12))
        d.ellipse([x - hw * .9 - S(22), y - S(110), x - hw * .9 + S(22), y - S(50)], fill=(50, 50, 55))
        d.line([(x - hw * .85, y - S(60)), (x - S(40), y + S(5))], fill=(50, 50, 55), width=W_(6))

def ghost(img, x, y, s=1.0, t=0.0, alpha=1.0, pixel=0, bob=True, **kw):
    """Pega un fantasma con transparencia (alpha 0..1) y opcionalmente pixelado (pixel = tamaño de bloque)."""
    if alpha <= 0.01: return ImageDraw.Draw(img)
    if bob: y += math.sin(t * 2.2) * 18 * s
    size = int(560 * s) + 40
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ghost_draw(ImageDraw.Draw(layer), size / 2, size / 2, s, t, **kw)
    if pixel > 1:
        small = layer.resize((max(1, size // pixel), max(1, size // pixel)), Image.NEAREST); layer = small.resize((size, size), Image.NEAREST)
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha)); layer.putalpha(a)
    img.paste(layer, (int(x - size / 2), int(y - size / 2)), layer)
    return ImageDraw.Draw(img)

def mummy(d, x, y, s=1.0, t=0.0, arms="forward", mood="neutral", trail=0.0, hat=None):
    """Momia de pie; y = pies. arms: forward | down | wave | up. mood: neutral | happy | scared. trail = venda suelta (0..1)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    B, L = (235, 225, 195), (190, 175, 140)
    d.ellipse([x - S(120), y - S(14), x + S(120), y + S(14)], fill=(70, 70, 75))
    for sx in (-1, 1):                                              # piernas
        d.rounded_rectangle([x + sx * S(12) - (S(62) if sx < 0 else 0), y - S(200), x + sx * S(12) + (S(62) if sx > 0 else 0), y], int(S(20)), fill=B, outline=BLK, width=W_(4))
    def arm(hx, hy, sx):
        d.line([(x + sx * S(95), y - S(370)), (hx, hy)], fill=BLK, width=W_(52), joint="curve"); d.line([(x + sx * S(95), y - S(370)), (hx, hy)], fill=B, width=W_(42), joint="curve")
        for k in range(1, 4):
            u = k / 4; px, py = x + sx * S(95) + (hx - x - sx * S(95)) * u, y - S(370) + (hy - y + S(370)) * u
            d.line([(px - S(18), py - S(10)), (px + S(18), py + S(10))], fill=L, width=W_(4))
    wy = math.sin(t * 9) * S(30)
    poses = {"forward": ((x - S(40), y - S(420)), (x + S(250), y - S(380))), "down": ((x - S(140), y - S(200)), (x + S(140), y - S(200))),
             "wave": ((x - S(140), y - S(200)), (x + S(210), y - S(560) + wy)), "up": ((x - S(190), y - S(560)), (x + S(190), y - S(560)))}
    (lx, ly), (rx, ry) = poses.get(arms, poses["down"])
    arm(lx, ly, -1)
    d.rounded_rectangle([x - S(110), y - S(430), x + S(110), y - S(180)], int(S(50)), fill=B, outline=BLK, width=W_(5))
    for k in range(7):                                              # vendas del torso
        yy = y - S(410) + k * S(34)
        d.line([(x - S(100), yy + S(14)), (x + S(100), yy - S(6))], fill=L, width=W_(5))
    hy = y - S(520)
    d.ellipse([x - S(95), hy - S(100), x + S(95), hy + S(95)], fill=B, outline=BLK, width=W_(5))
    for k in range(5):
        yy = hy - S(80) + k * S(36)
        d.line([(x - S(85), yy), (x + S(85), yy + S(12))], fill=L, width=W_(5))
    d.rectangle([x - S(70), hy - S(30), x + S(70), hy + S(10)], fill=(40, 30, 30))      # rendija de los ojos
    er = S(14) if mood != "scared" else S(18)
    for sx in (-1, 1):
        d.ellipse([x + sx * S(32) - er, hy - S(10) - er, x + sx * S(32) + er, hy - S(10) + er], fill=(250, 230, 120) if mood != "scared" else WHITE)
        if mood == "scared": d.ellipse([x + sx * S(32) - S(6), hy - S(16), x + sx * S(32) + S(6), hy - S(4)], fill=BLK)
    if mood == "happy": d.arc([x - S(35), hy + S(25), x + S(35), hy + S(60)], 20, 160, fill=BLK, width=W_(5))
    elif mood == "scared": d.ellipse([x - S(14), hy + S(30), x + S(14), hy + S(62)], fill=BLK)
    arm(rx, ry, 1)
    if trail > 0:
        pts = [(x - S(60), y - S(260))]
        for k in range(1, 8):
            u = k / 7; pts.append((x - S(60) - u * S(420) * trail, y - S(260) + u * S(250) + math.sin(t * 4 + u * 6) * S(18)))
        d.line(pts, fill=BLK, width=W_(26), joint="curve"); d.line(pts, fill=B, width=W_(18), joint="curve")
    if hat == "nurse":
        d.polygon([(x - S(80), hy - S(80)), (x + S(80), hy - S(80)), (x + S(60), hy - S(150)), (x - S(60), hy - S(150))], fill=WHITE, outline=BLK)
        d.rectangle([x - S(8), hy - S(140), x + S(8), hy - S(95)], fill=RED); d.rectangle([x - S(22), hy - S(126), x + S(22), hy - S(110)], fill=RED)

def brain(d, x, y, s=1.0, t=0.0, mood="happy", eyes_open=True, broom=False):
    """Cerebro con cara (x, y = centro)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); P = (245, 160, 180)
    d.ellipse([x - S(200), y - S(150), x + S(200), y + S(140)], fill=P, outline=BLK, width=W_(6))
    d.line([(x, y - S(140)), (x, y + S(120))], fill=dk(P, .75), width=W_(6))
    for k, (ax, ay) in enumerate(((-120, -70), (-60, -100), (60, -95), (120, -60), (-140, 20), (140, 30), (-70, 80), (70, 85))):
        d.arc([x + S(ax) - S(40), y + S(ay) - S(25), x + S(ax) + S(40), y + S(ay) + S(25)], 200 if k % 2 else 20, 340 if k % 2 else 160, fill=dk(P, .75), width=W_(5))
    for sx in (-1, 1):
        ex = x + sx * S(65)
        if eyes_open:
            d.ellipse([ex - S(30), y - S(30), ex + S(30), y + S(30)], fill=WHITE, outline=BLK, width=W_(4)); d.ellipse([ex - S(12), y - S(12), ex + S(12), y + S(12)], fill=BLK)
        else:
            d.line([(ex - S(28), y), (ex + S(28), y)], fill=BLK, width=W_(6))
    if mood == "happy": d.arc([x - S(45), y + S(30), x + S(45), y + S(90)], 20, 160, fill=BLK, width=W_(5))
    else: d.arc([x - S(40), y + S(55), x + S(40), y + S(95)], 200, 340, fill=BLK, width=W_(5))
    if broom:
        bx = x + S(230); d.line([(bx, y - S(120)), (bx - S(40), y + S(200))], fill=(140, 95, 55), width=W_(14))
        d.polygon([(bx - S(90), y + S(190)), (bx + S(10), y + S(190)), (bx + S(30), y + S(290)), (bx - S(110), y + S(290))], fill=(230, 190, 80), outline=BLK)

def rat(d, x, y, s=1.0, t=0.0, flip=False):
    """Rata de laboratorio de lado; y = piso."""
    S = lambda v: v * s; f = -1 if flip else 1; W_ = lambda v: max(2, int(v * s)); G = (235, 235, 240)
    pts = [(x - f * S(120), y - S(30))]
    for k in range(1, 8): pts.append((x - f * S(120 + k * 25), y - S(30) + math.sin(t * 4 + k) * S(12) - k * S(4)))
    d.line(pts, fill=(240, 170, 180), width=W_(8))
    d.ellipse([x - S(130), y - S(110), x + S(90), y], fill=G, outline=BLK, width=W_(4))
    hx = x + f * S(110)
    d.ellipse([hx - S(60), y - S(120), hx + S(60), y - S(30)], fill=G, outline=BLK, width=W_(4))
    d.ellipse([hx - f * S(20) - S(30), y - S(165), hx - f * S(20) + S(30), y - S(100)], fill=(250, 190, 200), outline=BLK, width=W_(3))
    d.ellipse([hx + f * S(52) - S(9), y - S(85), hx + f * S(52) + S(9), y - S(67)], fill=(240, 120, 150))
    d.ellipse([hx + f * S(10) - S(9), y - S(98), hx + f * S(10) + S(9), y - S(80)], fill=(200, 40, 60))
    for dx in (-80, 40): d.ellipse([x + S(dx) - S(14), y - S(10), x + S(dx) + S(14), y + S(4)], fill=(240, 170, 180))

def heart_face(d, x, y, s=1.0, t=0.0):
    """Corazón con cara, latiendo rápido (x, y = centro)."""
    S = lambda v: v * s * (1 + .08 * abs(math.sin(t * 14)))
    d.ellipse([x - S(110), y - S(90), x, y + S(20)], fill=RED, outline=BLK, width=5); d.ellipse([x, y - S(90), x + S(110), y + S(20)], fill=RED, outline=BLK, width=5)
    d.polygon([(x - S(106), y - S(20)), (x + S(106), y - S(20)), (x, y + S(120))], fill=RED, outline=BLK)
    d.rectangle([x - S(100), y - S(40), x + S(100), y - S(10)], fill=RED)
    for sx in (-1, 1): d.ellipse([x + sx * S(35) - S(16), y - S(40) - S(16), x + sx * S(35) + S(16), y - S(40) + S(16)], fill=WHITE, outline=BLK, width=3); d.ellipse([x + sx * S(35) - S(6), y - S(46), x + sx * S(35) + S(6), y - S(34)], fill=BLK)
    d.ellipse([x - S(14), y + S(5), x + S(14), y + S(35)], fill=(80, 10, 20))

def rat_skeleton(d, x, y, s=1.0):
    """Esqueleto de rata de caricatura (huesitos blancos, sin sangre). y = piso, mira a la derecha."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); B = (245, 242, 230)
    d.line([(x - S(110), y - S(40)), (x - S(200), y - S(20)), (x - S(260), y - S(45))], fill=BLK, width=W_(10), joint="curve")
    d.line([(x - S(110), y - S(40)), (x - S(200), y - S(20)), (x - S(260), y - S(45))], fill=B, width=W_(5), joint="curve")
    for k in range(7):
        rx = x - S(90) + k * S(26)
        d.arc([rx - S(16), y - S(95), rx + S(16), y - S(15)], 200, 340, fill=BLK, width=W_(9)); d.arc([rx - S(16), y - S(95), rx + S(16), y - S(15)], 200, 340, fill=B, width=W_(5))
    d.line([(x - S(110), y - S(75)), (x + S(80), y - S(75))], fill=BLK, width=W_(14)); d.line([(x - S(110), y - S(75)), (x + S(80), y - S(75))], fill=B, width=W_(8))
    for dx in (-80, 40):
        d.line([(x + S(dx), y - S(70)), (x + S(dx), y)], fill=BLK, width=W_(9)); d.line([(x + S(dx), y - S(70)), (x + S(dx), y)], fill=B, width=W_(4))
    d.ellipse([x + S(60), y - S(115), x + S(160), y - S(45)], fill=B, outline=BLK, width=W_(4))
    d.ellipse([x + S(100), y - S(100), x + S(125), y - S(78)], fill=BLK)
    d.polygon([(x + S(150), y - S(95)), (x + S(195), y - S(70)), (x + S(150), y - S(60))], fill=B, outline=BLK)

def llorona(d, x, y, s=1.0, t=0.0, mood="wail", arms="down"):
    """La Llorona (caricatura, no gore): vestido blanco largo que flota, velo, cabello negro largo y lágrimas.
    y = orilla del vestido (flota sola, sin pies). mood: wail (llora con boca abierta) | happy | neutral | sad.
    arms: down | up (lamento) | mic (sostiene micrófono, mano en x+170s, y-420s) | point.
    Boca en (x, y - 545·s), radio de cabeza ≈ 95·s (para say)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    DR, SH, HAIR, SK = (245, 247, 252), (205, 215, 235), (25, 22, 35), (225, 232, 240)
    y = y + math.sin(t * 2.2) * S(10)
    hy = y - S(560)
    VE = (232, 238, 250)
    veil = [(x - S(95), hy - S(95)), (x + S(95), hy - S(95)), (x + S(140), y - S(330) + math.sin(t * 3) * S(8)), (x - S(140), y - S(330) - math.sin(t * 3) * S(8))]
    d.polygon(veil, fill=VE, outline=BLK); d.line(veil + [veil[0]], fill=BLK, width=W_(4))
    hem = []
    for k in range(13):
        u = k / 12; hx_ = x - S(170) + u * S(340); hy_ = y + math.sin(t * 4 + u * 9) * S(14) - (S(18) if k % 2 else 0)
        hem.append((hx_, hy_))
    d.polygon([(x - S(70), y - S(440)), (x + S(70), y - S(440))] + hem[::-1], fill=DR)
    d.line([(x - S(70), y - S(440))] + hem + [(x + S(70), y - S(440))], fill=BLK, width=W_(5))
    for k in range(4): d.line([(x - S(40) + k * S(27), y - S(380)), (x - S(80) + k * S(55), y - S(20))], fill=SH, width=W_(5))
    for sx in (-1, 1):
        d.polygon([(x + sx * S(60), hy - S(70)), (x + sx * S(100), hy - S(40)), (x + sx * S(95), y - S(380)), (x + sx * S(55), y - S(410))], fill=HAIR)
    def arm(hx, hy2, sx):
        sh = (x + sx * S(65), y - S(420))
        d.line([sh, (hx, hy2)], fill=BLK, width=W_(44)); d.line([sh, (hx, hy2)], fill=DR, width=W_(36))
        d.ellipse([hx - S(20), hy2 - S(20), hx + S(20), hy2 + S(20)], fill=SK, outline=BLK, width=W_(3))
    if arms == "up": arm(x - S(150), hy - S(40), -1); arm(x + S(150), hy - S(40), 1)
    elif arms == "mic":
        arm(x - S(120), y - S(230), -1); arm(x + S(140), y - S(470), 1); microphone(d, x + S(140), y - S(470), s * .9)
    elif arms == "point": arm(x - S(120), y - S(230), -1); arm(x + S(230), y - S(470), 1)
    else: arm(x - S(120), y - S(230), -1); arm(x + S(120), y - S(230), 1)
    d.ellipse([x - S(78), hy - S(90), x + S(78), hy + S(85)], fill=SK, outline=BLK, width=W_(4))
    d.chord([x - S(88), hy - S(105), x + S(88), hy + S(5)], 180, 360, fill=HAIR)
    d.polygon([(x - S(88), hy - S(50)), (x - S(40), hy - S(55)), (x - S(78), hy + S(60))], fill=HAIR)
    d.polygon([(x + S(88), hy - S(50)), (x + S(40), hy - S(55)), (x + S(78), hy + S(60))], fill=HAIR)
    d.arc([x - S(98), hy - S(112), x + S(98), hy + S(20)], 190, 350, fill=VE, width=W_(16)); d.arc([x - S(106), hy - S(120), x + S(106), hy + S(28)], 190, 350, fill=BLK, width=W_(4))
    for sx in (-1, 1):
        ex, ey = x + sx * S(30), hy + S(5)
        if mood in ("wail", "sad"):
            d.arc([ex - S(18), ey - S(12), ex + S(18), ey + S(14)], 200, 340, fill=BLK, width=W_(6))
            d.line([(ex - sx * S(18), ey - S(28)), (ex + sx * S(16), ey - S(20))], fill=HAIR, width=W_(6))
            ty = (t * 160 + (sx + 1) * 20) % S(110)
            d.line([(ex, ey + S(10)), (ex + sx * S(4), ey + S(10) + ty)], fill=(110, 180, 255), width=W_(9))
            d.ellipse([ex + sx * S(4) - S(9), ey + S(4) + ty, ex + sx * S(4) + S(9), ey + S(22) + ty], fill=(110, 180, 255))
        else:
            d.ellipse([ex - S(15), ey - S(14), ex + S(15), ey + S(14)], fill=WHITE, outline=BLK, width=W_(3)); d.ellipse([ex - S(7), ey - S(7), ex + S(7), ey + S(7)], fill=BLK)
    mx, my = x, y - S(510)
    if mood == "wail":
        o = S(22) + math.sin(t * 7) * S(5); d.ellipse([mx - S(18), my - o, mx + S(18), my + o], fill=(60, 20, 40), outline=BLK, width=W_(3))
    elif mood == "happy": d.arc([mx - S(28), my - S(22), mx + S(28), my + S(14)], 20, 160, fill=BLK, width=W_(6))
    elif mood == "sad": d.arc([mx - S(24), my - S(4), mx + S(24), my + S(26)], 200, 340, fill=BLK, width=W_(6))
    else: d.line([(mx - S(18), my), (mx + S(18), my)], fill=BLK, width=W_(5))

def microphone(d, x, y, s=1.0):
    """Micrófono de mano; (x, y) = donde se agarra."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.line([(x, y + S(20)), (x - S(10), y - S(60))], fill=BLK, width=W_(22)); d.line([(x, y + S(20)), (x - S(10), y - S(60))], fill=(60, 60, 70), width=W_(14))
    d.ellipse([x - S(42), y - S(110), x + S(22), y - S(46)], fill=(170, 175, 185), outline=BLK, width=W_(4))
    for k in range(3): d.line([(x - S(36), y - S(95) + k * S(14)), (x + S(14), y - S(95) + k * S(14))], fill=(120, 125, 135), width=W_(3))

def elf(d, x, y, s=1.0, t=0.0, mood="happy", arms="down", col=(60, 150, 80), hat=None, sweater=False, flip=False):
    """Duende navideño (caricatura): gorro puntiagudo con cascabel, orejas puntiagudas, túnica con cinturón,
    medias de rayas y zapatos curvos. y = pies; alto ≈ 470·s. Manos en (x±115s, y-190s) con arms='down'.
    mood: happy | sleepy (ojeras, resaca) | scared | sad | sly. arms: down | up | hold (al frente) | scratch | point.
    sweater=True: suéter navideño rojo con zigzag (pica). hat: color del gorro (por defecto = col)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); f = -1 if flip else 1
    SK, CH = (250, 205, 170), (240, 140, 140)
    hat = hat or col; body = (200, 45, 55) if sweater else col
    d.ellipse([x - S(95), y - S(12), x + S(95), y + S(12)], fill=(70, 72, 75))
    for sx in (-1, 1):
        lx = x + sx * S(32)
        d.rectangle([lx - S(16), y - S(150), lx + S(16), y - S(30)], fill=WHITE, outline=BLK, width=W_(3))
        for k in range(4): d.rectangle([lx - S(16), y - S(140) + k * S(30), lx + S(16), y - S(126) + k * S(30)], fill=(210, 40, 50))
        d.polygon([(lx - S(22), y - S(35)), (lx + sx * S(40), y - S(35)), (lx + sx * S(62), y - S(60)), (lx + sx * S(55), y), (lx - S(22), y)], fill=(120, 70, 40), outline=BLK)
    def arm(hx, hy, sx):
        sh = (x + sx * S(62), y - S(275))
        d.line([sh, (hx, hy)], fill=BLK, width=W_(36)); d.line([sh, (hx, hy)], fill=body, width=W_(28))
        d.ellipse([hx - S(17), hy - S(17), hx + S(17), hy + S(17)], fill=SK, outline=BLK, width=W_(3))
    hands = {"down": ((x - S(105), y - S(170)), (x + S(105), y - S(170))), "up": ((x - S(130), y - S(420)), (x + S(130), y - S(420))),
             "hold": ((x - S(55), y - S(200)), (x + S(55), y - S(200))), "scratch": ((x - S(40), y - S(260)), (x + S(130), y - S(330))),
             "point": ((x - S(105), y - S(170)), (x + f * S(160), y - S(300)))}[arms]
    if arms not in ("hold", "scratch"): arm(*hands[0], -1); arm(*hands[1], 1)
    tun = [(x - S(70), y - S(300)), (x + S(70), y - S(300)), (x + S(95), y - S(140)), (x + S(60), y - S(115)), (x + S(30), y - S(140)), (x, y - S(112)), (x - S(30), y - S(140)), (x - S(60), y - S(115)), (x - S(95), y - S(140))]
    d.polygon(tun, fill=body, outline=BLK); d.line(tun + [tun[0]], fill=BLK, width=W_(4))
    if sweater:
        for k in range(6):
            zx = x - S(60) + k * S(24); d.line([(zx, y - S(225)), (zx + S(12), y - S(205)), (zx + S(24), y - S(225))], fill=WHITE, width=W_(5))
        d.polygon([(x - S(10), y - S(270)), (x + S(10), y - S(270)), (x, y - S(250))], fill=(240, 200, 60))
        if mood != "happy":
            for k in range(5):
                ax, ay = x + S(((k * 37) % 120) - 60), y - S(160 + (k * 23) % 110)
                d.line([(ax - S(8), ay - S(8)), (ax + S(8), ay + S(8))], fill=(255, 230, 120), width=W_(3)); d.line([(ax + S(8), ay - S(8)), (ax - S(8), ay + S(8))], fill=(255, 230, 120), width=W_(3))
    else:
        d.rectangle([x - S(80), y - S(200), x + S(80), y - S(175)], fill=(40, 30, 25), outline=BLK, width=W_(2))
        d.rectangle([x - S(18), y - S(206), x + S(18), y - S(169)], fill=(240, 200, 60), outline=BLK, width=W_(3))
    if arms in ("hold", "scratch"): arm(*hands[0], -1); arm(*hands[1], 1)
    hx, hy = x, y - S(380)
    for sx in (-1, 1):
        ear = [(hx + sx * S(70), hy - S(20)), (hx + sx * S(135), hy - S(55)), (hx + sx * S(78), hy + S(25))]
        d.polygon(ear, fill=SK, outline=BLK); d.line(ear + [ear[0]], fill=BLK, width=W_(3))
    d.ellipse([hx - S(80), hy - S(85), hx + S(80), hy + S(78)], fill=SK, outline=BLK, width=W_(4))
    tipx = hx - f * S(110) + math.sin(t * 3) * S(8)
    hatp = [(hx - S(88), hy - S(40)), (hx - S(30), hy - S(150)), (tipx, hy - S(205)), (hx + S(60), hy - S(110)), (hx + S(90), hy - S(40))]
    d.polygon(hatp, fill=hat, outline=BLK); d.line(hatp + [hatp[0]], fill=BLK, width=W_(4))
    d.rounded_rectangle([hx - S(95), hy - S(55), hx + S(95), hy - S(25)], int(S(12)), fill=WHITE, outline=BLK, width=W_(3))
    d.ellipse([tipx - S(18), hy - S(223), tipx + S(18), hy - S(187)], fill=(240, 200, 60), outline=BLK, width=W_(3))
    for sx in (-1, 1):
        ex, ey = hx + sx * S(30), hy + S(5)
        if mood == "sleepy":
            d.chord([ex - S(16), ey - S(10), ex + S(16), ey + S(16)], 0, 180, fill=BLK)
            d.arc([ex - S(18), ey + S(8), ex + S(18), ey + S(30)], 20, 160, fill=(150, 110, 160), width=W_(4))
        else:
            r = S(19) if mood == "scared" else S(14)
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=WHITE, outline=BLK, width=W_(3))
            d.ellipse([ex - S(6) + (f * S(3) if mood == "sly" else 0), ey - S(6), ex + S(6) + (f * S(3) if mood == "sly" else 0), ey + S(6)], fill=BLK)
            if mood == "sly": d.line([(ex - S(16), ey - S(14)), (ex + S(16), ey - S(8))], fill=BLK, width=W_(5))
        d.ellipse([hx + sx * S(52) - S(14), hy + S(25), hx + sx * S(52) + S(14), hy + S(43)], fill=CH)
    d.ellipse([hx - S(12), hy + S(14), hx + S(12), hy + S(36)], fill=(235, 150, 130), outline=BLK, width=W_(2))
    my = hy + S(52)
    if mood in ("happy", "sly"): d.arc([hx - S(28), my - S(18), hx + S(28), my + S(14)], 20, 160, fill=BLK, width=W_(5))
    elif mood == "scared": d.ellipse([hx - S(12), my - S(6), hx + S(12), my + S(18)], fill=(80, 20, 30), outline=BLK, width=W_(3))
    elif mood == "sad": d.arc([hx - S(22), my, hx + S(22), my + S(24)], 200, 340, fill=BLK, width=W_(5))
    else: d.line([(hx - S(18), my + S(4)), (hx + S(14), my + S(8))], fill=BLK, width=W_(5))

def krampus(d, x, y, s=1.0, t=0.0, mood="grin", arms="down", sack=False, rods=True, mask=False, flip=False, torch=False):
    """Krampus (caricatura, no gore): peludo café oscuro, cuernos curvos, lengua roja larga, un pie humano y una pezuña.
    y = pies; alto ≈ 720·s. mood: grin | tired | suspicious | stop (frenado/sorprendido). arms: down | up | hold (taza al frente) | stop.
    sack=True: costal al hombro que se mueve solo. rods: manojo de varas en la mano. mask=True: máscara de madera (desfile)."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s)); f = -1 if flip else 1
    FUR, FUR2, SKN = (70, 45, 35), (95, 62, 45), (120, 40, 45)
    d.ellipse([x - S(140), y - S(16), x + S(140), y + S(16)], fill=(50, 50, 55))
    # piernas: izquierda pezuña, derecha pie humano descalzo
    d.polygon([(x - S(90), y - S(260)), (x - S(25), y - S(260)), (x - S(35), y - S(40)), (x - S(85), y - S(40))], fill=FUR, outline=BLK)
    d.polygon([(x - S(95), y - S(45)), (x - S(30), y - S(45)), (x - S(22), y), (x - S(102), y)], fill=(40, 30, 28), outline=BLK)
    d.line([(x - S(62), y - S(40)), (x - S(62), y)], fill=BLK, width=W_(4))
    d.polygon([(x + S(25), y - S(260)), (x + S(90), y - S(260)), (x + S(80), y - S(55)), (x + S(35), y - S(55))], fill=FUR, outline=BLK)
    d.rounded_rectangle([x + S(30), y - S(60), x + S(115), y], int(S(18)), fill=(240, 194, 160), outline=BLK, width=W_(3))
    for k in range(4): d.ellipse([x + S(85) + k * S(8), y - S(20) - k * S(2), x + S(97) + k * S(8), y - S(8) - k * S(2)], fill=(240, 194, 160), outline=BLK, width=W_(2))
    # costal (atrás)
    if sack:
        wob = math.sin(t * 7) * S(10)
        d.ellipse([x - f * S(250) - S(110) + wob, y - S(600), x - f * S(250) + S(110) + wob, y - S(330)], fill=(150, 120, 80), outline=BLK, width=W_(5))
        d.line([(x - f * S(250) + wob, y - S(600)), (x - f * S(80), y - S(560))], fill=(110, 85, 55), width=W_(14))
    # cuerpo peludo
    body = [(x - S(130), y - S(520)), (x + S(130), y - S(520)), (x + S(120), y - S(240)), (x - S(120), y - S(240))]
    d.polygon(body, fill=FUR, outline=BLK); d.line(body + [body[0]], fill=BLK, width=W_(5))
    for k in range(10):
        px = x - S(120) + k * S(26); d.polygon([(px, y - S(250)), (px + S(13), y - S(215)), (px + S(26), y - S(250))], fill=FUR)
    for k in range(9):
        fx = x - S(100) + (k % 3) * S(80) + (k // 3) * S(12); fy = y - S(480) + (k // 3) * S(80)
        d.arc([fx, fy, fx + S(40), fy + S(40)], 200, 340, fill=FUR2, width=W_(6))
    # cadena cruzada
    for k in range(9):
        u = k / 8; cx_, cy_ = x - S(120) + u * S(240), y - S(500) + u * S(230)
        d.ellipse([cx_ - S(16), cy_ - S(10), cx_ + S(16), cy_ + S(10)], outline=(150, 150, 160), width=W_(6))
    def arm(hx, hy, sx):
        sh = (x + sx * S(120), y - S(480))
        d.line([sh, (hx, hy)], fill=BLK, width=W_(62)); d.line([sh, (hx, hy)], fill=FUR, width=W_(52))
        d.ellipse([hx - S(32), hy - S(30), hx + S(32), hy + S(30)], fill=SKN, outline=BLK, width=W_(4))
        for k in (-1, 0, 1): d.polygon([(hx + k * S(18) - S(6), hy + S(22)), (hx + k * S(18) + S(6), hy + S(22)), (hx + k * S(22), hy + S(46))], fill=(230, 225, 210), outline=BLK)
    pose = {"down": ((x - S(190), y - S(270)), (x + S(190), y - S(270))), "up": ((x - S(230), y - S(700)), (x + S(230), y - S(700))),
            "hold": ((x - S(80), y - S(330)), (x + S(80), y - S(330))), "stop": ((x - S(190), y - S(270)), (x + f * S(260), y - S(520)))}[arms]
    arm(*pose[0], -1); arm(*pose[1], 1)
    if rods and arms != "hold":
        hx, hy = pose[0]
        for k in range(5): d.line([(hx - S(10) + k * S(5), hy + S(10)), (hx - S(60) + k * S(25), hy + S(200))], fill=(140, 110, 70), width=W_(7))
        d.rectangle([hx - S(16), hy - S(4), hx + S(20), hy + S(26)], fill=(200, 40, 40), outline=BLK, width=W_(3))
    if torch:
        hx, hy = pose[1]
        d.line([(hx, hy), (hx + S(10), hy - S(180))], fill=(110, 75, 45), width=W_(16))
        fl = math.sin(t * 12) * S(8)
        d.polygon([(hx - S(20), hy - S(175)), (hx + S(10) + fl, hy - S(270)), (hx + S(40), hy - S(175))], fill=(250, 160, 40), outline=(220, 90, 30))
    # cabeza de cabra
    hx, hy = x, y - S(600)
    for sx in (-1, 1):
        horn = [(hx + sx * S(50), hy - S(70)), (hx + sx * S(110), hy - S(170)), (hx + sx * S(190), hy - S(190)), (hx + sx * S(170), hy - S(150)), (hx + sx * S(115), hy - S(120)), (hx + sx * S(85), hy - S(55))]
        d.polygon(horn, fill=(215, 200, 170), outline=BLK); d.line(horn + [horn[0]], fill=BLK, width=W_(4))
        d.polygon([(hx + sx * S(90), hy - S(20)), (hx + sx * S(170), hy - S(10)), (hx + sx * S(100), hy + S(25))], fill=FUR2, outline=BLK)
    face = (180, 150, 120) if mask else SKN
    d.ellipse([hx - S(100), hy - S(110), hx + S(100), hy + S(110)], fill=FUR, outline=BLK, width=W_(5))
    d.ellipse([hx - S(70), hy - S(70), hx + S(70), hy + S(95)], fill=face, outline=BLK, width=W_(4))
    if mask:
        for k in range(3): d.arc([hx - S(55), hy - S(50) + k * S(30), hx + S(55), hy - S(10) + k * S(30)], 200, 340, fill=(140, 110, 80), width=W_(4))
    # ojos
    for sx in (-1, 1):
        ex, ey = hx + sx * S(32), hy - S(15)
        if mood == "tired":
            d.chord([ex - S(20), ey - S(8), ex + S(20), ey + S(18)], 0, 180, fill=(255, 220, 80), outline=BLK)
            d.arc([ex - S(22), ey + S(10), ex + S(22), ey + S(32)], 20, 160, fill=(70, 30, 60), width=W_(5))
        else:
            r = S(24) if mood == "stop" else S(19)
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 220, 80), outline=BLK, width=W_(4))
            pr = S(6) if mood == "suspicious" else S(8)
            d.rectangle([ex - pr / 2, ey - S(14), ex + pr / 2, ey + S(14)], fill=BLK)
            if mood == "suspicious": d.line([(ex - S(24), ey - S(8)), (ex + S(24), ey - S(8))], fill=face, width=W_(14)); d.line([(ex - S(24), ey - S(14)), (ex + S(24), ey - S(14))], fill=BLK, width=W_(5))
            else: d.line([(ex - sx * S(26), ey - S(32)), (ex + sx * S(20), ey - S(22))], fill=BLK, width=W_(7))
    d.polygon([(hx - S(30), hy + S(90)), (hx + S(30), hy + S(90)), (hx, hy + S(170))], fill=FUR2, outline=BLK)
    # boca y lengua
    my = hy + S(45)
    if mood == "stop": d.ellipse([hx - S(26), my - S(14), hx + S(26), my + S(34)], fill=(60, 15, 25), outline=BLK, width=W_(4))
    else:
        d.chord([hx - S(50), my - S(20), hx + S(50), my + S(40)], 0, 180, fill=(60, 15, 25), outline=BLK)
        for k in range(5): d.polygon([(hx - S(40) + k * S(20), my + S(10)), (hx - S(30) + k * S(20), my + S(10)), (hx - S(35) + k * S(20), my + S(24))], fill=WHITE)
        if mood in ("grin", "suspicious"):
            tl = S(110) + math.sin(t * 5) * S(12)
            d.polygon([(hx - S(14), my + S(20)), (hx + S(14), my + S(20)), (hx + f * S(10), my + S(20) + tl), (hx - f * S(20), my + tl - S(5))], fill=(220, 50, 70), outline=BLK)

def bells(d, x, y, s=1.0, t=0.0, n=3):
    """Cascabeles colgando de una correa; (x, y) = punto de arriba."""
    S = lambda v: v * s; W_ = lambda v: max(2, int(v * s))
    d.line([(x - S(60), y), (x + S(60), y)], fill=(120, 70, 40), width=W_(10))
    for k in range(n):
        bx = x - S(45) + k * S(45) + math.sin(t * 12 + k) * S(4); by = y + S(30)
        d.ellipse([bx - S(20), by - S(20), bx + S(20), by + S(20)], fill=(235, 190, 60), outline=BLK, width=W_(3))
        d.line([(bx - S(12), by + S(4)), (bx + S(12), by + S(4))], fill=BLK, width=W_(3))
