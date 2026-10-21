"""Fondos completos (imagen 1080x1920). Se cargan bajo demanda desde src/."""
from ._lazy import make
MAP = {
 "make_store": "reel", "make_outside": "reel", "make_coldroom_in": "reel", "store_day": "reel8", "outside_day": "reel8",
 "room": "reel12", "make_space": "reel13", "city": "reel13", "night_room": "reel14", "store_bg": "reel14", "office": "reel15",
 "kitchen": "reel16", "moon": "reel17", "night": "reel17", "make_sea": "reel3", "make_jungle": "reel4", "make_bath": "reel7",
 "make_street": "reel9", "make_room": "reel9", "skyline": "reel24", "town": "reel25", "make_fridge": "reel26",
 "make_kitchen": "reel27", "make_milky": "reel23", "make_field": "reel23", "desk_glow": "reel2",
 "desert_pixel": "mision002:desert", "garden_pixel": "mision003:garden", "forest_pixel": "oso:forest", "altar_pixel": "ofrenda:altar",
}
__getattr__ = make(MAP, __name__)
