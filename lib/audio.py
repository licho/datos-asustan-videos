"""Capa delgada: este módulo vive en el motor (reels_engine.audio). Se conserva el nombre lib.audio para los specs."""
import sys, reels_engine.audio as _m
sys.modules[__name__] = _m
