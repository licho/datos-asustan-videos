"""Objetos reutilizables. Se cargan bajo demanda desde src/."""
from ._lazy import make
MAP = {
 "card": "reel", "icon": "reel", "freezer": "reel",
 "taco": "reel24", "trompo": "reel24", "street_sign": "reel24", "portal": "reel24", "tank": "reel24", "land": "reel24",
 "plane": "reel25", "building": "reel25", "car": "reel25", "clock": "reel25", "wave": "reel25",
 "taper": "reel26", "jar": "reel26", "milk": "reel26", "lettuce": "reel26", "rice_bowl": "reel26", "microwave": "reel26",
 "meat": "reel26", "salad": "reel26", "fruit": "reel26", "cloud": "reel26",
 "sandal": "reel27", "glass": "reel27",
 "asteroid": "reel13", "bus": "reel13", "ship": "reel13", "window_frame": "reel13", "table": "reel13",
 "bed": "reel12", "banana": "reel12", "pillow": "reel12", "pie": "reel12", "shoe": "reel12",
 "garlic": "reel14", "blood_bag": "reel14", "desk": "reel15", "thermo": "reel19", "ticket": "reel19",
 "pizza": "reel2", "phone": "reel2", "toilet_seat": "reel2", "magnifier": "reel2", "bottle": "reel2",
 "boat": "reel3", "book": "reel3", "offering": "reel4", "keys": "reel4", "corn": "reel4", "washer": "reel5", "vacuum": "reel5",
 "big_toilet": "reel7", "truck": "reel8", "pot": "reel8", "coffee_machine": "reel8", "ice_machine": "reel8", "phone_small": "reel9",
 "voyager": "reel23", "planet_earth": "reel23", "jupiter": "reel23", "sun": "reel23", "spin_earth": "reel25", "earth": "reel13",
 "ufo": "alien", "backpack": "alien", "heli": "mision002", "cactus": "mision002", "hive": "mision003", "mower": "mision003",
 # nuevos (lib/objetos.py)
"podium": "lib.objetos", "radar": "lib.objetos", "bucket": "lib.objetos", "tire": "lib.objetos", "flowerpot": "lib.objetos", "cake": "lib.objetos", "balloons": "lib.objetos", "spray": "lib.objetos", "net": "lib.objetos", "skull": "lib.objetos", "egg_raft": "lib.objetos",
}
__getattr__ = make(MAP, __name__)
