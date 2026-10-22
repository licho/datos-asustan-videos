"""Canal Datos que Asustan: el motor vive en el paquete reels_engine (repo licho/reels-engine).
Aquí se registra la configuración del canal antes de que se use cualquier parte del motor."""
from reels_engine import configure as _configure
from .canal import CANAL as _CANAL
_configure(_CANAL)
