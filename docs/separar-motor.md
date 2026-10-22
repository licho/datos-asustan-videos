# Encargo: separar el motor de video en su propio repositorio

Para la sesión que hará la separación. Luis (dueño) quiere un **motor compartido** para varios canales de reels (Datos que Asustan, un canal de pixel art y uno nuevo, probablemente de finanzas personales). Este repo (`licho/datos-asustan-videos`) seguirá siendo el canal **Datos que Asustan**; otra sesión sigue produciendo videos aquí mientras tú separas el motor.

Habla con Luis **en español y con explicaciones sencillas**. Antes de crear el repo nuevo, confirma con él el nombre (propuesta: `licho/motor-reels`) y si será público o privado.

## Cómo está hoy

- `lib/` (~2,700 líneas) es el motor + la librería de piezas, todo junto:
  - **Motor (genérico):** `produce.py` (comandos texto/hoja/preview/check/sinvoz/final, render en paralelo, caché de revisión), `motion.py` (curvas de animación, `tw`, `yoyo`, `layer`, `glow`, `radial_bg`, `space_bg`, subtítulos palabra por palabra, viñeta), `check.py` (revisión automática de subtítulos, bordes, textos encimados, contraste opcional), `align.py` (sincroniza la voz con detección de silencios), `audio.py` (mezcla voz + efectos + música generada), `catalogo.py` (genera `lib/CATALOGO.md`), `_lazy.py` (carga perezosa de piezas por alias).
  - **`core.py`:** mezcla de motor (zonas seguras, `canvas`, `grad`, `chip`, `bigtext`, globos `bubble`/`say`, `fit_font`, `follow_btn`, `stamp`) con piezas.
  - **Piezas:** `humanos.py`, `animales.py`, `criaturas.py`, `objetos.py`, `pantallas.py`, `muebles.py`, `exterior.py`, `escenarios.py`, `pixel_mision.py`; catálogos `personajes.py`, `props.py`, `fondos.py` (diccionario `MAP` → módulo).
- **Dependencia del código viejo:** `core.py`, `humanos.py`, `_lazy.py` y `pixel_mision.py` meten `src/` en el `sys.path` e importan de `src/reel.py` (fuente `F`, colores, `chip`, `bigtext`, `rich_caption`, `guy`, `lerp`, `ease`, `pop`, `dk`, `lc`…). Los catálogos apuntan a ~29 piezas que viven en `src/reelNN.py`, `mision00N.py`, `pixel.py`, `alien.py`, etc.
- **Specs** (`specs/s27…s39`): cada video importa de `lib.core`, `lib.motion`, `lib.personajes`, `lib.props`, `lib.fondos`. Formato descrito en `CLAUDE.md`.
- Valores fijos de este canal dentro del motor: fuente DejaVu Sans Bold, colores, `W,H = 1080,1920`, zonas (`CHIP1/2 = 300/420`, subtítulos en 1500, franja libre 1380–1640), `WPS = 2.75`, carpeta de salida `/tmp/dqa_out/`, estilos de música, viñeta 0.35, subtítulos estilo "words".

## Qué se quiere

1. **Repo nuevo del motor**, instalable con `pip install git+https://github.com/licho/<motor>@vX.Y.Z` (con `pyproject.toml`), sin nada de terror ni de este canal:
   - Todo lo genérico de arriba, más las piezas neutras que sirven a cualquier canal: personaje base (`guy` + `anchors`), muebles, exterior, pantallas (documentos, celular con chat, gráficas, `bar_chart`, `people_grid`, monitor), calendario, reloj, etc.
   - **Sin depender de `src/`**: lo que hoy se importa de `src/reel.py` pasa al motor.
   - **Configurable por canal** (un archivo/objeto de configuración del canal): fuentes, colores, zonas seguras, estilo de subtítulos, viñeta, velocidad de lectura (WPS), carpeta de salida, estilos de música, umbrales de la revisión.
   - Mecanismo de catálogo extensible: el canal registra sus propias piezas (como hoy el `MAP`) y `catalogo` genera el `CATALOGO.md` del canal.
   - Pensado para admitir más adelante un segundo "pincel" de dibujo (vectorial con cairo) para el canal nuevo, sin romper el actual (PIL). No hace falta construirlo ahora; solo no cerrar la puerta.
2. **Este repo queda como canal**: conserva sus piezas propias (monstruos, Llorona, momia, zombis, soldados, emú, hormigas, templo, pixel art de "Misiones", etc.), sus specs, guiones, `IDEAS.md`, `CLAUDE.md`, audio y videos, y usa el motor como dependencia fija (versión con etiqueta).
3. **Los specs no deben cambiar** (o cambiar lo mínimo): conserva los nombres `lib.core`, `lib.motion`, `lib.personajes`, `lib.props`, `lib.fondos` en este repo como capa delgada que importa del motor + piezas del canal.
4. `src/` (reels viejos) se queda en este repo como código heredado; el motor no debe necesitarlo.

## Cómo hacerlo sin romper la producción

- **No toques `main` de este repo hasta el final.** Trabaja el motor en su repo nuevo. La integración aquí va en una rama `motor-externo` con pull request para que Luis la apruebe.
- La otra sesión seguirá agregando piezas en `lib/humanos.py`, `lib/animales.py`, `lib/criaturas.py`, `lib/objetos.py`, `lib/pantallas.py` y specs nuevos. Antes de abrir el PR, trae lo último de `main` y migra lo nuevo.
- **Prueba de que nada cambió (obligatoria):** antes de empezar, guarda en una carpeta de referencia los cuadros de `python3 -m lib.produce specs/sNN.py preview 2 10 20 30 45 60` y la salida de `check` para **todos** los specs `s27`–`s39` (y los que haya nuevos). Al terminar, genera lo mismo con el motor externo y compáralo píxel a píxel (diferencia ≈ 0) y el `check` igual. Genera además un `sinvoz` completo de un spec y verifica la duración.
- Corre `python3 -m lib.catalogo` y revisa que el catálogo siga listando todas las piezas.
- Actualiza `CLAUDE.md` y `README.md` de este repo (cómo instalar el motor, cómo subir de versión) y escribe el `README` del motor (cómo crear un canal nuevo desde cero: configuración, primer spec, comandos).

## Convenciones

- Commits en español. Termina cada mensaje de commit con:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: <enlace de tu sesión>
  ```
- Después de cada push a este repo: `git fetch -q origin +main:refs/remotes/origin/main`.
- Requisitos del sistema: Python 3, `pillow`, `numpy`, `scipy` (opcional), `ffmpeg`, fuente DejaVu Sans (`/usr/share/fonts/truetype/dejavu/`).

## Entregable para Luis

Un resumen corto: dónde quedó el motor, qué versión usa este repo, cómo se crea un canal nuevo (pasos), y el resultado de la comparación de cuadros (todo igual o qué cambió y por qué).
