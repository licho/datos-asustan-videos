// Genera index.html (composición HyperFrames) con los mismos dibujos que la versión Remotion.
// Uso: node build.mjs && npx hyperframes render
import * as A from "../shared/art.mjs";
import fs from "fs";

const H = A.HOOK, clic = H.clic, D = H.dur;
const guySvg = A.guy(), sunSvg = A.sun(165), lineSvg = A.clothesline();

const words = H.words.map(([w, t0, hl], i) =>
  `<span class="w${hl ? " hl" : ""}" id="w${i}">${w}</span>`).join("");
const timers = [20, 19, 18, 17].map((s, i) =>
  `<div class="chip chip2" id="tm${i}"><span>TE ENTERAS EN 8:${s}</span></div>`).join("");

const html = `<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
  @font-face { font-family: DQA; src: url(assets/DejaVuSans-Bold.ttf); }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
  #root { position: relative; width: 1080px; height: 1920px; font-family: DQA; }
  .layer { position: absolute; inset: 0; }
  .chip { position: absolute; left: 0; right: 0; display: flex; justify-content: center; }
  .chip span { font-size: 56px; line-height: 1; padding: 17px 36px; border-radius: 34px; border: 6px solid #111; white-space: nowrap; }
  .chip1 { top: 300px; transform: translateY(-50%); } .chip1 span { background: ${A.C.red}; color: #fff; }
  .chip2 { top: 420px; transform: translateY(-50%); opacity: 0; } .chip2 span { background: #111; color: ${A.C.yel}; font-size: 48px; padding: 14px 31px; }
  #caps { position: absolute; left: 60px; right: 60px; top: 1500px; transform: translateY(-50%);
          display: flex; flex-wrap: wrap; justify-content: center; column-gap: 22px; row-gap: 4px; }
  .w { font-size: 70px; line-height: 1.15; color: #fff; -webkit-text-stroke: 12px #111; paint-order: stroke fill;
       display: inline-block; transform: scale(0); }
  .w.hl { color: ${A.C.yel}; }
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="${D}" data-width="1080" data-height="1920">
  <svg id="scene" class="clip layer" data-start="0" data-duration="${D}" data-track-index="0"
       width="1080" height="1920" viewBox="0 0 1080 1920">
    ${A.defs()}
    <g id="world">
      ${A.sky()}
      <g transform="translate(540 700)"><g id="sunBody">${sunSvg}</g></g>
      <circle id="flash" cx="540" cy="700" r="165" fill="#fffbe6" opacity="0"/>
      <g id="farL">${A.skylineFar()}</g>
      <g id="nearL">${A.skylineNear()}</g>
      ${A.rooftop()}${A.tinaco()}${lineSvg}
      <g transform="translate(810 1290) scale(1.12)">${guySvg}</g>
      ${A.photons(7)}
      <g transform="translate(255 600) rotate(-12)"><g id="clic" opacity="0">
        <text text-anchor="middle" dominant-baseline="middle" font-family="DQA" font-size="110" fill="${A.C.yel}"
          stroke="#111" stroke-width="16" paint-order="stroke" stroke-linejoin="round">¡CLIC!</text></g></g>
    </g>
    ${A.vignette()}
  </svg>
  <div class="clip layer" data-start="0" data-duration="${D}" data-track-index="1">
    <div class="chip chip1" id="chip1"><span>${H.chip1}</span></div>
    ${timers}
    <div id="caps">${words}</div>
  </div>
</div>
<script>
  const clic = ${clic}, D = ${D};
  const tl = gsap.timeline({ paused: true });
  const BEAM = ${JSON.stringify(A.BEAM)};
  const beamAt = p => ({ x: BEAM.x0 + (BEAM.x1 - BEAM.x0) * p, y: BEAM.y0 + (BEAM.y1 - BEAM.y0) * p - Math.sin(p * Math.PI) * 60 });

  // Cámara: empuje, sacudida en el clic y viaje hacia el señor (objeto proxy -> atributo transform)
  const cam = { s: 1, travel: 0, shake: 0 };
  const world = document.getElementById("world");
  const applyCam = () => {
    const sc = cam.s + cam.travel * 0.14, fx = 540 + cam.travel * 170, fy = 960 + cam.travel * 40;
    const t = tl.time(), shx = Math.sin(t * 90) * 14 * cam.shake, shy = Math.cos(t * 77) * 10 * cam.shake;
    world.setAttribute("transform", \`translate(\${540 + shx} \${960 + shy}) scale(\${sc}) translate(\${-fx} \${-fy})\`);
  };
  tl.to(cam, { s: 1.06, duration: clic, ease: "power2.inOut", onUpdate: applyCam }, 0);
  tl.fromTo(cam, { shake: 1 }, { shake: 0, duration: 0.35, ease: "none", onUpdate: applyCam }, clic);
  tl.to(cam, { travel: 1, duration: D - 2.3, ease: "power2.inOut", onUpdate: applyCam }, 2.3);

  // Paralaje de la ciudad
  tl.to("#farL", { x: -12 * D, duration: D, ease: "none" }, 0);
  tl.to("#nearL", { x: -26 * D, duration: D, ease: "none" }, 0);

  // Sol: rayos giran, brillo late, parpadeo, aplastón antes del clic, se apaga con destello
  tl.to("#sunRays", { rotation: 14 * D, svgOrigin: "0 0", duration: D, ease: "none" }, 0);
  tl.to("#sunGlow", { scale: 1.04, svgOrigin: "0 0", duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }, 0);
  tl.to("#sunEyes", { scaleY: 0.12, svgOrigin: "0 -24", duration: 0.07, yoyo: true, repeat: 1 }, 0.8);
  tl.to("#sunBody", { scaleX: 1.07, scaleY: 0.93, svgOrigin: "0 0", duration: 0.18, ease: "power2.in" }, clic - 0.18);
  tl.to("#sunBody", { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 0.5, ease: "elastic.out(1.2, 0.4)" }, clic);
  tl.to("#sunOn", { opacity: 0, duration: 0.12 }, clic);
  tl.to("#sunOff", { opacity: 1, duration: 0.12 }, clic);
  tl.to("#sunRays", { scale: 0.25, opacity: 0, svgOrigin: "0 0", duration: 0.12 }, clic);
  tl.to("#sunGlow", { opacity: 0, duration: 0.2 }, clic);
  tl.fromTo("#flash", { opacity: 0, scale: 1, svgOrigin: "540 700" }, { opacity: 0.7, duration: 0.04 }, clic);
  tl.to("#flash", { opacity: 0, scale: 1.85, svgOrigin: "540 700", duration: 0.31, ease: "power2.out" }, clic + 0.04);
  tl.to("#sunOff", { x: 3, duration: 0.05, yoyo: true, repeat: 30, ease: "none" }, clic + 0.2);
  tl.fromTo("#clic", { scale: 0, opacity: 1, svgOrigin: "0 0" }, { scale: 1, duration: 0.45, ease: "back.out(3)" }, clic);
  tl.to("#clic", { opacity: 0, duration: 0.25 }, clic + 0.9);

  // Luz que sigue viajando hacia el señor
  const ph = [...document.querySelectorAll(".ph")];
  const light = { k: 0, p: 0 };
  const applyLight = () => ph.forEach((c, i) => {
    const p = (light.p + i / ph.length) % 1, q = beamAt(p);
    c.setAttribute("cx", q.x); c.setAttribute("cy", q.y);
    c.setAttribute("r", 24 + 6 * Math.sin(tl.time() * 9 + i));
    c.setAttribute("opacity", light.k * Math.min(1, p * 6, (1 - p) * 6));
  });
  tl.to(light, { p: (D - clic) * 0.75, duration: D - clic, ease: "none", onUpdate: applyLight }, clic);
  tl.to(light, { k: 1, duration: 0.35, ease: "none", onUpdate: applyLight }, clic + 0.25);

  // Tendedero
  ["#cloth1 .sway", "#cloth2 .sway", "#cloth3 .sway"].forEach((s, i) =>
    tl.fromTo(s, { rotation: -5, svgOrigin: "0 0" }, { rotation: 5, duration: 1.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, i * 0.2));

  // Señor: respira y se ríe del celular
  tl.to("#guyArms", { y: 3, duration: 0.7, yoyo: true, repeat: 4, ease: "sine.inOut" }, 0);
  tl.set("#guySmile", { opacity: 0 }, 3.55); tl.set("#guyLaugh", { opacity: 1 }, 3.55);
  tl.to("#guyHead", { y: -401, rotation: 4, duration: 0.11, yoyo: true, repeat: 9, ease: "sine.inOut" }, 3.55);
  tl.set("#guySmile", { opacity: 1 }, 4.6); tl.set("#guyLaugh", { opacity: 0 }, 4.6);
  tl.to("#phoneGlow", { opacity: 0.55, duration: 0.45, yoyo: true, repeat: 10, ease: "sine.inOut" }, 0);

  // Letreros
  tl.fromTo("#chip1", { scale: 0.85 }, { scale: 1, duration: 0.25, ease: "back.out(2)" }, 0);
  [0, 1, 2, 3].forEach(i => {
    const t0 = clic + 0.55 + i;
    if (i === 0) tl.fromTo("#tm0", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, t0);
    else { tl.set("#tm" + (i - 1), { opacity: 0 }, t0); tl.set("#tm" + i, { opacity: 1 }, t0); }
  });

  // Subtítulos palabra por palabra
  const W = ${JSON.stringify(H.words)};
  W.forEach(([w, t0], i) => {
    tl.to("#w" + i, { scale: 1.1, duration: 0.12, ease: "power2.out" }, t0);
    tl.to("#w" + i, { scale: 1, duration: 0.14, ease: "power2.in" }, t0 + 0.12);
    const t1 = i < W.length - 1 ? W[i + 1][1] : D;
    tl.to("#w" + i, { y: -6, duration: 0.08 }, t0);
    tl.to("#w" + i, { y: 0, duration: 0.08 }, t1);
  });

  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
  tl.seek(0); applyCam(); applyLight();
</script>
</body>
</html>
`;
fs.writeFileSync(new URL("./index.html", import.meta.url), html);
console.log("index.html listo");
