import math, random
from PIL import Image, ImageDraw
from reel import F, lc, YEL, RED, WHITE, BLK, zombie
from reel2 import germ, keyboard

W, H = 1640, 856
img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
for r in range(1100, 0, -5):
    d.ellipse([W/2 - r*1.3, H/2 - r*0.7, W/2 + r*1.3, H/2 + r*0.7], fill=lc((70, 30, 110), (8, 6, 16), r / 1100))
rng = random.Random(3)
for i in range(70):
    x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.5, 4)
    d.ellipse([x - s, y - s, x + s, y + s], fill=lc((90, 70, 130), (190, 170, 230), rng.random()))
# slime drips from top
d.rectangle([0, 0, W, 22], fill=(120, 210, 90))
for i in range(26):
    x = 20 + i * 64 + rng.uniform(-14, 14); L = rng.choice([135, 150, 165, 185, 205])
    d.rounded_rectangle([x - 12, 0, x + 12, L], 12, fill=(120, 210, 90))
    d.ellipse([x - 18, L - 14, x + 18, L + 20], fill=(120, 210, 90))
# zombie peeking from the right
zombie(d, 1400, 1060, 1.2, t=0.6, face=-1)
# keyboard + germs bottom-center/left (leave far bottom-left for profile pic)
keyboard(d, 760, 700, 560, dirt=0.9, seed=5)
for (x, y, r, k, ph) in [(470, 610, 42, "ecoli", 0.2), (300, 470, 36, "coli", 1.1), (1080, 620, 40, "staph", 2.0),
                         (1110, 480, 30, "coli", 3.0), (330, 300, 36, "staph", 0.7), (1290, 290, 34, "coli", 1.7)]:
    germ(d, x, y, r, k, 0.5, ph)
# title block in safe zone
cx = W / 2
d.text((cx, 410), "ASUSTAN", font=F(168), fill=YEL, anchor="mm", stroke_width=16, stroke_fill=BLK)
d.text((cx, 272), "DATOS QUE", font=F(118), fill=WHITE, anchor="mm", stroke_width=14, stroke_fill=BLK)
d.rounded_rectangle([cx - 430, 492, cx + 430, 552], 30, fill=RED, outline=BLK, width=5)
d.text((cx, 522), "Lo que no sabías… y ojalá no supieras", font=F(38), fill=WHITE, anchor="mm")
img.save("/home/claude/datos_que_asustan_portada_facebook.png")
# preview with desktop + mobile crop guides
p = img.copy(); pd = ImageDraw.Draw(p)
dh = W * 312 / 820; y0 = (H - dh) / 2
pd.rectangle([0, y0, W - 1, y0 + dh], outline=(0, 255, 255), width=4)
mw = dh * 0.0 + H * 640 / 360; mx = (W - mw) / 2
pd.rectangle([mx, 0, mx + mw, H - 1], outline=(255, 0, 255), width=4)
p.resize((820, 428)).save("cover_prev.png")
