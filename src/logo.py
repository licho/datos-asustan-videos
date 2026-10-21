import math
from PIL import Image, ImageDraw
from reel import F, lc, YEL, RED, WHITE, BLK
from reel2 import germ

S = 1080
def make(with_text=True, out="perfil.png"):
    img = Image.new("RGB", (S, S)); d = ImageDraw.Draw(img)
    # radial dark purple background
    for r in range(760, 0, -4):
        d.ellipse([S/2 - r, S/2 - r, S/2 + r, S/2 + r], fill=lc((60, 25, 95), (8, 6, 16), r / 760))
    cy = 430 if with_text else 500
    cx = 500
    R = 270 if with_text else 310
    # handle
    hx0, hy0 = cx + R * 0.72, cy + R * 0.72
    d.line([(hx0, hy0), (hx0 + R * 0.75, hy0 + R * 0.75)], fill=(30, 20, 15), width=int(R * 0.30))
    d.line([(hx0, hy0), (hx0 + R * 0.75, hy0 + R * 0.75)], fill=(120, 75, 40), width=int(R * 0.22))
    # lens content
    lens = Image.new("RGB", (2 * R, 2 * R), (150, 220, 140)); ld = ImageDraw.Draw(lens)
    for r in range(R, 0, -3):
        ld.ellipse([R - r, R - r, R + r, R + r], fill=lc((170, 235, 160), (60, 140, 70), r / R))
    for (a, b, k) in [(0.35, 0.3, 0.12), (1.6, 0.45, 0.09), (1.5, 1.6, 0.1), (0.4, 1.55, 0.08)]:
        germ(ld, R * a, R * b, R * k, ["coli", "staph", "coli", "staph"][int(a * 3) % 4], 0.3, a, shade=0.75)
    germ(ld, R * 1.05, R * 1.02, R * 0.42, "ecoli", 0.0)
    mask = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(mask).ellipse([0, 0, 2 * R, 2 * R], fill=255)
    img.paste(lens, (int(cx - R), int(cy - R)), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], outline=BLK, width=50)
    d.ellipse([cx - R - 24, cy - R - 24, cx + R + 24, cy + R + 24], outline=(235, 190, 50), width=36)
    d.arc([cx - R * 0.8, cy - R * 0.8, cx + R * 0.8, cy + R * 0.8], 200, 245, fill=WHITE, width=16)
    # drips under rim for horror touch
    for (ang, L) in [(115, 60), (80, 95), (55, 45)]:
        a = math.radians(ang); x = cx + math.cos(a) * (R + 30); y = cy + math.sin(a) * (R + 30)
        d.rounded_rectangle([x - 11, y, x + 11, y + L], 11, fill=(120, 210, 90))
        d.ellipse([x - 17, y + L - 14, x + 17, y + L + 18], fill=(120, 210, 90))
    if with_text:
        for txt, y, size, col in [("DATOS QUE", 805, 92, WHITE), ("ASUSTAN", 905, 112, YEL)]:
            d.text((S / 2, y), txt, font=F(size), fill=col, anchor="mm", stroke_width=12, stroke_fill=BLK)
    img.save(out)

make(True, "/home/claude/datos_que_asustan_perfil.png")
make(False, "/home/claude/datos_que_asustan_icono.png")
prev = Image.new("RGB", (1100, 540), (255, 255, 255))
for i, f in enumerate(["/home/claude/datos_que_asustan_perfil.png", "/home/claude/datos_que_asustan_icono.png"]):
    im = Image.open(f).resize((520, 520)); m = Image.new("L", (520, 520), 0); ImageDraw.Draw(m).ellipse([0, 0, 520, 520], fill=255)
    prev.paste(im, (20 + i * 550, 10), m)
prev.save("logo_prev.png")
