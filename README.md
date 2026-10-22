# Datos que Asustan — videos

Reels verticales de terror cómico y datos curiosos. Aquí viven las piezas propias del canal (`lib/`), los guiones, las especificaciones de cada video (`specs/`), las voces y los videos finales que se programan en Metricool.

- **Cómo producir un video y reglas del canal:** [`CLAUDE.md`](CLAUDE.md)
- **Temas hechos y pendientes:** [`IDEAS.md`](IDEAS.md)
- **Piezas reutilizables:** [`lib/CATALOGO.md`](lib/CATALOGO.md)

El motor de animación es un repo aparte, [`licho/reels-engine`](https://github.com/licho/reels-engine), que se instala con versión fija desde `requirements.txt`.

Requisitos: Python 3 con `pip install -r requirements.txt` (instala también el motor), `ffmpeg` y la fuente DejaVu Sans (`/usr/share/fonts/truetype/dejavu/`).

Subir de versión el motor: cambiar la etiqueta `@vX.Y.Z` en `requirements.txt`, reinstalar y revisar `preview`/`check` de los specs recientes.
