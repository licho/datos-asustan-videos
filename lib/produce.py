"""Capa delgada: los comandos viven en el motor (reels_engine.produce).
Uso:  python3 -m lib.produce SPEC.py texto|hoja|preview|check|check-contraste|sinvoz|final VOZ.mp3"""
import sys, reels_engine.produce as _m
if __name__ == "__main__":
    _m.main()
else:
    sys.modules[__name__] = _m
