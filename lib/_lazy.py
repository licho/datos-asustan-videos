import importlib, os, sys
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
if SRC not in sys.path: sys.path.insert(0, SRC)
def make(MAP, modname):
    def __getattr__(name):
        if name not in MAP: raise AttributeError(f"{modname}: no existe '{name}'. Disponibles: {', '.join(sorted(MAP))}")
        mod, _, real = MAP[name].partition(":")
        obj = getattr(importlib.import_module(mod), real or name)
        if callable(obj) and not modname.endswith("fondos"):
            from .check import element_wrap
            obj = element_wrap(obj, name)
        return obj
    return __getattr__
