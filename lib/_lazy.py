import importlib, os, sys
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
if SRC not in sys.path: sys.path.insert(0, SRC)
def make(MAP, modname):
    def __getattr__(name):
        if name not in MAP: raise AttributeError(f"{modname}: no existe '{name}'. Disponibles: {', '.join(sorted(MAP))}")
        mod, _, real = MAP[name].partition(":")
        return getattr(importlib.import_module(mod), real or name)
    return __getattr__
