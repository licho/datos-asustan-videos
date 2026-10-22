import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from reel import (F, cl, lerp, ease, pop, lc, dk, rich_caption, chip, bigtext, guy, W, H, YEL, RED, WHITE, BLK, FEET)
from reel13 import SPACE, earth

FPS = 30
CX, CY = 540, 820

def face(d, cx, cy, r, mood="happy", look=(0.0, 0.0), eye=1.0):
    """look=(dx, dy) hacia dónde mira (-1..1); eye = tamaño de ojos (1 normal, 1.3 sorpresa)."""
    for sx in (-1, 1):
        ex, ey = cx + sx * r * 0.32, cy - r * 0.12
        d.ellipse([ex - r * 0.13 * eye, ey - r * 0.16 * eye, ex + r * 0.13 * eye, ey + r * 0.16 * eye], fill=WHITE, outline=BLK, width=max(2, int(r * 0.03)))
        px_, py_ = ex + look[0] * r * 0.06, ey + look[1] * r * 0.07
        d.ellipse([px_ - r * 0.06, py_ - r * 0.06, px_ + r * 0.06, py_ + r * 0.1], fill=BLK)
        if mood == "angry":
            d.line([(ex - r * 0.17, ey - r * 0.24 - sx * r * 0.06), (ex + r * 0.17, ey - r * 0.24 + sx * r * 0.06)], fill=BLK, width=max(3, int(r * 0.05)))
        if mood == "scared":
            d.arc([ex - r * 0.17, ey - r * 0.36, ex + r * 0.17, ey - r * 0.16], 200, 340, fill=BLK, width=max(2, int(r * 0.04)))
    if mood == "happy":
        d.arc([cx - r * 0.28, cy + r * 0.05, cx + r * 0.28, cy + r * 0.45], 20, 160, fill=BLK, width=max(3, int(r * 0.06)))
    elif mood == "angry":
        d.line([(cx - r * 0.2, cy + r * 0.35), (cx + r * 0.2, cy + r * 0.3)], fill=BLK, width=max(3, int(r * 0.06)))
    elif mood == "scared":
        d.ellipse([cx - r * 0.1, cy + r * 0.2, cx + r * 0.1, cy + r * 0.45], fill=(60, 10, 20), outline=BLK, width=max(2, int(r * 0.03)))
    elif mood == "sad":
        d.arc([cx - r * 0.25, cy + r * 0.28, cx + r * 0.25, cy + r * 0.6], 200, 340, fill=BLK, width=max(3, int(r * 0.06)))
    else:
        d.line([(cx - r * 0.18, cy + r * 0.32), (cx + r * 0.18, cy + r * 0.32)], fill=BLK, width=max(3, int(r * 0.05)))

def planet_earth(d, cx, cy, r, mood="happy", look=(0.0, 0.0), eye=1.0, shade=True):
    earth(d, cx, cy, r)
    if shade:
        from lib.motion import sphere_shade
        sphere_shade(d._image, cx, cy, r)
    if r > 60: face(d, cx, cy, r, mood, look, eye)

def jupiter(d, cx, cy, r, mood="neutral"):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(215, 170, 120), outline=(120, 80, 50), width=max(2, int(r * 0.02)))
    for k, (dy, h, c) in enumerate([(-0.6, 0.12, (180, 120, 80)), (-0.25, 0.16, (230, 200, 160)), (0.1, 0.14, (170, 110, 70)), (0.45, 0.12, (200, 150, 100))]):
        y0 = cy + dy * r; hw = math.sqrt(max(0, 1 - (dy + h / 2) ** 2)) * r
        d.rectangle([cx - hw * 0.98, y0, cx + hw * 0.98, y0 + h * r], fill=c)
    d.ellipse([cx + r * 0.2, cy + r * 0.25, cx + r * 0.5, cy + r * 0.42], fill=(200, 90, 60))
    if r > 60: face(d, cx, cy - r * 0.1, r * 0.8, mood)

def sun(d, cx, cy, r, t, mood="happy"):
    for k in range(5, 0, -1):
        rr = r * (1 + 0.04 * k + 0.01 * math.sin(t * 3 + k))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=lc((255, 200, 60), (255, 120, 30), k / 5))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 215, 70), outline=(255, 150, 40), width=max(2, int(r * 0.02)))
    if r > 60: face(d, cx, cy, r * 0.8, mood)

def make_milky():
    img = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    rng = random.Random(9)
    d.ellipse([370, 370, 530, 530], fill=(255, 240, 200, 160))
    for i in range(5000):
        arm = i % 2; a = rng.uniform(0, 4.4); r = 40 + a * 90
        ang = a + arm * math.pi + rng.gauss(0, 0.18)
        x = 450 + math.cos(ang) * r + rng.gauss(0, 10); y = 450 + math.sin(ang) * r * 0.75 + rng.gauss(0, 8)
        c = rng.choice([(200, 210, 255, 220), (255, 240, 220, 220), (170, 190, 255, 200)])
        s = rng.uniform(1, 3)
        d.ellipse([x - s, y - s, x + s, y + s], fill=c)
    return img.filter(ImageFilter.GaussianBlur(0.8))
MILKY = make_milky()

def make_field():
    img = Image.new("RGB", (W, H), (3, 3, 12)); d = ImageDraw.Draw(img)
    rng = random.Random(4)
    small = MILKY.resize((90, 90))
    for i in range(260):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if rng.random() < 0.35:
            sz = int(rng.uniform(30, 90)); g = small.resize((sz, int(sz * rng.uniform(0.4, 1.0)))).rotate(rng.uniform(0, 180), expand=True)
            img.paste(g, (int(x), int(y)), g)
        else:
            s = rng.uniform(4, 14)
            d.ellipse([x - s, y - s * 0.6, x + s, y + s * 0.6], fill=rng.choice([(255, 220, 180), (200, 210, 255), (255, 190, 200)]))
    return img
FIELD = make_field()

def voyager(d, x, y, s=1.0):
    d.line([(x - 60 * s, y), (x + 60 * s, y)], fill=(200, 200, 200), width=max(2, int(4 * s)))
    d.line([(x, y), (x + 20 * s, y + 70 * s)], fill=(200, 200, 200), width=max(2, int(4 * s)))
    d.ellipse([x - 45 * s, y - 70 * s, x + 45 * s, y - 10 * s], fill=(235, 235, 235), outline=BLK, width=3)
    d.rectangle([x - 18 * s, y - 12 * s, x + 18 * s, y + 18 * s], fill=(200, 160, 60), outline=BLK, width=3)

CAPS = [
    (0.0, 5.0, "Esta es la *Tierra*. Tu casa, tu tráfico, tus deudas…"),
    (5.0, 8.5, "¿Te parece enorme? Ahora pon a su lado a *Júpiter*"),
    (8.5, 12.0, "*11 Tierras* de ancho… y adentro le caben *más de 1,300*"),
    (12.0, 15.0, "Pero Júpiter, al lado del Sol, es *una canica*"),
    (15.0, 18.0, "Dentro del Sol caben *1.3 millones* de Tierras"),
    (18.0, 22.0, "Y el Sol… es una estrella *promedio*. Del montón."),
    (22.0, 26.5, "*Betelgeuse*, en Orión, es *cientos de veces* más ancha"),
    (26.5, 31.0, "En lugar del Sol, se tragaría a Mercurio, Venus, la Tierra… *y Marte*"),
    (31.0, 35.5, "La sonda *Voyager 1* salió en *1977*"),
    (35.5, 40.0, "Casi 50 años viajando… y apenas va a *1 día luz*"),
    (40.0, 45.0, "La estrella más cercana: a más de *4 años luz*"),
    (45.0, 48.5, "Nuestra galaxia mide unos *100,000 años luz*…"),
    (48.5, 52.0, "…y hay *cientos de miles de millones* de galaxias"),
    (52.0, 56.0, "Y tú preocupado porque te dejaron *en visto*"),
    (56.0, 70.0, "¿Te *asusta* o te *tranquiliza*? Te leo en comentarios"),
]

def render(v, t=None):
    if t is None: t = v
    img = SPACE.copy(); d = ImageDraw.Draw(img)
    if v < 5.0:
        r = 300 * (0.6 + 0.4 * ease(v / 0.8))
        planet_earth(d, CX, CY, r, "happy")
        if v > 1.2: chip(d, "AQUÍ ESTÁS TÚ", 330, bg=(40, 120, 220), appear=(v - 1.2) / 0.3)
        if v > 1.2:
            d.polygon([(CX - 20, CY - r - 60), (CX + 20, CY - r - 60), (CX, CY - r - 20)], fill=YEL, outline=BLK)
    elif v < 12.0:
        k = ease((v - 5.0) / 1.5)
        er = lerp(300, 40, k); ex = lerp(CX, 90, k)
        jr = 400 * k; jx = lerp(1400, 590, k); jy = CY + 60
        if jr > 2: jupiter(d, jx, jy, jr, "neutral")
        planet_earth(d, ex, jy, er, "scared" if k > 0.5 else "happy")
        if v > 8.5:
            n = min(11, int((v - 8.5) / 0.15) + 1)
            for i in range(n):
                cx = jx - jr + jr / 11 + i * 2 * jr / 11
                earth(d, cx, jy + jr + 55, 32)
            chip(d, "11 TIERRAS DE ANCHO", 250, bg=(200, 120, 40), appear=(v - 8.5) / 0.3)
        if v > 10.3:
            chip(d, "CABEN +1,300", 370, bg=RED, appear=(v - 10.3) / 0.3)
    elif v < 22.0:
        k = ease((v - 12.0) / 1.8)
        sr = lerp(0, 520, k); jr = lerp(440, 48, k); jx = lerp(600, 960, k)
        sx = CX - 120
        if sr > 2: sun(d, sx, CY + 40, sr, t, "angry" if v >= 18.0 else "happy")
        jy = lerp(CY + 60, CY - 420, k)
        jupiter(d, jx, jy, jr, "scared")
        earth(d, jx - 70 * k - 10, jy + 70 * k, max(5, jr * 0.09))
        if 12.0 <= v < 15.0 and k > 0.9: chip(d, "JÚPITER = CANICA", 300, bg=(200, 120, 40), appear=(v - 13.8) / 0.3)
        if 15.0 <= v < 18.0: chip(d, "CABEN 1,300,000 TIERRAS", 300, bg=RED, appear=(v - 15.0) / 0.3)
        if v >= 18.0: chip(d, "ESTRELLA PROMEDIO", 300, bg=(90, 90, 90), appear=(v - 18.0) / 0.3)
    elif v < 31.0:
        orbits = [("MERCURIO", 90, (180, 170, 160)), ("VENUS", 160, (230, 190, 120)), ("TIERRA", 230, (60, 130, 220)), ("MARTE", 330, (210, 90, 50))]
        br = float(np.interp(v, [22.6, 26.5, 28.15, 28.9, 29.6, 30.3, 30.8], [0, 75, 95, 165, 235, 335, 420])); nams = []; labels = []
        for i, (nm, r, c) in enumerate(orbits):
            d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(90, 90, 130), width=3)
            a = t * (1.2 - i * 0.2) + i
            px, py = CX + math.cos(a) * r, CY + math.sin(a) * r
            if br < r - 8:
                d.ellipse([px - 18, py - 18, px + 18, py + 18], fill=c, outline=BLK, width=3)
                labels.append((px, py - 44, nm))
            elif br < r + 60:
                nams.append((px, py - 44))
        d.ellipse([CX - 8, CY - 8, CX + 8, CY + 8], fill=(255, 215, 70))
        if br > 4:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.ellipse([CX - br, CY - br, CX + br, CY + br], fill=(220, 60, 40, 235), outline=(255, 130, 80, 255), width=8)
            img.paste(ov, (0, 0), ov); d = ImageDraw.Draw(img)
            if br > 120: face(d, CX, CY, br * 0.6, "happy")
        for (lx, ly, nm) in labels:
            d.text((lx, ly), nm, font=F(40), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=BLK)
        for (nx, ny) in nams:
            d.text((nx, ny), "¡ÑAM!", font=F(56), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)
        chip(d, "BETELGEUSE", 210, bg=(200, 50, 40), appear=(v - 22.0) / 0.3)
        if v > 26.5: chip(d, "CIENTOS DE VECES EL SOL", 320, bg=BLK, size=46, appear=(v - 26.5) / 0.3)
    elif v < 40.0:
        k = cl((v - 31.0) / 6.0)
        earth(d, 110, CY, 60)
        for x in range(200, 1040, 40): d.line([(x, CY), (x + 20, CY)], fill=(150, 150, 190), width=4)
        vx = lerp(220, 900, ease(k))
        voyager(d, vx, CY - 30, 1.2)
        year = int(lerp(1977, 2026, k))
        bigtext(d, str(year), CX, 470, 150, fill=WHITE)
        if v > 37.0:
            chip(d, "1 DÍA LUZ ✓", 1180, bg=(30, 140, 80), appear=(v - 37.0) / 0.3)
        chip(d, "VOYAGER 1", 300, bg=(40, 120, 220), appear=(v - 31.0) / 0.3)
    elif v < 45.0:
        k = ease((v - 40.0) / 2.0)
        y = CY
        d.line([(80, y), (lerp(81, 1000, k), y)], fill=WHITE, width=10)
        d.line([(80, y - 40), (80, y + 40)], fill=(60, 200, 90), width=6)
        bigtext(d, "1 DÍA LUZ", 220, y - 90, 50, fill=(120, 230, 140))
        d.ellipse([60, y - 20, 100, y + 20], outline=YEL, width=4)
        if k > 0.98:
            d.ellipse([970, y - 30, 1030, y + 30], fill=(255, 120, 120), outline=WHITE, width=4)
            bigtext(d, "ESTRELLA MÁS CERCANA", 700, y + 100, 46, fill=WHITE)
            bigtext(d, "4.2 AÑOS LUZ", 760, y - 100, 64, fill=YEL)
        chip(d, "×1,500 VECES MÁS LEJOS", 330, bg=RED, appear=(v - 42.0) / 0.3) if v > 42.0 else None
    elif v < 52.0:
        if v < 48.5:
            k = ease((v - 45.0) / 1.2)
            sz = int(lerp(200, 900, k))
            g = MILKY.resize((sz, sz)).rotate(t * 3)
            img.paste(g, (CX - sz // 2, CY - sz // 2), g); d = ImageDraw.Draw(img)
            ax, ay = CX + sz * 0.22, CY + sz * 0.12
            d.polygon([(ax, ay), (ax + 30, ay - 70), (ax - 30, ay - 70)], fill=YEL, outline=BLK)
            bigtext(d, "ESTÁS AQUÍ", ax, ay - 110, 52, fill=YEL)
            chip(d, "100,000 AÑOS LUZ", 300, bg=(90, 60, 160), appear=(v - 45.3) / 0.3)
        else:
            k = ease((v - 48.5) / 1.5)
            zoom = lerp(3.0, 1.0, k)
            cw, ch = int(W / zoom), int(H / zoom)
            img = FIELD.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H)); d = ImageDraw.Draw(img)
            chip(d, "CIENTOS DE MILES DE MILLONES", 300, bg=RED, size=48, appear=(v - 49.0) / 0.3)
    elif v < 56.0:
        img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
        for y in range(H): pass
        d.rectangle([0, 0, W, H], fill=(140, 190, 240)); d.rectangle([0, 1150, W, H], fill=(110, 170, 90))
        bx, by = 540, 760
        SK = (241, 194, 150)
        d.rounded_rectangle([bx - 120, by + 300, bx + 120, H + 40], 60, fill=SK, outline=BLK, width=6)
        d.ellipse([bx - 210, by + 180, bx + 210, by + 470], fill=SK, outline=BLK, width=6)
        d.rounded_rectangle([bx - 230, by - 400, bx + 230, by + 400], 50, fill=(30, 30, 30), outline=BLK, width=8)
        d.rounded_rectangle([bx - 200, by - 360, bx + 200, by + 360], 26, fill=(235, 240, 245))
        d.rounded_rectangle([bx - 10, by - 250, bx + 180, by - 150], 24, fill=(120, 200, 120))
        d.text((bx + 85, by - 200), "¿Hola?", font=F(52), fill=BLK, anchor="mm")
        d.text((bx + 100, by - 110), "Visto ✓✓", font=F(40), fill=(40, 120, 220), anchor="mm")
        for fy in (by + 230, by + 300, by + 370):
            d.rounded_rectangle([bx - 270, fy - 30, bx - 190, fy + 30], 28, fill=SK, outline=BLK, width=5)
        d.rounded_rectangle([bx + 180, by + 210, bx + 270, by + 270], 28, fill=SK, outline=BLK, width=5)
        chip(d, "DRAMA CÓSMICO", 240, bg=(90, 60, 160), appear=(v - 52.5) / 0.3)
    else:
        lt = v - 56.0
        planet_earth(d, CX, CY + 60, 200, "happy")
        bigtext(d, "¿TE ASUSTA", CX, 360, 100, fill=WHITE)
        bigtext(d, "O TE TRANQUILIZA?", CX, 480, 90, fill=YEL)
        if lt > 2.5:
            sc = pop((lt - 2.5) / 0.35)
            d.rounded_rectangle([540 - 330 * sc, 1180 - 80 * sc, 540 + 330 * sc, 1180 + 80 * sc], int(26 * sc), fill=RED, outline=WHITE, width=6)
            d.text((540, 1180), "SÍGUEME", font=F(max(8, 80 * sc)), fill=WHITE, anchor="mm")
    for cs, ce, txt in CAPS:
        if cs <= v < ce: rich_caption(d, txt, appear=(v - cs) / 0.25)
    return np.asarray(img)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        out = [Image.fromarray(render(float(x))).resize((270, 480)) for x in sys.argv[2:]]
        sheet = Image.new("RGB", (270 * min(6, len(out)), 480 * ((len(out) + 5) // 6)))
        for i, im in enumerate(out): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("sheet_r23.png"); sys.exit()
    from warp23 import v_of_T, DUR
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", sys.argv[1]],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(render(v_of_T(i / FPS), i / FPS).tobytes())
    p.stdin.close(); p.wait()
