"""Capa delgada: este módulo vive en el motor (reels_engine.align). Se conserva el nombre lib.align para los specs."""
import sys, reels_engine.align as _m
sys.modules[__name__] = _m
