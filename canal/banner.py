import sys, math, random
sys.path.insert(0, "/home/claude/datos-asustan-videos")
from PIL import Image, ImageDraw
from lib.core import F, BLK, WHITE, YEL, RED
from lib.motion import radial_bg
from lib.personajes import zombie, mummy, llorona, alien_cw, vampire, tyranno
from lib.criaturas import ghost_draw
from lib.props import planet_earth, tombstone

BW, BH = 2560, 1440
img = radial_bg(((0, (95, 45, 130)), (.6, (40, 20, 70)), (1, (12, 8, 28))), cy=720).resize((BW, BH))
d = ImageDraw.Draw(img)
r = random.Random(3)
for k in range(220):
    x, y = r.uniform(0, BW), r.uniform(0, BH * .7); s = r.choice((2, 3, 4)); d.ellipse([x - s, y - s, x + s, y + s], fill=(240, 235, 255))
d.ellipse([2050, 120, 2330, 400], fill=(250, 245, 220), outline=BLK, width=8)   # luna
# piso / panteón (el piso queda en el borde de abajo de la franja que se ve en compu)
FL = 930
d.rectangle([0, FL, BW, BH], fill=(35, 25, 45)); d.line([(0, FL), (BW, FL)], fill=BLK, width=8)
tombstone(d, 70, FL + 4, .9, text="R.I.P."); tombstone(d, 2500, FL + 4, .9, text="R.I.P.")
# personajes a los lados, fuera del texto (x < 520 y x > 2040), cabezas dentro de la franja visible
zombie(d, 230, FL + 8, .62, 0, face=1)
mummy(d, 380, FL + 8, .55, 0, "forward")
ghost_draw(d, 330, 330, .7, 0, mood="happy")
vampire(d, 2170, FL + 8, .58, 0, mood="smug")
llorona(d, 2360, FL + 8, .55, 0, mood="happy", arms="down")
# zona segura (1546x423 al centro): título y lema
cx, cy = BW // 2, BH // 2
def outlined(text, y, size, fill, sw):
    d.text((cx, y), text, font=F(size), fill=fill, anchor="mm", stroke_width=sw, stroke_fill=BLK)
outlined("DATOS QUE ASUSTAN", cy - 60, 98, YEL, 11)
outlined("Datos reales · terror cómico · humor negro", cy + 35, 44, WHITE, 6)
d.rounded_rectangle([cx - 400, cy + 85, cx + 400, cy + 150], 32, fill=RED, outline=BLK, width=6)
d.text((cx, cy + 117), "VIDEO NUEVO DE LUNES A SÁBADO", font=F(38), fill=WHITE, anchor="mm")
img.save("canal/banner_youtube.png", optimize=True)
# vista de cómo se recorta en celular (zona segura)
img.crop((cx - 773, cy - 211, cx + 773, cy + 212)).save("/tmp/banner_celular.png")
print("ok")

img.crop((cx - 618, cy - 169, cx + 617, cy + 169)).save("/tmp/banner_minimo.png")
