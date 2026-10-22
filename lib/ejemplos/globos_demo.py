import sys; sys.path.insert(0, "/home/claude/datos-asustan-videos")
from PIL import Image, ImageDraw
from lib.core import say, say_reset, W, H
from lib.humanos import guy, don_tono, anchors
from lib.animales import stego
from lib.muebles import shelf

def frame(fn):
    img = Image.new("RGB", (W, H), (60, 70, 110)); d = ImageDraw.Draw(img)
    say_reset(); fn(img, d); return img

def p1(img, d):
    d.rectangle([0, 1250, W, H], fill=(190, 160, 110))
    stego(d, 680, 1290, .8, mood="normal")
    guy(d, 230, 1290, .7)
    a = anchors(230, 1290, .7)
    say(d, "¿Y tú qué haces aquí?", a["mouth"], head=a["head_r"], avoid=[(420, 800, 1000, 1290)])
    say(d, "Llegué antes que las pirámides", (890, 1185), head=60, avoid=[a["box"], (480, 1150, 1000, 1290)])

def p2(img, d):
    d.rectangle([0, 1250, W, H], fill=(120, 120, 130))
    guy(d, 300, 1290, .7); don_tono(d, 780, 1290, .7)
    a, b = anchors(300, 1290, .7), anchors(780, 1290, .7)
    say(d, "¿Otra vez usted?", a["mouth"], head=a["head_r"], avoid=[b["box"]])
    say(d, "Vengo por mis chicles", b["mouth"], head=b["head_r"], avoid=[a["box"]])

def p3(img, d):
    shelf(d, 60, 500, 560, 1250)
    d.rectangle([0, 1250, W, H], fill=(200, 200, 190))
    guy(d, 880, 1290, .7); a = anchors(880, 1290, .7)
    say(d, "Dicen que el refri hace ruidos de noche y nadie sabe por qué", a["mouth"], head=a["head_r"])

ims = [frame(f) for f in (p1, p2, p3)]
out = Image.new("RGB", (W * 3 + 40, H), (0, 0, 0))
for i, im in enumerate(ims): out.paste(im, (i * (W + 20), 0))
out.resize((out.width // 2, out.height // 2)).save("/tmp/dqa_out/globo_demo.png")
