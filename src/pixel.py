import math, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Low-res canvas, scaled up 6x with nearest neighbour -> crisp pixels
LW, LH, SC, FPS, DUR = 180, 320, 6, 30, 16.0
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 8)
FONTB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)

# PICO-8 style palette
P = {
    "black": (0, 0, 0), "navy": (29, 43, 83), "purple": (126, 37, 83), "dgreen": (0, 135, 81),
    "brown": (171, 82, 54), "dgray": (95, 87, 79), "lgray": (194, 195, 199), "white": (255, 241, 232),
    "red": (255, 0, 77), "orange": (255, 163, 0), "yellow": (255, 236, 39), "green": (0, 228, 54),
    "blue": (41, 173, 255), "lav": (131, 118, 156), "pink": (255, 119, 168), "peach": (255, 204, 170),
}

def rect(d, x, y, w, h, c):
    d.rectangle([int(x), int(y), int(x + w - 1), int(y + h - 1)], fill=P[c])

def text(d, x, y, s, c="white", font=FONT, shadow="black", center=True):
    d.fontmode = "1"
    if center:
        w = d.textlength(s, font=font); x = x - w / 2
    if shadow:
        d.text((int(x) + 1, int(y) + 1), s, font=font, fill=P[shadow])
    d.text((int(x), int(y)), s, font=font, fill=P[c])

def sky(d, t):
    for y in range(0, 232, 4):
        rect(d, 0, y, LW, 4, "navy" if y < 120 else "purple" if y < 180 else "navy")
    rng = random.Random(1)
    for i in range(40):
        x, y = rng.randint(0, LW - 1), rng.randint(0, 150)
        if (int(t * 3) + i) % 9: d.point((x, y), fill=P["white" if i % 3 else "lav"])
    d.ellipse([136, 26, 152, 42], fill=P["white"]); d.ellipse([141, 23, 157, 39], fill=P["navy"])

def ground(d):
    rect(d, 0, 230, LW, 90, "dgray")
    for x in range(0, LW, 16): rect(d, x, 270, 8, 2, "yellow")
    rect(d, 0, 228, LW, 2, "lgray")

def store(d, t, light=True):
    rect(d, 6, 96, 168, 134, "lgray")
    rect(d, 6, 90, 168, 8, "dgray")
    rect(d, 40, 66, 100, 22, "black")
    on = light and (int(t * 8) % 13 != 0)
    text(d, 90, 70, "MINI 24H", "green" if on else "dgreen", FONTB)
    win = "yellow" if on else "orange"
    rect(d, 14, 112, 92, 76, win); rect(d, 116, 112, 50, 118, win)
    rect(d, 14, 112, 92, 3, "dgray"); rect(d, 58, 112, 3, 76, "dgray"); rect(d, 140, 112, 3, 118, "dgray")
    for k in range(6):
        rect(d, 18 + k * 14, 168, 11, 16, ["red", "blue", "green", "pink", "orange", "lav"][k])

def hero(d, x, y, scared=False, frame=0, big=2):
    R = lambda a, b, w, h, c: rect(d, x + a * big, y + b * big, w * big, h * big, c)
    R(2, 0, 8, 8, "peach"); R(2, 0, 8, 3, "brown")
    R(4, 4, 1, 1 + scared, "black"); R(7, 4, 1, 1 + scared, "black")
    R(1, 8, 10, 9, "orange")
    R(2, 17, 3, 6, "navy"); R(7, 17, 3, 6, "navy")
    if scared:
        R(-2, 4 - frame, 3, 3, "peach"); R(11, 4 - frame, 3, 3, "peach")

def zombie(d, x, y, frame=0, big=1):
    s = big
    R = lambda a, b, w, h, c: rect(d, x + a * s, y + b * s, w * s, h * s, c)
    R(2, 0, 8, 8, "green"); R(2, 0, 8, 2, "dgreen")
    R(3, 3, 2, 2, "red"); R(7, 4, 1, 1, "red")
    R(4, 6, 4, 1, "black")
    R(1, 8, 10, 9, "lav"); R(4, 13, 3, 4, "purple")
    R(-6, 9, 7, 3, "green"); R(-6, 12, 7, 2, "green")
    if frame % 2 == 0:
        R(2, 17, 3, 7, "brown"); R(7, 17, 3, 6, "brown")
    else:
        R(1, 17, 3, 6, "brown"); R(8, 17, 3, 7, "brown")

def typed(s, t0, t, cps=14):
    n = max(0, int((t - t0) * cps))
    return s[:n]

def frame(t):
    img = Image.new("RGB", (LW, LH), P["black"]); d = ImageDraw.Draw(img)
    shake = (0, 0)
    if t < 3.0:
        sky(d, t); ground(d)
        y = int(60 + max(0, 1 - t / 0.6) * -80)
        text(d, LW / 2, y, "DATOS QUE", "white", FONTB)
        text(d, LW / 2, y + 18, "ASUSTAN", "yellow", FONTB)
        if t > 1.0 and int(t * 4) % 2 == 0:
            text(d, LW / 2, 250, "PRESS START", "pink")
        zombie(d, 30, 182, int(t * 4), big=2); hero(d, 130, 184)
    elif t < 10.5:
        lt = t - 3.0
        sky(d, t); ground(d); store(d, t)
        hero(d, 128, 184, scared=lt > 3.0, frame=int(t * 8) % 2)
        zx = int(-30 + min(lt, 6.0) * 13)
        zombie(d, zx, 182, int(t * 5), big=2)
        if lt > 3.5:
            zombie(d, zx - 46, 182, int(t * 5) + 1, big=2)
        rect(d, 0, 0, LW, 22, "black")
        text(d, LW / 2, 7, typed("3:00 A.M.  MINISUPER...", 0.2, lt), "white")
        rect(d, 10, 280, 160, 30, "black"); rect(d, 10, 280, 160, 1, "white"); rect(d, 10, 309, 160, 1, "white")
        text(d, LW / 2, 286, typed("AFUERA EMPIEZAN LOS GRITOS", 2.5, lt), "yellow")
    elif t < 14.0:
        lt = t - 10.5
        rect(d, 0, 0, LW, LH, "navy")
        for y in range(30, 250, 2):
            if y % 6 == 0: rect(d, 10, y, 160, 1, "blue")
        zombie(d, 50, 60, int(t * 3), big=5)
        rect(d, 10, 30, 160, 2, "lgray"); rect(d, 10, 250, 160, 2, "lgray")
        if int(lt * 10) % 2 == 0 and lt > 0.3:
            for k in range(3):
                rect(d, 30 + k * 50, 120 + (k % 2) * 30, 10, 12, "green")
        if lt > 0.8:
            sc = min(1.0, (lt - 0.8) / 0.2)
            rect(d, 15, 262, 150, 36, "red"); rect(d, 15, 262, 150, 2, "white"); rect(d, 15, 296, 150, 2, "white")
            text(d, LW / 2, 271, "¿SOBREVIVIRIAS?", "white", FONTB)
        if 0.0 < lt < 0.6:
            shake = (random.randint(-3, 3), random.randint(-3, 3))
    else:
        lt = t - 14.0
        rect(d, 0, 0, LW, LH, "black")
        text(d, LW / 2, 120, "GAME OVER?", "red", FONTB)
        text(d, LW / 2, 150, "COMENTA QUE", "white")
        text(d, LW / 2, 162, "AGARRARIAS PRIMERO", "yellow")
        if int(lt * 3) % 2 == 0: text(d, LW / 2, 200, "> CONTINUAR <", "pink")
    big = img.resize((LW * SC, LH * SC), Image.NEAREST)
    arr = np.asarray(big)
    if shake != (0, 0):
        arr = np.roll(arr, shake[0] * SC, axis=1); arr = np.roll(arr, shake[1] * SC, axis=0)
    # subtle scanlines for the retro screen feel
    arr = arr.copy(); arr[::SC, :, :] = (arr[::SC, :, :] * 0.82).astype(np.uint8)
    return arr

def chiptune(path):
    SR = 44100; N = int(SR * DUR); out = np.zeros(N)
    def sq(f, d, duty=0.5):
        n = int(d * SR); ph = (np.arange(n) * f / SR) % 1.0
        return np.where(ph < duty, 1.0, -1.0) * np.exp(-np.arange(n) / SR / (d * 0.9))
    def add(st, sig, g):
        i = int(st * SR); j = min(N, i + len(sig)); out[i:j] += sig[:j - i] * g
    bpm = 132; beat = 60 / bpm; step = beat / 2
    mel = [220, 0, 261.6, 220, 329.6, 311.1, 293.7, 0, 220, 0, 261.6, 220, 196, 207.7, 220, 0]
    bass = [55, 55, 65.4, 65.4, 49, 49, 51.9, 51.9]
    for k, st in enumerate(np.arange(0, DUR - 0.5, step)):
        f = mel[k % 16] * (2 if st > 10.5 else 1)
        if f: add(st, sq(f, step * 0.9, 0.25), 0.18)
        if k % 2 == 0: add(st, sq(bass[(k // 2) % 8], step * 1.8, 0.5), 0.16)
        if k % 4 == 2:
            n = np.random.default_rng(k).uniform(-1, 1, int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR / 0.015)
            add(st, n, 0.25)
        if k % 4 == 0:
            kick = np.sin(2 * np.pi * np.cumsum(np.linspace(150, 40, int(0.1 * SR))) / SR) * np.exp(-np.arange(int(0.1 * SR)) / SR / 0.04)
            add(st, kick, 0.5)
    # hit at the zombie close-up
    n = np.random.default_rng(1).uniform(-1, 1, int(0.5 * SR)) * np.exp(-np.arange(int(0.5 * SR)) / SR / 0.15)
    add(10.5, n, 0.6); add(10.5, sq(80, 0.6, 0.5), 0.3)
    for k in range(4): add(14.0 + k * 0.18, sq([523, 392, 330, 262][k], 0.17, 0.5), 0.2)
    out = out / np.max(np.abs(out)) * 0.9
    fade = np.ones(N); fade[-int(0.3 * SR):] = np.linspace(1, 0, int(0.3 * SR)); out *= fade
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        ims = [Image.fromarray(frame(float(x))).resize((270, 480), Image.NEAREST) for x in sys.argv[2:]]
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im, (i * 270, 0))
        sh.save("pixel_prev.png"); sys.exit()
    chiptune("pixel.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW*SC}x{LH*SC}",
                          "-r", str(FPS), "-i", "-", "-i", "pixel.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", sys.argv[1]], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
