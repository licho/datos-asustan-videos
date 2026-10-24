# Datos que Asustan — guía para retomar la producción

Reels verticales (1080x1920) en español para la página **Datos que Asustan** (Facebook Reels + YouTube Shorts).
Tono: terror cómico / curiosidad, humor negro y sarcasmo, caricatura (o pixel art en la serie "Misiones").
Dueño: Luis. **Respóndele siempre en español, con explicaciones sencillas (sin jerga técnica).**

Antes de empezar lee: `IDEAS.md` (temas hechos y pendientes) y `lib/CATALOGO.md` (todas las piezas reutilizables).

## Reglas de contenido (no negociables)
- **Sin marcas** (ni en voz ni en dibujos) y **sin referencias locales** a Yucatán/Mérida.
- **Datos exactos y con fuente.** Verifica en la web; las fuentes van al final del guion (`guiones/*.txt`) y en la respuesta.
- **Duración: la necesaria, no la máxima.** Tope duro 90 s, pero no se llena hasta ahí. Guía: un solo dato o curiosidad → 30–45 s; lista, guía o "qué pasaría si" → 60–75 s; más de 75 s solo si cada línea lo justifica. Prueba de cada línea: "si la quito, ¿se pierde algo?" Si no, se quita.
- **Primero el guion, luego el video.** Muestra el guion (con escenas propuestas) y espera aprobación antes de construir. Muestra el video antes de programarlo.
- Pide más humor si el guion queda plano: Luis prefiere chistes cotidianos mexicanos, sarcasmo y humor negro ligero.
- Políticas de plataformas (anuncios): **sin armas en pantalla**, sin símbolos nazis ni uniformes reconocibles, sin sangre/gore, sin muertos visibles. Mencionar temas sensibles está bien; mostrarlos, no.
- Revisar que no haya objetos flotando, elementos encimados ni texto cortado. El contraste lo revisa Luis al final (no correr `check-contraste` salvo que lo pida).

## Estructura de cada guion: gancho → tensión → recompensa
- **Gancho (línea 1, ≤ 3 s, ~10 palabras máximo):** rompe el patrón para que no deslicen. Debe ser uno de estos 4 tipos:
  1. **Error común:** "Si crees que el animal más peligroso es el tiburón… estás muy lejos."
  2. **Resultado impactante:** "Esta cucaracha no tiene cabeza… y va a vivir una semana más."
  3. **Contradicción:** "El ejército más grande de la historia no es humano."
  4. **"Hice la cuenta" / prueba** (la página no tiene cara, así que en vez de historia personal): "Hice la cuenta: Santa tendría que visitar 9,000 casas por segundo."
- **No abrir con el título ni la serie.** Nada de "¿Qué pasaría si…?", "Guía laboral, episodio cinco" o "Misión 006: …" como primeras palabras: el nombre de la serie va en el letrero (chip) o en la segunda línea. El gancho es el dato o la imagen más fuerte, aunque luego se explique.
- **Primer cuadro = la imagen más fuerte** (el monstruo, el resultado, el contraste), no un fondo vacío ni un título. Lo que se ve y lo que se oye en el segundo 0 deben decir lo mismo.
- **Tensión:** cada línea abre la siguiente (listas numeradas, contadores, "pero espera", "y lo peor viene al final"). Nada de líneas de contexto que no empujen hacia adelante.
- **Recompensa:** el remate o el dato prometido llega al final y cumple lo que prometió el gancho. Si el gancho usa el mejor dato, el final lo cierra con un giro (no lo repite igual).
- Al proponer un guion, marca qué línea es gancho (y de qué tipo), cuáles son tensión y cuál es la recompensa, y di la duración estimada.

## Estructura del repo
| Ruta | Qué es |
|---|---|
| `specs/sNN_nombre.py` | Un video = un spec (guion por líneas + escenas). Copia uno parecido para empezar. |
| `lib/` | Capa del canal sobre el motor: `canal.py` (configuración del canal), catálogos `personajes.py` / `props.py` / `fondos.py` y piezas propias (`humanos.py`, `animales.py`, `criaturas.py`, `objetos.py`, `pantallas.py`, `pixel_mision.py`, `escenarios.py`), fondos nuevos en `fondos_canal.py` y efectos sobrepuestos en `efectos.py` (`tag`, `rubber_stamp`, `snow_fall`, `sound_waves`). `core`, `motion`, `produce`, `check`, `audio`, `align` son capas delgadas que apuntan al motor. |
| `lib/CATALOGO.md` | Lista generada de todas las piezas con su firma. Regenerar con `python3 -m lib.catalogo` cada vez que agregues piezas. |
| `lib/muestras/` | Imágenes de muestra de piezas y escenarios. |
| `src/` | Reels antiguos (código heredado; sus piezas se reusan vía los catálogos). |
| `guiones/` | Guion final de cada video (texto para la voz + fuentes + comando final). |
| `sinvoz/` | Versiones sin voz (para revisar antes de grabar la voz). |
| `audio/` | Voces de ElevenLabs (`NN-nombre.mp3`). |
| `videos/` | Videos finales que se suben a Metricool. |
| `IDEAS.md` | Temas hechos, en producción e ideas pendientes. |

## Motor (repo aparte)
El motor vive en **`licho/reels-engine`** (público) y se instala como dependencia con versión fija en `requirements.txt`
(`pip install -r requirements.txt`). Trae lo genérico: comandos de producción, animación, subtítulos, globos, revisión,
audio y las piezas neutras (`guy`, `anchors`, `medal`, muebles, exteriores, documentos, chat, gráficas, `people_grid`, monitor…).
Los specs siguen importando de `lib.core`, `lib.motion`, `lib.personajes`, `lib.props` y `lib.fondos` como siempre.
- **Lo propio del canal** (colores, zonas, carpeta de salida `/tmp/dqa_out`, encabezado del catálogo) está en `lib/canal.py`.
- **Piezas nuevas de este canal** van aquí (`lib/*.py` + su `MAP`). Si una pieza sirve a cualquier canal, puede subirse al motor en una versión nueva.
- **Subir de versión el motor:** cambia la etiqueta (`@vX.Y.Z`) en `requirements.txt`, `pip install -r requirements.txt`, corre `preview` y `check` de los specs recientes y revisa que se vean igual; luego commit.
- **Cámara (motor ≥ v0.4):** `from reels_engine.camera import Shot, film, path, pan, zoom_in, zoom_out, ken_burns, whip, handheld, impact`. Dibuja la escena más grande que la pantalla ("mundo") y fílmala con `film(img, mundo, shot)`; `view.to_screen(p)` y `view.scale` para que globos y letreros sigan a la cámara. Ejemplo completo: `channel_template/specs/s03_camera.py` del motor.
- `draft` hace un video de revisión rápido (15 cuadros/s, mitad de tamaño). Los comandos en español (`hoja`, `sinvoz`, `texto`) siguen funcionando.
- Para cambiar el motor mismo, trabaja en `licho/reels-engine` (ver su `README.md`) y publica una etiqueta nueva; nunca apuntes a `main` del motor.

## Flujo para un video nuevo
1. **Tema** de `IDEAS.md` (o el que pida Luis). Investiga datos y fuentes.
2. **Guion** en la respuesta: líneas con escena propuesta, chip (letrero) y fuentes. Espera "me late".
3. **Spec**: copia `specs/` más parecido → `specs/sNN_tema.py`. Define `NAME`, `LINES`, escenas, `SCENES`, `SFX`, `MUSIC`.
4. **Nada reusable se queda dentro del spec:** si una función de dibujo (pieza, fondo, efecto) puede servir en otro video, va a la librería desde el principio. **Piezas nuevas** del canal van a la librería (`lib/humanos.py`, `lib/animales.py`, `lib/criaturas.py`, `lib/objetos.py`, `lib/pantallas.py`, …), se registran en `lib/personajes.py` o `lib/props.py` (diccionario `MAP`) y se regenera el catálogo. Toda pieza lleva contorno negro.
5. Comandos (desde la raíz del repo):
   ```
   python3 -m lib.produce specs/sNN.py texto        # texto para la voz + palabras + duración estimada
   python3 -m lib.produce specs/sNN.py hoja         # hoja de cuadros (~4 s) para revisar composición
   python3 -m lib.produce specs/sNN.py preview 3 15 # cuadros sueltos en segundos nominales
   python3 -m lib.produce specs/sNN.py check        # revisión automática (~5 s): subtítulos, bordes, textos encimados
   python3 -m lib.produce specs/sNN.py sinvoz       # video sin voz en /tmp/dqa_out/ (~90 s, usa todos los núcleos)
   python3 -m lib.produce specs/sNN.py final audio/NN-nombre.mp3   # video final sincronizado con la voz
   ```
   Salidas en `/tmp/dqa_out/`. Copia el sin voz a `sinvoz/` y el final a `videos/AAAA-MM-DD_nombre.mp4`.
6. **Revisa** la hoja/preview con tus propios ojos (no solo el `check`): tamaños, cosas flotando, encimados.
7. **Guarda** `guiones/AAAA-MM-DD_nombre.txt` (formato: ver cualquier guion existente) y actualiza `IDEAS.md`.
8. **Commit y push** a `main` (repo público `licho/datos-asustan-videos`). Después del push: `git fetch -q origin +main:refs/remotes/origin/main`.

## Formato del spec (resumen)
- `LINES = [(etiqueta_voz, texto_hablado, subtítulo_con_*resaltado*), …]`. Etiquetas: `mischievously`, `sarcastic`, `serious`, `dramatically`, `whispers`, `excited`, `confident` o `""`. Números hablados en palabras ("cuatrocientos cincuenta mil").
- `SCENES = [(índice_de_línea, función), …]`; cada función recibe `c` (`c.t` tiempo global, `c.lt` tiempo en la escena, `c.dur` duración) y devuelve una imagen 1080x1920.
- `SFX = [(línea, segundo, "pop|ding|whoosh|buzzer|boing|thud|sting|jingle|sadtrom|rumble|splat|skid|alarm", {}), …]`, `MUSIC = ("bass|chiptune|waltz|pad", [(línea_silencio_ini, fin)], línea_sube_volumen)`.
- Zonas seguras: letreros (`chip`) en y=300 (`CHIP1`) / 420 (`CHIP2`); acción 480–1320; piso 1290–1300; **nada entre 1380 y 1640** (subtítulos en 1500).
- Personajes: `anchors(x, pies, escala)` da cabeza, boca, manos, caja → úsalo para poner objetos y globos sin que floten.
- Diálogos: `say(d, texto, boca, radio_cabeza, avoid=[cajas])` acomoda el globo solo (no usar `bubble` a mano).
- Animación: `tw`, `yoyo`, `shake`, `layer` (escala/giro/alpha), `glow`, `radial_bg` (fondos estándar). Subtítulos palabra por palabra y viñeta salen solos.

## Voz (ElevenLabs)
- Voz **Erick – Cinematic Storyteller** `nFcvfxkh4Fldtkn096yh`, modelo `eleven_v4`. El texto exacto lo da `texto` (con las etiquetas entre corchetes).
- **Generar con `generations_count=1`** (el conector hace 2 tomas por defecto y cobra el doble). Costo: 1 crédito por carácter (~1,100 por video). Usar `estimate_only` si hay duda.
- Créditos: plan Starter, se renueva el **día 19** de cada mes. Si no hay créditos, se hacen versiones sin voz y la voz se agrega después.
- Para bajar el audio al repo: crear `pedidos/NN-nombre.url` con el enlace temporal del mp3 y hacer push; la acción `.github/workflows/bajar-audio.yml` lo descarga a `audio/NN-nombre.mp3`.

## Publicación (Metricool)
- Marca **"Datos que asustan"**, brandId `7531941`, zona horaria `America/Merida` (Facebook + YouTube conectados).
- **Una sola publicación con los dos proveedores** (facebook + youtube), no dos separadas.
- Horario: **lunes a sábado a las 10:00** (America/Merida), un video al día; domingo no se publica.
- Formato que se usa (ver publicaciones existentes con `getScheduledPosts`):
  - `text`: gancho + emoji + pregunta para comentarios 👇, línea de fuentes si aplica, hashtags `#DatosQueAsustan` + 2–3 del tema + `#Shorts`.
  - `facebookData`: `{type: "REEL", title: "<título>"}`.
  - `youtubeData`: `{title: "<título> <emoji> #Shorts", type: "short", privacy: "public", tags: [...], category: "ENTERTAINMENT" o "EDUCATION", madeForKids: false}`.
  - `media`: el mp4 de `videos/` publicado en el repo (URL raw de GitHub); Metricool lo copia a su almacenamiento.
- Muestra el video a Luis antes de programarlo.

## Pendientes conocidos (octubre 2026)
- Noviembre ya tiene versión sin voz de todos los videos; el **19 de noviembre** (renovación de créditos) se graban las voces, se hace `final` de cada uno y se programan.
- Diciembre: asteroide-ciudad, momia, ejércitos y Llorona listos sin voz (ver `IDEAS.md`).
