# Animación nueva (Remotion y HyperFrames)

Prueba del estilo mejorado: mismo canal (caricatura plana, contorno negro, letreros y subtítulos en su lugar),
con personajes que se mueven, cámara, luz y brillos.

- `shared/art.mjs`: dibujos en SVG compartidos (sol con cara, azotea, señor en silla, ciudad, tendedero) y guion del gancho.
- `rm-sol/`: versión Remotion. `npm install` y `npm run render` (usa el Chrome del sistema).
- `hf-sol/`: versión HyperFrames. `node build.mjs` genera `index.html`; `npx hyperframes@0.9.78 render -o renders/gancho.mp4`.

Video: "¿Qué pasaría si el Sol se apagara?" (guion aprobado el 21 nov 2026).
