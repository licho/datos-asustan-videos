"""Revisión automática de cuadros: registra la caja (bbox) de todo lo que se dibuja y avisa de
  1) elementos que invaden los subtítulos, 2) textos cortados por el borde, 3) textos encimados entre sí.
Uso:  python3 -m lib.produce SPEC check"""
from contextlib import contextmanager
from PIL import ImageDraw
from .core import W, H

_OPS = ("ellipse", "rectangle", "rounded_rectangle", "polygon", "line", "arc", "chord", "pieslice", "text")
_orig = {k: getattr(ImageDraw.ImageDraw, k) for k in _OPS}

def _bbox_pts(xy):
    if hasattr(xy, "__len__") and len(xy) == 4 and all(isinstance(v, (int, float)) for v in xy):
        return [xy[0], xy[1], xy[2], xy[3]]
    pts = list(xy)
    if pts and isinstance(pts[0], (int, float)): pts = list(zip(pts[0::2], pts[1::2]))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)]

class Rec:
    def __init__(self): self.items = []; self.tag = "scene"

@contextmanager
def recording(rec):
    def wrap(name):
        f = _orig[name]
        def g(self, xy, *a, **kw):
            try:
                if name == "text":
                    txt = a[0] if a else kw.get("text", "")
                    bb = list(self.textbbox(xy, txt, font=kw.get("font"), anchor=kw.get("anchor"), stroke_width=kw.get("stroke_width", 0)))
                    rec.items.append((rec.tag, "text", str(txt), bb))
                else:
                    bb = _bbox_pts(xy); w = kw.get("width", 0) or 0
                    bb = [bb[0] - w / 2, bb[1] - w / 2, bb[2] + w / 2, bb[3] + w / 2]
                    rec.items.append((rec.tag, name, "", bb))
            except Exception:
                pass
            return f(self, xy, *a, **kw)
        return g
    for k in _OPS: setattr(ImageDraw.ImageDraw, k, wrap(k))
    try: yield rec
    finally:
        for k in _OPS: setattr(ImageDraw.ImageDraw, k, _orig[k])

def _inter(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
def _area(a): return max(1, (a[2] - a[0]) * (a[3] - a[1]))

def analyze(items, margin=18):
    """Devuelve lista de problemas (texto) para un cuadro."""
    probs = []
    cap = [b for tg, k, s, b in items if tg == "caption"]
    capbox = [min(b[0] for b in cap) - margin, min(b[1] for b in cap) - margin, max(b[2] for b in cap) + margin, max(b[3] for b in cap) + margin] if cap else None
    scene = [(k, s, b) for tg, k, s, b in items if tg == "scene"]
    for k, s, b in scene:
        bw, bh = b[2] - b[0], b[3] - b[1]
        if bw >= .9 * W or bh >= .6 * H: continue                 # fondo / bandas de piso
        if capbox and _inter(b, capbox) > 0 and (k == "text" or bw * bh > 45 * 45):
            lvl = "leve (línea delgada)" if k in ("line", "arc") else "GRAVE"
            probs.append((f"invade subtítulos [{lvl}]: {k} {s!r}".replace(" ''", ""), int(b[3]) - int(capbox[1])))
        if k == "text" and (b[0] < 0 or b[2] > W or b[1] < 0):
            probs.append((f"texto cortado por el borde [GRAVE]: {s!r}", int(max(-b[0], b[2] - W, -b[1]))))
    texts = [(s, b) for k, s, b in scene if k == "text" and s.strip()]
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            (s1, b1), (s2, b2) = texts[i], texts[j]
            if _inter(b1, b2) > .15 * min(_area(b1), _area(b2)) and s1 != s2:
                probs.append((f"textos encimados [GRAVE]: {s1!r} / {s2!r}", 0))
    return probs
