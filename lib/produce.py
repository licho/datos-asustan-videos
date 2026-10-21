"""Producción de un video a partir de un archivo de especificación (spec).

Uso:
  python3 -m lib.produce SPEC.py texto              -> texto para ElevenLabs
  python3 -m lib.produce SPEC.py preview 1.5 8 20   -> hoja de cuadros (tiempos nominales)
  python3 -m lib.produce SPEC.py sinvoz             -> video sin voz (música + efectos)
  python3 -m lib.produce SPEC.py final VOZ.mp3      -> video final sincronizado con la voz
Cada render genera también una hoja de verificación (1 cuadro cada 2 s)."""
import importlib.util, os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
from .core import W, H, rich_caption, CAP_Y
from .audio import Mix
from . import align

FPS = 30; WPS = 2.75; GAP = 0.35
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

class Ctx:
    pass

def load(spec_path):
    sp = importlib.util.spec_from_file_location("spec", spec_path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    lines = [L if len(L) == 3 else (L[0], L[1], L[1]) for L in m.LINES]
    m.LINES = lines
    st, t = [], 0.0
    for tag, spoken, cap in lines:
        st.append(t); t += align.nwords(spoken) / WPS + GAP
    m.NSTART = st; m.NEND = t + getattr(m, "END", 4.0)
    return m

def voice_text(m):
    return " ".join((f"[{tag}] " if tag else "") + spoken for tag, spoken, cap in m.LINES)

def make_warp(m, voice=None):
    if not voice:
        return (lambda T: T), (lambda v: v), m.NEND
    real, dur = align.line_starts(voice, [s for _, s, _ in m.LINES])
    end_real = dur + getattr(m, "END", 4.0)
    TK = np.array([0.0] + real[1:] + [dur, end_real]); VK = np.array([0.0] + m.NSTART[1:] + [m.NSTART[-1] + (dur - real[-1]), m.NEND])
    order = np.argsort(TK); TK, VK = TK[order], VK[order]
    return (lambda T: float(np.interp(T, TK, VK))), (lambda v: float(np.interp(v, VK, TK))), end_real

def scene_at(m, v):
    cur = None
    for i, (li, fn) in enumerate(m.SCENES):
        start = m.NSTART[li]
        if v >= start: cur = (fn, start, (m.NSTART[m.SCENES[i + 1][0]] if i + 1 < len(m.SCENES) else m.NEND))
    return cur

def render_frame(m, v, t):
    fn, s0, s1 = scene_at(m, v)
    c = Ctx(); c.v = v; c.t = t; c.lt = v - s0; c.dur = s1 - s0; c.shake = 0
    c.at = lambda i: m.NSTART[i] - s0          # inicio de la línea i relativo a la escena
    img = fn(c)
    d = ImageDraw.Draw(img)
    for i, (tag, spoken, cap) in enumerate(m.LINES):
        e = m.NSTART[i + 1] if i + 1 < len(m.LINES) else m.NEND
        if m.NSTART[i] <= v < e and cap: rich_caption(d, cap, y=CAP_Y, appear=(v - m.NSTART[i]) / 0.25)
    arr = np.asarray(img)
    if c.shake: arr = np.roll(arr, int(math.sin(t * 60) * c.shake), axis=1)
    return arr

def build_audio(m, out_wav, T_of_v, v_of_T, dur, voice=None):
    mx = Mix(dur, T_of_v); mx.v_of_T = v_of_T
    mus = getattr(m, "MUSIC", ("bass", [], None))
    quiet = [(m.NSTART[a], m.NSTART[b] if b < len(m.LINES) else m.NEND) for a, b in mus[1]]
    mx.music(mus[0], quiet=quiet, loud_from=(m.NSTART[mus[2]] if mus[2] is not None else None))
    for li, off, name, *kw in getattr(m, "SFX", []):
        mx.fx(name, m.NSTART[li] + off, **(kw[0] if kw else {}))
    for (li, fn) in m.SCENES[1:]:
        mx.whoosh(m.NSTART[li])
    mx.render(out_wav, voice)

def encode(m, out_mp4, v_of_T, dur, wav):
    tmp = out_mp4 + ".v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        T = i / FPS
        p.stdin.write(render_frame(m, v_of_T(T), T).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out_mp4], check=True)
    os.remove(tmp)
    sheet = out_mp4.replace(".mp4", "_tile.png")
    cols = int(math.ceil(dur / 2 / 3))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out_mp4, "-vf", f"fps=1/2,scale=180:320,tile={cols}x3", "-frames:v", "1", sheet])
    return sheet

def main():
    spec, cmd = sys.argv[1], sys.argv[2]
    m = load(spec)
    name = getattr(m, "NAME", os.path.splitext(os.path.basename(spec))[0])
    outdir = getattr(m, "OUTDIR", "/tmp/dqa_out"); os.makedirs(outdir, exist_ok=True)
    if cmd == "texto":
        print(voice_text(m)); print(f"\n# palabras: {sum(align.nwords(s) for _, s, _ in m.LINES)}  duración estimada: {m.NEND:.0f} s"); return
    if cmd == "preview":
        ts = [float(x) for x in sys.argv[3:]]
        ims = [Image.fromarray(render_frame(m, x, x)).resize((270, 480)) for x in ts]
        sh = Image.new("RGB", (270 * min(6, len(ims)), 480 * ((len(ims) + 5) // 6)))
        for i, im in enumerate(ims): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
        p = os.path.join(outdir, f"{name}_preview.png"); sh.save(p); print(p); return
    voice = sys.argv[3] if cmd == "final" else None
    v_of_T, T_of_v, dur = make_warp(m, voice)
    wav = os.path.join(outdir, f"{name}.wav"); build_audio(m, wav, T_of_v, v_of_T, dur, voice)
    out = os.path.join(outdir, f"{name}{'_SINVOZ' if cmd == 'sinvoz' else ''}.mp4")
    sheet = encode(m, out, v_of_T, dur, wav)
    print(out); print(sheet); print(f"duración: {dur:.1f} s")

if __name__ == "__main__":
    main()
