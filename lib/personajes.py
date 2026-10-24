"""Personajes y criaturas reutilizables (cartoon salvo indicación). Se cargan bajo demanda.
Los comunes (guy, anchors, medal) vienen del motor; aquí se agregan los del canal."""
from ._lazy import make
from reels_engine.registry import PERSONAJES
MAP = {**PERSONAJES,
 # humanos
 "zombie": "reel", "employee": "reel8", "taquero": "reel24", "president": "reel24", "scientist": "reel24",
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
 "mummy": "lib.criaturas",
 "don_tono": "lib.humanos",
 "brain": "lib.criaturas", "rat": "lib.criaturas", "heart_face": "lib.criaturas",

 "mammoth": "lib.animales", "stego": "lib.animales", "trex": "lib.animales", "cleopatra": "lib.humanos",
 "soldier": "lib.humanos", "napoleon": "lib.humanos", "scribe": "lib.humanos", "emu": "lib.animales", "army_ant": "lib.animales", "ant_column": "lib.animales", "rat_skeleton": "lib.criaturas", "llorona": "lib.criaturas", "robo_cw": "lib.humanos", "elf": "lib.criaturas", "krampus": "lib.criaturas", "louse": "lib.criaturas", "hawk": "lib.animales", "tyranno": "lib.animales", "chaya": "lib.criaturas", "chaya_leaf_zoom": "lib.criaturas", "giraffe": "lib.animales", "stamp_point": "lib.humanos", "raptor": "lib.animales", "pigeon": "lib.animales", "shrew": "lib.animales", "elephant": "lib.animales", "st_nicholas": "lib.humanos"
}
__getattr__ = make(MAP, __name__)
