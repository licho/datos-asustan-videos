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
       "Escenarios: `lib/escenarios.py` (piso, rango de pies y zona libre de cada fondo; guía visual en `lib/muestras/escenarios.png`). Flujo: `hoja` (revisión visual en ~4 s) → `check` (~5 s; se recuerda si no cambió nada) → `sinvoz` (todos los núcleos, ~90 s). El contraste (`check-contraste`, ~50 s) solo si se pide; Luis revisa el contraste en el video final.\n",
       "Contraste: toda pieza nueva lleva contorno; sobre fondos oscuros, contorno + relleno claro o un foco de luz detrás. `check-contraste` mide la silueta real de cada pieza contra lo que tiene detrás y avisa si más del 30% de su orilla se confunde (GRAVE desde 50%).\n",
       "Objetos en personajes: usa `anchors(x, pies, escala)` (lib.personajes) para cabeza, cuello, pecho y manos de cada pose; nunca coordenadas a ojo.\n",
       "Animación estándar (lib.motion): entradas con `tw(t, t0, dur, a, b, back_out|elastic_out)`, flotar con `yoyo`, aplastar/estirar/girar/desvanecer con `layer`, susto con `shake`, brillo con `glow`, volumen con `sphere_shade`. Subtítulos palabra por palabra y viñeta salen solos (CAPTION_STYLE='static' / VIGNETTE=0 para desactivar).\n",
       "Diálogos: usa `say(d, texto, mouth, head)` (lib.core): el globo se acomoda solo arriba o a un lado de quien habla, sin tapar su cabeza y con punta corta. Para guy/don_tono: a=anchors(x, pies, s); say(d, texto, a['mouth'], a['head_r']).\n",
       "Zonas seguras (1080x1920): letreros y=300/420 · acción 480–1320 · piso 1300 · subtítulos 1500 (no poner nada entre 1380 y 1640).\n"]
for f in ["core", "motion", "audio"]:
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
