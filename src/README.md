# Código de producción — Datos que Asustan

Scripts en Python (PIL + ffmpeg) que generan cada reel.

- `reelNN.py`, `misionNNN.py`, `ofrenda.py`: dibujan los cuadros del video (caricatura o pixel art).
- `warpNN.py`: sincroniza la animación con la voz (tiempos reales de la transcripción).
- `audioNN.py`: mezcla voz + efectos + música.
- Base compartida: `reel.py`, `reel2.py`, `reel8.py`, `reel13.py`, `reel15.py`, `reel17.py`, `pixel.py`, `alien.py`.

Flujo: `python3 reelNN.py salida.mp4` (sin `warpNN.py` sale la versión sin voz con tiempos nominales).
Con voz: `python3 audioNN.py` → `python3 reelNN.py v.mp4` → `ffmpeg -i v.mp4 -i audioNN_vo.wav -c:v copy -c:a aac -shortest final.mp4`.
Las voces están en `audio/`.
