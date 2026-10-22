"""Capa delgada: este módulo vive en el motor (reels_engine.core). Se conserva el nombre lib.core para los specs."""
import sys, reels_engine.core as _m
sys.modules[__name__] = _m
