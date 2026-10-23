"""Objetos reutilizables. Se cargan bajo demanda.
Los comunes (muebles, exteriores, pantallas) vienen del motor; aquí se agregan los del canal."""
from ._lazy import make
from reels_engine.registry import PROPS
MAP = {**PROPS,
 "card": "reel", "icon": "reel", "freezer": "reel",
 "taco": "reel24", "trompo": "reel24", "street_sign": "reel24", "portal": "reel24", "tank": "reel24", "land": "reel24",
 "plane": "reel25", "car": "reel25", "clock": "reel25", "wave": "reel25",
 "taper": "reel26", "jar": "reel26", "milk": "reel26", "lettuce": "reel26", "rice_bowl": "reel26", "microwave": "reel26",
 "meat": "reel26", "salad": "reel26", "fruit": "reel26", "cloud": "reel26",
 "sandal": "reel27", "glass": "reel27",
 "asteroid": "reel13", "bus": "reel13", "ship": "reel13", "window_frame": "reel13",  "bed": "reel12", "banana": "reel12", "pillow": "reel12", "pie": "reel12", "shoe": "reel12",
 "garlic": "reel14", "blood_bag": "reel14", "desk": "reel15", "thermo": "reel19", "ticket": "reel19",
 "pizza": "reel2", "phone": "reel2", "toilet_seat": "reel2", "magnifier": "reel2", "bottle": "reel2",
 "boat": "reel3", "book": "reel3", "offering": "reel4", "keys": "reel4", "corn": "reel4", "washer": "reel5", "vacuum": "reel5",
 "big_toilet": "reel7", "truck": "reel8", "pot": "reel8", "coffee_machine": "reel8", "ice_machine": "reel8", "phone_small": "reel9",
 "voyager": "reel23", "planet_earth": "reel23", "jupiter": "reel23", "sun": "reel23", "spin_earth": "reel25", "earth": "reel13",
 "ufo": "alien", "backpack": "alien", "heli": "mision002", "hive": "mision003", "mower": "mision003",
 # nuevos (lib/objetos.py)
"podium": "lib.objetos", "radar": "lib.objetos", "bucket": "lib.objetos", "tire": "lib.objetos", "flowerpot": "lib.objetos", "cake": "lib.objetos", "balloons": "lib.objetos", "spray": "lib.objetos", "net": "lib.objetos", "skull": "lib.objetos", "egg_raft": "lib.objetos",
  "outhouse": "lib.objetos", "white_flag": "lib.objetos", "helmet": "lib.objetos", "tortillas": "lib.objetos", "coffin": "lib.objetos", "templo": "lib.objetos", "fish": "lib.objetos", "empty_clothes": "lib.objetos", "plastic_bag": "lib.objetos", "old_tv": "lib.objetos", "tombstone": "lib.objetos", "shades": "lib.objetos", "trash_can": "lib.objetos", "torta": "lib.objetos", "soup_bowl": "lib.objetos", "place_setting": "lib.objetos", "snack_plate": "lib.objetos", "pet_collar": "lib.objetos", "tears": "lib.efectos", "office_desk": "lib.objetos", "xmas_tree": "lib.objetos", "tag": "lib.efectos", "rubber_stamp": "lib.efectos", "snow_fall": "lib.efectos", "sound_waves": "lib.efectos", "curtain": "lib.objetos", "open_box": "lib.objetos", "bells": "lib.criaturas", "box_lid": "lib.objetos", "bookshelf_crooked": "lib.objetos", "screw": "lib.objetos", "scroll": "lib.objetos", "sausages": "lib.objetos", "ball_chain": "lib.objetos", "cardboard_box": "lib.objetos", "captcha": "lib.pantallas", "candle": "lib.objetos", "shopping_cart": "lib.objetos", "time_clock": "lib.objetos", "microphone": "lib.criaturas", "codex": "lib.pantallas:codex",
 # antes sin registrar
 "building_v25": "reel25:building", "building_v13": "reel13:building", "table_v13": "reel13:table", "cactus_pixel": "mision002:cactus", "sofa": "reel9", "scar": "reel9", "dna": "reel9", "fridge_empty": "reel8", "bottle_v8": "reel8:bottle", "can": "reel8", "ice": "reel8", "heater": "reel8", "item_card": "reel8:card", "poop": "reel7", "phone_case": "reel7:case_shape", "port_zoom": "reel7", "skin_flake": "reel5:flake", "pellet": "reel5", "bed_v5": "reel5:bed", "microscope_circle": "reel5", "covers": "reel5", "dehumidifier": "reel5", "sun_pillow": "reel5", "bridge": "reel4", "casita": "reel4", "fridge_alux": "reel4:fridge", "post": "reel4", "cloud_rain": "reel4", "waves": "reel3", "bubbles": "reel3", "eye_icon": "reel3", "keyboard": "reel2", "dirty_hand": "reel2", "dust": "reel2", "culprit_card": "reel2", "air_can": "reel2", "step_badge": "reel2", "credit_card": "reel24:card", "key_on_neck": "reel19", "ice_bags": "reel19:bags", "milk_v19": "reel19:milk", "loose_arm": "reel18", "germ_swarm": "reel16:swarm", "fungus": "reel12", "store_shelf": "reel:shelf", "glass_overlay": "reel", "store_lights": "reel:draw_lights", "flicker": "reel", "car_pixel": "mision002:car", "items_mision002": "mision002:item", "house_pixel": "mision003:house", "tree_pixel": "mision003:tree", "bush_pixel": "mision003:bush", "items_mision003": "mision003:item", "items_ofrenda": "ofrenda:obj", "altar_items_pixel": "ofrenda:altar_items", "panel_catalogo_pixel": "ofrenda:panel", "sandwich_pixel": "oso:sandwich", "heart_pixel": "oso:heart", "dialog_pixel": "oso:dialog", "popup_pixel": "oso:popup", "lives_score_pixel": "oso:lives_score", "icon_pixel": "alien:icon", "slot_pixel": "alien:slot", "inventory_pixel": "alien:inventory", "car_pixel_v1": "zombi11:car", "extra_icon_pixel": "zombi11:extra_icon",
 "camera": "lib.objetos", "rec_frame": "lib.objetos",
 "item_px": "lib.pixel_mision", "evil_eyes_px": "lib.pixel_mision:evil_eyes",
 "snowflake": "lib.objetos",
 "ranger_hat": "lib.objetos",
 "sarcophagus": "lib.objetos", "gift": "lib.objetos", "ring_light": "lib.objetos",
 "helicopter": "lib.objetos", "whistle": "lib.objetos", "campfire": "lib.objetos",
 "mug": "lib.objetos", "hourglass": "lib.objetos",
 "pyramid": "lib.objetos", "rocket": "lib.objetos", "nopal": "lib.objetos"
}
__getattr__ = make(MAP, __name__)
