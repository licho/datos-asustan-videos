"""Mapa de escenarios: dónde está el piso y qué zonas quedan libres.
  floor  = línea donde termina la pared y empieza el piso (o el horizonte)
  feet   = rango de 'y' válido para los pies de personajes parados (no flotan y no tapan subtítulos)
  air    = caja libre para cosas que vuelan o letreros grandes (x0, y0, x1, y1)
  tipo   = interior | exterior | agua | espacio
Uso:  from lib.escenarios import ESC, feet_y ;  guy(d, 540, feet_y("make_kitchen"), ...)"""
from .core import W

CAP_TOP = 1350   # nada que pise debe bajar de aquí (subtítulos empiezan ~1380)

ESC = {
 "make_kitchen":     dict(floor=1240, feet=(1250, 1330), air=(0, 480, W, 1150), tipo="interior", nota="cocina con azulejo y zoclo café (1160–1240)"),
 "kitchen":          dict(floor=1229, feet=(1240, 1330), air=(0, 480, W, 1100), tipo="interior", nota="cocina de la esponja"),
 "room":             dict(floor=1149, feet=(1170, 1330), air=(0, 480, W, 1100), tipo="interior", nota="recámara de día; room(mess, dark)"),
 "make_room":        dict(floor=1149, feet=(1170, 1330), air=(0, 480, W, 1100), tipo="interior", nota="sala; make_room(dark)"),
 "night_room":       dict(floor=1199, feet=(1210, 1330), air=(0, 620, W, 1150), tipo="interior", nota="cuarto de noche con ventana y luna arriba a la derecha (y 280–600)"),
 "office":           dict(floor=1199, feet=(1210, 1330), air=(0, 480, W, 1150), tipo="interior", nota="oficina"),
 "make_store":       dict(floor=1150, feet=(1170, 1330), air=(0, 480, W, 1100), tipo="interior", nota="minisúper de noche"),
 "make_coldroom_in": dict(floor=1150, feet=(1170, 1330), air=(0, 480, W, 1100), tipo="interior", nota="cuarto frío por dentro"),
 "make_bath":        dict(floor=1299, feet=(1300, 1335), air=(0, 480, W, 1250), tipo="interior", nota="baño; piso muy bajo, usar personajes chicos"),
 "make_jungle":      dict(floor=1209, feet=(1220, 1330), air=(0, 480, W, 1150), tipo="exterior", nota="selva"),
 "make_street":      dict(floor=1069, feet=(1090, 1330), air=(0, 480, W, 1050), tipo="exterior", nota="calle con banqueta"),
 "city":             dict(floor=1200, feet=(1220, 1330), air=(0, 300, W, 900), tipo="exterior", nota="ciudad; edificios hasta ~1200"),
 "make_sea":         dict(floor=1049, feet=None, air=(0, 300, W, 1040), tipo="agua", nota="mar de noche; horizonte en 1049, barcos flotan en 1040–1100"),
 "make_space":       dict(floor=None, feet=None, air=(0, 300, W, 1340), tipo="espacio", nota="espacio con estrellas"),
 "make_field":       dict(floor=None, feet=None, air=(0, 300, W, 1340), tipo="espacio", nota="campo de galaxias"),
}

def feet_y(name, k=0.5):
    """Y para pies de personaje parado (k=0 fondo del cuarto, k=1 al frente)."""
    a, b = ESC[name]["feet"]; return a + (b - a) * k
