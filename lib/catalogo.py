"""Regenera lib/CATALOGO.md:  python3 -m lib.catalogo"""
import ast, importlib, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def sig(fn, name=None):
    a = fn.args; names = [x.arg for x in a.args]; dfl = [None] * (len(names) - len(a.defaults)) + [ast.unparse(x) for x in a.defaults]
    ps = [n if v is None else f"{n}={v}" for n, v in zip(names, dfl)]
    if a.vararg: ps.append("*" + a.vararg.arg)
    ps += [k.arg for k in a.kwonlyargs]
    if a.kwarg: ps.append("**" + a.kwarg.arg)
    return f"{name or fn.name}({', '.join(ps)})"
def path_of(mod):
    return os.path.join(ROOT, *mod.split(".")) + ".py" if mod.startswith("lib.") else os.path.join(ROOT, "src", mod + ".py")
out = ["# Catálogo de la librería (`lib/`)\n",
       "Generado con `python3 -m lib.catalogo`. Para un video nuevo: copia un spec de `specs/`, cambia LINES/SCENES/SFX y usa `python3 -m lib.produce SPEC texto|preview|sinvoz|final VOZ.mp3`.\n",
       "Escenarios: `lib/escenarios.py` (piso, rango de pies y zona libre de cada fondo; guía visual en `lib/muestras/escenarios.png`). Revisión automática: `python3 -m lib.produce SPEC check` (también corre sola antes de cada render).\n",
       "Zonas seguras (1080x1920): letreros y=300/420 · acción 480–1320 · piso 1300 · subtítulos 1500 (no poner nada entre 1380 y 1640).\n"]
for f in ["core", "audio"]:
    out.append(f"\n## lib.{f}\n")
    for n in ast.walk(ast.parse(open(path_of("lib." + f)).read())):
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_"):
            doc = (ast.get_docstring(n) or "").split("\n")[0]
            out.append(f"- `{sig(n)}`" + (f" — {doc}" if doc else ""))
for f in ["personajes", "props", "fondos"]:
    M = importlib.import_module(f"lib.{f}"); out.append(f"\n## lib.{f}\n")
    for k, v in sorted(M.MAP.items()):
        mod, _, real = v.partition(":")
        node = next((n for n in ast.parse(open(path_of(mod)).read()).body if isinstance(n, ast.FunctionDef) and n.name == (real or k)), None)
        doc = (ast.get_docstring(node) or "").split("\n")[0] if node else ""
        out.append(f"- `{sig(node, k) if node else k}` · {mod}" + (f" — {doc}" if doc else ""))
open(os.path.join(ROOT, "lib", "CATALOGO.md"), "w").write("\n".join(out) + "\n")
print(len(out), "líneas")
