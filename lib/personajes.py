"""Personajes y criaturas reutilizables (cartoon salvo indicación). Se cargan bajo demanda desde src/."""
from ._lazy import make
MAP = {
 # humanos
 "guy": "reel", "zombie": "reel", "employee": "reel8", "taquero": "reel24", "president": "reel24", "scientist": "reel24",
 "stamp_guy": "reel25", "sick_guy": "reel26", "crouch_guy": "reel13", "person": "reel2", "doc": "reel14", "face": "reel23",
 # monstruos y criaturas
 "creature": "reel24", "vampire": "reel14", "alien_cw": "reel15", "zomb": "reel18", "doppel": "reel9", "cthulhu": "reel3",
 "tentacle": "reel3", "alux": "reel4", "blob": "reel15",
 # animales y bichos
 "wolf": "reel17", "dog": "reel17", "cat": "reel17", "cow": "reel25", "dino": "reel13", "roach": "reel27", "roach_head": "reel27",
 "fly": "reel12", "mite": "reel5", "germ": "reel2", "bacteria": "reel26", "listeria": "reel26", "mold": "reel26", "sponge": "reel16",
 # nuevos (lib/animales.py)
 "mosquito": "lib.animales", "shark": "lib.animales", "snake": "lib.animales", "lion": "lib.animales",
 # pixel art
 "hero_pixel": "mision002:hero", "bee": "mision003", "swarm": "mision003", "bear": "oso", "soul": "ofrenda",
 "roach_v12": "reel12:roach", "alien_pixel": "alien:alien", "hero_pixel_v1": "pixel:hero", "zombie_pixel": "pixel:zombie", "alux_laugh": "reel4:jiji", "thief": "reel4",
 "ghost": "lib.criaturas", "ghost_draw": "lib.criaturas",
 "crab": "lib.animales", "coral": "lib.animales",
 "mummy": "lib.criaturas"
}
__getattr__ = make(MAP, __name__)
