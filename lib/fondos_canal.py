"""Fondos nuevos del canal (imagen 1080x1920)."""
from PIL import Image, ImageDraw
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

def city_street(t=0.0, decay=0.0, w=1080, h=1920, seed=3):
    """Calle de ciudad vacía de día. decay 0..1: grietas, hierba, hiedra en edificios y un árbol que sale de la alcantarilla. Devuelve (img, d)."""
    import random
    from reels_engine.exterior import building, tree
    img = radial_bg(((0, (200, 225, 245)), (1, (150, 185, 220))), cy=600).resize((w, h)); d = ImageDraw.Draw(img)
    r = random.Random(seed)
    for k, (x, bw, bh, c) in enumerate(((110, 240, 700, (170, 150, 140)), (380, 220, 820, (150, 160, 180)), (640, 260, 640, (190, 170, 130)), (930, 240, 760, (160, 140, 150)))):
        if x - bw / 2 < w: building(d, x, 1150, w=bw, h=bh, col=c, seed=k + 1)
        if decay > .3:
            for j in range(int(12 * decay)):
                vx = x - bw / 2 + r.uniform(0, bw); vy = 1150 - r.uniform(0, bh * decay)
                d.ellipse([vx - 18, vy - 12, vx + 18, vy + 12], fill=(70, 140, 70))
    d.rectangle([0, 1150, w, 1380], fill=(110, 110, 120)); d.rectangle([0, 1150, w, 1180], fill=(170, 170, 175))
    for x in range(40, w, 200): d.rectangle([x, 1260, x + 110, 1272], fill=(235, 220, 120))
    if decay > .2:
        from reels_engine.screens import cracks
        cracks(d, (60, 1190, w - 60, 1370), seed=seed, n=int(4 + 10 * decay), col=(60, 60, 65), width=6)
        for j in range(int(30 * decay)):
            gx = r.uniform(0, w); gy = r.uniform(1185, 1370); d.polygon([(gx - 8, gy), (gx, gy - 26), (gx + 8, gy)], fill=(80, 160, 70))
    if decay > .5:
        d.ellipse([700, 1290, 860, 1330], fill=(50, 50, 55), outline=BLK, width=4)
        tree(d, 780, 1310, .55 + .5 * (decay - .5), kind="round", col=(70, 150, 70))
    return img, d

def subway_tunnel(t=0.0, water=0.0):
    """Corte de un túnel de metro con un tren detenido; water 0..1 = qué tanto se inundó. Devuelve (img, d)."""
    img = radial_bg(((0, (90, 90, 100)), (1, (35, 35, 45))), cy=900); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1080, 480], fill=(120, 110, 100))
    d.rectangle([0, 470, 1080, 500], fill=(80, 75, 70))
    d.chord([-200, 520, 1280, 1700], 180, 360, fill=(55, 55, 65), outline=BLK, width=10)
    d.rectangle([0, 1110, 1080, 1380], fill=(70, 65, 60))
    for x in range(0, 1080, 90): d.rectangle([x, 1200, x + 60, 1214], fill=(110, 90, 70))
    d.line([(0, 1190), (1080, 1190)], fill=(170, 170, 180), width=8); d.line([(0, 1230), (1080, 1230)], fill=(170, 170, 180), width=8)
    d.rounded_rectangle([120, 830, 960, 1180], 40, fill=(190, 195, 205), outline=BLK, width=6)
    for k in range(5): d.rounded_rectangle([170 + k * 155, 880, 270 + k * 155, 990], 12, fill=(60, 80, 110), outline=BLK, width=4)
    d.rectangle([120, 1040, 960, 1070], fill=(200, 60, 60))
    if water > 0:
        import math
        wy = 1380 - water * 820
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        pts = [(x, wy + math.sin(x / 60 + t * 3) * 10) for x in range(0, 1100, 20)]
        ld.polygon(pts + [(1080, 1380), (0, 1380)], fill=(40, 90, 150, 170))
        img.paste(layer, (0, 0), layer); d = ImageDraw.Draw(img)
        d.line(pts, fill=(140, 190, 240), width=6)
    return img, d

def forest_city(t=0.0, w=2160, h=3840, seed=5):
    """Ciudad tragada por el bosque (mundo grande para alejar la cámara): edificios en ruinas entre árboles. Devuelve (img, d)."""
    import random
    from reels_engine.exterior import building, tree
    img = radial_bg(((0, (200, 225, 245)), (1, (150, 190, 215))), cy=800).resize((w, h)); d = ImageDraw.Draw(img)
    r = random.Random(seed)
    base = int(h * .62)
    d.rectangle([0, base, w, h], fill=(80, 130, 70))
    for k in range(14):
        x = r.uniform(80, w - 80); bh = r.uniform(400, 1100)
        building(d, x, base, w=r.uniform(160, 280), h=bh, col=(150, 145, 135), seed=k)
        for j in range(10): vx = x + r.uniform(-90, 90); vy = base - r.uniform(0, bh); d.ellipse([vx - 30, vy - 20, vx + 30, vy + 20], fill=(70, 140, 70))
    trees = sorted((base + r.uniform(20, 900), r.uniform(0, w), r.uniform(.8, 1.8), r.choice(("round", "pine")), r.randint(0, 40)) for k in range(60))
    for ty, tx, ts, kind, g in trees: tree(d, tx, ty, ts, kind=kind, col=(60, 130 + g, 60))
    return img, d

def savanna(t=0.0, night=False, w=1080, h=1920, seed=4, ground_y=1290):
    """Sabana africana: cielo (día o noche con luna), acacias de copa plana, pasto seco. Devuelve (img, d)."""
    import random, math
    r = random.Random(seed)
    sky = ((0, (20, 25, 60)), (1, (60, 50, 100))) if night else ((0, (255, 215, 150)), (1, (240, 160, 90)))
    img = radial_bg(sky, cy=900).resize((w, h)); d = ImageDraw.Draw(img)
    if night:
        for k in range(60):
            x, y = r.uniform(0, w), r.uniform(0, ground_y - 300); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(240, 240, 255))
        d.ellipse([w - 300, 520, w - 180, 640], fill=(250, 245, 220), outline=BLK, width=4)
    else:
        d.ellipse([w * .5 - 160, ground_y - 470, w * .5 + 160, ground_y - 150], fill=(255, 240, 180))
    d.rectangle([0, ground_y - 160, w, ground_y], fill=(200, 170, 100) if not night else (90, 80, 70))
    for k in range(int(3 * w / 1080)):                                   # acacias al fondo
        x = r.uniform(60, w - 60); by = ground_y - 150; s = r.uniform(.7, 1.1)
        col = (110, 90, 60) if not night else (40, 35, 40)
        d.line([(x, by), (x, by - 170 * s)], fill=col, width=int(16 * s))
        d.line([(x, by - 110 * s), (x - 60 * s, by - 190 * s)], fill=col, width=int(10 * s))
        d.ellipse([x - 170 * s, by - 250 * s, x + 170 * s, by - 170 * s], fill=(120, 140, 60) if not night else (35, 45, 40))
    d.rectangle([0, ground_y, w, ground_y + 90], fill=(180, 150, 80) if not night else (70, 60, 55))
    d.line([(0, ground_y), (w, ground_y)], fill=BLK, width=4)
    for k in range(int(40 * w / 1080)):
        gx = r.uniform(0, w); gy = ground_y + r.uniform(-4, 60)
        d.line([(gx, gy), (gx - 6, gy - 26)], fill=(150, 120, 60) if not night else (60, 55, 45), width=4); d.line([(gx, gy), (gx + 6, gy - 22)], fill=(150, 120, 60) if not night else (60, 55, 45), width=4)
    return img, d

def monte(t=0.0, night=False, seed=6, ground_y=1290):
    """Monte bajo / patio maya: arbustos, árboles chaparros y tierra roja. night=True con luna y luciérnagas. Devuelve (img, d)."""
    import random, math
    from reels_engine.exterior import tree, bush
    r = random.Random(seed)
    sky = ((0, (25, 35, 70)), (1, (60, 60, 110))) if night else ((0, (200, 230, 250)), (1, (150, 200, 230)))
    img = radial_bg(sky, cy=800); d = ImageDraw.Draw(img)
    if night: d.ellipse([820, 520, 940, 640], fill=(250, 245, 220), outline=BLK, width=4)
    for k in range(5): tree(d, r.uniform(0, 1080), ground_y - 140, r.uniform(.45, .65), kind="round", col=(45, 70, 70) if night else (120, 170, 120))
    d.rectangle([0, ground_y - 90, 1080, ground_y + 90], fill=(110, 60, 45) if night else (185, 95, 60))
    for k in range(4): bush(d, r.uniform(0, 1080), ground_y - 70, r.uniform(.4, .6), col=(45, 70, 70) if night else (120, 170, 120))
    d.line([(0, ground_y), (1080, ground_y)], fill=BLK, width=4)
    if night:
        for k in range(14):
            x = (r.uniform(0, 1080) + math.sin(t + k) * 30); y = r.uniform(700, 1200) + math.cos(t * 1.3 + k) * 20
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(240, 255, 150))
    return img, d
