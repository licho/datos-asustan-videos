"""Regenera lib/CATALOGO.md:  python3 -m lib.catalogo  (el generador vive en el motor; lo que se lista sale de lib/canal.py)"""
from . import personajes, props, fondos   # asegura src/ en sys.path para leer las piezas viejas
from reels_engine.catalogo import generate
if __name__ == "__main__":
    generate()
