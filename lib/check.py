"""Capa delgada: este módulo vive en el motor (reels_engine.check). Se conserva el nombre lib.check para los specs."""
import sys, reels_engine.check as _m
sys.modules[__name__] = _m
