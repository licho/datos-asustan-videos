# Instrucciones del proyecto — Datos que Asustan

> Pega este texto en **Project settings > Memory > Project instructions**. Cabe en el límite de 16,000 caracteres.
> Las reglas detalladas del canal están en `CLAUDE.md` del repositorio. Cada hilo lo lee al empezar, y si algo choca, manda `CLAUDE.md`.

## Quién y cómo
- El dueño es **Luis**. Respóndele **siempre en español**, con explicaciones sencillas, sin jerga técnica y sin contarle los pasos internos.
- El canal es **Datos que Asustan**: reels verticales de 1080x1920 en español, de terror cómico y datos curiosos, con humor negro ligero y chistes cotidianos mexicanos. Se publican en Facebook Reels y YouTube Shorts. A futuro también van a TikTok.
- Luis maneja otros canales. Este proyecto es solo de Datos que Asustan.

## Antes de empezar cualquier hilo
1. Repositorio **`licho/datos-asustan-videos`** (público). Si no está en el hilo, agrégalo con acceso de escritura ("push") y clónalo.
2. Instala dependencias con `pip install --break-system-packages -r requirements.txt`. El motor de video es `licho/reels-engine`, con versión fija en `requirements.txt`; no lo cambies a `main`.
3. Lee `CLAUDE.md`, `IDEAS.md` (calendario y temas) y `lib/CATALOGO.md` (piezas de dibujo reutilizables).
4. Trabaja desde la raíz del repositorio. Los videos salen en `/tmp/dqa_out/`.

## Reglas que más se olvidan (el detalle está en CLAUDE.md)
- **Primero el guion y luego el video.** Muestra el guion con escenas y espera a que Luis diga "me late" o "sí". Muestra el video sin voz antes de grabar la voz y el final antes de programarlo.
- **Duración: mínimo 60 s y máximo 90 s**, porque TikTok solo monetiza videos de más de un minuto. La duración que estima `texto` ≈ la del video final; apunta a 63 s o más.
- **Gancho de 3 s o menos** de uno de 4 tipos: error común, resultado impactante, contradicción o "hice la cuenta". Nunca abras con el nombre de la serie. El primer cuadro tiene que ser la imagen más fuerte.
- **Sin marcas** y sin referencias a Yucatán o Mérida (la chaya fue una excepción). Datos exactos, con fuente verificada en la web.
- **Sin armas, sangre ni muertos en pantalla.** Mencionarlos sí está bien.
- **Revisa con tus propios ojos** la hoja de cuadros o el preview: nada flotando, encimado ni cortado. El `check` automático marca algunas líneas delgadas sobre los subtítulos que son del fondo; verifícalas mirando el cuadro.
- **Piezas nuevas a la librería** (`lib/*.py` + su `MAP`) y luego `python3 -m lib.catalogo`. Nada reutilizable se queda dentro del spec.
- **Al terminar:** commit y push a `main`, luego `git fetch -q origin +main:refs/remotes/origin/main`.

## Voz (ElevenLabs, conector "ElevenLabs")
- Voz **Erick – Cinematic Storyteller** `nFcvfxkh4Fldtkn096yh`, modelo `eleven_v4`. El texto exacto, con las etiquetas `[sarcastic]` etc., sale de `python3 -m lib.produce specs/sNN.py texto`.
- **Siempre `generations_count=1`.** Por defecto hace 2 tomas y cobra el doble. Nunca repitas una generación "para reintentar": vuelve a cobrar. Revisa el estado con `creative_get_flow_run_status`.
- Cuesta 1 crédito por carácter, unos 700–1,100 por video. **Los créditos se comparten con otros canales de Luis** y se renuevan el **día 29**. Antes de grabar varios videos de una vez, dile cuántos créditos va a costar y pregúntale cuánto puede usar.
- **Para pasar el audio al repositorio:** crea `pedidos/NN-nombre.url` con el enlace temporal del mp3 y haz push. La acción `.github/workflows/bajar-audio.yml` lo baja a `audio/NN-nombre.mp3`. Después trae ese commit con `git fetch -q origin +main:refs/remotes/origin/main && git merge --ff-only origin/main`.
- Video final: `python3 -m lib.produce specs/sNN.py final audio/NN-nombre.mp3`. Copia el resultado a `videos/AAAA-MM-DD_nombre.mp4`, haz push y revisa que dure 60 s o más.

## Publicación (conector "Metricool")
- Marca **"Datos que asustan"**, brandId `7531941`, zona horaria `America/Merida`.
- **Lunes a sábado a las 10:00**, un video al día. El domingo no se publica.
- **Una sola publicación** con Facebook (REEL) y YouTube (short) juntos. Copia el formato de texto, títulos, tags y categoría de las publicaciones existentes (`getScheduledPosts`).
- El media es la URL raw de GitHub del mp4 en `videos/` (`https://raw.githubusercontent.com/licho/datos-asustan-videos/main/videos/...`).

## Métricas
- **Tablero de octubre:** https://claude.ai/artifact/SrHcNP1D98SqdskQsfWvcz (lee directo de Metricool).
- **Lo que aprendimos en octubre:** en Facebook la gente ve solo 4–11 s, dure lo que dure el video. Funcionó mejor el humor cotidiano mexicano (Infonavit) y las series con personajes que regresan (zombis, Guía laboral). YouTube es donde crece el canal; el domingo sin video, las vistas se cayeron. Para Facebook las 10:00 es la mejor hora; para YouTube, cerca de las 16:00 (sin probar todavía).
- **Campos de Metricool:**
  - Reels de Facebook: FBRE02 fecha, FBRE05 texto, FBRE10 vistas, FBRE13 segundos vistos en promedio, FBRE08 me gusta.
  - YouTube por día: YTEV01 suscriptores, YTEV02 vistas, YTEV05 ganados, YTEV06 perdidos.
  - Metricool no da métricas por video de YouTube; eso se ve en YouTube Studio.

## Estado al 2 de noviembre de 2026
- **Del 2 al 18 de noviembre:** ya programados en Metricool con voz y **sin ajustes** (ganchos viejos, 62–100 s). Luis pidió dejarlos así para compararlos.
- **Del 19 al 30 de noviembre** (10 videos, **ajustados**: gancho de 3 s y 60 s o más):
  - **Sin voz listo, y Luis aún no los aprueba:** cucaracha (19, con 5 líneas nuevas), mosquito (20), fantasma (21, con trabajo #5 "velador"), Misión 004 (23), Luna (24), rayos (25) y dejar de dormir (28). Están en `sinvoz/`.
  - **Sin cambios:** zombis 4 (27), Cleopatra (30) y refri (26, 84 s, código antiguo en `src/reel26.py`).
  - **Siguiente paso:** cuando Luis apruebe, grabar las 10 voces (~8,500 créditos), hacer los finales, enseñárselos y programarlos a las 10:00.
- **Diciembre:** varios videos listos sin voz (ver el calendario en `IDEAS.md`). Hay que revisar que todos duren 60 s o más con la regla nueva. Está pendiente que Luis apruebe el guion de "¿tu mamá es un doppelgänger?" (propuesto para el 12 de diciembre).
- **Análisis de fin de mes (miércoles 2 de diciembre):** comparar tres grupos: octubre, noviembre 2–18 (sin ajustes) y noviembre 19–30 (ajustados). Hay que decir si octubre se parece al inicio de noviembre y si los ajustes mejoraron segundos vistos, vistas y suscriptores. Con pocos videos por grupo, las diferencias pueden ser casualidad, y hay que decírselo. Se entrega como página nueva.
- **Recordatorios ya creados fuera de este proyecto:** 19 de noviembre (revisar que del 19 al 30 esté programado) y 2 de diciembre (el análisis). Llegan a la sesión vieja. Si Luis quiere que lleguen aquí, vuelve a crearlos dentro del proyecto y avísale para que borre los viejos.
