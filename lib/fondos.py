"""Fondos completos (imagen 1080x1920). Se cargan bajo demanda.
make_space y radial_bg vienen del motor; aquí se agregan los del canal."""
from ._lazy import make
from reels_engine.registry import FONDOS
MAP = {**FONDOS,
 "make_store": "reel", "make_outside": "reel", "make_coldroom_in": "reel", "store_day": "reel8", "outside_day": "reel8",
 "room": "reel12", "make_space_v1": "reel13:make_space", "city": "reel13", "night_room": "reel14", "store_bg": "reel14", "office": "reel15",
 "kitchen": "reel16", "moon": "reel17", "night": "reel17", "make_sea": "reel3", "make_jungle": "reel4", "make_bath": "reel7",
 "make_street": "reel9", "make_room": "reel9", "skyline": "reel24", "town": "reel25", "make_fridge": "reel26",
 "make_kitchen": "reel27", "make_milky": "reel23", "make_field": "reel23", "desk_glow": "reel2",
 "desert_pixel": "mision002:desert", "garden_pixel": "mision003:garden", "forest_pixel": "oso:forest", "altar_pixel": "ofrenda:altar",
 "make_coldroom_out": "reel", "store_floor": "reel:floor", "store_ceiling": "reel:ceiling", "make_site": "reel4", "sun_desert": "reel19", "rlyeh_city": "reel3:city", "city_pixel": "alien:city", "street_pixel": "zombi11:street", "store_pixel": "pixel:store", "sky_pixel": "pixel:sky", "ground_pixel": "pixel:ground", "room_ofrenda_pixel": "ofrenda:room", "oficina": "lib.fondos_canal", "river_night": "lib.fondos_canal", "living_room": "lib.fondos_canal", "village": "lib.fondos_canal", "city_street": "lib.fondos_canal", "subway_tunnel": "lib.fondos_canal", "forest_city": "lib.fondos_canal", "savanna": "lib.fondos_canal", "monte": "lib.fondos_canal"
}
__getattr__ = make(MAP, __name__)
