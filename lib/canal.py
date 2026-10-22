"""Configuración del canal Datos que Asustan para el motor (reels_engine).
Todo lo que es propio de este canal (colores, zonas, carpeta de salida, catálogo) se ajusta aquí."""
import os
from reels_engine import Channel

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

CANAL = Channel(
    name="datos-que-asustan",
    root=ROOT,
    outdir="/tmp/dqa_out",
    code_dirs=("lib",),
    contrast_skip=("popup", "dialog_px", "hud_px", "finish", "canvas_px"),   # piezas pixel art: no se revisan por contraste
    # Música extra del canal. Melodías de dominio público (Jingle Bells, J. Pierpont, 1857). Cada paso = media negra;
    # mel se toca una octava arriba (frecuencia × 2).
    music_styles={
        "navidad": dict(bpm=92, wave="sq",
                        bass=[98, 0, 73.4, 0, 98, 0, 73.4, 0],
                        mel=[246.9, 246.9, 246.9, 0, 246.9, 246.9, 246.9, 0, 246.9, 293.7, 196, 220, 246.9, 0, 0, 0]),
        "navidad_oscura": dict(bpm=70, wave="saw",
                        bass=[49, 0, 49, 0, 73.4, 0, 46.2, 0],
                        mel=[233.1, 233.1, 233.1, 0, 233.1, 233.1, 233.1, 0, 233.1, 277.2, 196, 207.7, 233.1, 0, 0, 0]),
    },
    catalog_out="lib/CATALOGO.md",
    catalog_api=(("lib.core", "reels_engine.core"), ("lib.motion", "reels_engine.motion"), ("lib.audio", "reels_engine.audio")),
    catalog_maps=("lib.personajes", "lib.props", "lib.fondos"),
    catalog_header=("# Catálogo de la librería (`lib/`)\n",
       "Generado con `python3 -m lib.catalogo`. Para un video nuevo: copia un spec de `specs/`, cambia LINES/SCENES/SFX y usa `python3 -m lib.produce SPEC texto|preview|sinvoz|final VOZ.mp3`.\n",
       "Escenarios: `lib/escenarios.py` (piso, rango de pies y zona libre de cada fondo; guía visual en `lib/muestras/escenarios.png`). Flujo: `hoja` (revisión visual en ~4 s) → `check` (~5 s; se recuerda si no cambió nada) → `sinvoz` (todos los núcleos, ~90 s). El contraste (`check-contraste`, ~50 s) solo si se pide; Luis revisa el contraste en el video final.\n",
       "Contraste: toda pieza nueva lleva contorno; sobre fondos oscuros, contorno + relleno claro o un foco de luz detrás. `check-contraste` mide la silueta real de cada pieza contra lo que tiene detrás y avisa si más del 30% de su orilla se confunde (GRAVE desde 50%).\n",
       "Objetos en personajes: usa `anchors(x, pies, escala)` (lib.personajes) para cabeza, cuello, pecho y manos de cada pose; nunca coordenadas a ojo.\n",
       "Animación estándar (lib.motion): entradas con `tw(t, t0, dur, a, b, back_out|elastic_out)`, flotar con `yoyo`, aplastar/estirar/girar/desvanecer con `layer`, susto con `shake`, brillo con `glow`, volumen con `sphere_shade`. Subtítulos palabra por palabra y viñeta salen solos (CAPTION_STYLE='static' / VIGNETTE=0 para desactivar).\n",
       "Diálogos: usa `say(d, texto, mouth, head)` (lib.core): el globo se acomoda solo arriba o a un lado de quien habla, sin tapar su cabeza y con punta corta. Para guy/don_tono: a=anchors(x, pies, s); say(d, texto, a['mouth'], a['head_r']).\n",
       "Zonas seguras (1080x1920): letreros y=300/420 · acción 480–1320 · piso 1300 · subtítulos 1500 (no poner nada entre 1380 y 1640).\n"),
)
