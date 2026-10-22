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
