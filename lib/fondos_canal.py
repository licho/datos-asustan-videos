"""Fondos nuevos del canal (imagen 1080x1920)."""
from PIL import ImageDraw
from reels_engine.motion import radial_bg
from .core import BLK, WHITE, dk

def oficina(night=False):
    """Oficina: pared con ventana (sin invadir letreros), piso y zoclo. Piso en y=1290."""
    stops = ((0, (230, 236, 242)), (1, (190, 198, 210))) if not night else ((0, (60, 65, 95)), (1, (25, 28, 50)))
    img = radial_bg(stops, cy=800); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, 1080, 1380], fill=(150, 150, 162) if not night else (55, 55, 70))
    d.rectangle([0, 1238, 1080, 1252], fill=(120, 120, 130))
    wx0, wy0, wx1, wy1 = 640, 520, 1000, 820
    d.rectangle([wx0, wy0, wx1, wy1], fill=(160, 205, 235) if not night else (15, 20, 45), outline=(245, 245, 245), width=12)
    d.line([((wx0 + wx1) // 2, wy0), ((wx0 + wx1) // 2, wy1)], fill=(245, 245, 245), width=8)
    return img

def river_night(t, ground_y=1150, moon=(900, 790)):
    """Río de noche con agua que se mueve y orilla de pasto (Llorona, leyendas). Devuelve (img, d)."""
    import math
    from reels_engine.exterior import moon as moon_disc
    img = radial_bg(((0, (60, 70, 130)), (.6, (25, 30, 70)), (1, (8, 10, 30))), cy=700); d = ImageDraw.Draw(img)
    if moon: moon_disc(d, moon[0], moon[1], 60, bg=(30, 35, 80))
    d.rectangle([0, ground_y, 1080, 1380], fill=(30, 60, 110))
    for k in range(6):
        yy = ground_y + 25 + k * 40; ph = t * 2 + k
        d.line([(x, yy + math.sin(x / 70 + ph) * 6) for x in range(0, 1120, 40)], fill=(80, 120, 180), width=4)
    d.rectangle([0, ground_y - 20, 1080, ground_y], fill=(40, 70, 50))
    return img, d

def living_room(night=False):
    """Sala cálida con piso de madera (escenas navideñas, de casa). Devuelve (img, d)."""
    stops = ((0, (250, 225, 200)), (1, (215, 170, 140))) if not night else ((0, (40, 55, 110)), (.6, (20, 28, 65)), (1, (8, 10, 30)))
    img = radial_bg(stops, cy=800); d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, 1080, 1380], fill=(150, 100, 70)); d.line([(0, 1250), (1080, 1250)], fill=(110, 70, 45), width=6)
    return img, d

def village(t=0.0, w=1080, h=1920, lights=True):
    """Pueblo alpino nevado de noche, con montañas, casas y pinos (sirve de 'mundo' para la cámara). Devuelve (img, d)."""
    from reels_engine.exterior import house, tree
    img = radial_bg(((0, (55, 65, 120)), (.6, (25, 30, 70)), (1, (10, 12, 35))), cy=600).resize((w, h)); d = ImageDraw.Draw(img)
    for k, (x0, top, x1) in enumerate(((-200, 520, 520), (300, 440, 1050), (750, 560, 1400))):
        d.polygon([(x0, 1000), ((x0 + x1) / 2, top), (x1, 1000)], fill=(70, 80, 120))
        d.polygon([((x0 + x1) / 2 - 90, top + 100), ((x0 + x1) / 2, top), ((x0 + x1) / 2 + 90, top + 100)], fill=(235, 240, 250))
    d.rectangle([0, 1000, w, h], fill=(225, 232, 245)); d.line([(0, 1000), (w, 1000)], fill=(180, 190, 210), width=6)
    for k, x in enumerate((120, 420, 760, 1000)):
        if x < w: house(d, x, 1250, .9 + .1 * (k % 2), wall=(230, 200, 160), roof=(120, 60, 50), lights=lights)
    tree(d, 290, 1260, .9, kind="pine", col=(40, 100, 70)); tree(d, 900, 1250, .8, kind="pine", col=(40, 100, 70))
    d.rectangle([0, 1250, w, 1380], fill=(240, 244, 252))
    return img, d
