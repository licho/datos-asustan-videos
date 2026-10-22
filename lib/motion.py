"""Capa delgada: este módulo vive en el motor (reels_engine.motion). Se conserva el nombre lib.motion para los specs."""
import sys, reels_engine.motion as _m
sys.modules[__name__] = _m
